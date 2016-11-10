# Rojak OVR for pair of candidates
# This is enhanced version of Rojak SVM (rojak_svm.py)
import csv
import sys
import re
import pickle
import itertools

from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import LinearSVC
from sklearn import metrics
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot
import numpy as np

import stopwords

# Classifier names
CLASSIFIER_AGUS_SYLVI = 'classifier_agus_sylvi'
CLASSIFIER_AHOK_DJAROT = 'classifier_ahok_djarot'
CLASSIFIER_ANIES_SANDI = 'classifier_anies_sandi'
CLASSIFIER_OOT = 'classifier_oot'

# Compile regex to remove non-alphanum char
nonalpha = re.compile('[^a-z\-\.]+')

# Map the commonly used candidate name and their corresponding official pair 
# name. This is used to improve classifier accuracy
official_candidates = {
    'agus': 'agus-sylvi',
    'harimurti': 'agus-sylvi',
    'yudhoyono': 'agus-sylvi',
    'ahy': 'agus-sylvi',
    'sylvi': 'agus-sylvi',
    'sylviana': 'agus-sylvi',
    'agus-sylviana': 'agus-sylvi',
    'yudhoyono-sylviana': 'agus-sylvi',
    'agus-sylvia': 'agus-sylvi',
    'harimurti-sylviana': 'agus-sylvi',
    'ahok': 'ahok-djarot',
    'basuki': 'ahok-djarot',
    'tjahaja': 'ahok-djarot',
    'purnama': 'ahok-djarot',
    'btp': 'ahok-djarot',
    'djarot': 'ahok-djarot',
    'saiful': 'ahok-djarot',
    'hidayat': 'ahok-djarot',
    'petahana': 'ahok-djarot',
    'ahok-djarot': 'ahok-djarot',
    'basuki-djarot': 'ahok-djarot',
    'ahokdjarot.id': 'ahok-djarot',
    'incumbent': 'ahok-djarot',
    'petahana': 'ahok-djarot',
    'anies': 'anies-sandi',
    'baswedan': 'anies-sandi',
    'sandi': 'anies-sandi',
    'sandiaga': 'anies-sandi',
    'uno': 'anies-sandi',
    'anies-sandiaga': 'anies-sandi',
    'baswedan-sandiaga': 'anies-sandi',
    'anies-uno': 'anies-sandi',
    'aniesbaswedan': 'anies-sandi',
    'anis': 'anies-sandi'
}

# Normalize the word
def normalize_word(w, use_synonym=True):
    word = w.lower()
    word = nonalpha.sub('', word)
    word = word.strip()

    # Remove -kan in di..kan form
    # Example: disebutkan => disebut
    # if (len(word) > 5 and word[:2] == 'di' and word[-3:] == 'kan'):
    #     word = word[:len(word)-3]

    # Remove -kan in me..kan form
    # Example: menyetorkan => menyetor
    # if (len(word) > 5 and word[:2] == 'me' and word[-3:] == 'kan'):
    #     word = word[:len(word)-3]

    # Remove -lah form
    # Example: bukanlah
    # lah_except = ['masalah']
    # if (len(word) > 5 and word[-3:] == 'lah' and not word in lah_except):
    #     word = word[:len(word)-3] 

    # Remove -nya form
    # Example: bukannya => bukan, disayanginya => disayang, 
    # komunikasinya => komunikasi
    if (len(word) > 5 and word[-3:] == 'nya'):
        word = word[:len(word)-3]

    # Remove the non-char '-' in front of the word
    if len(word) > 0 and word[0] == '-':
        word = word[1:]

    # Remove the non-char '-' in the end of the word
    if len(word) > 0 and word[-1] == '-':
        word = word[:len(word)-1]

    # Remove the non-char '.' in front of the word
    if len(word) > 0 and word[0] == '.':
        word = word[1:]

    # Remove the non-char '.' in the end of the word
    if len(word) > 0 and word[-1] == '.':
        word = word[:len(word)-1]

    # Replace the candidate name with their official pair name
    if use_synonym and word in official_candidates:
        word = official_candidates[word]

    return word

# Compile regex to remove author signature from the text
# Example: (nkn/dnu)
author_signature = re.compile('\([a-zA-Z]+/[a-zA-Z]+\)')

# Function to clean the raw string
def clean_string(s, use_synonym=True):
    result_str = []

    # Remove the noise: html tag
    clean_str = BeautifulSoup(s, 'lxml').text
    # Remove the noise: author signature
    clean_str = author_signature.sub(' ', clean_str)

    # For each word we clear out the extra format
    words = clean_str.split(' ')

    # Remove the stop words
    stopwords_removed = []
    for w in words:
        word = normalize_word(w, use_synonym=use_synonym)
        if word != '' and not word in stopwords.stopwords:
            stopwords_removed.append(word)

    word_len = len(stopwords_removed)
    skipword = False
    for i in xrange(word_len):
        # Skip negation bigram
        # Example: 'tidak_bisa' we skip the 'bisa'
        if skipword:
            skipword = False
            continue

        # Current word
        word = stopwords_removed[i]

        # Normalize the negation
        negations = ['tidak', 'enggak', 'bukan', 'tdk', 'bkn', 'tak', 
            'belum', 'tidaklah', 'bukanlah', 'ga']
        if word in negations:
            if i < (word_len-2):
                next_word = normalize_word(stopwords_removed[i+1])
                if next_word != '':
                    word = '{}_{}'.format('tidak', next_word)
                    skipword = True
            else:
                word = 'tidak'

        # Collect the pre-processed word
        if word != '' and word != '-':
            result_str.append(word)

    result = ' '.join(result_str).encode('utf-8', 'ignore')
    return result

# Plot confusion matrix
def plot_confusion_matrix(cm, classes, normalize=False, title='',
        cmap=pyplot.cm.Blues, classifier_name=''):
    pyplot.close('all')
    pyplot.imshow(cm, interpolation='nearest', cmap=cmap)
    pyplot.title(title)
    pyplot.colorbar()
    tick_marks = np.arange(len(classes))
    pyplot.xticks(tick_marks, classes, rotation=45)
    pyplot.yticks(tick_marks, classes)

    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]

    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        pyplot.text(j, i, cm[i, j],
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")
    
    pyplot.ylabel('True label')
    pyplot.xlabel('Predicted label' + '\n\n' + classifier_name)
    pyplot.tight_layout()
    full_title = title + ' ' + classifier_name
    file_name = '_'.join(full_title.lower().split(' '))
    pyplot.savefig(file_name + '.png')

# Custom tokenizer
def whitespace_tokenizer(s):
    return s.split(' ')

class RojakOvRPair():
    # Storing classifier
    classifiers = {}

    # Map of label name and the corresponding classifier ID
    # We create 4 classifiers:
    # * classifier_agus_sylvi => to predict pos/neg/not about agus-sylvi
    # * classifier_ahok_djarot => to predict pos/neg/not about ahok-djarot
    # * classifier_anies_sandi => to predict pos/neg/not about anies-sandi
    # * classifier_oot => to predict oot or not
    #
    # Infer rules:
    # - Given news, Is it oot or not?
    #     - If oot => label news as oot
    #     - If not:
    #         - For each classifier classifier_agus_sylvi, 
    #           classifier_ahok_djarot, classifier_anies_sandi take the 
    #           label that have confident score larger than given threshold
    #           otherwise we don't label the news
    classifier_label = {
        'pos_agus_sylvi': CLASSIFIER_AGUS_SYLVI,
        'neg_agus_sylvi': CLASSIFIER_AGUS_SYLVI,
        'pos_ahok_djarot': CLASSIFIER_AHOK_DJAROT,
        'neg_ahok_djarot': CLASSIFIER_AHOK_DJAROT,
        'pos_anies_sandi': CLASSIFIER_ANIES_SANDI,
        'neg_anies_sandi': CLASSIFIER_ANIES_SANDI,
        'oot': CLASSIFIER_OOT
    }

    # Map classifier ID and the training and test data
    training_data_text = {}
    training_data_class = {}
    test_data_text = {}
    test_data_class = {}

    def __init__(self, max_ngram=3, min_df=3, tokenizer=None):
        self.max_ngram = max_ngram
        self.min_df = min_df
        self.tokenizer = tokenizer

    # Collect the data from csv file
    def _collect_data_from_csv(self, input_file, container_text, 
            container_class):
        # Read the input_file
        csv_file = open(input_file)
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            # Get the data
            try:
                title = row['title']
                raw_content = row['raw_content']
                labels = row['labels'].split(',')
            except KeyError as err:
                print 'Cannot load csv:', err
                sys.exit()

            # Clean the string
            clean_title = clean_string(title)
            clean_content = clean_string(raw_content)
            clean_text = '{} {}'.format(clean_title, clean_content)

            # For debugging purpose
            # print '=== Debug start'
            # print 'title:', title
            # print 'clean_title:', clean_title
            # print 'raw_content:', raw_content
            # print 'clean_content:', clean_content
            # print '=== Debug end' 

            # Collect the labels
            for label in labels:
                # Skip unknown label
                if not label in self.classifier_label: continue
                classifier_id = self.classifier_label[label]
                if (classifier_id in container_text 
                    and classifier_id in container_class):
                    container_text[classifier_id].append(clean_text)
                    container_class[classifier_id].append(label)
                else:
                    container_text[classifier_id] = [clean_text]
                    container_class[classifier_id] = [label]

            # Create artificial label not_oot
            if not 'oot' in labels:
                label = 'not_oot'
                classifier_name = CLASSIFIER_OOT
                if (classifier_name in container_text 
                    and classifier_name in container_class):
                    container_text[classifier_name].append(clean_text)
                    container_class[classifier_name].append(label)
                else:
                    container_text[classifier_name] = [clean_text]
                    container_class[classifier_name] = [label]

            # Create artificial label not_agus_sylvi
            if (not 'pos_agus_sylvi' in labels 
                    and not 'neg_agus_sylvi' in labels):
                label = 'not_agus_sylvi'
                classifier_name = CLASSIFIER_AGUS_SYLVI
                if (classifier_name in container_text 
                    and classifier_name in container_class):
                    container_text[classifier_name].append(clean_text)
                    container_class[classifier_name].append(label)
                else:
                    container_text[classifier_name] = [clean_text]
                    container_class[classifier_name] = [label]

            # Create artificial label not_ahok_djarot
            if (not 'pos_ahok_djarot' in labels 
                    and not 'neg_ahok_djarot' in labels):
                label = 'not_ahok_djarot'
                classifier_name = CLASSIFIER_AHOK_DJAROT
                if (classifier_name in container_text 
                    and classifier_name in container_class):
                    container_text[classifier_name].append(clean_text)
                    container_class[classifier_name].append(label)
                else:
                    container_text[classifier_name] = [clean_text]
                    container_class[classifier_name] = [label]

            # Create artificial label not_anies_sandi
            if (not 'pos_anies_sandi' in labels 
                    and not 'neg_anies_sandi' in labels):
                label = 'not_anies_sandi'
                classifier_name = CLASSIFIER_ANIES_SANDI
                if (classifier_name in container_text 
                    and classifier_name in container_class):
                    container_text[classifier_name].append(clean_text)
                    container_class[classifier_name].append(label)
                else:
                    container_text[classifier_name] = [clean_text]
                    container_class[classifier_name] = [label]

        csv_file.close()

    # input_file is a path to csv with the following headers: 
    # 'title', 'raw_content', 'labels'
    # output_file is a path where the model written into
    def train(self, input_file, output_file):
        # Collect the training data
        self._collect_data_from_csv(input_file, self.training_data_text, 
            self.training_data_class)

        # For each classifier, we extract the features and train the 
        # classifier
        for key in self.training_data_text:
            news_texts = self.training_data_text[key]
            news_labels = self.training_data_class[key]
            
            # Create feature extractor
            feature_extractor = TfidfVectorizer(min_df=self.min_df,
                ngram_range=(1,self.max_ngram), 
                decode_error='ignore',
                stop_words=stopwords.stopwords,
                tokenizer=self.tokenizer)
            feature_extractor.fit(news_texts)

            # For debugging purpose, print out all the features
            # print '=========='
            # print key
            # print '----------'
            # for word in feature_extractor.get_feature_names():
            #     print word
            # print '=========='

            # Extract the features
            X = feature_extractor.transform(news_texts)
            y = news_labels

            # Train the classifier
            classifier = OneVsRestClassifier(LinearSVC(random_state=0))
            classifier.fit(X, y)

            # Save the classifier
            self.classifiers[key] = {
                'classifier': classifier,
                'feature_extractor': feature_extractor
            }

        # Save the model as binary file
        pickle.dump(self.classifiers, open(output_file, 'w'), 
            protocol=pickle.HIGHEST_PROTOCOL)

    def load_model(self, model):
        self.classifiers = pickle.load(open(model))

    def eval(self, model, test_data):
        # Load the model
        self.load_model(model)

        # Collect the test data
        self._collect_data_from_csv(test_data, self.test_data_text, 
            self.test_data_class)

        # We do the evaluation
        for key in self.test_data_text:
            news_texts = self.test_data_text[key]
            news_labels = self.test_data_class[key]
            classifier = self.classifiers[key]['classifier']
            feature_extractor = self.classifiers[key]['feature_extractor']

            # Extract the features
            X = feature_extractor.transform(news_texts)
            y_true = news_labels

            # Predict
            y_pred = classifier.predict(X)

            # For debugging purpose
            # print '=== Start debug'
            # print 'Classifier:', key
            # for i in xrange(len(y_pred)):
            #     true_label = y_true[i]
            #     pred_label = y_pred[i]
            #     if true_label != pred_label:
            #         print 'content:', news_texts[i]
            #         print 'true label:', true_label
            #         print 'pred label:', pred_label
            #         print '-------'
            # print '=== End debug'

            # Evaluate the score
            precision = metrics.precision_score(y_true, y_pred, 
                average='micro')
            recall = metrics.recall_score(y_true, y_pred, 
                average='micro')
            f1_score = 2*((precision*recall)/(precision+recall))
            print 'classifier:', key
            print 'precision:', precision
            print 'recall:', recall
            print 'f1:', f1_score

            # Create the confusion matrix visualization
            conf_matrix = metrics.confusion_matrix(y_true, y_pred)
            plot_confusion_matrix(conf_matrix, 
                classes=classifier.classes_,
                title='Confusion matrix without normalization',
                classifier_name=key)

    def predict_proba(self, news_text, threshold=0.5):
        result = {}
        score = {}
        labels = []
        oot_status = '' # 'not_oot' or 'oot'
        # Pre-process the input
        clean_text = clean_string(news_text)
        for key in self.classifiers:
            classifier = self.classifiers[key]['classifier']
            feature_extractor = self.classifiers[key]['feature_extractor']
            X = feature_extractor.transform([clean_text])
            res = classifier.decision_function(X)
            if key == CLASSIFIER_OOT:
                if res[0][0] > 0:
                    oot_status = classifier.classes_[1]
                    score['oot'] = res[0][0]
                else:
                    oot_status = classifier.classes_[0]
                    score['oot'] = res[0][0]
            else:
                for i, class_name in enumerate(classifier.classes_):
                    confident_score = res[0][i]
                    score[class_name] = confident_score
        result['confident_score'] = score
        result['oot_status'] = oot_status
        # Create label summary
        if oot_status == 'not_oot':
            for key in score:
                if score[key] >= threshold:
                    if not 'not' in key:
                        labels.append(key)
        else:
            labels.append('oot')

        result['labels'] = labels
        return result

if __name__ == '__main__':
    max_ngram = 5
    rojak = RojakOvRPair(max_ngram=max_ngram, tokenizer=whitespace_tokenizer)
    model_name = 'rojak_ovr_pair_latest_{}_gram_model.bin'.format(max_ngram)
    rojak.train('data_training_7_labels_latest.csv', model_name)
    rojak.eval(model_name, 'data_training_7_labels_latest.csv')
    
    print '== Test'
    test_news_text = '''
    Ogah Ikut 'Perang' Statement di Pilgub DKI, Agus: Menghabiskan Energi
    <strong>Jakarta </strong> - Pasangan incumbent DKI Basuki T Purnama (
    Ahok) dan Djarot Saiful Hidayat beberapa kali tampak adu statement 
    dengan pasangan bakal calon Anies Baswedan dan Sandiaga Uno. Kandidat 
    bakal Cagub DKI Agus Harimurti mengaku tak mau ikut-ikutan terlebih 
    dahulu. <br> <br> ""Pertama masa kampanye baru dimulai 28 Oktober. 
    Artinya itu berdasarkan UU itulah yang akan saya gunakan langsung 
    official untuk menyebarluaskan menyampaikan gagasan visi misi program 
    kerja dan sebagainya,"" ungkap Agus. <br> <br> Hal tersebut 
    disampaikannya saat berbincang di redaksi detikcom, Jalan Warung Jati 
    Barat Raya, Jakarta Selatan, Kamis (6/10/2016). Agus mengaku saat ini 
    lebih ingin memanfaatkan waktu untuk mensosialisasikan diri sesuai 
    tahapan KPUD. <br> <br> ""Pada akhirnya tentu saya akan lakukan itu. 
    Saya menghindari konflik karena hati saya mengatakan buat apa saya 
    mencari dari kesalahan orang atau terlibat dalam konflik karena 
    menghabiskan energi,"" ucapnya. <br> <br> Apalagi menurut Agus, ia 
    berhubungan baik dengan para pasangan calon tersebut. Mantan Danyon 203/
    Arya Kemuning itu mengaku ingin fokus menyapa masyarakat bersama dengan 
    pasangan cawagubnya, Sylvia Murni. <br> <br> ""Saatnya nanti kita akan 
    langsung ke masyarakat. (Untuk mensosialisasikan) yang saya miliki, 
    mengapa anda harus memahami dan mengapa ada kepentingan Anda untuk 
    memilih saya,"" kata Agus. <br> <br> Kehadiran putra sulung Presiden 
    ke-6 RI Susilo Bambang Yudhoyono (SBY) itu seperti antitesa seorang Ahok 
    yang dikenal keras. Agus dinilai sebagai sosok yang santun dan membumi. <
    br> <br> ""Insya Allah yang saya tampilkan sehari-hari itu apa adanya 
    saya. Karena saya tidak setuju kalau mengubah karakter yang sudah 
    dibentuk selama puluhan tahun kemudian dibentuk hanya untuk memenuhi 
    permintaan pasar atau permintaan media,"" terang dia. <br> <br> 
    ""Artinya saya menjadi sesuatu yang artificial, saya di CFD berlari 
    menyapa masyarakat itu juga yang sebetulnya saya biasa lakukan dulu 
    ataupun sebelum saya punya kesibukan di kota lain,"" imbuh Agus. <br> <
    br> Mantan perwira berpangkat Mayor itu memastikan penampilan atau sikap 
    sehari-harinya bukan sebagai sesuatu yang palsu. Agus juga menyatakan 
    ada banyak aspirasi masyarakat yang ia dapati ketika turun menyapa ke 
    lapangan. <br> <br> ""Mereka mengekpresikan banyak hal. Yang paling (
    saya) senang ya tentu mendoakan 'Pak, semoga sukses'. Tetapi saya tidak 
    ingin hanya disenangi tapi untuk mencari tahu apa yang menjadi keluhan 
    dan kebutuhan masyakarat,"" urainya. <br> <br> Lantas apa yang paling 
    banyak didapat Agus ketika menyapa warga? <br> <br> ""Mereka ingin 
    kehidupan ekonominya menjadi baik, lingkungan lebih baik, nggak terlalu 
    macet, bisa memiliki akses kesehatan yang lebih baik. Tapi banyak juga 
    yang mereka (mengatakan) 'Pak kami ingin dihargai, ingin diayomi,'. As 
    simpel as that,"" jawab Agus. <br> <br> Pernyataan itu tampaknya seperti 
    menyindir Ahok yang beberapa kali beradu mulut dengan warga. Ini terkait 
    dengan kebijakan Ahok yang tidak diterima warga. Tak jarang petahana itu 
    mengeluarkan kata-kata makian. <br> <br> ""(Warga juga bilang) 'kami 
    punya harga diri pak. Kami nggak butuh itu, tidak perlu yang 
    berlebihan-lebihan asalkan kami dihargai sebagai warga masyarakat'. 
    Sebagai human being yang memiliki hak dan kewajiban yang juga untuk 
    memajukan daerahnya. Jadi kadang ada yang begitu juga,"" cerita Agus. <
    br> <br> Seperti diketahui, Ahok beberapa kali memberi pernyataan 
    'serangan' kepada pasangan Anies-Sandiaga. Ahok sempat terlibat argumen 
    lewat media tentang kebersihan sungai di Jakarta. Kemudian Ahok dan 
    Sandiaga juga 'perang' pernyataan tentang pembuktian harta terbalik. 
    Terakhir Ahok menyerang dengan mengatakan Sandiaga adalah pengemplang 
    pajak karena ikut program Tax Amnesty. <br> <br>   <iframe src=""http://
    tv.detik.com/20detik/embed/161007018/"" frameborder=""0"" 
    scrolling=""no"" width=""420"" height=""236"" 
    allowfullscreen=""allowfullscreen""></iframe>   <br> <br>   <strong>(ear/
    imk)</strong>"
    '''
    test_news_label = 'pos_agus_sylvi'
    prediction = rojak.predict_proba(test_news_text)
    print 'Text news:'
    print test_news_text
    print 'True label:', test_news_label
    print 'Prediction:', prediction


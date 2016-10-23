# Rojak SVM for sentiment classification
# References:
# * Thumbs up? Sentiment Classification using Machine Learning Techniques 
#   http://www.cs.cornell.edu/home/llee/papers/sentiment.pdf 
# * Fast and accurate sentiment classification using an enhanced Naive Bayes
#   model 
#   https://arxiv.org/pdf/1305.6143.pdf
# * Exploring Sentiment Classification Techniques in News Articles 
#   http://researchdatabase.ac.zw/519/2/Exploring%20Sentiment%20Classification%20Techniques%20in%20News%20Articles.pdf 
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

# Compile regex to remove non-alphanum char
nonalpha = re.compile('[^a-z\-]+')

# Normalize the word
def normalize_word(w):
    word = w.lower()
    word = nonalpha.sub(' ', word)
    word = word.strip()
    return word

# Compile regex to remove author signature from the text
# Example: (nkn/dnu)
author_signature = re.compile('\([a-zA-Z]+/[a-zA-Z]+\)')

# Function to clean the raw string
def clean_string(s):    
    result_str = []

    # Remove the noise: html tag
    clean_str = BeautifulSoup(s, 'lxml').text
    # Remove the noise: author signature
    clean_str = author_signature.sub(' ', clean_str)

    # For each word we clear out the extra format
    for w in clean_str.split(' '):
        word = normalize_word(w)
        if word != '' and word != '-':
            result_str.append(word)

    return ' '.join(result_str)

# Given list of news texts, this function will return a sparse matrix
# feature X
def extract_features(news_texts, vocabulary=None, method='tf'):
    # We use {uni,bi,tri}gram as feature here
    # The feature should appear in at least in 3 docs
    vectorizer = CountVectorizer(ngram_range=(1,3), 
        vocabulary=vocabulary, decode_error='ignore', 
        min_df=3).fit(news_texts)
    X = vectorizer.transform(news_texts)
    if method == 'tfidf':
        X = TfidfTransformer().fit_transform(X)
    return X, vectorizer.get_feature_names()

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

class RojakSVM():
    # Storing classifier
    classifiers = {}

    # Map of label name and the corresponding classifier ID
    classifier_label = {
        'pos_ahok_djarot': 'classifier_ahok_djarot',
        'neg_ahok_djarot': 'classifier_ahok_djarot',
        'pos_anies_sandi': 'classifier_anies_sandi',
        'neg_anies_sandi': 'classifier_anies_sandi',
        'pos_agus_sylvi': 'classifier_agus_sylvi',
        'neg_agus_sylvi': 'classifier_agus_sylvi',
        'oot': 'all_classifier'
    }

    # Map classifier ID and the training and test data
    training_data_text = {
        'classifier_ahok_djarot': [],
        'classifier_anies_sandi': [],
        'classifier_agus_sylvi': []
    }
    training_data_class = {
        'classifier_ahok_djarot': [],
        'classifier_anies_sandi': [],
        'classifier_agus_sylvi': []
    }
    test_data_text = {
        'classifier_ahok_djarot': [],
        'classifier_anies_sandi': [],
        'classifier_agus_sylvi': []
    }
    test_data_class = {
        'classifier_ahok_djarot': [],
        'classifier_anies_sandi': [],
        'classifier_agus_sylvi': []
    }

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
            clean_title = clean_string(title).encode('utf-8', 'ignore')
            clean_content = clean_string(raw_content).encode('utf-8', 
                'ignore')
            clean_text = '{} {}'.format(clean_title, clean_content)

            # Collect the training data
            for label in labels:
                # Skip unknown label
                if not label in self.classifier_label: continue
                classifier_name = self.classifier_label[label]
                if classifier_name == 'all_classifier':
                    for key in self.training_data_text:
                        container_text[key].append(clean_text)
                        container_class[key].append(label)
                else:
                    container_text[classifier_name].append(
                        clean_text)
                    container_class[classifier_name].append(label)
        csv_file.close()

    # input_file is a path to csv with the following headers: 
    # 'title', 'raw_content' and 'labels'.
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
            feature_extractor = TfidfVectorizer(ngram_range=(1,3), 
                decode_error='ignore', min_df=3)
            feature_extractor.fit(news_texts)

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

    def eval(self, model, test_data):
        # Load the model
        self.classifiers = pickle.load(open(model))

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

    def predict(self, news_texts):
        result = []
        for key in self.classifiers:
            classifier = self.classifiers[key]['classifier']
            feature_extractor = self.classifiers[key]['feature_extractor']
            X = feature_extractor.transform(news_texts)
            res = classifier.decision_function(X)
            result = result + zip(classifier.classes_, res[0])
        return result

if __name__ == '__main__':
    rojak = RojakSVM()
    rojak.train('sentiment_classification_data.csv', 'rojak_svm_model.bin')
    rojak.eval('rojak_svm_model.bin', 'sentiment_classification_data.csv')
    
    print '== Test'
    test_news_texts = ['''
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
    ''']
    test_news_label = 'pos_agus_sylvi'
    prediction = rojak.predict(test_news_texts)
    print 'Text news:'
    print test_news_texts
    print 'True label:', test_news_label
    print 'Prediction:', prediction


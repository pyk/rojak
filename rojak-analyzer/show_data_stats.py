import csv
from collections import Counter
import re

from bs4 import BeautifulSoup

csv_file = open('data_detikcom_labelled.csv')
csv_reader = csv.DictReader(csv_file)

words = []
docs = []
label_counter = {}
unique_label_counter = {}
for row in csv_reader:
    title = row['title'].strip().lower()
    raw_content = row['raw_content']

    clean_content = BeautifulSoup(raw_content, 'lxml').text
    # Compile regex to remove non-alphanum char
    nonalpha = re.compile('[\W_]+')

    for word in title.split(' '):
        word = word.lower()
        word = nonalpha.sub('', word)
        if word != '':
            words.append(word)
    for word in clean_content.split(' '):
        word = word.lower()
        word = nonalpha.sub('', word)
        if word != '':
            words.append(word)

    labels = []
    sentiment_1 = row['sentiment_1']
    if sentiment_1 != '':
        labels.append(sentiment_1)
        if sentiment_1 in unique_label_counter:
            unique_label_counter[sentiment_1] += 1
        else:
            unique_label_counter[sentiment_1] = 1

    sentiment_2 = row['sentiment_2']
    if sentiment_2 != '':
        labels.append(sentiment_2)
        if sentiment_2 in unique_label_counter:
            unique_label_counter[sentiment_2] += 1
        else:
            unique_label_counter[sentiment_2] = 1

    sentiment_3 = row['sentiment_3']
    if sentiment_3 != '':
        labels.append(sentiment_3)
        if sentiment_3 in unique_label_counter:
            unique_label_counter[sentiment_3] += 1
        else:
            unique_label_counter[sentiment_3] = 1

    label_name = ','.join(sorted(labels))
    if label_name != '':
        if label_name in label_counter:
            label_counter[label_name] += 1
        else:
            label_counter[label_name] = 1
    else:
        print 'WARNING: "{}" does not have label'.format(title)

print 'Unique label statistics:'
for key in unique_label_counter:
    label_name = key
    label_count = unique_label_counter[key]
    print '{}: {}'.format(label_name, label_count)
print ''

print 'Label statistics:'
total_data = 0
for key in label_counter:
    label_name = key
    label_count = label_counter[key]
    total_data += label_count
    print '{}: {}'.format(label_name, label_count)
print 'Total data:', total_data
print ''

counter = Counter(words)
print '10 Most common words:'
for word in counter.most_common(10):
    print '{},{}'.format(word[0], word[1])

csv_file.close()

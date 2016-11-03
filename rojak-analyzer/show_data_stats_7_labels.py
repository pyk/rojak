import csv
from collections import Counter
import re

from bs4 import BeautifulSoup

csv_file = open('data_training_7_labels_latest.csv')
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

    labels = row['labels'].split(',')
    for label in labels:
        if label in unique_label_counter:
            unique_label_counter[label] += 1
        else:
            unique_label_counter[label] = 1

    label_name = ','.join(sorted(labels))
    if label_name != '':
        if label_name in label_counter:
            label_counter[label_name] += 1
        else:
            label_counter[label_name] = 1
    else:
        print 'WARNING: "{}" does not have label'.format(title)

print 'Unique label statistics:'
for key in sorted(unique_label_counter):
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

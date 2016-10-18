import csv
from bs4 import BeautifulSoup
from collections import Counter
import re
import os

OUTPUT_NAME = os.getenv('OUTPUT_NAME', 'train.data')
LABEL_PREFIX = os.getenv('LABEL_PREFIX', '__LABEL__')

csv_file = open('data_detikcom_labelled.csv')
csv_reader = csv.DictReader(csv_file)

train_file = open(OUTPUT_NAME, 'w')
for row in csv_reader:
    title = row['title'].strip().lower()
    raw_content = row['raw_content']
    clean_content = BeautifulSoup(raw_content, 'lxml').text
    content = []
    labels = []

    # Compile regex to remove non-alphanum char
    nonalpha = re.compile('[^a-z\-]+')

    for word in title.split(' '):
        word = word.lower()
        word = nonalpha.sub('', word)
        if word != '':
            content.append(word)
    for word in clean_content.split(' '):
        word = word.lower()
        word = nonalpha.sub('', word)
        if word != '':
            content.append(word)
    content_str = ' '.join(content).strip()

    if row['sentiment_1'] != '':
        label = row['sentiment_1']
        label_name = '{}{}'.format(LABEL_PREFIX, label)
        labels.append(label_name)
    if row['sentiment_2'] != '':
        label = row['sentiment_2']
        label_name = '{}{}'.format(LABEL_PREFIX, label)
        labels.append(label_name)
    if row['sentiment_3'] != '':
        label = row['sentiment_3']
        label_name = '{}{}'.format(LABEL_PREFIX, label)
        labels.append(label_name)

    # Skip content if label not exists
    if not labels: continue
    label_str = ' '.join(labels)
    train_line = '{} {}\n'.format(label_str, content_str)
    train_file.write(train_line)

csv_file.close()

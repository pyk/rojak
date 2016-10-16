# TODO: create training data
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

    content = ' '.join(content)
    train_line = '{}'
counter = Counter(words)
for word in counter.most_common(len(counter)):
    print '{},{}'.format(word[0], word[1])

csv_file.close()

import csv
from bs4 import BeautifulSoup
from collections import Counter
import re
import os

OUTPUT_NAME = os.getenv('OUTPUT_NAME', 'test_data.txt')

csv_file = open('data_detikcom_labelled.csv')
csv_reader = csv.DictReader(csv_file)

test_file = open(OUTPUT_NAME, 'w')
headers = ['clean_content', 'labels']
csv_writer = csv.DictWriter(test_file, fieldnames=headers)
csv_writer.writeheader()
for row in csv_reader:
    title = row['title'].strip().lower()
    raw_content = row['raw_content']
    clean_content = BeautifulSoup(raw_content, 'lxml').text
    content = []
    labels = []

    # Compile regex to remove non-alphanum char
    nonalpha = re.compile('[^a-z\-]+')
    for word in title.split(' '):
        lower_word = word.lower()
        clean_word = nonalpha.sub('', lower_word)
        if clean_word != '':
            content.append(clean_word)
    for word in clean_content.split(' '):
        lower_word = word.lower()
        clean_word = nonalpha.sub('', lower_word)
        if clean_word != '':
            content.append(clean_word)
    content_str = ' '.join(content).strip()

    if row['sentiment_1'] != '':
        label = row['sentiment_1']
        labels.append(label)
    if row['sentiment_2'] != '':
        label = row['sentiment_2']
        labels.append(label)
    if row['sentiment_3'] != '':
        label = row['sentiment_3']
        labels.append(label)

    # Skip content if label not exists
    if not labels: continue
    label_str = ','.join(labels)
    test_data ={
        'clean_content': content_str,
        'labels': label_str
    }
    csv_writer.writerow(test_data)

csv_file.close()
test_file.close()

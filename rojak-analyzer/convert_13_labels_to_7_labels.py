import csv
from bs4 import BeautifulSoup
from collections import Counter
import re
import os

OUTPUT_NAME = os.getenv('OUTPUT_NAME', 
    'data_detikcom_labelled_740_7_class.csv')

csv_file = open('data_detikcom_labelled_740.csv')
csv_reader = csv.DictReader(csv_file)

# Tranform individual label to candidate pair label
label_map = {
    'pos_ahok': 'pos_ahok_djarot',
    'pos_djarot': 'pos_ahok_djarot',
    'pos_anies': 'pos_anies_sandi',
    'pos_sandi': 'pos_anies_sandi',
    'pos_agus': 'pos_agus_sylvi',
    'pos_sylvi': 'pos_agus_sylvi',
    'neg_ahok': 'neg_ahok_djarot',
    'neg_djarot': 'neg_ahok_djarot',
    'neg_anies': 'neg_anies_sandi',
    'neg_sandi': 'neg_anies_sandi',
    'neg_agus': 'neg_agus_sylvi',
    'neg_sylvi': 'neg_agus_sylvi',
    'oot': 'oot'
}

fields = ['title', 'raw_content', 'labels']
train_file = open(OUTPUT_NAME, 'w')
csv_writer = csv.DictWriter(train_file, fields)
csv_writer.writeheader()
for row in csv_reader:
    title = row['title']
    raw_content = row['raw_content']
    labels = []

    label_1 = row['sentiment_1']
    if label_1 != '':
        candidate_pair_label = label_map[label_1]
        if not candidate_pair_label in labels:
            labels.append(candidate_pair_label)
    label_2 = row['sentiment_2']
    if label_2 != '':
        candidate_pair_label = label_map[label_2]
        if not candidate_pair_label in labels:
            labels.append(candidate_pair_label)
    label_3 = row['sentiment_3']
    if label_3 != '':
        candidate_pair_label = label_map[label_3]
        if not candidate_pair_label in labels:
            labels.append(candidate_pair_label)

    # Skip content if label not exists
    if not labels: continue
    label_str = ','.join(labels)

    data_row = {'title': title, 'raw_content': raw_content, 
        'labels': label_str}
    csv_writer.writerow(data_row)

print OUTPUT_NAME, 'created'
csv_file.close()
train_file.close()

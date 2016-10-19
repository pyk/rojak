import csv
from bs4 import BeautifulSoup
from collections import Counter
import re

csv_file = open('data_detikcom_740.csv')
csv_reader = csv.DictReader(csv_file)

words = []
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

counter = Counter(words)
for word in counter.most_common(len(counter)):
    print '{},{}'.format(word[0], word[1])

csv_file.close()

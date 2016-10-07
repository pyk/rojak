import MySQLdb as mysql
from faker import Factory
import random
import os
import sys

ROJAK_DB_HOST = os.getenv('ROJAK_DB_HOST', 'localhost')
ROJAK_DB_PORT = os.getenv('ROJAK_DB_PORT', '3306')
ROJAK_DB_USER = os.getenv('ROJAK_DB_USER', 'root')
ROJAK_DB_PASS = os.getenv('ROJAK_DB_PASS', 'rojak')
ROJAK_DB_NAME = os.getenv('ROJAK_DB_NAME', 'rojak_database')

# Open database connection
db = mysql.connect(host=ROJAK_DB_HOST, port=ROJAK_DB_PORT,
        user=ROJAK_DB_USER, passwd=ROJAK_DB_PASS,
        db=ROJAK_DB_NAME)

# Create new db cursor
cursor = db.cursor()

# Get list of the media
medias = []
sql_get_medias = '''
select id,website_url from media;
'''
try:
    cursor.execute(sql_get_medias)
    results = cursor.fetchall()
    for row in results:
        media_id = row[0]
        media_url = row[1]
        medias.append({'id': media_id, 'url': media_url})
except mysql.Error as err:
    print 'Unable to fetch media data', err
    sys.exit()

# Get list of sentiment
sentiment_ids = []
sql_get_sentiment = '''
select id from sentiment;
'''
try:
    cursor.execute(sql_get_sentiment)
    results = cursor.fetchall()
    for row in results:
        sentiment_id = row[0]
        sentiment_ids.append(sentiment_id)
except mysql.Error as err:
    print 'Unable to fetch sentiment data', err
    sys.exit()

# Get list of candidate
candidate_ids = []
sql_get_candidate = '''
select id from candidate;
'''
try:
    cursor.execute(sql_get_candidate)
    results = cursor.fetchall()
    for row in results:
        candidate_id = row[0]
        candidate_ids.append(candidate_id)
except mysql.Error as err:
    print 'Unable to fetch candidate data', err
    sys.exit()

# Generate random data for the news
MAX_NEWS=100
sql_insert_news = '''
INSERT INTO `news`(`media_id`, `title`, `content`, `url`)
VALUES ('{}', '{}', '{}', '{}');
'''
sql_insert_sentiment = '''
INSERT INTO `news_sentiment`(`news_id`, `sentiment_id`, `score`)
VALUES ('{}', '{}', '{}');
'''
sql_insert_mention = '''
INSERT INTO `mention`(`news_id`, `candidate_id`)
VALUES ('{}', '{}');
'''
fake = Factory.create()
total_sentiment = len(sentiment_ids)
total_candidate = len(candidate_ids)
for media in medias:
    media_id = media['id']
    media_url = media['url']
    for i in xrange(MAX_NEWS):
        content = fake.text()
        title = ' '.join(content.split()[:10]) + ' ' + str(media_id)
        content += ' ' + fake.text()
        content += ' ' + fake.text()
        title_url = title.lower().replace(' ', '-')
        url = '{}/{}'.format(media_url, title_url)

        n_label = random.randint(1, 3)
        sentiments = set([])
        for i in xrange(n_label):
            sentiment_i = random.randint(0, total_sentiment-1)
            sentiments.add(sentiment_ids[sentiment_i])

        n_mention = random.randint(1, 5)
        mentions = set([])
        for i in xrange(n_mention):
            candidate_i = random.randint(0, total_candidate-1)
            mentions.add(candidate_ids[candidate_i])

        # insert to the database
        try:
            # Parse the SQL command
            insert_sql = sql_insert_news.format(media_id, title, content, url)
            cursor.execute(insert_sql)
            news_id = cursor.lastrowid
            for sentiment_id in sentiments:
                score = random.uniform(0.5, 1.0)
                insert_sql = sql_insert_sentiment.format(news_id,
                        sentiment_id, score)
                cursor.execute(insert_sql)

            for candidate_id in mentions:
                insert_sql = sql_insert_mention.format(news_id,
                        candidate_id)
                cursor.execute(insert_sql)
            db.commit()
        except mysql.Error as err:
            print("Something went wrong: {}".format(err))
            db.rollback()

# Close the DB connection
db.close()


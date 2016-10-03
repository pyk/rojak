import MySQLdb as mysql
from faker import Factory
import random

MAX_MEDIA = 100
MAX_SENTIMENT = 10

# Open database connection
db = mysql.connect('localhost', 'root', 'rojak', 'rojak_database')

# Create new db cursor
cursor = db.cursor()

sql_news = '''
INSERT INTO `news`(`media_id`, `title`, `content`, `url`)
VALUES ('{}', '{}', '{}', '{}');
'''

sql_sentiment = '''
INSERT INTO `news_sentiment`(`news_id`, `sentiment_id`)
VALUES ('{}', '{}');
'''

MAX_NEWS=1000
fake = Factory.create()
for i in xrange(MAX_NEWS):
    print ''
    print '== DEBUG: generate data'
    # Generate random data for the news
    media_id = random.randint(1, MAX_MEDIA)
    title = ' '.join(fake.text().split()[:10]) + ' ' + str(media_id)
    content = fake.text()
    content += ' ' + fake.text()
    content += ' ' + fake.text()
    title_url = title.lower().replace(' ', '-')
    url = 'https://artificialintelligence.id/{}-{}'.format(title_url, media_id)
    n_label = random.randint(1, 3)
    sentiments = set([])
    for i in xrange(n_label):
        sentiment_id = random.randint(1, MAX_SENTIMENT)
        sentiments.add(sentiment_id)

    # insert to the database
    try:
        # Parse the SQL command
        insert_sql = sql_news.format(media_id, title, content, url)
        cursor.execute(insert_sql)
        news_id = cursor.lastrowid
        print '== DEBUG: news_data:'
        print insert_sql
        print '== DEBUG: news_id:', news_id
        for sentiment_id in sentiments:
            insert_sql = sql_sentiment.format(news_id, sentiment_id)
            cursor.execute(insert_sql)
            print '== DEBUG: sentiment_id', sentiment_id
        db.commit()
    except mysql.Error as err:
        print("Something went wrong: {}".format(err))
        db.rollback()

# Close the DB connection
db.close()



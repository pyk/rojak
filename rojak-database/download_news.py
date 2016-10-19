import MySQLdb as mysql
import os
import csv
import sys

MEDIA_NAME = os.getenv('MEDIA_NAME', 'detikcom')
ROJAK_DB_HOST = os.getenv('ROJAK_DB_HOST', 'localhost')
ROJAK_DB_PORT = int(os.getenv('ROJAK_DB_PORT', 3306))
ROJAK_DB_USER = os.getenv('ROJAK_DB_USER', 'root')
ROJAK_DB_PASS = os.getenv('ROJAK_DB_PASS', 'rojak')
ROJAK_DB_NAME = os.getenv('ROJAK_DB_NAME', 'rojak_database')

# Open database connection
db = mysql.connect(host=ROJAK_DB_HOST, port=ROJAK_DB_PORT,
        user=ROJAK_DB_USER, passwd=ROJAK_DB_PASS,
        db=ROJAK_DB_NAME)

# Create new db cursor
cursor = db.cursor()

sql_get_media_id = '''
select id from media where name=%s;
'''
try:
    cursor.execute(sql_get_media_id, [MEDIA_NAME])
    result = cursor.fetchone()
    media_id = result[0]
except mysql.Error as err:
    print 'Unable to fetch media id', err
    sys.exit()

sql_get_news_count = '''
select count(*) from news where media_id=%s;
'''
try:
    cursor.execute(sql_get_news_count, [media_id])
    result = cursor.fetchone()
    news_count = result[0]
except mysql.Error as err:
    print 'Unable to fetch news count', err
    sys.exit()

sql_get_news = """
select title,url,raw_content,published_at from news where media_id=%s;
"""

# Read CSV file
file_name = 'data_{}_{}.csv'.format(MEDIA_NAME, news_count)
output_file = open(file_name, 'w')
fields = ['title', 'url', 'raw_content', 'published_at_utc']
csv_writer = csv.DictWriter(output_file, fields)
csv_writer.writeheader()

try:
    cursor.execute(sql_get_news, [media_id])
    for i in xrange(news_count):
        result = cursor.fetchone()
        title = result[0]
        url = result[1]
        raw_content = result[2]
        published_at = result[3]
        csv_writer.writerow({'title': title, 'url': url, 'raw_content':
            raw_content, 'published_at_utc': published_at})
except mysql.Error as err:
    print 'Unable to fetch news', err
    sys.exit()

output_file.close()

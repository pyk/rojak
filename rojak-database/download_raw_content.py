import MySQLdb as mysql
import os
import csv

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

sql_get_news = """
select title,url,raw_content from news where url=%s;
"""

# Read CSV file
csv_file = open('labeling_data_detikcom_0-500.csv')
output_file = open('data_detikcom.csv', 'w')
fields = ['title', 'url', 'raw_content', 'sentiment_1', 'sentiment_2', 'sentiment_3']
csv_writer = csv.DictWriter(output_file, fields)
csv_reader = csv.DictReader(csv_file)
csv_writer.writeheader()
for row in csv_reader:
    url = row['url']
    cursor.execute(sql_get_news, [url])
    result = cursor.fetchone()
    if result:
        title = result[0]
        url = result[1]
        raw_content = result[2]
        sentiment_1 = row['sentiment_1']
        sentiment_2 = row['sentiment_2']
        sentiment_3 = row['sentiment_3']
        csv_writer.writerow({'title': title, 'url': url, 'raw_content':
            raw_content, 'sentiment_1': sentiment_1, 'sentiment_2': sentiment_2,
            'sentiment_3': sentiment_3})
    else:
        print url, 'not exists in the database'

csv_file.close()
output_file.close()

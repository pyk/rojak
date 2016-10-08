import MySQLdb as mysql
from faker import Factory
import os
import json
import sys

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

data_file = open('data_media.json')
data_media = json.load(data_file)
sql_insert_media = '''
INSERT INTO `media`(`name`, `website_url`, `logo_url`,
    `fbpage_username`, `twitter_username`, `instagram_username`)
VALUES (%s, %s, %s, %s, %s, %s);
'''

for media in data_media['media']:
    media_name = media['name']
    media_website_url = media['website_url']
    media_logo_url = media['logo_url']
    if media_logo_url == '':
        media_logo_url = None
    media_fbpage_username = media['fbpage_username']
    if media_fbpage_username == '':
        media_fbpage_username = None
    media_twitter_username = media['twitter_username']
    if media_twitter_username == '':
        media_twitter_username = None
    media_instagram_username = media['instagram_username']
    if media_instagram_username == '':
        media_instagram_username = None

    # insert to the database
    try:
        cursor.execute(sql_insert_media, (media_name, media_website_url,
            media_logo_url, media_fbpage_username, media_twitter_username,
            media_instagram_username))
        db.commit()
    except mysql.Error as err:
        print("Something went wrong: {}".format(err))
        db.rollback()

# Close the DB connection
db.close()

# Close the file stream
data_file.close()

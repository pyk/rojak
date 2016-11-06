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

sql_insert_candidate = '''
INSERT INTO `candidate`(`full_name`, `alias_name`, `place_of_birth`,
    `date_of_birth`, `religion`, `website_url`, `photo_url`,
    `fbpage_username`, `twitter_username`, `instagram_username`)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
'''
sql_insert_candidate_pair = '''
INSERT INTO `pair_of_candidates`(`cagub_id`, `cawagub_id`, `name`,
    `website_url`, `logo_url`, `fbpage_username`, `slogan`,
    `description`, `twitter_username`, `instagram_username`)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
'''
sql_insert_sentiment = '''
INSERT INTO `sentiment`(`name`, `pair_of_candidates_id`)
VALUES (%s, %s);
'''

# Insert data from file_name to the database db
def insert_data(db, file_name):
    # Read the data
    data_pasangan = json.load(open(file_name))
    if not 'pasangan_calon' in data_pasangan:
        raise ValueError('key pasangan_calon not exists')

    # Create database cursor
    cursor = db.cursor()

    for pasangan in data_pasangan['pasangan_calon']:
        pair_name = pasangan['name']
        pair_website_url = pasangan['website_url']
        if pair_website_url == '':
            pair_website_url = None
        pair_logo_url = pasangan['logo_url']
        if pair_logo_url == '':
            pair_logo_url = None
        pair_slogan = pasangan['slogan']
        pair_description = pasangan['description']
        pair_fbpage_username = pasangan['fbpage_username']
        if pair_fbpage_username == '':
            pair_fbpage_username = None
        pair_twitter_username = pasangan['twitter_username']
        if pair_twitter_username == '':
            pair_twitter_username = None
        pair_instagram_username = pasangan['instagram_username']
        if pair_instagram_username == '':
            pair_instagram_username = None

        # Insert cagub data
        cagub_full_name = pasangan['cagub']['full_name']
        cagub_alias_name = pasangan['cagub']['alias_name']
        cagub_place_of_birth = pasangan['cagub']['place_of_birth']
        cagub_date_of_birth = pasangan['cagub']['date_of_birth']
        cagub_religion = pasangan['cagub']['religion']
        cagub_photo_url = pasangan['cagub']['photo_url']
        if cagub_photo_url == '':
            cagub_photo_url = None
        cagub_fbpage_username = pasangan['cagub']['fbpage_username']
        if cagub_fbpage_username == '':
            cagub_fbpage_username = None
        cagub_twitter_username = pasangan['cagub']['twitter_username']
        if cagub_twitter_username == '':
            cagub_twitter_username = None
        cagub_instagram_username = pasangan['cagub']['instagram_username']
        if cagub_instagram_username == '':
            cagub_instagram_username = None
        cagub_website_url = pasangan['cagub']['website_url']
        if cagub_website_url == '':
            cagub_website_url = None
        cagub_id = -1
        try:
            cursor.execute(sql_insert_candidate, [cagub_full_name,
                cagub_alias_name, cagub_place_of_birth,
                cagub_date_of_birth, cagub_religion, cagub_website_url,
                cagub_photo_url, cagub_fbpage_username,
                cagub_twitter_username, cagub_instagram_username])
            cagub_id = cursor.lastrowid
            db.commit()
        except mysql.Error as err:
            print("Something went wrong: {}".format(err))
            db.rollback()
            sys.exit()

        # Insert cawagub data
        cawagub_full_name = pasangan['cawagub']['full_name']
        cawagub_alias_name = pasangan['cawagub']['alias_name']
        cawagub_place_of_birth = pasangan['cawagub']['place_of_birth']
        cawagub_date_of_birth = pasangan['cawagub']['date_of_birth']
        cawagub_religion = pasangan['cawagub']['religion']
        cawagub_photo_url = pasangan['cawagub']['photo_url']
        cawagub_photo_url = pasangan['cawagub']['photo_url']
        if cawagub_photo_url == '':
            cawagub_photo_url = None
        cawagub_fbpage_username = pasangan['cawagub']['fbpage_username']
        if cawagub_fbpage_username == '':
            cawagub_fbpage_username = None
        cawagub_twitter_username = pasangan['cawagub']['twitter_username']
        if cawagub_twitter_username == '':
            cawagub_twitter_username = None
        cawagub_instagram_username = pasangan['cawagub']['instagram_username']
        if cawagub_instagram_username == '':
            cawagub_instagram_username = None
        cawagub_website_url = pasangan['cawagub']['website_url']
        if cawagub_website_url == '':
            cawagub_website_url = None
        cawagub_id = -1
        try:
            cursor.execute(sql_insert_candidate, [cawagub_full_name,
                cawagub_alias_name, cawagub_place_of_birth,
                cawagub_date_of_birth, cawagub_religion, cawagub_website_url,
                cawagub_photo_url, cawagub_fbpage_username,
                cawagub_twitter_username, cawagub_instagram_username])
            cawagub_id = cursor.lastrowid
            db.commit()
        except mysql.Error as err:
            print("Something went wrong: {}".format(err))
            db.rollback()
            sys.exit()

        # Insert to the database
        try:
            cursor.execute(sql_insert_candidate_pair, [cagub_id, cawagub_id,
                pair_name, pair_website_url, pair_logo_url, 
                pair_fbpage_username, pair_slogan, pair_description,
                pair_twitter_username, pair_instagram_username])
            pair_candidate_id = cursor.lastrowid
            db.commit()
        except mysql.Error as err:
            print("Something went wrong: {}".format(err))
            db.rollback()

        # Insert sentiment
        sentiments = pasangan['sentiments']
        for sentiment_name in sentiments:
            try:
                cursor.execute(sql_insert_sentiment, [sentiment_name, 
                    pair_candidate_id])
                db.commit()
            except mysql.Error as err:
                print("Something went wrong: {}".format(err))
                db.rollback()

    # Insert oot sentiment
    try:
        cursor.execute(sql_insert_sentiment, ['oot', 
            None])
        db.commit()
    except mysql.Error as err:
        print("Something went wrong: {}".format(err))
        db.rollback()

if __name__ == '__main__':
    # Open database connection
    db = mysql.connect(host=ROJAK_DB_HOST, port=ROJAK_DB_PORT,
            user=ROJAK_DB_USER, passwd=ROJAK_DB_PASS,
            db=ROJAK_DB_NAME)

    # Create new db cursor
    insert_data(db, 'data_pasangan_cagub_cawagub.json')

    # Close the DB connection
    db.close()

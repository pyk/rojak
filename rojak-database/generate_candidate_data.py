import MySQLdb as mysql
from faker import Factory
import os

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

sql_candidate = '''
INSERT INTO `candidate`(`full_name`, `alias_name`, `place_of_birth`,
    `date_of_birth`, `religion`, `website_url`, `photo_url`,
    `fbpage_username`, `twitter_username`, `instagram_username`)
VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}',
        '{}', '{}');
'''

# Create random candidate data
MAX_CANDIDATES=6
fake = Factory.create()
candidate_ids = []
for i in xrange(MAX_CANDIDATES):
    # Generate random data for the candidates
    full_name = fake.name()
    alias_name = full_name
    place_of_birth = 'Indonesia'
    date_of_birth = '2016-10-01'
    religion = 'Universe'
    website_name = full_name.replace(' ', '').lower()
    website_url = 'https://{}.com'.format(website_name)
    cat_img = 'http://lorempixel.com/500/500/cats/{}'.format(full_name)
    photo_url = cat_img
    fbpage_username = website_name
    twitter_username = website_name
    instagram_username = website_name

    # Parse the SQL command
    insert_sql = sql_candidate.format(full_name, alias_name, place_of_birth,
            date_of_birth, religion, website_url, photo_url, fbpage_username,
            twitter_username, instagram_username)

    # insert to the database
    try:
        cursor.execute(insert_sql)
        candidate_id = cursor.lastrowid
        candidate_ids.append({'id': candidate_id, 'name': full_name})
        db.commit()
    except mysql.Error as err:
        print("Something went wrong: {}".format(err))
        db.rollback()

# Generate candidate pair
sql_candidate_pair = '''
INSERT INTO `pair_of_candidates`(`cagub_id`, `cawagub_id`, `name`,
    `website_url`, `logo_url`, `fbpage_username`, `slogan`,
    `description`, `twitter_username`, `instagram_username`)
VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}');
'''
is_skip = -1
for i in xrange(MAX_CANDIDATES):
    if is_skip == i: continue
    cagub_i = candidate_ids[i]['id']
    cawagub_i = candidate_ids[i+1]['id']
    is_skip = i + 1
    cagub_name = candidate_ids[i]['name']
    cawagub_name = candidate_ids[i+1]['name']
    pair_name = '{} dan {}'.format(cagub_name, cawagub_name)
    website_name = pair_name.replace(' ', '').lower()
    website_url = 'https://{}.com'.format(website_name)
    cat_img = 'http://lorempixel.com/500/500/cats/{}'.format(website_name)
    logo_url = cat_img
    fbpage_username = website_name
    twitter_username = website_name
    instagram_username = website_name
    slogan = 'Slogan {} dan {}'.format(cagub_name, cawagub_name)
    description = fake.text()

    # Parse the SQL command
    insert_sql = sql_candidate_pair.format(cagub_i, cawagub_i, pair_name,
            website_url, logo_url, fbpage_username, slogan, description,
            twitter_username, instagram_username)

    # insert to the database
    try:
        cursor.execute(insert_sql)
        db.commit()
    except mysql.Error as err:
        print("Something went wrong: {}".format(err))
        db.rollback()

# Close the DB connection
db.close()



import MySQLdb as mysql
from faker import Factory
import os

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

sql = '''
INSERT INTO `media`(`name`, `website_url`, `logo_url`, `fbpage_username`,
    `description`)
VALUES ('{}', '{}', '{}', '{}', '{}');
'''

MAX_MEDIA=100
fake = Factory.create()
for i in xrange(MAX_MEDIA):
    # Generate random data for the media
    media_name = fake.name() + ' Media ' + str(i)
    website_name = media_name.lower().replace(' ', '')
    website_url = 'https://{}.com'.format(website_name)
    cat_img = 'http://lorempixel.com/500/500/cats/{}'.format(website_name)
    logo_url = cat_img
    fbpage_username = website_name
    description = fake.text()

    # Parse the SQL command
    insert_sql = sql.format(media_name, website_url, logo_url,
        fbpage_username, description)

    # insert to the database
    try:
        cursor.execute(insert_sql)
        db.commit()
    except mysql.Error as err:
        print("Something went wrong: {}".format(err))
        db.rollback()

# Close the DB connection
db.close()



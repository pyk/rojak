import MySQLdb as mysql
from faker import Factory

# Open database connection
db = mysql.connect('localhost', 'root', 'rojak', 'rojak_database')

# Create new db cursor
cursor = db.cursor()

sql = '''
INSERT INTO `media`(`name`, `website_url`, `logo_url`, `facebookpage_url`,
    `slogan`)
VALUES ('{}', '{}', '{}', '{}', '{}');
'''

MAX_MEDIA=100
fake = Factory.create('it_IT')
for i in xrange(MAX_MEDIA):
    # Generate random data for the media
    media_name = fake.name() + ' Media ' + str(i)
    website_name = media_name.lower().replace(' ', '')
    website_name = website_name.replace("'", '')
    website_url = 'https://{}.com'.format(website_name)
    cat_txt = website_name
    cat_img = 'http://lorempixel.com/500/500/cats/{}'.format(cat_txt)
    logo_url = cat_img
    facebookpage_url = 'https://facebook.com/{}'.format(website_name)
    slogan = ' '.join(fake.text().split()[:5])

    # Parse the SQL command
    insert_sql = sql.format(media_name, website_url, logo_url,
        facebookpage_url, slogan)

    # insert to the database
    try:
        cursor.execute(insert_sql)
        db.commit()
    except mysql.Error as err:
        print("Something went wrong: {}".format(err))
        db.rollback()

# Close the DB connection
db.close()



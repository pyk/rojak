import MySQLdb as mysql
from faker import Factory

# Open database connection
db = mysql.connect('localhost', 'root', 'rojak', 'rojak_database')

# Create new db cursor
cursor = db.cursor()

sql = '''
INSERT INTO `candidates`(`name`, `website_url`, `image_url`, `logo_url`,
    `facebookpage_url`, `slogan`)
VALUES ('{}', '{}', '{}', '{}', '{}', '{}');
'''

MAX_CANDIDATES=5
fake = Factory.create()
for i in xrange(MAX_CANDIDATES):
    # Generate random data for the candidates
    cagub = fake.name()
    cawagub = fake.name()
    candidate_name = '{} - {}'.format(cagub, cawagub)
    website_name = '{}-and-{}'.format(cagub, cawagub).replace(' ', '').lower()
    website_url = 'https://{}.com'.format(website_name)
    cat_txt = '-'.join(cagub.lower().split(' '))
    cat_img = 'http://lorempixel.com/500/500/cats/{}'.format(cat_txt)
    image_url = cat_img
    logo_url = cat_img
    facebookpage_url = 'https://facebook.com/{}'.format(website_name)
    slogan = ' '.join(fake.text().split()[:5])

    # Parse the SQL command
    insert_sql = sql.format(candidate_name, website_url, image_url,
        logo_url, facebookpage_url, slogan)

    # insert to the database
    try:
       cursor.execute(insert_sql)
       db.commit()
    except mysql.Error as err:
       print("Something went wrong: {}".format(err))
       db.rollback()

# Close the DB connection
db.close()



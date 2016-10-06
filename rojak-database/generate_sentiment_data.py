import MySQLdb as mysql
from faker import Factory
import os
import sys

ROJAK_DB_HOST = os.getenv('ROJAK_DB_HOST', 'localhost')
ROJAK_DB_USER = os.getenv('ROJAK_DB_USER', 'root')
ROJAK_DB_PASS = os.getenv('ROJAK_DB_PASS', 'rojak')
ROJAK_DB_NAME = os.getenv('ROJAK_DB_NAME', 'rojak_database')

# Open database connection
db = mysql.connect(ROJAK_DB_HOST, ROJAK_DB_USER,
        ROJAK_DB_PASS, ROJAK_DB_NAME)

# Create new db cursor
cursor = db.cursor()

sql = '''
INSERT INTO `sentiment`(`name`, `candidate_id`)
VALUES ('{}', '{}');
'''

# Get list of the candidates
candidates = []
sql_get_candidates = '''
SELECT id,name FROM candidate;
'''

try:
    cursor.execute(sql_get_candidates)
    results = cursor.fetchall()
    for row in results:
        candidate_id = row[0]
        candidate_name = row[1]
        candidates.append({
            'id': candidate_id,
            'name': candidate_name})
except mysql.Error as err:
    print 'Unable to fetch candidate data', err
    sys.exit()

    # Generate random data for the sentiment
for candidate in candidates:
    candidate_id = candidate['id']
    candidate_name = candidate['name']
    for sentiment in  ['pro', 'con', 'net']:
        candidate_first_name = candidate_name.split(' ')[0].lower()
        sentiment_name = '{}_{}'.format(sentiment, candidate_first_name)

        # Parse the SQL command
        insert_sql = sql.format(sentiment_name, candidate_id)

        # insert to the database
        try:
            cursor.execute(insert_sql)
            db.commit()
        except mysql.Error as err:
            print("Something went wrong: {}".format(err))
            db.rollback()

# Close the DB connection
db.close()



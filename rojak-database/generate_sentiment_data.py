import MySQLdb as mysql
from faker import Factory

# Open database connection
db = mysql.connect('localhost', 'root', 'rojak', 'rojak_database')

# Create new db cursor
cursor = db.cursor()

sql = '''
INSERT INTO `sentiment`(`name`)
VALUES ('{}');
'''

MAX_SENTIMENT=10
for i in xrange(MAX_SENTIMENT):
    # Generate random data for the sentiment
    sentiment_name = 'sentiment_{}'.format(i + 1)

    # Parse the SQL command
    insert_sql = sql.format(sentiment_name)

    # insert to the database
    try:
        cursor.execute(insert_sql)
        db.commit()
    except mysql.Error as err:
        print("Something went wrong: {}".format(err))
        db.rollback()

# Close the DB connection
db.close()



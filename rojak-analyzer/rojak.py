# TODO: add rojak.py train --data path/to/file --output path/to/model
# TODO: add rojak.py run --model path/to/model
# TODO: make easy to change the algorithm, add class wrapper with two methods:
#       train, load_model & predict
import csv

import click
import MySQLdb as mysql

# Change class below to use different method
#from rojak_fasttext import RojakFastTextWrapper
#from rojak_svm import RojakSVM
from rojak_ovr import RojakOvR as Rojak
rojak = Rojak()

@click.group()
def cli():
    pass

# Train Rojak
@click.command('train')
@click.option('--input', 'input_file',
        default='', help='Path to training data file',
        type=click.Path(exists=True))
@click.option('--output', 'output_file',
        default='', help='Where the model written to',
        type=click.Path())
def train(input_file, output_file):
    """Train Rojak"""
    rojak.train(input_file, output_file)
cli.add_command(train)

# Eval Rojak
@click.command('eval')
@click.option('--model', default='', help='Path to the model file',
        type=click.Path(exists=True))
@click.option('--test-data', default='', help='Path to test data',
        type=click.Path(exists=True))
def evaluate(model, test_data):
    rojak.eval(model, test_data)
cli.add_command(evaluate)

# Run Rojak
@click.command('run')
@click.option('--model', default='', help='Path to the model file',
    type=click.Path(exists=True))
@click.option('--db-host', 'db_host', default='localhost', 
    help='Database host')
@click.option('--db-port', 'db_port', default=3306, 
    help='Database port number')
@click.option('--db-user', 'db_user', default='root', 
    help='Database user name')
@click.option('--db-pass', 'db_pass', default='rojak', 
    help='Database user password')
@click.option('--db-name', 'db_name', default='rojak_database', 
    help='Database name')
@click.option('--max-news', default=100, help='Maximal news analyzed')
@click.option('--exclude-media', 'exclude_media_id', default=-1, 
    help='Exclude news that have media_id to be analyzed')
def run(model, db_host, db_port, db_user, db_pass, db_name, max_news, 
    exclude_media_id):
    """Run Rojak to analyze data on the database"""
    # Load the model
    rojak.load_model(model)

    # Open database connection
    db = mysql.connect(host=db_host, port=db_port, user=db_user, 
        passwd=db_pass, db=db_name)

    # Create new db cursor
    cursor = db.cursor()

    # SQL query to get the news
    sql_get_news = '''
        select id, title, raw_content
        from news
        where is_analyzed=false and media_id!=%s
        limit %s;
    '''
    cursor.execute(sql_get_news, [exclude_media_id, max_news])
    for i in xrange(max_news):
        title = ''
        raw_content = ''

        result = cursor.fetchone()
        if result:
            news_id = result[0]
            news_title = result[1]
            news_raw_content = result[2]
        else:
            print 'Cannot fetch news, skipping ...'
            continue

        # Get the sentiment
        raw_text = '{} {}'.format(news_title, news_raw_content)
        print [raw_text]

        pred_labels = rojak.predict_proba([raw_text])
        print pred_labels
        # TODO: 
        # - predict the raw_text
        # - insert sentiment to the database (up to 0.5)

    # TODO: get news where is_analyzed=false from the database
    # with limit max-news
    # TODO: for each news we perform prediction then insert it to the
    # database news_sentiment
    # TODO: We also perform mention check here, a simple string matching
    #print db_host, db_port, db_user, db_pass, db_name, max_news

cli.add_command(run)

if __name__ == '__main__':
    cli()

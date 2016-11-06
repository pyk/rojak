import csv

import click
import MySQLdb as mysql

# Custom tokenizer
# TODO: fix this, we can't load the model without this declaration
# something wrong with the pickle stuff
def whitespace_tokenizer(s):
    return s.split(' ')

# Change class below to use different method
#from rojak_fasttext import RojakFastTextWrapper
#from rojak_svm import RojakSVM
# from rojak_ovr import RojakOvR as Rojak
import rojak_ovr_pair
from rojak_ovr_pair import RojakOvRPair
rojak = RojakOvRPair(max_ngram=5, min_df=3,
    tokenizer=rojak_ovr_pair.whitespace_tokenizer)

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

# Map candidate name to their corresponding data
candidate_data = {
    'Agus Harimurti Yudhoyono': {
        'alias': ['agus', 'harimurti', 'ahy'],
        'id': -1
    },
    'Sylviana Murni': {
        'alias': ['sylvi', 'sylviana', 'silvy'],
        'id': -1
    },
    'Basuki Tjahaja Purnama': {
        'alias': ['ahok', 'basuki'],
        'id': -1
    },
    'Djarot Saiful Hidayat': {
        'alias': ['djarot'],
        'id': -1
    },
    'Anies Baswedan': {
        'alias': ['anies'],
        'id': -1
    },
    'Sandiaga Salahuddin Uno': {
        'alias': ['sandiaga', 'sandi', 'uno'],
        'id': -1
    }
}

# Sentiment data
# Map sentiment name to id
sentiment_data_id = {
    'pos_agus_sylvi': -1,
    'neg_agus_sylvi': -1,
    'pos_ahok_djarot': -1,
    'neg_ahok_djarot': -1,
    'pos_anies_sandi': -1,
    'neg_anies_sandi': -1,
    'oot': -1
}

# Function to scale the score
# value score_raw:
# -1.x < score_raw < 1.x
# we want to convert it to 0 < x <= 1.0 scale
def scale_confident_score(score_raw):
    score = abs(score_raw)
    if score >= 1.0:
        return 1.0
    else:
        return score

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
@click.option('--exclude-media', 'exclude_media_names', default='',
    help='Exclude media, media name separated by comma')
@click.option('--only-media', 'only_media_names', default='',
    help='Run analyzer only for this media')
def run(model, db_host, db_port, db_user, db_pass, db_name, max_news, 
    exclude_media_names, only_media_names):
    """Run Rojak to analyze data on the database"""
    # Load the model
    rojak.load_model(model)

    # Open database connection
    db = mysql.connect(host=db_host, port=db_port, user=db_user, 
        passwd=db_pass, db=db_name)
    # Set autocommit to false
    db.autocommit(False)
    # Create new db cursor
    select_cursor = db.cursor()

    # Get candidate ID
    sql_get_candidate_id = 'select id from candidate where full_name=%s;'
    for candidate_name in candidate_data:
        try:
            select_cursor.execute(sql_get_candidate_id, [candidate_name])
            res = select_cursor.fetchone()
            candidate_id = int(res[0])
            candidate_data[candidate_name]['id'] = candidate_id
        except mysql.Error as err:
            raise Exception(err)

    # Get sentiment ID
    sql_get_sentiment_id = 'select id from sentiment where name=%s;'
    for sentiment_name in sentiment_data_id:
        try:
            select_cursor.execute(sql_get_sentiment_id, [sentiment_name])
            res = select_cursor.fetchone()
            sentiment_id = int(res[0])
            sentiment_data_id[sentiment_name] = sentiment_id
        except mysql.Error as err:
            raise Exception(err)

    # Exclude media if any
    excluded_media = exclude_media_names.split(',')
    excluded_media_ids = []
    sql_get_media_id = 'select id from media where name=%s;'
    for media_name in excluded_media:
        if media_name == '': continue
        # Get the id
        try:
            select_cursor.execute(sql_get_media_id, [media_name])
            res = select_cursor.fetchone()
            media_id = res[0]
        except mysql.Error as err:
            raise Exception(err)
        # Concat the sql string
        excluded_media_ids.append('media_id!=' + str(media_id) + ' ')

    # Run only for the following media
    only_media = only_media_names.split(',')
    only_media_ids = []
    for media_name in only_media:
        if media_name == '': continue
        # Get the id
        try:
            select_cursor.execute(sql_get_media_id, [media_name])
            res = select_cursor.fetchone()
            media_id = res[0]
        except mysql.Error as err:
            raise Exception(err)
        # Concat the sql string
        only_media_ids.append('media_id=' + str(media_id) + ' ')

    # SQL query to get the news
    sql_get_news_template = '''
        select id, title, raw_content, media_id
        from news
        where is_analyzed=false
        {}{}
    '''
    excluded_media_sql = ''
    if len(excluded_media_ids) > 0:
        excluded_media_sql = 'and '.join(excluded_media_ids)
        excluded_media_sql = 'and ({})'.format(excluded_media_sql)
    only_media_sql = ''
    if len(only_media_ids) > 0:
        only_media_sql = 'or '.join(only_media_ids)
        only_media_sql = 'and ({})'.format(only_media_sql)

    sql_get_news = sql_get_news_template.format(excluded_media_sql,
        only_media_sql)
    print '=== Start debug sql_get_news'
    print 'sql_get_news:', sql_get_news
    print '=== End debug sql_get_news'
    select_cursor.execute(sql_get_news)
    for i in xrange(max_news):
        title = ''
        raw_content = ''

        result = select_cursor.fetchone()
        if result:
            news_id = result[0]
            news_title = result[1]
            news_raw_content = result[2]
            news_media_id = result[3]
        else:
            print 'Cannot fetch news, skipping ...'
            continue
        raw_text = '{} {}'.format(news_title, news_raw_content)

        # Get mention information
        print '=== Start debug mention'
        clean_raw_text = rojak_ovr_pair.clean_string(raw_text, 
            use_synonym=False)
        normalized_words = clean_raw_text.lower().split(' ')
        print 'raw_text:', raw_text
        print 'normalized_words:', normalized_words
        mentioned_candidates = []
        for candidate_name in candidate_data:
            alias = candidate_data[candidate_name]['alias']
            is_mentioned = False
            for alias_name in alias:
                if alias_name in normalized_words:
                    is_mentioned = True
            if is_mentioned:
                mentioned_candidates.append(candidate_name)
        print 'mentioned_candidates:', mentioned_candidates
        print '=== End debug mention'

        print '=== Start debug label'
        pred = rojak.predict_proba(raw_text)
        print 'label:', pred['labels']
        print 'confident_score:', pred['confident_score']
        print '=== End debug label'
        
        # Insert to the database
        insert_cursor = db.cursor()
        sql_insert_mention = '''
            insert into mention(`news_id`, `candidate_id`)
            values (%s, %s);
        '''
        sql_insert_sentiment = '''
            insert into news_sentiment(`news_id`, `sentiment_id`, 
                `confident_score_raw`, `confident_score_scaled`)
            values (%s, %s, %s, %s);
        '''
        sql_update_is_analyzed = '''
            update news set is_analyzed=true where id=%s;
        '''
        try:
            # For mention data
            for candidate_name in mentioned_candidates:
                candidate_id = candidate_data[candidate_name]['id']
                if candidate_id == -1: 
                    raise Exception('candidate_id data not updated')
                insert_cursor.execute(sql_insert_mention, [news_id, 
                    candidate_id])

            # For sentiment data
            labels = pred['labels']
            if not labels:
                raise Exception('Cannot predict the labels')
            for label in labels:
                sentiment_id = sentiment_data_id[label]
                if sentiment_id == -1: 
                    raise Exception('candidate_id data not updated')
                score = pred['confident_score'][label]
                score_scaled = scale_confident_score(score)
                insert_cursor.execute(sql_insert_sentiment, [news_id, 
                    sentiment_id, score, score_scaled])

            # Update is_analyzed status
            insert_cursor.execute(sql_update_is_analyzed, [news_id])
            db.commit()
            insert_cursor.close()
        except Exception as err:
            db.rollback()
            print 'Failed to analyze news:', news_id
            print 'Error:', err
            continue
    select_cursor.close()
    db.close()

cli.add_command(run)

if __name__ == '__main__':
    cli()

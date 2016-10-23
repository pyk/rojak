# TODO: add rojak.py train --data path/to/file --output path/to/model
# TODO: add rojak.py run --model path/to/model
# TODO: make easy to change the algorithm, add class wrapper with two methods:
#       train, load_model & predict
import csv

import click
import fasttext
import sklearn.preprocessing as prep

# Change class below to use different method
#from rojak_fasttext import RojakFastTextWrapper
from rojak_svm import RojakSVM
rojak = RojakSVM()

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
@click.option('--db-host', default='localhost', help='Database host')
@click.option('--db-port', default='3306', help='Database port number')
@click.option('--db-user', default='root', help='Database user name')
@click.option('--db-pass', default='rojak', help='Database user password')
@click.option('--db-name', default='rojak', help='Database name')
@click.option('--max-news', default=100, help='Maximal news analyzed')
def run(host, port, user, password, name, max_news):
    """Run Rojak to analyze data on the database"""
    # TODO: get news where is_analyzed=false from the database
    # with limit max-news
    # TODO: for each news we perform prediction then insert it to the
    # database news_sentiment
    # TODO: We also perform mention check here, a simple string matching
    print host, port, user, password, name

cli.add_command(run)

if __name__ == '__main__':
    cli()


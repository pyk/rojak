# TODO: add rojak.py train --data path/to/file --output path/to/model
# TODO: add rojak.py run --model path/to/model
# TODO: make easy to change the algorithm, add class wrapper with two methods:
#       train, load_model & predict
import csv

import click
import fasttext
import sklearn.preprocessing as prep

@click.group()
def cli():
    pass

# Train Rojak
@click.command('train')
@click.option('--data', default='', help='Path to training data file',
        type=click.Path(exists=True))
@click.option('--output', default='', help='Where the model written to',
        type=click.Path())
def train(data, output):
    # TODO: access label prefix info from create_training_data.py
    #       or create new sub-command to create training data
    # TODO: access training fasttext model using class wrapper
    fasttext.supervised(data, output, label_prefix='__LABEL__',
        dim=300, min_count=1, thread=2, silent=0)

cli.add_command(train)

# Eval Rojak
@click.command('eval')
@click.option('--model', default='', help='Path to model file',
        type=click.Path(exists=True))
@click.option('--test-data', default='', help='Path to test data',
        type=click.Path(exists=True))
def evaluate(model, test_data):
    """
    Test data should be in CSV format with the following headers:

        clean_content,labels

    \b
    * clean_content: clean content of the news
    * labels: string list of labels separated by commas
    """
    # TODO: access load_model using class wrapper
    classifier = fasttext.load_model(model, label_prefix='__LABEL__')
    # Read the correct labels and convert it to binary format
    test_data_file = open(test_data)
    csv_reader = csv.DictReader(test_data_file)
    classes = []
    text_labels = []
    for row in csv_reader:
        # get correct labels
        labels = row['labels'].split(',')
        for label in labels:
            if not label in classes:
                classes.append(label)
        text_labels.append(labels)

        # predict the label
        text = row['clean_content']
        print text
        pred_labels = classifier.predict([text], len(classes))
        print labels
        print pred_labels
        print ''
        print ''
    # TODO: convert to multilabel binary format
    classes = sorted(classes)
    mlb = prep.MultiLabelBinarizer(classes=classes)
    correct_labels = mlb.fit_transform(text_labels)

    test_data_file.close()
cli.add_command(evaluate)


if __name__ == '__main__':
    cli()

# Given list of detikcom data unlabelled and labelled, we want to find 
# data that unlabelled yet
import csv

def diff(unlabelled_file, labelled_file, output_file):
    # Prepare the output file
    fields = ['title', 'url', 'raw_content', 'sentiment_1', 'sentiment_2',
        'sentiment_3']
    output_csv = csv.DictWriter(open(output_file, 'w'), fields)
    output_csv.writeheader()

    # Read data from labelled
    labelled_urls = set([])
    labelled = csv.DictReader(open(labelled_file))
    for row in labelled:
        try:
            url = row['url']
        except Exception as err:
            raise ValueError(err)
        labelled_urls.add(url)

    # Read from unlabelled data
    unlabelled = csv.DictReader(open(unlabelled_file))
    for row in unlabelled:
        try:
            title = row['title']
            url = row['url']
            raw_content = row['raw_content']
        except Exception as err:
            raise ValueError(err)

        if not url in labelled_urls:
            unlabelled_data = {
                'title': title,
                'url': url,
                'raw_content': raw_content
            }
            output_csv.writerow(unlabelled_data)

if __name__ == '__main__':
    unlabelled = 'data_detikcom_740.csv'
    labelled = 'data_detikcom_labelled.csv'
    diff(unlabelled, labelled, 'data_detikcom_unlabelled.csv')

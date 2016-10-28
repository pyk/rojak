# Given list of detikcom data: unlabelled with raw_content and labelled 
# without raw_content. We want to merge the  data to  
# data_detikcom_labelled.csv
import csv

def merge_data(unlabelled_file, labelled_files, output_file):
    # Prepare the output file
    fields = ['title', 'url', 'raw_content', 'sentiment_1', 'sentiment_2',
        'sentiment_3']
    output_csv = csv.DictWriter(open(output_file, 'w'), fields)
    output_csv.writeheader()

    # Read data from unlabelled
    news = {} # Map url to content
    unlabelled = csv.DictReader(open(unlabelled_file))
    for row in unlabelled:
        try:
            title = row['title']
            url = row['url']
            raw_content = row['raw_content']
            published_at_utc = row['published_at_utc']
        except Exception as err:
            raise ValueError(err)

        news[url] = {'title': title, 'url': url, 'raw_content': raw_content,
            'published_at_utc': published_at_utc}

    # Create labelled data
    for file in labelled_files:
        labelled = csv.DictReader(open(file))
        for row in labelled:
            try:
                title = row['title']
                url = row['url']
                sentiment_1 = row['sentiment_1']
                sentiment_2 = row['sentiment_2']
                sentiment_3 = row['sentiment_3']
            except Exception as err:
                raise ValueError(err)

            if url in news:
                data = news[url]
                labelled_data = {
                    'title': data['title'],
                    'url': data['url'],
                    'raw_content': data['raw_content'],
                    'sentiment_1': sentiment_1,
                    'sentiment_2': sentiment_2,
                    'sentiment_3': sentiment_3
                }
                output_csv.writerow(labelled_data)
            else:
                print url, 'not exists'

if __name__ == '__main__':
    unlabelled = 'data_detikcom_740.csv'
    labelled = ['data_detikcom_labelled_0_500.csv',
        'data_detikcom_labelled_501_1000.csv']
    merge_data(unlabelled, labelled, 'data_detikcom_labelled.csv')

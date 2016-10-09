# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb as mysql
from scrapy.exceptions import CloseSpider

class SaveToMySQL(object):
    sql_insert_news = '''
        INSERT INTO `news`(`media_id`, `title`, `raw_content`,
            `url`, `author_name`, `published_at`)
        VALUES (%s, %s, %s, %s, %s, %s);
    '''

    def process_item(self, item, spider):
        url = item.get('url')
        title = item.get('title')
        author_name = item.get('author_name')
        raw_content = item.get('raw_content')
        published_at = item.get('published_at')

        # Insert to the database
        try:
            spider.cursor.execute(self.sql_insert_news, [spider.media['id'],
                title, raw_content, url, author_name, published_at])
            spider.db.commit()
        except mysql.Error as err:
            spider.db.rollback()
            error_msg = '{}: Unable to save news: {}'.format(
                spider.name, err)
            spider.slack.chat.post_message('#rojak-pantau-errors', error_msg,
                as_user=True)

        return item

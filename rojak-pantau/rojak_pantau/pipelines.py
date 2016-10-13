# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb as mysql
from scrapy.exceptions import CloseSpider, DropItem

class NewsValidation(object):
    def process_item(self, item, spider):
        title = item.get('title', 'title_not_set')
        if title == 'title_not_set':
            err_msg = 'Missing title in: %s' % item.get('url')
            raise DropItem(err_msg)

        raw_content = item.get('raw_content', 'raw_content_not_set')
        if raw_content == 'raw_content_not_set':
            err_msg = 'Missing raw_content in: %s' % item.get('url')
            raise DropItem(err_msg)

        published_at = item.get('published_at', 'published_at_not_set')
        if published_at == 'published_at_not_set':
            err_msg = 'Missing published_at in: %s' % item.get('url')
            raise DropItem(err_msg)

        # Pass item to the next pipeline, if any
        return item

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
            if spider.is_slack:
                error_msg = '{}: Unable to save news: {}\n```\n{}\n```\n'.format(
                    spider.name, url, err)
                spider.slack.chat.post_message('#rojak-pantau-errors', error_msg,
                    as_user=True)

        return item

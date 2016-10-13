from scrapy import Request
from scrapy.http import HtmlResponse


"""
Create scrapy fake HTTP response from HTML file
@param file_name : sample html file to provide response from, relative path
@param url : the url to mock the response to
"""
def mock_response(file_name, url):
    request = Request(url=url)

    file_content = open(file_name, 'r').read()
    response = HtmlResponse(url=url, request=request, body=file_content,
        encoding='utf-8')

    return response

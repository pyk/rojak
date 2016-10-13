from unittest.case import TestCase
from datetime import datetime

from rojak_pantau.spiders.metrotvnews import MetrotvnewsSpider
from rojak_pantau.tests.util.mock_response import mock_response


class MetrotvnewsTest(TestCase):
    def setUp(self):
        self.spider = MetrotvnewsSpider()

    def test_parse(self):
        scraped_urls = 20
        valid_urls = [
            'http://news.metrotvnews.com/metro/GKd3veek-sandi-ajak-cagub-cawagub-lain-transparan',
            'http://video.metrotvnews.com/headline-news/zNPAyqXb-warga-dukung-kpud-dki-bertindak-profesional',
            'http://video.metrotvnews.com/360/ob37nLJb-ibu-kota-butuh-suara-ibu',
            'http://video.metrotvnews.com/360/ZkeW535N-kekuatan-sang-calon-wakil-gubernur-dki-jakarta',
            'http://pilkada.metrotvnews.com/news-pilkada/8N0YpXdb-sandiaga-berharap-bisa-lebih-banyak-bantu-kaum-duafa',
            'http://news.metrotvnews.com/metro/Dkqjn14K-bawaslu-dki-tak-persoalkan-kontrak-politik-pasangan-calon-dengan-rakyat',
            'http://news.metrotvnews.com/politik/aNrJG7gN-sandiaga-mengakui-biaya-demokrasi-mahal',
            'http://video.metrotvnews.com/30-minutes/nN9Jl2Gb-pilihan-jakarta',
            'http://news.metrotvnews.com/metro/aNrJG0gN-bawaslu-dki-pernyataan-ahok-di-kepulauan-seribu-bukan-pelanggaran',
            'http://news.metrotvnews.com/politik/akWw69qk-ruhut-di-ambang-sanksi',
            'http://pilkada.metrotvnews.com/news-pilkada/wkBq9Xgb-bnn-waspadai-masuknya-uang-bandar-narkoba-di-pilkada',
            'http://pilkada.metrotvnews.com/news-pilkada/aNrJGvaN-ahok-serahkan-proses-hukum-soal-penistaan-agama-ke-polisi',
            'http://video.metrotvnews.com/mata-najwa/8N0YpwAb-highlight-mata-najwa-bertaruh-di-jakarta',
            'http://pilkada.metrotvnews.com/news-pilkada/Wb77l4Pb-visi-misi-agus-sylvi',
            'http://pilkada.metrotvnews.com/news-pilkada/Rb1l4z1N-ucapan-ahok-rawan-dijadikan-alat-propaganda',
            'http://pilkada.metrotvnews.com/news-pilkada/yNLyoPqb-visi-misi-anies-sandi',
            'http://pilkada.metrotvnews.com/news-pilkada/ZkeW5YPN-visi-misi-ahok-djarot',
            'http://news.metrotvnews.com/politik/VNxJV48k-ahok-dianggap-perlu-jubir',
            'http://news.metrotvnews.com/politik/GNGyvBLk-ahy-sby-dan-kursi-ri-1',
            'http://news.metrotvnews.com/politik/akWw63Wk-bagi-agus-ikut-pilkada-panggilan-jiwa'
        ]
        start_page = 'http://www.metrotvnews.com/more/topic/8602/0'
        next_page = 'http://www.metrotvnews.com/more/topic/8602/20'

        response = mock_response(
            'tests/data/metrotvnews_sample_page.html', start_page)
        items = self.spider.parse(response)

        # Iterate the response generator
        for i, item in enumerate(items):
            if i == scraped_urls:
                self.assertEqual(item.url, next_page)
            else:
                self.assertEqual(item.url, valid_urls[i])

    def test_parse_news(self):
        start_page = 'http://news.metrotvnews.com/metro/GKd3veek-sandi-ajak-cagub-cawagub-lain-transparan'
        response = mock_response(
            'tests/data/metrotvnews_sample_article.html', start_page)
        item = self.spider.parse_news(response)

        self.assertEqual(
            item['title'][0], 'Sandi Ajak Cagub-Cawagub Lain Transparan')
        self.assertEqual(
            item['author_name'][0], 'Meilikhah')
        # Original 13 October 2016 23:11 WIB => 13 October 2016 16:11 UTC
        self.assertEqual(
            item['published_at'][0], datetime(2016, 10, 13, 16, 11))
        # Validate if raw html content, not text
        self.assertIsNotNone(item['raw_content'][0])
        self.assertTrue('</div>' in item['raw_content'][0])

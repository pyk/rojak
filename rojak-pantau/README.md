# rojak-pantau

Kita menggunakan [Scrapy](https://doc.scrapy.org) untuk dasar `rojak-pantau`.
Hal ini dikarenakan beberapa pertimbangan yang telah kita diskusikan
antara lain:

1. Cocok untuk tim. Setiap anggota tim yang mau menambah media tinggal melakukan
   penambahan dan perubahan sedikit pada source code.
2. Mudah di deploy
3. Lengkapnya dokumentasi

## Setup
Pastikan kamu sudah mensetup instance MySQL lokal lalu mempopulate database
nya:

    cd rojak-database
    python insert_candidate_data.py
    python insert_media_data.py


## Jalanin pemantau

    sh install_dependencies.sh
    scrapy crawl detikcom # untuk jalanin rojak-pantau-detik

## Cara penambahan media baru

Untuk penambahan media baru tinggal copy file `rojak_pantau/spider/detikcom.py`
lalu mengubah nama file dan class sesuai nama media.

Lalu tinggal memodifikasi `name`, `start_urls`, method `parse` dan
method `parse_news`

## Catatan untuk untuk membuat spider baru

* `raw_content` harus berisi raw HTML bukan raw plain text. Karena ini kita
gunakan untuk proses selanjutnya. (Contoh: extract first paragraph)

## Resources

* [Scrapy 1.2 documentation](https://doc.scrapy.org/en/latest/index.html)

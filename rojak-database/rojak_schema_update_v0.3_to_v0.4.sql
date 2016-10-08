-- TODO: solve masalah kalau ada error di tengah2 statement
--       untuk saat ini solusinya buat duplicate versi sebelumnya
--       lalu run against it, sampe bener2 gak ada error
--       NOTE: we can't use MySQL transaction for data definition

-- Ubah nama column `content` di `news` jadi `raw_content`
ALTER TABLE `news`
    CHANGE COLUMN `content` `raw_content`
    text collate utf8_unicode_ci NOT NULL;

-- Tambah column ke `news`
ALTER TABLE `news`
    ADD COLUMN `author_name`
    varchar(255) collate utf8_unicode_ci UNIQUE;
ALTER TABLE `news`
    ADD COLUMN `published_at`
    timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP;


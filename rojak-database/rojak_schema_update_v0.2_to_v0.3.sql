-- TODO: solve masalah kalau ada error di tengah2 statement
--       untuk saat ini solusinya buat duplicate versi sebelumnya
--       lalu run against it, sampe bener2 gak ada error
--       NOTE: we can't use MySQL transaction for data definition

-- Ubah column jadi nullable
ALTER TABLE `media`
    MODIFY COLUMN `logo_url`
    varchar(255) collate utf8_unicode_ci UNIQUE;
ALTER TABLE `media`
    MODIFY COLUMN `fbpage_username`
    varchar(255) collate utf8_unicode_ci UNIQUE;

-- Remove `description` dari `media`
ALTER TABLE `media`
    DROP COLUMN `description`;

-- Tambah column ke `media`
ALTER TABLE `media`
    ADD COLUMN `twitter_username`
    varchar(255) collate utf8_unicode_ci UNIQUE;
ALTER TABLE `media`
    ADD COLUMN `instagram_username`
    varchar(255) collate utf8_unicode_ci UNIQUE;
ALTER TABLE `media`
    ADD COLUMN `last_scraped_at`
    timestamp NOT NULL DEFAULT '1970-01-01 00:00:01';


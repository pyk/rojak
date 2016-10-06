-- TODO: solve masalah kalau ada error di tengah2 statement
--       untuk saat ini solusinya buat duplicate versi sebelumnya
--       lalu run against it, sampe bener2 gak ada error
--       NOTE: we can't use MySQL transaction for data definition

-- Ubah column jadi nullable
ALTER TABLE `candidate`
    MODIFY COLUMN `website_url`
    varchar(255) collate utf8_unicode_ci UNIQUE;
ALTER TABLE `candidate`
    MODIFY COLUMN `photo_url`
    varchar(255) collate utf8_unicode_ci UNIQUE;
ALTER TABLE `candidate`
    MODIFY COLUMN `fbpage_username`
    varchar(255) collate utf8_unicode_ci UNIQUE;

-- Ubah nama column `name` di `candidate` jadi `full_name`
ALTER TABLE `candidate`
    CHANGE COLUMN `name` `full_name`
        varchar(255) collate utf8_unicode_ci NOT NULL UNIQUE;

-- Remove `description` dari `candidate`
ALTER TABLE `candidate`
    DROP COLUMN `description`;

-- Tambah column ke `candidate`
ALTER TABLE `candidate`
    ADD COLUMN `alias_name`
    varchar(255) collate utf8_unicode_ci NOT NULL UNIQUE;
ALTER TABLE `candidate`
    ADD COLUMN `place_of_birth`
    varchar(255) collate utf8_unicode_ci NOT NULL;
ALTER TABLE `candidate`
    ADD COLUMN `date_of_birth`
    date NOT NULL;
ALTER TABLE `candidate`
    ADD COLUMN `religion`
    varchar(255) collate utf8_unicode_ci NOT NULL;
ALTER TABLE `candidate`
    ADD COLUMN `twitter_username`
    varchar(255) collate utf8_unicode_ci UNIQUE;
ALTER TABLE `candidate`
    ADD COLUMN `instagram_username`
    varchar(255) collate utf8_unicode_ci UNIQUE;

-- Ubah column jadi nullable
ALTER TABLE `pair_of_candidates`
    MODIFY COLUMN `website_url`
    varchar(255) collate utf8_unicode_ci UNIQUE;
ALTER TABLE `pair_of_candidates`
    MODIFY COLUMN `logo_url`
    varchar(255) collate utf8_unicode_ci UNIQUE;
ALTER TABLE `pair_of_candidates`
    MODIFY COLUMN `fbpage_username`
    varchar(255) collate utf8_unicode_ci UNIQUE;

-- Tambah column ke `pair_of_candidates`
ALTER TABLE `pair_of_candidates`
    ADD COLUMN `twitter_username`
    varchar(255) collate utf8_unicode_ci UNIQUE;
ALTER TABLE `pair_of_candidates`
    ADD COLUMN `instagram_username`
    varchar(255) collate utf8_unicode_ci UNIQUE;

-- Tambah column is_analyzed ke news
ALTER TABLE `news`
    ADD COLUMN `is_analyzed`
    bool DEFAULT false;


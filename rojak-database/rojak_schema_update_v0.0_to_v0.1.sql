-- TODO: solve masalah kalau ada error di tengah2 statement
--       untuk saat ini solusinya buat duplicate versi sebelumnya
--       lalu run against it, sampe bener2 gak ada error
--       NOTE: we can't use MySQL transaction for data definition

-- Ubah nama table 'candidates' ke 'candidate'
RENAME TABLE `candidates` to `candidate`;

-- Ubah nama column `image_url` di `candidate` jadi `photo_url`
ALTER TABLE `candidate`
    CHANGE `image_url` `photo_url`
    varchar(255) collate utf8_unicode_ci NOT NULL UNIQUE;

-- Ubah nama column `facebookpage_url` di `candidate` jadi `fbpage_username`
ALTER TABLE `candidate`
    CHANGE `facebookpage_url` `fbpage_username`
        varchar(255) collate utf8_unicode_ci NOT NULL UNIQUE;

-- Ubah nama column `slogan` jadi `description` dan allow null di `candidate`
ALTER TABLE `candidate`
    CHANGE `slogan` `description`
        text collate utf8_unicode_ci;

-- Hapus column `logo_url` dari table `candidate`
ALTER TABLE `candidate`
    DROP COLUMN `logo_url`;

-- Ubah nama column `facebookpage_url` di `media` jadi `fbpage_username`
ALTER TABLE `media`
    CHANGE `facebookpage_url` `fbpage_username`
        varchar(255) collate utf8_unicode_ci NOT NULL UNIQUE;

-- Ubah nama column `slogan` jadi `description` dan allow null di `media`
ALTER TABLE `media`
    CHANGE `slogan` `description`
        text collate utf8_unicode_ci;

-- Buat table baru pair_of_candidates
CREATE TABLE `pair_of_candidates` (
    `id` int(10) unsigned NOT NULL UNIQUE auto_increment,
    `cagub_id` int(10) unsigned NOT NULL,
    FOREIGN KEY (`cagub_id`) REFERENCES candidate(`id`) ON DELETE CASCADE,
    `cawagub_id` int(10) unsigned NOT NULL,
    FOREIGN KEY (`cawagub_id`) REFERENCES candidate(`id`) ON DELETE CASCADE,
    `name` varchar(255) collate utf8_unicode_ci NOT NULL UNIQUE,
    `website_url` varchar(255) collate utf8_unicode_ci NOT NULL UNIQUE,
    `logo_url` varchar(255) collate utf8_unicode_ci NOT NULL UNIQUE,
    `fbpage_username` varchar(255) collate utf8_unicode_ci NOT NULL UNIQUE,
    `slogan` varchar(255) collate utf8_unicode_ci,
    `description` text collate utf8_unicode_ci,
    `inserted_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- Tambah foreign key `candidate_id` di table `sentiment`
ALTER TABLE `sentiment`
    ADD `candidate_id` int(10) unsigned NOT NULL DEFAULT 0;
ALTER TABLE `sentiment`
    ADD CONSTRAINT fk_candidate_id FOREIGN KEY (`candidate_id`)
    REFERENCES candidate(`id`)
    ON DELETE CASCADE;

-- Tambah column `score` di table `news_sentiment`
ALTER TABLE `news_sentiment`
    ADD `score` double NOT NULL;

-- Tambah table `mention`
CREATE TABLE `mention` (
    `id` int(10) unsigned NOT NULL UNIQUE auto_increment,
    `news_id` int(10) unsigned NOT NULL,
    FOREIGN KEY (`news_id`) REFERENCES news(`id`) ON DELETE CASCADE,
    `candidate_id` int(10) unsigned NOT NULL,
    FOREIGN KEY (`candidate_id`) REFERENCES candidate(`id`) ON DELETE CASCADE,
    `inserted_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    UNIQUE (`news_id`, `candidate_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;


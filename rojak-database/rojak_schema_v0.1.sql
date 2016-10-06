-- Catatan:
-- max int(10) = 4294967295

-- Menyimpan profile per-orangan dari candidate cagub/cawagub
DROP TABLE IF EXISTS `candidate`;
CREATE TABLE `candidate` (
    `id` int(10) unsigned NOT NULL UNIQUE auto_increment,
    `name` varchar(255) collate utf8_unicode_ci NOT NULL UNIQUE,
    `website_url` varchar(255) collate utf8_unicode_ci NOT NULL UNIQUE,
    `photo_url` varchar(255) collate utf8_unicode_ci NOT NULL UNIQUE,
    `fbpage_username` varchar(255) collate utf8_unicode_ci NOT NULL UNIQUE,
    `description` text collate utf8_unicode_ci,
    `inserted_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- Menyimpan informasi pasangan cagub-cawagub
DROP TABLE IF EXISTS `pair_of_candidates`;
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

-- Menyimpan informasi tentang media
DROP TABLE IF EXISTS `media`;
CREATE TABLE `media` (
    `id` int(10) unsigned NOT NULL UNIQUE auto_increment,
    `name` varchar(255) collate utf8_unicode_ci NOT NULL UNIQUE,
    `website_url` varchar(255) collate utf8_unicode_ci NOT NULL UNIQUE,
    `logo_url` varchar(255) collate utf8_unicode_ci NOT NULL UNIQUE,
    `fbpage_username` varchar(255) collate utf8_unicode_ci NOT NULL UNIQUE,
    `description` varchar(255) collate utf8_unicode_ci,
    `inserted_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- Menyimpan jenis-jenis sentiment
DROP TABLE IF EXISTS `sentiment`;
CREATE TABLE `sentiment` (
    `id` int(10) unsigned NOT NULL UNIQUE auto_increment,
    `candidate_id` int(10) unsigned NOT NULL,
    FOREIGN KEY (`candidate_id`) REFERENCES candidate(`id`) ON DELETE CASCADE,
    `name` varchar(255) collate utf8_unicode_ci NOT NULL UNIQUE,
    `inserted_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- Untuk menyimpan berita yang di terbitkan oleh media
DROP TABLE IF EXISTS `news`;
CREATE TABLE `news` (
    `id` int(10) unsigned NOT NULL UNIQUE auto_increment,
    `media_id` int(10) unsigned NOT NULL,
    FOREIGN KEY (`media_id`) REFERENCES media(`id`) ON DELETE CASCADE,
    `title` varchar(255) collate utf8_unicode_ci NOT NULL UNIQUE,
    `content` text collate utf8_unicode_ci NOT NULL,
    `url` varchar(255) collate utf8_unicode_ci NOT NULL UNIQUE,
    `inserted_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- Untuk menyimpan sentiment suatu berita
DROP TABLE IF EXISTS `news_sentiment`;
CREATE TABLE `news_sentiment` (
    `id` int(10) unsigned NOT NULL UNIQUE auto_increment,
    `news_id` int(10) unsigned NOT NULL,
    FOREIGN KEY (`news_id`) REFERENCES news(`id`) ON DELETE CASCADE,
    `sentiment_id` int(10) unsigned NOT NULL,
    FOREIGN KEY (`sentiment_id`) REFERENCES sentiment(`id`) ON DELETE CASCADE,
    `score` double NOT NULL,
    `inserted_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    UNIQUE (`news_id`, `sentiment_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- Untuk menyimpan data berita mention candidate siapa aja
DROP TABLE IF EXISTS `mention`;
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


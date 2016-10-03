-- Catatan:
-- max int(10) = 4294967295

DROP TABLE IF EXISTS `candidates`;
CREATE TABLE `candidates` (
    `id` int(10) unsigned NOT NULL UNIQUE auto_increment,
    `name` varchar(255) collate utf8_unicode_ci NOT NULL UNIQUE,
    `website_url` varchar(255) collate utf8_unicode_ci NOT NULL UNIQUE,
    `image_url` varchar(255) collate utf8_unicode_ci NOT NULL UNIQUE,
    `logo_url` varchar(255) collate utf8_unicode_ci NOT NULL UNIQUE,
    `facebookpage_url` varchar(255) collate utf8_unicode_ci NOT NULL UNIQUE,
    `slogan` varchar(255) collate utf8_unicode_ci NOT NULL,
    `inserted_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

DROP TABLE IF EXISTS `media`;
CREATE TABLE `media` (
    `id` int(10) unsigned NOT NULL UNIQUE auto_increment,
    `name` varchar(255) collate utf8_unicode_ci NOT NULL UNIQUE,
    `website_url` varchar(255) collate utf8_unicode_ci NOT NULL UNIQUE,
    `logo_url` varchar(255) collate utf8_unicode_ci NOT NULL UNIQUE,
    `facebookpage_url` varchar(255) collate utf8_unicode_ci NOT NULL UNIQUE,
    `slogan` varchar(255) collate utf8_unicode_ci NOT NULL,
    `inserted_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

DROP TABLE IF EXISTS `sentiment`;
CREATE TABLE `sentiment` (
    `id` int(10) unsigned NOT NULL UNIQUE auto_increment,
    `name` varchar(255) collate utf8_unicode_ci NOT NULL UNIQUE,
    `inserted_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

DROP TABLE IF EXISTS `news`;
CREATE TABLE `news` (
    `id` int(10) unsigned NOT NULL UNIQUE auto_increment,
    `media_id` int(10) unsigned NOT NULL,
    `title` varchar(255) collate utf8_unicode_ci NOT NULL UNIQUE,
    `content` text collate utf8_unicode_ci NOT NULL,
    `url` varchar(255) collate utf8_unicode_ci NOT NULL UNIQUE,
    FOREIGN KEY (`media_id`) REFERENCES media(`id`) ON DELETE CASCADE,
    `inserted_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

DROP TABLE IF EXISTS `news_sentiment`;
CREATE TABLE `news_sentiment` (
    `id` int(10) unsigned NOT NULL UNIQUE auto_increment,
    `news_id` int(10) unsigned NOT NULL,
    `sentiment_id` int(10) unsigned NOT NULL,
    FOREIGN KEY (`news_id`) REFERENCES news(`id`) ON DELETE CASCADE,
    FOREIGN KEY (`sentiment_id`) REFERENCES sentiment(`id`) ON DELETE CASCADE,
    `inserted_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    UNIQUE (`news_id`, `sentiment_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

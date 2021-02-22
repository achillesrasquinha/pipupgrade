PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS `tabPackage` (
    -- `id`                INTEGER     PRIMARY KEY AUTOINCREMENT,
    `name`              TEXT        NOT NULL    UNIQUE,
    `latest_version`    TEXT,
    `home_page`         TEXT,
    `releases`          TEXT,
    `_created_at`       TEXT,
    `_updated_at`       TEXT
);

CREATE TABLE IF NOT EXISTS `tabSettings` (
    `version`           TEXT        NOT NULL
);

CREATE TABLE IF NOT EXISTS `tabProxies` (
    `host`                  TEXT        NOT NULL,
    `port`                  INTEGER     NOT NULL,
    `secure`                INTEGER     NOT NULL,
    `anonymity`             TEXT,
    `country_code`          TEXT        NOT NULL,
    `available`             INTEGER     NOT NULL,
    `error_rate`            REAL        NOT NULL,
    `average_response_time` REAL        NOT NULL,
    UNIQUE(`host`, `port`, `secure`, `anonymity`, `country_code`, `available`, `error_rate`,
        `average_response_time`)
);

CREATE TABLE IF NOT EXISTS `tabPackageDependency` (
    `name`          TEXT         NOT NULL,
    `version`       TEXT         NOT NULL,
    `requires`      TEXT
);
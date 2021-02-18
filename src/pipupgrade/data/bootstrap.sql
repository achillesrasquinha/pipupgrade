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

CREATE TABLE IF NOT EXISTS `tabPackageDependency` (
    -- `id`                INTEGER     PRIMARY KEY AUTOINCREMENT,
    `package_id`        INTEGER     NOT NULL,
    `version`           TEXT        NOT NULL,
    FOREIGN KEY(package_id) REFERENCES tabPackage(id)
);

CREATE TABLE IF NOT EXISTS `tabSettings` (
    `version`           TEXT        NOT NULL
);

CREATE TABLE IF NOT EXISTS `tabProxies` (
    `ip`                TEXT        NOT NULL,
    `port`              INTEGER     NOT NULL,
    `country_code`      TEXT        NOT NULL,
    `secure`            INTEGER     NOT NULL,
    `anonymity`         TEXT        NOT NULL,
    `one_way`           INTEGER     NOT NULL,
    `google_passed`     INTEGER     NOT NULL,
    `status`            INTEGER,
    UNIQUE(`ip`, `port`, `country_code`, `secure`, `anonymity`, `one_way`, `google_passed`)
);
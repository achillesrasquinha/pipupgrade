CREATE TABLE IF NOT EXISTS `tabPackage` (
    `name`              TEXT        NOT NULL    UNIQUE,
    `latest_version`    TEXT,
    `home_page`         TEXT,
    `releases`          TEXT,
    `_created_at`       TEXT,
    `_updated_at`       TEXT
);
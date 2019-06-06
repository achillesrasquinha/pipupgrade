CREATE TABLE IF NOT EXISTS `tabPackage` (
    `id`                INTEGER     PRIMARY KEY AUTOINCREMENT,
    `name`              TEXT        NOT NULL,
    `latest_version`    TEXT,
    `home_page`         TEXT,
    `_created_at`       DATETIME,
    `_updated_at`       DATETIME
);
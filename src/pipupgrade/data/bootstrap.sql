CREATE TABLE IF NOT EXISTS `tabPackage` (
    `id`                INTEGER     PRIMARY KEY AUTOINCREMENT,
    `name`              TEXT        NOT NULL    UNIQUE,
    `latest_version`    TEXT,
    `home_page`         TEXT,
    `_created_at`       TIMESTAMP,
    `_updated_at`       TIMESTAMP
);

CREATE TABLE IF NOT EXISTS `tabPackageDependency` (
    `id`                INTEGER     PRIMARY KEY AUTOINCREMENT,
    `package_id`        INTEGER     NOT NULL,
    `version`           TEXT        NOT NULL,
    FOREIGN KEY(package_id) REFERENCES tabPackage(id)
);

CREATE TABLE IF NOT EXISTS `tabSettings` (
    `version`           TEXT        NOT NULL
);
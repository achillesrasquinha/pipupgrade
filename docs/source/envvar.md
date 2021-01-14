### Environment Variables

| Name                                  | Type                                  | Description |
|---------------------------------------|---------------------------------------|-------------|
| `PIPUPGRADE_ACCEPT_ALL_DIALOGS`       | `boolean`                             | Confirm for all dialogs.
| `PIPUPGRADE_DRY_RUN`                  | `boolean`                             | Perform a dry-run, avoid updating packages.
| `PIPUPGRADE_UPDATE_LATEST`            | `boolean`                             | Update all packages to latest.
| `PIPUPGRADE_DISPLAY_FORMAT`           | `string` (table, tree, json, yaml)    | Display packages format.
| `PIPUPGRADE_DISPLAY_ALL_PACKAGES`     | `boolean`                             | List all packages.
| `PIPUPGRADE_UPDATE_PIP`               | `boolean`                             | Update pip. 
| `PIPUPGRADE_INTERACTIVE`              | `boolean`                             | Interactive Mode.
| `PIPUPGRADE_GIT_USERNAME`             | `string`                              | Git Username
| `PIPUPGRADE_GIT_EMAIL`                | `string`                              | Git Email
| `PIPUPGRADE_GITHUB_ACCESS_TOKEN`      | `string`                              | GitHub Access Token
| `PIPUPGRADE_GITHUB_REPONAME`          | `string`                              | Target GitHub Repository Name
| `PIPUPGRADE_GITHUB_USERNAME`          | `string`                              | Target GitHub Username
| `PIPUPGRADE_TARGET_BRANCH`            | `string`                              | Target Branch
| `PIPUPGRADE_JOBS`                     | `integer`                             | Number of Jobs to be used.
| `PIPUPGRADE_USER_ONLY`                | `boolean`                             | Install to the Python user install directory for environment variables and user configuration.
| `PIPUPGRADE_NO_INCLUDED_REQUIREMENTS` | `boolean`                             | Avoid updating included requirements.
| `PIPUPGRADE_NO_CACHE`                 | `boolean`                             | Avoid fetching latest updates from PyPI server.
| `PIPUPGRADE_FORCE`                    | `boolean`                             | Force search for files within a project.
| `PIPUPGRADE_NO_COLOR`                 | `boolean`                             | Avoid colored output.
| `PIPUPGRADE_OUTPUT_FILE`              | `string`                              | Output File.
| `PIPUPGRADE_CONFIG`                   | `string`                              | Path to custom configuration file.
| `PIPUPGRADE_VERBOSE`                  | `boolean`                             | Display Verbose output.
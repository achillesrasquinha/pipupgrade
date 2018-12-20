export NODE_MAJOR_VERSION="10"

apt-get update                                                                                      \
    `# Install Dependencies`                                                                        \
    && apt-get install -y --no-install-recommends                                                   \
        curl                                                                                        \
    && curl -sL https://deb.nodesource.com/setup_10.x | bash -                     \
    && apt-get install -y --no-install-recommends nodejs                                            \
    && npm install -g @semantic-release@15                                                          \
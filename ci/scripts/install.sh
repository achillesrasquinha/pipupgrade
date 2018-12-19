if [[ -z "${NODE_MAJOR_VERSION}" ]]; then
    NODE_MAJOR_VERSION="10"
fi

apt-get update                                                                                      \
    `# Install Dependencies`                                                                        \
    && apt-get install -y --no-install-recommends                                                   \
        curl                                                                                        \
    && curl -sL https://deb.nodesource.com/setup_$NODE_MAJOR_VERSION.x | bash -                     \
    && apt-get install -y --no-install-recommends nodejs                                            \
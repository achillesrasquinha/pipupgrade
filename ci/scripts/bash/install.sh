#!/bin/bash

if [[ $TRAVIS_PYTHON_VERSION == "3.3" ]]; then
    pip install virtualenv==15.1.0
fi

NODE_MAJOR_VERSION=${NODE_MAJOR_VERSION:="10"}
SEMANTIC_RELEASE_MAJOR_VERSION=${SEMANTIC_RELEASE_MAJOR_VERSION:="15"}

apt-get update
apt-get install -y --no-install-recommends curl

curl -sL https://deb.nodesource.com/setup_$NODE_MAJOR_VERSION.x | bash -

apt-get install -y nodejs

npm install -g semantic-release@$SEMANTIC_RELEASE_MAJOR_VERSION \
    @semantic-release/exec \
    @semantic-release/git  
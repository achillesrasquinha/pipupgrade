#!/bin/bash

if [[ $TRAVIS_PYTHON_VERSION == "3.3" ]]; then
    # https://github.com/aws/base64io-python/issues/4#issuecomment-412696588
    pip install virtualenv==15.2.0
    pip install tox==3.1.3
fi

NODE_MAJOR_VERSION=${NODE_MAJOR_VERSION:="10"}
SEMANTIC_RELEASE_MAJOR_VERSION=${SEMANTIC_RELEASE_MAJOR_VERSION:="15"}

apt-get update
apt-get install -y --no-install-recommends curl

curl -sL https://deb.nodesource.com/setup_$NODE_MAJOR_VERSION.x | bash -

apt-get install -y nodejs

npm install -g semantic-release@$SEMANTIC_RELEASE_MAJOR_VERSION
export NODE_MAJOR_VERSION="10"
export SEMANTIC_RELEASE_MAJOR_VERSION="15"

apt-get update
apt-get install -y --no-install-recommends curl

curl -sL https://deb.nodesource.com/setup_$NODE_MAJOR_VERSION.x | bash -

apt-get install -y --no-install-recommends nodejs

npm install -g @semantic-release@$SEMANTIC_RELEASE_MAJOR_VERSION
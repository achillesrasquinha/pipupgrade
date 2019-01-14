if [[ "$TRAVIS_BRANCH" == "master" ]]; then
    npx semantic-release
fi
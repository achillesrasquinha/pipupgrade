if [[ "$TRAVIS_BRANCH" == "master" ]]; then
    echo "$DOCKER_PASSWORD" | docker login --username "$DOCKER_USERNAME" --password-stdin
    docker push "$DOCKER_HUB_USERNAME/$PROJECT"
fi
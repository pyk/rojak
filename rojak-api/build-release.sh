#/usr/bin/env sh

VERSION=$1

if [[ -z $VERSION ]]; then
  echo "Error: Please provide a version number."
  echo "       Make sure it is the same as the one in mix.exs file."
  echo "Usage:"
  echo "    ./build-release.sh [version]"
  echo "Example:"
  echo "    ./build-release.sh 0.2.0"
  exit 1
fi

# Build a release
docker-compose run --rm --no-deps -e MIX_ENV=prod builder mix release --env=prod

# Build the docker container
docker build --build-arg VERSION=$VERSION -t rojak/rojak-api:$VERSION .

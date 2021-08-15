#!/usr/bin/env bash
set -e

# Swith to given paths
if [ -d "${GITHUB_WORKSPACE}" ]; then
  cd ${GITHUB_WORKSPACE}
fi

# Error if no API Token is available
if [[ "${BALENA_API_TOKEN}" == "" ]]; then
  echo "Error: Please set the environment variable BALENA_API_TOKEN with a Balena API token"
  exit 1
fi

# Log in to Balena
balena login --token ${BALENA_API_TOKEN} > /dev/null

# Deploy to Balena Cloud
for line in $(cat $GITHUB_WORKSPACE/.github/workflows/image-builder/apps-$1.txt)
do
  # Run each Balena push command concurrently
  balena push $line &
done

# Wait for all Balena push commands to finish and check exit codes
wait || exit 1

# Pre-load images
for env in $GITHUB_WORKSPACE/.github/workflows/image-builder/env-files/$1/*.env; do

  # Export env variables from file
  export $(grep -v '^#' "$env" | xargs -d '\n')

  imageFile="$GITHUB_WORKSPACE/.github/workflows/image-builder/Learners-Block-$device_name-$RELEASE_VERSION.img"

  # Fetch required image file
  balena os download $type -o $imageFile

  # Preload files into image file
  balena preload $imageFile --fleet $app --commit latest

  # Inject the config file to the image
  balena os configure $imageFile --config-app-update-poll-interval $appUpdatePollInterval --config-network=ethernet --fleet $app

  # Zip the image file ready for adding to release assets
  zip -j $GITHUB_WORKSPACE/Learners-Block-$device_name-$RELEASE_VERSION.zip $imageFile

done

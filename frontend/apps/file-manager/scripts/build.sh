#!/bin/bash

#######################################
# BUILD SCRIPT
# Run this script via "composer build"
# to build the distribution package.
#######################################

# helper functions
indent() { sed 's/^/  /'; }
bold=$(tput bold)
normal=$(tput sgr0)

# test if composer is installed
composer -v > /dev/null 2>&1
COMPOSER_IS_INSTALLED=$?


# Intro
echo ''
echo $'\e[1;44m learnersblock/ifm \e[0m'
echo

# Start
echo -n "${bold}> Starting build process...${normal}" 

sleep 1
echo $' \e[32m✔\e[0m'
echo



# Step 1: Check that composer is installed
echo -n "${bold}> Checking build requirements...${normal}"

if [[ $COMPOSER_IS_INSTALLED -ne 0 ]]; then
  echo
  echo $'\e[41m ERROR \e[0m \e[31mComposer is not installed but required to run the build process.\e[0m' | indent
  exit
fi

echo $' \e[32m✔\e[0m'
echo



# Step 2: Install composer dependencies
echo "${bold}> Installing production dependencies...${normal}"
echo $(composer install --no-dev --no-interaction --no-ansi)
echo



# Step 3: Run the IFM compile script
echo -n "${bold}> Compiling IFM library...${normal}"
echo -n $(rm -rf dist/; php compiler.php --languages=all)

echo $' \e[32m✔\e[0m'
echo



# Step 4: Inject custom extensions
echo -n "${bold}> Compiling IFM extensions...${normal}"
echo -n $(cp -R vendor/. dist/vendor/)
echo -n $(cp -R extensions/. dist/extensions/)

echo $' \e[32m✔\e[0m'
echo



# Step 4: Preparing dist
echo -n "${bold}> Preparing distribution...${normal}"
echo -n $(rm dist/ifm.min.php; rm dist/libifm.php)
echo -n $(mv dist/ifm.php dist/index.php)

echo $' \e[32m✔\e[0m'
echo


# Complete
echo $'\e[42m DONE \e[0m \e[32mBuild complete.\e[0m'
echo ''
exit
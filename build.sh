#!/bin/bash

# This script takes one or two arguments
# $1 'dev' or 'prod'
# $2 'skip' [optional]

# Any subsequent(*) commands which fail will cause the shell script to exit immediately
# http://www.gnu.org/software/bash/manual/bashref.html#The-Set-Builtin
set -e

# JS
# -----------------------------------------------------------------------------
# Write configuration variables into config file.
CHROME_JS_CONFIG='g2e/web/extension/common/js/config-chrome.js'
FIREFOX_JS_CONFIG='g2e/web/extension/common/js/config-firefox.js'

# Create empty files
> $CHROME_JS_CONFIG
> $FIREFOX_JS_CONFIG

printf '%s\n' '// This file is built by deploy.sh in the root directory.' >> $CHROME_JS_CONFIG
printf '%s\n' '// This file is built by deploy.sh in the root directory.' >> $FIREFOX_JS_CONFIG

dbconf="g2e/orm/db.conf"
if [ "$1" = "dev" ]; then
    echo '--------------------- dev ---------------------'
    printf '%s\n' 'var DEBUG = true;' >> $CHROME_JS_CONFIG
    printf '%s\n' 'var SERVER = "http://localhost:8083/g2e/";' >> $CHROME_JS_CONFIG
    printf '%s\n' 'var DEBUG = true;' >> $FIREFOX_JS_CONFIG
    printf '%s\n' 'var SERVER = "http://localhost:8083/g2e/";' >> $FIREFOX_JS_CONFIG
    extId="khihlgenlacbajndipgglejkmomonocn";

    credentials=$(head -n 1 db-dev.conf)
    echo $credentials > $dbconf
else
    echo '--------------------- prod ---------------------'
    printf '%s\n' 'var DEBUG = false;' >> $CHROME_JS_CONFIG
    printf '%s\n' 'var SERVER = "http://amp.pharm.mssm.edu/g2e/";' >> $CHROME_JS_CONFIG
    printf '%s\n' 'var DEBUG = false;' >> $FIREFOX_JS_CONFIG
    printf '%s\n' 'var SERVER = "http://amp.pharm.mssm.edu/g2e/";' >> $FIREFOX_JS_CONFIG
    extId="pcbdeobileclecleblcnadplfcicfjlp";

    credentials=$(head -n 1 db-prod.conf)
    echo $credentials > $dbconf
fi

printf 'var IMAGE_PATH = "chrome-extension://'$extId'/logo-50x50.png";' >> $CHROME_JS_CONFIG
# In a Firefox plugin, self refers to JS object in the bootstrapping file.
# http://stackoverflow.com/a/16848890/1830334
printf 'var IMAGE_PATH = self.options.logoUrl;' >> $FIREFOX_JS_CONFIG

# Then build with grunt
# -----------------------------------------------------------------------------
printf '%s\n' 'Building front-end'
grunt --gruntfile=scripts/gruntfile.js build > /dev/null

# Run unit tests
# -----------------------------------------------------------------------------
if [ "$2" = "skip" ]; then
    printf '%s\n' 'Skipping Python unit tests'
else
    printf '%s\n' 'Running Python unit tests'
    nosetests --exe --nocapture
fi

# Run Docker
# -----------------------------------------------------------------------------
boot2docker init
boot2docker up
boot2docker shellinit

PRIVATE_DOCKER_REPO_IP='146.203.54.165:5000'
echo {$PRIVATE_DOCKER_REPO_IP}
docker build -t $PRIVATE_DOCKER_REPO_IP/g2e:latest .
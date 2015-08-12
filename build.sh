#!/bin/bash

# This script takes one or two arguments
# $1 'dev' or 'prod'
# $2 'skip' [optional]
# $3 'push' [optional - use 'test' as the second argument to not skip tests']

# Any subsequent(*) commands which fail will cause the shell script to exit immediately
# http://www.gnu.org/software/bash/manual/bashref.html#The-Set-Builtin
set -e

# JS
# -----------------------------------------------------------------------------
# Write configuration variables into config file.
CHROME_JS_CONFIG='g2e/extension/common/js/config-chrome.js'
FIREFOX_JS_CONFIG='g2e/extension/common/js/config-firefox.js'

# Create empty files
> $CHROME_JS_CONFIG
> $FIREFOX_JS_CONFIG

printf '%s\n' '// This file is built by deploy.sh in the root directory.' >> $CHROME_JS_CONFIG
printf '%s\n' '// This file is built by deploy.sh in the root directory.' >> $FIREFOX_JS_CONFIG

if [[ $1 = 'dev' ]]; then
    echo '--------------------- dev ---------------------'
    printf '%s\n' 'var DEBUG = true;' >> $CHROME_JS_CONFIG
    printf '%s\n' 'var SERVER = "http://localhost:8083/g2e/";' >> $CHROME_JS_CONFIG
    printf '%s\n' 'var DEBUG = true;' >> $FIREFOX_JS_CONFIG
    printf '%s\n' 'var SERVER = "http://localhost:8083/g2e/";' >> $FIREFOX_JS_CONFIG
    extId="omkofmggjapmpfpijnnnnpclfejpfpmd";
else
    echo '--------------------- prod ---------------------'
    printf '%s\n' 'var DEBUG = false;' >> $CHROME_JS_CONFIG
    printf '%s\n' 'var SERVER = "http://amp.pharm.mssm.edu/g2e/";' >> $CHROME_JS_CONFIG
    printf '%s\n' 'var DEBUG = false;' >> $FIREFOX_JS_CONFIG
    printf '%s\n' 'var SERVER = "http://amp.pharm.mssm.edu/g2e/";' >> $FIREFOX_JS_CONFIG
    extId="pcbdeobileclecleblcnadplfcicfjlp";
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
if [[ $2 = 'skip' ]]; then
    printf '%s\n' 'Skipping Python unit tests'
else
    printf '%s\n' 'Running Python unit tests'
    nosetests --exe
fi

# Configure DB. Do this *after* running the unit tests, so tests don't get
# logged in production.
# -----------------------------------------------------------------------------
printf '%s\n' 'Configuring the database.'
dbconf='g2e/db.conf'
if [[ $1 = 'dev' ]]; then
    credentials=$(head -n 1 g2e/db-dev.conf)
    echo $credentials > $dbconf
else
    credentials=$(head -n 1 g2e/db-prod.conf)
    echo $credentials > $dbconf
fi

# Run Docker
# -----------------------------------------------------------------------------
DOCKER_IMAGE='maayanlab/g2e:latest'
if [[ $1 = 'prod' ]]; then
    boot2docker init
    boot2docker up
    boot2docker shellinit
    docker build -t $DOCKER_IMAGE .
fi

# Critical step! We need to reset the DB credentials so we can keep developing locally.
reset=$(head -n 1 g2e/db-dev.conf)
printf 'reseting credentials to:\n%s\n' $reset
echo $reset > $dbconf

# Push to private docker repo if asked
# -----------------------------------------------------------------------------
if [[ $3 = 'push' ]]; then
    # We use an insecure, private registry. If this script errors, run the
    # following command to tell Docker to go ahead anyway.
    #
    # boot2docker ssh "echo $'EXTRA_ARGS=\"--insecure-registry 146.203.54.165:5000\"' | sudo tee -a /var/lib/boot2docker/profile && sudo /etc/init.d/docker restart"
    printf '%s\n' 'Pushing to private Docker repo'
    docker push $DOCKER_IMAGE
else
    printf '%s\n' 'Not pushing to private Docker repo'
fi
#!/bin/bash

# ARGUMENTS:
# $1 dev | prod [required - configure for development or production]
# $2 skip       [optional - skip unit tests]
# $3 build      [optional - use any other string to skip]
# $4 push       [optional - use any other string to skip]

# Any subsequent(*) commands which fail will cause the shell script to exit
# immediately:
# http://www.gnu.org/software/bash/manual/bashref.html#The-Set-Builtin
set -e

# Setup virtual environment
# =============================================================================
if hash deactivate 2 > /dev/null; then
    deactivate
    source venv/bin/activate
else
    source venv/bin/activate
fi

# Run unit tests
# =============================================================================
if [[ $2 = 'skip' ]]; then
    printf '%s\n' 'Skipping Python unit tests'
else
    printf '%s\n' 'Running Python unit tests'
    bash test.sh
fi

# Create front end (if tests pass)
# =============================================================================

# Configure JS
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

# Build with grunt
# -----------------------------------------------------------------------------
printf '%s\n' 'Building front-end'
grunt --gruntfile=scripts/gruntfile.js build > /dev/null

# Run Docker
# =============================================================================
# Even if Docker fails at this point, we want the script to finish. Otherwise,
# we may have a dev.conf file pointing to the production DB.
set +e

# Configure DB. Do this *after* running the unit tests, so tests don't get
# logged in production.
printf '%s\n' 'Configuring the database.'
dbconf='g2e/app.conf'
if [[ $1 = 'dev' ]]; then
    credentials=$(head -n 1 g2e/dev.conf)
    debug=$(tail -n +2 g2e/dev.conf)
    printf '%s\n%s' $credentials $debug > $dbconf
else
    credentials=$(head -n 1 g2e/prod.conf)
    debug=$(tail -n +2 g2e/prod.conf)
    printf '%s\n%s' $credentials $debug > $dbconf
fi

docker-machine start default
eval "$(docker-machine env default)"
DOCKER_IMAGE='maayanlab/g2e:latest'
if [[ $3 = 'build' ]]; then
    docker build --no-cache -t $DOCKER_IMAGE .
fi

# Critical step! We need to reset the DB credentials so we can keep developing
# locally.
reset_credentials=$(head -n 1 g2e/dev.conf)
reset_debug=$(tail -n +2 g2e/dev.conf)
printf 'Reseting credentials\n'
printf '%s\n%s' $reset_credentials $reset_debug > $dbconf

# Push to private docker repo if asked
# =============================================================================
if [[ $4 = 'push' ]]; then
    printf '%s\n' 'Pushing to Docker repo'
    docker push $DOCKER_IMAGE
else
    printf '%s\n' 'Not pushing to Docker repo'
fi
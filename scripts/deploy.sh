#!/bin/bash

# This script takes one argument, which should be 'dev' or 'prod'.

# JS
# -----------------------------------------------------------------------------
# Write configuration variables into config file.
JS_CONFIG='g2e/web/extension/js/config.js'
# Empty file

> $JS_CONFIG

if [ "$1" = "dev" ]; then
    echo '--------------------- dev ---------------------'
    printf '%s\n' '// This file is built by deploy.sh in the root directory.' >> $JS_CONFIG
    printf '%s\n' 'var EXTENSION_ID = "ggnfmgkbdnedgillmfoakkajnpeakbel";' >> $JS_CONFIG
    printf '%s\n' 'var DEBUG = true;' >> $JS_CONFIG
    printf '%s'   'var SERVER = "http://localhost:8083/g2e/";' >> $JS_CONFIG
else
    echo '--------------------- prod ---------------------'
    printf '%s\n' '// This file is built by deploy.sh in the root directory.' >> $JS_CONFIG
    printf '%s\n' 'var EXTENSION_ID = "pcbdeobileclecleblcnadplfcicfjlp";' >> $JS_CONFIG
    printf '%s\n' 'var DEBUG = false;' >> $JS_CONFIG
    printf '%s'   'var SERVER = "http://amp.pharm.mssm.edu/g2e/";' >> $JS_CONFIG
fi

# Then build with grunt
# -----------------------------------------------------------------------------
printf '%s\n' 'Building JavaScript'
grunt --gruntfile=scripts/gruntfile.js build > /dev/null

# Run unit tests
# -----------------------------------------------------------------------------
printf '%s\n' 'Running Python unit tests'
#nosetests g2e/ --quiet > /dev/null

# All files should be in extension/ now.
# -----------------------------------------------------------------------------
printf '%s\n' 'Zipping extension'
#zip -r extension.zip extension/ > /dev/null

# Done!
# -----------------------------------------------------------------------------
printf '%s\n' 'Done!'

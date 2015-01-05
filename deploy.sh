#!/bin/bash

# This script takes one argument, which should be 'dev' or 'prod'.

# CSS
# -----------------------------------------------------------------------------
cp css/main.css extension/main.css
cp css/open-sans.css extension/open-sans.cess

# Images
# -----------------------------------------------------------------------------
cp images/g2e-logo-50x50.png extension/images/g2e-logo-50x50.png
cp images/g2e-logo-128x128.png extension/images/g2e-logo-128x128.png

# JS
# -----------------------------------------------------------------------------
# Write configuration variables into config file.
JS_CONFIG='js/config.js'
# Empty file
> $JS_CONFIG
if [ "$1" = "dev" ]; then
    echo '--------------------- dev ---------------------'
    printf '%s\n' '// This file is built by deploy.sh in the root directory.' >> $JS_CONFIG
    printf '%s\n' 'var EXTENSION_ID = "jmocdkgcpalhikedehcdnofimpgkljcj";' >> $JS_CONFIG
    printf '%s\n' 'var DEBUG = true;' >> $JS_CONFIG
    printf '%s'   'var SERVER = "http://localhost:8083/";' >> $JS_CONFIG
else
    echo '--------------------- prod ---------------------'
    printf '%s\n' '// This file is built by deploy.sh in the root directory.' >> $JS_CONFIG
    printf '%s\n' 'var EXTENSION_ID = "pcbdeobileclecleblcnadplfcicfjlp";' >> $JS_CONFIG
    printf '%s\n' 'var DEBUG = false;' >> $JS_CONFIG
    printf '%s'   'var SERVER = "http://amp.pharm.mssm.edu/";' >> $JS_CONFIG
fi

# Then build with grunt
# -----------------------------------------------------------------------------
grunt --gruntfile js/grunt/gruntfile.js build

# All files should be in extension/ now.
# -----------------------------------------------------------------------------
zip -r extension.zip extension/

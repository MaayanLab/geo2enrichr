#!/usr/bin/env python

"""Build script for GEO2Enrichr. Manages unit tests, building the Chrome
extension, building the Docker container, and pushing the container.
"""

import argparse
from ConfigParser import ConfigParser
import json
import subprocess
import sys

import requests


# Setup default arguments
# ============================================================================
ap = argparse.ArgumentParser()
ap.add_argument('--dev',
                help='deploy debug or production version',
                action='store_false')
ap.add_argument('--skiptests',
                help='skip unit tests',
                action='store_true')
ap.add_argument('--build',
                help='build Docker container',
                action='store_true')
ap.add_argument('--image',
                help='Docker image',
                default='maayanlab/g2e:latest')
ap.add_argument('--deploy',
                help='push Docker container',
                action='store_true')
opts = ap.parse_args()
print(opts)


# Setup virtual environment
# ============================================================================


# Run unit tests
# ============================================================================
if opts.skiptests:
    print('Skipping Python unit tests')
else:
    print('Running Python unit tests')
    return_code = subprocess.call('source venv/bin/activate && bash test.sh',
                                  shell=True)
    if return_code != 0:
        raise Exception('Unit tests failed')


# Create front end (if tests pass)
# ============================================================================

# Configure JS
# ----------------------------------------------------------------------------

# Write configuration variables into config file.
CHROME_JS_CONFIG = 'g2e/extension/common/js/config-chrome.js'

with open(CHROME_JS_CONFIG, 'w+') as f:
    f.write('// This file is built by deploy.sh in the root directory.\n')
    if opts.dev:
        mode = 'dev'
        debug = 'true'
        server = 'http://localhost:8083/g2e/'
        id_ = 'omkofmggjapmpfpijnnnnpclfejpfpmd'
    else:
        mode = 'prod'
        debug = 'false'
        server = 'http://amp.pharm.mssm.edu/g2e/'
        id_ = 'pcbdeobileclecleblcnadplfcicfjlp'

    print('--------------------- %s ---------------------' % mode)
    f.write('var DEBUG = %s;\n' % debug)
    f.write('var SERVER = "%s";\n' % server)
    f.write('var IMAGE_PATH = "chrome-extension://%s/logo-50x50.png";\n' %
            id_)

# Build with grunt
# ----------------------------------------------------------------------------
print('Building front-end')
return_code = subprocess.call('grunt --gruntfile=scripts/gruntfile.js build > '
                              '/dev/null', shell=True)
if return_code != 0:
    raise Exception('Grunt build failed')

# Manage Docker
# ============================================================================

# Configure DB. Do this *after* running the unit tests, so tests don't get
# logged in production.
print('Creating config.ini file.\n')

config_in = ConfigParser()

config_out = ConfigParser()
config_out.add_section('mode')
config_out.add_section('db')
config_out.add_section('cookies')

# Configuration, primarily database connection string.
# ----------------------------------------------------------------------------
if opts.dev:
    config_in.read('g2e/dev.ini')
    config_out.set('mode', 'debug', True)
else:
    config_in.read('g2e/prod.ini')
    config_out.set('mode', 'debug', False)

config_out.set('db', 'uri', config_in.get('db', 'uri'))
config_out.set('cookies', 'secret_key',
               config_in.get('cookies', 'secret_key'))

with open('g2e/config.ini', 'wb') as configfile:
    config_out.write(configfile)

subprocess.call('docker-machine start default', shell=True)
subprocess.call('eval "$(docker-machine env default)"', shell=True)

if opts.build:
    subprocess.call('docker build -t %s .' % opts.image, shell=True)

# Reset DB credentials so we can keep developing locally.
# ----------------------------------------------------------------------------
config_in = ConfigParser()
config_in.read('g2e/dev.ini')

config_out = ConfigParser()
config_out.add_section('mode')
config_out.add_section('db')
config_out.add_section('cookies')
config_out.set('db', 'uri', config_in.get('db', 'uri'))
config_out.set('mode', 'debug', True)
config_out.set('cookies', 'secret_key',
               config_in.get('cookies', 'secret_key'))

with open('g2e/config.ini', 'wb') as configfile:
    config_out.write(configfile)


# Deploy if configured.
# =============================================================================
if not opts.deploy:
    print('Not deploying')
    sys.exit(0)

# Push to Docker repo.
# ----------------------------------------------------------------------------
print('Pushing to Docker repo')
subprocess.call('docker push $DOCKER_IMAGE', shell=True)

# PUT request to update Marathon.
# ----------------------------------------------------------------------------
payload = {
    'instances': 1,
    'cpus': 1,
    'mem': 2048,
    'constraints': [
        ['hostname', 'CLUSTER', 'charlotte.1425mad.mssm.edu']
    ],
    'container': {
        'type': 'DOCKER',
        'docker': {
            'image': opts.image,
            'forcePullImage': True,
            'network': 'BRIDGE',
            'portMappings': [
                {
                    'containerPort': 80,
                    'hostPort': 0,
                    'protocol': 'tcp'
                }
            ]
        },
        'volumes': [
            {
                'containerPath': '/g2e/g2e/static/genelist',
                'hostPath': '/data/g2e/static/genelist',
                'mode': 'RW'
            },
            {
                'containerPath': '/g2e/g2e/static/softfile',
                'hostPath': '/data/g2e/static/softfile',
                'mode': 'RW'
            }
        ]
    },
    'labels': {
        'public': 'true'
    }
}

resp = requests.put('maayanlab:systemsbiology@elizabeth:8080/v2/apps/g2e',
                    json.dumps(payload))
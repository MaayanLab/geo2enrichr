#!/bin/sh

DIR="$(dirname $0)"
EXT_DIR="${DIR}/../../g2e/extension/firefox/"
BUILD="../firefox.xpi"

cd ${EXT_DIR} && zip -r -FS ${BUILD} *

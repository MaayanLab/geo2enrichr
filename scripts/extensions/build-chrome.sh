#!/bin/sh

DIR="$(dirname $0)"
EXT_DIR="${DIR}/../../g2e/extension/chrome/"
BUILD="../chrome.zip"

cd ${EXT_DIR} && zip -r -FS ${BUILD} *

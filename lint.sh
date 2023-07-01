#!/bin/sh

# Meant to be run from within docker container.
# Fix style errors in place.

set -e 
set -o pipefail

REPO_DIR=$(dirname -- "$0")

black \
    $REPO_DIR/trudge \
    --line-length 100 \
    -t py39

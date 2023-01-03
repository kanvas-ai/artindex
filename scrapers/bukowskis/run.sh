#!/usr/bin/env bash

set -xeuo pipefail

docker build --tag buk .
docker run -it buk

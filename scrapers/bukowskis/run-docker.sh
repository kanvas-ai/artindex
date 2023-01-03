#!/usr/bin/env bash

set -xeuo pipefail

source venv/bin/activate

./01_iterate_archive_pages.py

./02_download_html_of_items.py

./03_convert_to_csv.py

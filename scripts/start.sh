#!/usr/bin/env sh
set -e

bundle check || bundle install
bundle exec jekyll serve --trace --open-url --livereload

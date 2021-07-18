#!/bin/bash

#arg 1 is the folder to be synced to the local and online repo
#arg 2 is the commit message

git_dir="/home/matt/Documents/text-files/git/mattwilsonprojects.github.io"

git_url="https://mattwilson888@github.com/mattwilson888/mattwilsonprojects.github.io"

rsync -a -v $1 "$git_dir"

cd "$git_dir"

git add -v .
git commit -v -m "$2"
echo "just committed"
git push -v "$git_url"

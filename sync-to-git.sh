#!/bin/bash

# Environment Variables
git_dir="/home/matt/Documents/text-files/git/mattwilsonprojects.github.io"
git_url="https://mattwilson888@github.com/mattwilson888/mattwilsonprojects.github.io"
full_dir="$git_dir$git_dir_extension"

# Argument Variables
verbose="false"
git_dir_extension=""
commit_message=""

print_usage() {
    echo "Usage: sync-to-git -e (git-directory-extension (new or existing)) file1 file2...";
    echo "-m [commit message]";
    echo "-t -- Shows local git-repo's tree then exits";
}

while getopts "e:vmt" flag; do
    case "${flag}" in
	e)
	    git_dir_extension="/${OPTARG}"
	    shift 2
	    ;;
	v)
	    verbose="true"
	    shift
	    ;;
	m)
	    commit_message="/${OPTARG}"
	    shift 2
	    ;;
	t)
	    ls -R "$git_dir" | grep ":"
	    exit 1
	    ;;
	*)
	    print_usage
	    exit 1
	    ;;
    esac
done


files=$@

echo "$files"

echo "$full_dir"


if [ ! -d "$full_dir" ]; then
    echo "Creating dir in local git repo.";
    mkdir "$full_dir"
fi

rsync -a -v $@ "$full_dir"

cd "$full_dir"

git add -v .
git commit -v -m "$commit_message"

git push -v "$git_url"

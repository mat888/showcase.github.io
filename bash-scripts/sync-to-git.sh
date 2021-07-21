#!/bin/bash

# Environment Variables
git_dir="/home/matt/Documents/text-files/git/mattwilsonprojects.github.io"
git_url="https://mattwilson888@github.com/mattwilson888/mattwilsonprojects.github.io"

# Argument Variables
verbose="false"
git_dir_extension=""
commit_message=""

print_usage() {
    echo "Usage: sync-to-git -e (git-directory-extension (new or existing)) file1 file2...";
    echo "-m [commit message]";
    echo "-t -- Shows local git-repo's tree then exits";
}

files=()

while [[ $# -gt 0 ]]; do
    case "$1" in
	-e|--extend-dir)
	    git_dir_extension="$2"
	    shift 2
	    ;;
	-m|--message)
	    commit_message="$2"
	    shift 2
	    ;;
	-t|--tree)
	    ls -R "$git_dir" | grep ":"
	    exit 1
	    ;;
	-v|--verbose)
	    verbose="true"
	    ;;
	-*|--*)
	    print_usage
	    exit 3
	    ;;
	*)
	    files+="$1 "
	    shift
	    ;;
    esac
done

full_dir="$git_dir$git_dir_extension"

if [ $verbose=='true' ]; then
    
    echo "files: $files"

    echo "commit: $commit_message"

    echo "full git dir: $full_dir"
fi

if [ ! -d "$full_dir" ]; then
    if [ $verbose=='true' ]; then
	echo "Creating dir in local git repo.";
    fi
    mkdir "$full_dir"
fi

rsync -a -v $files "$full_dir" 

cd "$full_dir"

git add -v .
git commit -v -m "$commit_message"

git push -v "$git_url"

exit 1

: '
while getopts "e:vm:t" flag; do
    case "${flag}" in
	e)
	    echo "args before -e $@"
	    git_dir_extension="${OPTARG}"
	    shift 2
	    echo "args after -e $@"
	    ;;
	v)
	    verbose="true"
	    shift 
	    ;;
	m)
	    echo "args before -m $@"
	    commit_message="${OPTARG}"
	    shift 2
	    echo "args after -m $@"
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
'

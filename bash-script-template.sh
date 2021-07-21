# shebang tells command line what to parse file with.
# bash is usually run without it, but should be included
# to remain compatible with all OS's or configurations

#!/bin/bash


# $ Dollar Sign and function Arguments ~

# the $ character is used for many special meta functions
# but most commonly for getting arguments provided to the script

# $1 lists the first argument, $2, the second and so on...
# these argmuments are typed after the script title seperated by spaces

# $@ provides an array like structure of all arguments
# $# provides the number of arguments
# neither of these include $0, which is the script title itself




# Functions ~

# Functions are used to abstractify operations that will be
# repeated, or to better organize an overall script.

echo_function () {
	echo this prints text to terminal;
}
echo_function

function echo_function {
	echo "so does this";
}
echo_function

# Function arguments are handled just like the script args.
# They are obtained locally with $n, and supplied to the
# function by writing them seperated by spaces after the function call

echo_arg () { echo "The first arg you provided was $1"; }
echo_arg ":)"

# Since $@ creates an array like structure, a colon (:) can be
# used to get just one value by index.

function echo_last_arg () { echo "The last arg provided was ${@:$#}"; }
echo_last_arg 1 "2" 3 "shoe"

# The use of brackets after $ can be confusing. The brackets tell bash
# to treat the expression inside is as one whole operation rather than
# just producing the string of the arguments, the colon, then the length.
# The first value in the brackets is expanded by the outside $, but the
# rest of the inner expressions which require $ in front of them
# must have it placed before them manually, as seen with $#.




# Conditionals ~




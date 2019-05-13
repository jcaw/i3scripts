#!/bin/bash


#+Script to pop up a cheatsheet of the available i3 shortcuts.
#
# Press q to close the cheatsheet.


#+Function to extract the contents of another function, as a string.
#
# Usage: in_func <function_name1> [ ...<function_name2> ... ]
# Output: The text in each <function_name>
in_func()
{
    while [ "$1" ]; do
        type $1 | sed  -n '/^    /{s/^    //p}' | sed '$s/.*/&;/'
        shift
    done
}

#+Function to display an i3 cheat sheet in the current shell.
#
# We include this here so it can be tweaked in a normal format before being sent
# to the bash command.
#
# This command was developed by trial and error and is thus completely
# incomprehensible. I am sorry.
i3cheatsheet()
{
    grep -E "^bindsym" ~/.config/i3/config | awk '{$1=""; print $0}' | sed 's/^ *//g' | grep -vE "^XF86" | tr -s ' ' | awk -F: '{ st = index($0," ");print substr($0,0,st-1) "...." substr($0,st+1)}' | sed "s/\$mod/\⊞/g" | sed "s/\+/ /g" | column -t -s '....' -R 1 -W 2 -T 2 -c 80 | column | pr -2 -w 160 -t | less
}

# HACK: We now extract the actual text of the function, and send *that* to bash.
#
# This is extremely hacky, but it works. Hey, it's a shell script. This is the
# wild west.
COMMAND_FOR_BASH=$(in_func i3cheatsheet)
# We have to start a subshell to be compatible with urxvt
urxvt -T 'i3 Shortcuts' -e sh -c "${COMMAND_FOR_BASH}"

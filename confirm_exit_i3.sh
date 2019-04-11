#!/bin/sh

# Pop up a confirmation prompt to exit i3

# Get choice with best available method, then execute on it.
#
# No should be the default choice.
if command -v "rofi"; then
    CHOICE=`echo -e "No\nYes" | rofi -p "Really exit i3?" -dmenu`
elif command -v "dmenu"; then
    CHOICE=`echo -e "No\nYes" | dmenu -p "Really exit i3?"`
else
    # If no menu program found, default to normal nagbar behaviour and exit.
    # Shouldn't get here since dmenu should exist, but include just in case.
    i3-nagbar -t warning -m 'You pressed the exit shortcut. Do you really want to exit i3? This will end your X session.' -B 'Yes, exit i3' 'i3-msg exit'
    exit 0
fi


if [[ $CHOICE = "Yes" ]]; then
    i3-msg exit
fi

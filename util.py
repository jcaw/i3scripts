# github.com/justbuchanan/i3scripts

import re
import logging
import subprocess as proc
from collections import namedtuple
import subprocess
import json

# A type that represents a parsed workspace "name".
NameParts = namedtuple("NameParts", ["num", "shortname", "icons"])


def focused_workspace(i3):
    return [w for w in i3.get_workspaces() if w.focused][0]


# Takes a workspace 'name' from i3 and splits it into three parts:
# * 'num'
# * 'shortname' - the workspace's name, assumed to have no spaces
# * 'icons' - the string that comes after the
# Any field that's missing will be None in the returned dict
def parse_workspace_name(name):
    m = re.match("(?P<num>\d+):?(?P<shortname>\w+)? ?(?P<icons>.+)?", name).groupdict()
    return NameParts(**m)


# Given a NameParts object, returns the formatted name
# by concatenating them together.
def construct_workspace_name(parts):
    new_name = str(parts.num)
    if parts.shortname or parts.icons:
        new_name += ":"

        if parts.shortname:
            new_name += parts.shortname

        if parts.icons:
            new_name += " " + parts.icons

    return new_name


def active_screens():
    """Get a list of the active screens from i3. (Screens are dicts.)"""
    result = subprocess.run(["i3-msg", "-t", "get_outputs"], capture_output=True)
    screens = json.loads(result.stdout)
    return [s for s in screens if s["active"]]


def primary_screen(active):
    """Get the primary screen (falls back to the first screen)."""
    for screen in active:
        if screen["primary"]:
            return screen
    # If there's no explicit primary screen, just use the first screen.
    return active[0]


def workspace_screen(workspace, screens):
    """Get the screen `workspace` is partially on."""
    for screen in screens:
        screen_ws = screen["current_workspace"]
        if workspace in screen_ws:
            # FIXME: How to handle numbers higher than 9? 10 will match 1, right?
            return screen
    return None


def workspace_to_screen(workspace, screen):
    subprocess.run(
        ["i3-msg", "--", "workspace", "--no-auto-back-and-forth", f"{workspace}"],
        check=True,
        capture_output=True,
    )
    subprocess.run(
        ["i3-msg", f"move workspace to output {screen}"],
        check=True,
        capture_output=True,
    )


def focus_workspace_number(workspace):
    """Focus `workspace` on the current screen."""
    subprocess.run(
        ["i3-msg", "--", "workspace", f"number {workspace}"],
        check=True,
        capture_output=True,
    )


def focus_output(output):
    return subprocess.run(
        ["i3-msg", f"focus output {output}"], check=True, capture_output=True
    )


# Return an array of values for the X property on the given window.
# Requires xorg-xprop to be installed.
def xprop(win_id, property):
    try:
        prop = proc.check_output(
            ["xprop", "-id", str(win_id), property], stderr=proc.DEVNULL
        )
        prop = prop.decode("utf-8")
        return re.findall('"([^"]*)"', prop)
    except proc.CalledProcessError as e:
        logging.warn("Unable to get property for window '%d'" % win_id)
        return None

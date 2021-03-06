#!/usr/bin/python

import sys
from util import (
    active_screens,
    focus_output,
    focus_workspace_number,
    primary_screen,
    workspace_screen,
    workspace_to_screen,
)
import subprocess
from math import floor


def get_next_screen(screen, screens):
    for screen_ in screens:
        if screen_ != screen:
            return screen_
    return None


def _workspace(screen):
    return screen["current_workspace"]


def _name(screen):
    return screen["name"]


if __name__ == "__main__":
    target_ws_partial = sys.argv[1]

    # TODO: Some way of bringing all background workspaces to screen one

    screens = active_screens()

    primary_screen = primary_screen(screens)
    primary_ws = _workspace(primary_screen)
    primary_name = _name(primary_screen)
    target_screen = workspace_screen(target_ws_partial, screens)
    # Full workspace name
    target_ws = target_screen and _workspace(target_screen)
    target_name = target_screen and _name(target_screen)

    if target_ws == primary_ws or target_ws_partial == "auto":
        # Focussing the current workspace should cause the screens to flip.
        next_screen = get_next_screen(primary_screen, screens)
        workspace_to_screen(primary_ws, _name(next_screen))
        workspace_to_screen(_workspace(next_screen), primary_name)
    elif target_screen and primary_screen != target_screen:
        # Target workspace may be on another screen. If so, we swap workspaces
        # with the main screen.
        workspace_to_screen(primary_ws, target_name)
        workspace_to_screen(target_ws, primary_name)
    else:
        workspace_to_screen(target_ws_partial, primary_name, number=True)
    rect = primary_screen["rect"]
    subprocess.run(
        [
            "xdotool",
            "mousemove",
            # Offset to bottom right corner.
            str(rect["x"] + floor(rect["width"] * .92)),
            str(rect["y"] + floor(rect["height"] * .90)),
        ],
        # Don't want to block
        check=False,
    )

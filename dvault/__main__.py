#!/usr/bin/env python3
import argparse
import logging
import os
import sys
import subprocess
import inspect
from shlex import quote
from dvault.common_utils import (format_date, parse_date, add_cmd_line_args, append_cmd_history, list_from_strings)
from dvault.log_msg import (LogMsg)
from dvault import (bots, charts)

def _call(dry_run, cmd):
    logging.info(LogMsg(" ".join([quote(str(x)) for x in cmd])))
    if not dry_run:
        subprocess.call(cmd)

def _check_call(dry_run, cmd):
    logging.info(LogMsg(" ".join([quote(str(x)) for x in cmd])))
    if not dry_run:
        subprocess.check_call(cmd)

def _get_class(
        module_name,
        class_name
        ):
    # look up the class representing this bot by using the reflection
    # ability of python
    objs_module = sys.modules[module_name]
    obj_classes = inspect.getmembers(objs_module, inspect.isclass)
    obj_class = None
    all_names = []
    for obj_class_name, cur_obj_class in obj_classes:
        all_names.append(obj_class_name)
        if obj_class_name == class_name:
            obj_class = cur_obj_class
    if obj_class is None:
        raise Exception(f"Could not find obj: {class_name} in {all_names}")

    return obj_class


def _run(
        obj_class,
        cmd_name,
        run,
        dry_run):

    if cmd_name:
        cmd = getattr(obj_class, cmd_name)

        if run:
            _check_call(dry_run, [str(x) for x in cmd])
        else:
            print(" ".join([quote(str(x)) for x in cmd]))
    else:
        raise Exception(f"No actions to take with {bot_name}")

def _dvault_main(
        bot_name,
        cmd_name,
        chart_name,
        run,
        dry_run,
        **kwargs,
        ):
    logging.debug(LogMsg("dvault main enter"))

    if bot_name:
        bot_class = _get_class( bots.__name__, bot_name)
        _run(bot_class, cmd_name, run, dry_run)
    if chart_name:
        chart_class = _get_class( charts.__name__, chart_name)
        _run(chart_class, cmd_name, run, dry_run)


    logging.debug(LogMsg("dvault main exit"))



def main():
    parser = argparse.ArgumentParser("vault is where you do configuration managment")

    parser.add_argument("--run", action='store_true', help="run a command as a subprocess")

    add_cmd_line_args(
            parser,
            '--log-level',
            '--bot-name',
            '--cmd-name',
            '--chart-name',
            '--dry-run',
            )

    args = parser.parse_args()
    append_cmd_history(sys.argv)
    logging.basicConfig(
            level=getattr(logging, args.log_level.upper(), None),
            format='%(levelname).1s:%(message)s')
    try:
        _dvault_main(**vars(args))
        return 0
    except Exception as ex:
        logging.exception(ex)
        return 1

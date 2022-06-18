#!/usr/bin/env python3
import argparse
import logging
import os
import sys
import subprocess
import inspect
from pprint import pprint
from shlex import quote
from dvault.common_utils import (format_date, parse_date, add_cmd_line_args,
        append_cmd_history, list_from_strings)
from dvault.log_msg import (LogMsg)
# the following must be here for the module lookup by name to work
from dvault import (bots, charts, accounts, strats, utils)

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
    objs_module = sys.modules[f"dvault.{module_name}"]
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
        entry_name,
        run,
        dry_run,
        no_check,
        passed_args
        ):

    if entry_name:
        try:
            cmd = getattr(obj_class, entry_name)
        except AttributeError:
            entries = [ x for x in obj_class.__dict__.keys() if not x.startswith("_") ]
            entries = str(entries).replace("'","")
            raise AttributeError(
                    "Entry: '" + entry_name + "' not found in " + str(entries))

        is_nested_list = isinstance(cmd, list) and len(cmd) > 0 and isinstance(cmd[0], list)

        if not is_nested_list:
            cmd = [cmd]
        else:
            logging.info(LogMsg(
                "Treating as nested command list",
                count=len(cmd)))

        for cur_cmd in cmd:
            if run:
                if no_check:
                    _call(dry_run, [str(x) for x in cur_cmd+passed_args])
                else:
                    _check_call(dry_run, [str(x) for x in cur_cmd+passed_args])
            else:
                print(" ".join([quote(str(x)) for x in cur_cmd+passed_args]))
    else:
        raise Exception(f"No actions to take with {bot_name}")


def _dvault_main(
        module_name,
        class_name,
        entry_name,
        run,
        dry_run,
        no_check,
        passed_args,
        **kwargs,
        ):
    if len(passed_args) and passed_args[0] == "--":
        passed_args = passed_args[1:]
    logging.debug(LogMsg("dvault main enter"))

    # we accept individual strings or quoted strings for these
    # there by definition can not have spaces in them
    module_name = list_from_strings(module_name)
    class_name = list_from_strings(class_name)
    entry_name = list_from_strings(entry_name)

    # user specifies lists of modules, classes, and entry points
    # iterate all that are specified and act upon them.
    for cur_module_name in module_name:
        for cur_class_name in class_name:
            bot_class = _get_class( cur_module_name, cur_class_name)
            for cur_entry_name in entry_name:
                if len(module_name) > 1 or len(class_name) > 1 or len(entry_name) > 1:
                    logging.info(LogMsg(
                        "Running Entry",
                        module_name=cur_module_name,
                        class_name=cur_class_name,
                        entry_name=cur_entry_name))
                _run(bot_class, cur_entry_name, run, dry_run, no_check, passed_args)

    logging.info(LogMsg("dvault exiting"))



def main():
    parser = argparse.ArgumentParser("vault is where you do configuration managment")

    parser.add_argument("--run", action='store_true', help="run a command as a subprocess")
    parser.add_argument("--no-check", action='store_true', help="do not check for non zero exit codes")
    parser.add_argument("--passed-args",nargs="*", default=[], help="extra arguments")

    add_cmd_line_args(
            parser,
            '--log-level',
            '--module-name',
            '--class-name',
            '--entry-name',
            '--dry-run',
            )

    args, passed_args = parser.parse_known_args()
    args.passed_args += passed_args

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

#!/usr/bin/env python3
#
# usage: advent2022 [day] [day...]
#
# Run days; if no day specified, run all days.
#

import os
import io
import pdb
import sys
import weakref
import argparse
import traceback
from importlib import import_module
import pkg_resources

def parse_args(args):
    p = argparse.ArgumentParser(
        description="Run advent 2022 day-specific problems."
    )
    p.add_argument("-P", "--pdb", action="store_true", help="Debug with PDB.")
    p.add_argument("-v", "--verbose", action="store_true", help="More output.")
    i = p.add_argument_group("Input Options")
    m = i.add_mutually_exclusive_group()
    m.add_argument(
        "-I",
        "--stdin",
        action="store_const",
        const="-",
        dest="input",
        help="Read from stdin.",
    )
    m.add_argument("-i", "--input", help="Input file (instead of day/input.txt")
    m.add_argument("-a", "--all", action="store_true", help="Run all days.")
    p.add_argument(
        "days",
        type=int,
        nargs=argparse.REMAINDER,
        help="Day(s) to run.",
    )
    opts = p.parse_args(args)
    # Days to run
    if opts.all and opts.days:
        p.error("cannot give days with --all")
    if opts.days is not None and len(opts.days) > 1 and opts.input:
        p.error("cannot give input with multiple days")
    if opts.all:
        opts.days = range(1, 26)
    # Find input
    if opts.input == "-":
        opts.input = sys.stdin
    elif opts.input is not None:
        opts.input = open(opts.input)
        opts.input = weakref.proxy(opts.input, opts.input.close)
    return opts

def day_modules(days, opts):
    for day in days:
        day_name = f"day{day:02d}"
        try:
            day_module = import_module("." + day_name, "advent2022")
        except (ImportError, ModuleNotFoundError) as e:
            if not all_days:
                print(f"warning: no such day {day}", file=sys.stderr)
        else:
            if hasattr(day_module, "main"):
                input = opts.input
                if input is None:
                    input = io.TextIOWrapper(
                        pkg_resources.resource_stream(day_module.__name__, "input.txt")
                    )
                yield day_module, input

def main(args=sys.argv[1:]):
    opts = parse_args(args)
    modules = day_modules(opts.days or range(1, 26), opts)
    if opts.days is None:
        modules = tuple(modules)[-1]
    for module, input_stream in modules:
        print(module.__name__.split(".")[-1])
        if opts.pdb:
            pdb.runcall(day_module.main, input_stream, opts)
        else:
            module.main(input_stream, opts)

if __name__ == "__main__":
    try:
        main()
    except BrokenPipeError:
        sys.exit(1)
    except OSError:
        raise
    except Exception:
        traceback.print_exc()
        pdb.post_mortem()
        sys.exit(1)

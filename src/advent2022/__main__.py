#!/usr/bin/env python3
#
# usage: advent2022 [day] [day...]
#
# Run days; if no day specified, run all days.
#

import os
import io
import sys
from importlib import import_module
import pkg_resources

def main(*days):
    all_days = len(days) == 0
    days = tuple(int(day) for day in days) if len(days) > 0 else range(1, 25)
    for day in days:
        day_name = f"day{day:02d}"
        try:
            day_module = import_module("." + day_name, "advent2022")
        except (ImportError, ModuleNotFoundError) as e:
            if not all_days:
                print(f"warning: no such day {day}", file=sys.stderr)
        else:
            if hasattr(day_module, "main"):
                print(day_name)
                with io.TextIOWrapper(pkg_resources.resource_stream(
                        day_module.__name__, "input.txt"
                    )) as input_stream:
                    day_module.main(input_stream)

if __name__ == "__main__":
    main(*sys.argv[1:])

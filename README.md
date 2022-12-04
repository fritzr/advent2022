# advent2022

Puzzle solutions for [Advent of Code 2022](https://adventofcode.com/2022) in
Python (for now).

# Sources

Days completed (click links for source code):

* [x] [day 1](src/advent2022/day01/__init__.py)
* [x] [day 2](src/advent2022/day02/__init__.py)
* [x] [day 3](src/advent2022/day03/__init__.py)
* [x] [day 4](src/advent2022/day04/__init__.py)
* [ ] [day 5](src/advent2022/day05/__init__.py)
* [ ] [day 6](src/advent2022/day06/__init__.py)
* [ ] [day 7](src/advent2022/day07/__init__.py)
* [ ] [day 8](src/advent2022/day08/__init__.py)
* [ ] [day 9](src/advent2022/day09/__init__.py)
* [ ] [day 10](src/advent2022/day10/__init__.py)
* [ ] [day 11](src/advent2022/day11/__init__.py)
* [ ] [day 12](src/advent2022/day12/__init__.py)
* [ ] [day 13](src/advent2022/day13/__init__.py)
* [ ] [day 14](src/advent2022/day14/__init__.py)
* [ ] [day 15](src/advent2022/day15/__init__.py)
* [ ] [day 16](src/advent2022/day16/__init__.py)
* [ ] [day 17](src/advent2022/day17/__init__.py)
* [ ] [day 18](src/advent2022/day18/__init__.py)
* [ ] [day 19](src/advent2022/day19/__init__.py)
* [ ] [day 20](src/advent2022/day20/__init__.py)
* [ ] [day 21](src/advent2022/day21/__init__.py)
* [ ] [day 22](src/advent2022/day22/__init__.py)
* [ ] [day 23](src/advent2022/day23/__init__.py)
* [ ] [day 24](src/advent2022/day24/__init__.py)
* [ ] [day 25](src/advent2022/day25/__init__.py)

# Running

The `./run` script wraps the driver for the [advent2022](src/advent2022/__main__.py)
package.  By default, it runs the latest day, but it also accepts a list of days
on the command-line. The default for each day is to read the baked-in input from
my advent2022 account. The driver also accepts an argument to read input from
a different file (which obviously only makes sense when running a single day).

# Usage

```
usage: advent2022 [-h] [-P] [-v] [-t] [-I | -i INPUT | -a] ...

Run advent 2022 day-specific problems.

positional arguments:
  days                  Day(s) to run.

optional arguments:
  -h, --help            show this help message and exit
  -P, --pdb             Debug with PDB.
  -v, --verbose         More output.
  -t, --time            Profile runtime.

Input Options:
  -I, --stdin           Read from stdin.
  -i INPUT, --input INPUT
                        Input file (instead of day/input.txt)
  -a, --all             Run all days.
```

# Dependencies

All scripts use standard library modules and expect Python >= 3.4.

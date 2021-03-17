#!/bin/env python3
""" Module that is used by users to interact with the configuration generation
framework.
Uses the argparse library to help with passing of command line arguments"""

import argparse
import logging
from GalaxyNV import app, term

parser = argparse.ArgumentParser(
    description="Interactive application for creating configuration files for\
         Galaxy"
)

run_group = parser.add_mutually_exclusive_group(required=True)

run_group.add_argument(
    "-t",
    "--terminal",
    help="runs terminal version of config generation",
    action="store_true",
    default=False,
)
run_group.add_argument(
    "-w",
    "--web",
    help="runs web version of config generation",
    action="store_true",
    default=True,
)


parser.add_argument(
    "-v",
    "--verbose",
    help="show verbose output",
    action="store_true",
    default=False,
)
args = parser.parse_args()

if args.verbose:
    logging.basicConfig(level=logging.DEBUG)
if args.terminal:
    term.create()
else:
    app.run()

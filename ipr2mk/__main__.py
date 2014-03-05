#!/usr/bin/env python

import sys
from argparse import ArgumentParser
from ipr2mk import *

parser = ArgumentParser(
    prog="ipr2mk",
    description="Compile an IntelliJ project to a Makefile")

parser.add_argument("-o", "--output", dest="output",
                    default="-")
parser.add_argument("-d", "--outdir", dest="outdir",
                    default="out")
parser.add_argument("project_dir")

args = parser.parse_args()
use_stdout = args.output == "-"

project = parse(args)
output = sys.stdout if use_stdout else open(args.output, "w")
try:
    to_makefile(project, args.outdir, output)
finally:
    if not use_stdout:
        output.close()

import sys
from argparse import ArgumentParser, Action
import ipr2mk
    
parser = ArgumentParser(
    prog="ipr2mk",
    description="Compile an IntelliJ project to a Makefile")
    
parser.add_argument("-o", "--output", dest="output", type=file, 
                    default=sys.stdout)
parser.add_argument("-d", "--outdir", dest="outdir",
                    default="out")
parser.add_argument("project_dir")

args = parser.parse_args()
project = ipr2mk.parse(args)
ipr2mk.to_makefile(project, args.outdir, args.output)

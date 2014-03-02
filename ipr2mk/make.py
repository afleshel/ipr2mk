
import os
from record import Record


class Rule(Record("target", "dependencies")):
    pass

class VarDef(Record("name", "value", "lazy")):
    pass


def to_rules(project, outdir):
    jar_rules = [Rule(target=os.path.join(outdir, m.name + ".jar"),
                      dependencies=[str.join(" ", ("$(shell find \"" + d + "\" -name '*.java')" for d in m.production_source))])
                 for m in project.modules]
    
    return jar_rules


def to_makefile(project, outdir, output):
    for rule in to_rules(project, outdir):
        for dependency in rule.dependencies:
            print rule.target + ": " + dependency


import os
import ipr
from record import Record
from itertools import chain


class Rule(Record("target", "dependencies")):
    pass

class VarDef(Record("name", "value", "lazy")):
    pass


def module_output(module, outdir, ext):
    return os.path.join(outdir, module.name + "." + ext)

def source_dependencies(project, module, outdir):
    return ["$(shell find \"" + d + "\" -name '*.java')" for d in module.production_source]

def jar_dependencies(project, module, outdir):
    for d in module.dependencies_for(ipr.production_compile):
        if d.isa(ipr.LibraryDependency):
            for jar in project.library(d.library).classpath:
                yield jar
        elif d.isa(ipr.ModuleDependency):
            yield module_output(project.module(d.module), outdir, "jar")


def dependencies_of(project, module, outdir):
    return chain(source_dependencies(project, module, outdir),
                 jar_dependencies(project, module, outdir))


def module_rules(project, module, outdir):
    return Rule(target=module_output(module, outdir, "compiled"),
                dependencies=dependencies_of(project, module, outdir))

def to_rules(project, outdir):
    return [module_rules(project, project.module(m), outdir) for m in project.modules]

def write_rules(rules, output):
    for rule in rules:
        for dependency in rule.dependencies:
            output.write(rule.target + ": " + dependency + "\n")

def to_makefile(project, outdir, output):
    write_rules(to_rules(project, outdir), output)

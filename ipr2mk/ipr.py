import re
from record import Record
from lxml import etree
import os
from glob import glob


class Project(Record('name', 'dir', 'libraries', 'modules')):
    def library(self, library_name):
        if library_name in self.libraries:
            return self.libraries[library_name]
        else:
            raise KeyError("no library named " + repr(library_name) + " defined in project " + repr(self.name))

    def module(self, module_name):
        return self.modules[module_name]


class Library(Record('name', 'classpath')):
    pass


class Module(Record('name', 'production_source', 'test_source', 'dependencies')):
    pass


class LibraryDependency(Record('library', 'scope')):
    pass


class ModuleDependency(Record('module', 'scope')):
    pass


class JDKDependency(Record('name')):
    pass


class ModuleLibrary(Record('classpath')):
    pass


SupportedVersion = "4"

_jar_url_pattern = re.compile("^jar://(?P<path>.+)!/")
_file_url_pattern = re.compile("^file://(?P<path>.+)")


def url_to_file(url):
    match = _jar_url_pattern.match(url) or _file_url_pattern.match(url)
    if match is None:
        raise ValueError("cannot parse URL " + url)
    return match.group('path')


def parse_ipr_xml(filename):
    doc = etree.parse(filename)
    version = doc.getroot().get("version")
    if version is None or version == SupportedVersion:
        return doc
    else:
        raise ValueError(filename + " has unsupported version " + version + ", supported: " + SupportedVersion)


def module_name_from_file(module_file):
    return os.path.splitext(os.path.basename(module_file))[0]


def parse_source_dirs(module_dir, module_xml, is_test):
    return [url_to_file(d).replace("$MODULE_DIR$", module_dir)
            for d
            in module_xml.xpath("/module/component/content/sourceFolder[@isTestSource=$flag]/@url",
        flag='true' if is_test else 'false')]

def parse_dependency_scope(e):
    return e.get("scope", "COMPILE")

class Parser:
    def __init__(self, dir):
        self.dir = dir
        self.config_dir = os.path.join(self.dir, ".idea")
        self.jdks = {}
        self.modules = {}
        self.libraries = {}


    def config_file(self, f):
        return os.path.join(self.config_dir, f)

    def parse_order_entry(self, e):
        type = e.get('type')

        if type == "library":
            return LibraryDependency(library=e.get("name").strip(), scope=parse_dependency_scope(e))
        elif type == "jdk":
            #TODO - JDKs are defined in ~/.IdeaIC12/config/options/jdk.table.xml
            return JDKDependency(name=e.get("jdkName"))
        elif type == "inheritedJdk":
            #TODO - resolve this correctly
            return JDKDependency(name="inherited")
        elif type == "module":
            return ModuleDependency(module=e.get("module-name"), scope=parse_dependency_scope(e))
        elif type == "module-library":
            return ModuleLibrary(classpath=[url_to_file(url) for url in e.xpath("library/CLASSES/root/@url")])
        else:
            raise ValueError("unknown " + e.tag + " type " + type)


    def parse_dependencies(self, module_xml):
        return [self.parse_order_entry(e)
                for e in module_xml.xpath("/module/component/orderEntry[@type!='sourceFolder']")]


    def parse_module(self, module_file):
        module_dir = os.path.dirname(module_file)
        module_xml = parse_ipr_xml(module_file)

        if module_xml.getroot().get("type") == "JAVA_MODULE":
            return Module(
                name=module_name_from_file(module_file),
                production_source=parse_source_dirs(module_dir, module_xml, is_test=False),
                test_source=parse_source_dirs(module_dir, module_xml, is_test=True),
                dependencies=self.parse_dependencies(module_xml))
        else:
            return None


    def parse_modules(self, modules_file):
        modules_xml = parse_ipr_xml(modules_file)
        modules = [self.parse_module(m.replace("$PROJECT_DIR$", self.dir.rstrip("/")))
                   for m
                   in modules_xml.xpath("/project/component/modules/module/@filepath")]

        return {m.name:m for m in filter(None, modules)}

    def parse_library(self, f):
        library_xml = parse_ipr_xml(f)
        name = library_xml.xpath("string(/component/library/@name)")
        classpath = [url_to_file(c).replace("$PROJECT_DIR$", self.dir.rstrip("/"))
                     for c in library_xml.xpath("/component/library/CLASSES/root/@url")]

        return Library(name=name, classpath=classpath)

    def parse_libraries(self):
        for f in glob(self.config_file("libraries/*.xml")):
            lib = self.parse_library(f)
            self.libraries[lib.name] = lib

    def parse(self):
        name = open(os.path.join(self.config_dir, ".name")).read().strip()
        self.parse_libraries()
        return Project(
            name=name,
            dir=self.dir,
            libraries=dict(self.libraries),
            modules=self.parse_modules(self.config_file("modules.xml")))

def parse(args):
    return Parser(args.project_dir).parse()

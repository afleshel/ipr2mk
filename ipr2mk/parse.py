
from lxml import etree
import os
from glob import glob
from ipr2mk import ipr

SupportedVersion = "4"

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
    return [d.replace("$MODULE_DIR$", module_dir).replace("file://", "")
            for d 
            in module_xml.xpath("/module/component/content/sourceFolder[@isTestSource=$flag]/@url",
                                flag='true' if is_test else 'false')]

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
            return ipr.LibraryDependency(library=self.libraries[e.get("name")], is_test=e.xpath("@scope='TEST'"))
        elif type == "jdk":
            #TODO - JDKs are defined in ~/.IdeaIC12/config/options/jdk.table.xml
            return ipr.JDKDependency(name=e.get("jdkName"))
        else:
            raise ValueError("unknown " + e.tag + " type " + type)

    
    def parse_order(self, module_xml):
        return [self.parse_order_entry(e) 
                for e 
                in module_xml.xpath("/module/component/orderEntry[@type!='sourceFolder']")]
    
    
    def parse_module(self, module_file):
        module_dir = os.path.dirname(module_file)
        module_xml = parse_ipr_xml(module_file)
        
        return ipr.Module(
            name=module_name_from_file(module_file),
            production_source=parse_source_dirs(module_dir, module_xml, is_test=False),
            test_source=parse_source_dirs(module_dir, module_xml, is_test=True),
            order=self.parse_order(module_xml))
    
    
    def parse_modules(self, modules_file):
        modules_xml = parse_ipr_xml(modules_file)
    
        return [self.parse_module(m.replace("$PROJECT_DIR$", self.dir.rstrip("/")))
                for m 
                in modules_xml.xpath("/project/component/modules/module/@filepath")]
    
    def parse_library(self, f):
        library_xml = parse_ipr_xml(f);
        name = library_xml.xpath("string(/component/library/@name)")
        classpath = [c.replace("jar://$PROJECT_DIR$", self.dir.rstrip("/")).rstrip("!/")
                     for c in library_xml.xpath("/component/library/CLASSES/root/@url")]
        
        return ipr.Library(name=name, classpath=classpath)
    
    def parse_libraries(self):
        self.libraries.update({lib.name: lib for lib in (self.parse_library(f) for f in glob(self.config_file("libraries/*.xml")))})
    
    def parse(self):
        name = open(os.path.join(self.config_dir, ".name")).read()
        self.parse_libraries()
        return ipr.Project(
            name=name,
            dir=self.dir,
            libraries=self.libraries.values(),
            modules=self.parse_modules(self.config_file("modules.xml")))


def parse(args):
    return Parser(args.project_dir).parse()

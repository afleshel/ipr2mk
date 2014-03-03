
from record import Record


class Project(Record('name', 'dir', 'libraries', 'modules')):
    pass

class Library(Record('name', 'classpath')):
    pass

class Module(Record('name', 'production_source', 'test_source', 'order')):
    @property
    def production_libs(self):
        return [l for l in self.libs if not l.is_test]



class LibraryDependency(Record('library', 'scope')):
    pass

class JDKDependency(Record('name')):
    pass

class ModuleDependency(Record('module', 'scope')):
    pass

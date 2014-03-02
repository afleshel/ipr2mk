
from record import Record


class Project(Record('name', 'dir', 'libraries', 'modules')):
    pass

class Library(Record('name', 'classpath')):
    pass

class LibraryDependency(Record('library', 'is_test')):
    pass

class JDKDependency(Record('name')):
    pass

class Module(Record('name', 'production_source', 'test_source', 'order')):
    @property
    def production_libs(self):
        return [l for l in self.libs if not l.is_test]


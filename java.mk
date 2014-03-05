# Make rules for compiling Java

JAR ?= jar
JAVAC ?= javac

java_classpath_of=$(subst $(eval) ,:,$(wildcard $1))

%.jar:
	@mkdir -p $@-content/
	$(JAVAC) $(filter %.java,$^) -cp $(call java_classpath_of,$(filter %.jar,$^)) -d $@-content/
	$(JAR) $(JARFLAGS) -cf $ $@ -C $@-content/ .

# Make rules for compiling Java

JAR ?= jar
JAVAC ?= javac

java_classpath_of=$(subst $(eval) ,:,$(wildcard $1))

%.jar:
	@mkdir -p $(basename $@)/
	$(JAVAC) -cp $(call java_classpath_of,$(filter %.jar,$^)) -d $(basename $@)/ $(filter %.java,$^)
	$(JAR) -cf$(JARFLAGS) $@ -C $(basename $@)/ .

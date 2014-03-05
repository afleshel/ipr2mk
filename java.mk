# Make rules for compiling Java

JAR ?= jar
JAVAC ?= javac

%.jar:
	@mkdir -p $@-content/
	$(JAVAC) $(filter %.java,$^) -cp $(call classpathify,$(filter %.jar,$^)) -d $@-content/
	$(JAR) $(JARFLAGS) -cf $ $@ -C $@-content/ .

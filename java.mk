# Make rules for compiling Java

JAR ?= jar
JAVAC ?= javac

java_classpath_of=$(subst $(eval) ,:,$1)

%.jar:
	@mkdir -p $(basename $@)/
	$(JAVAC) $(JAVACFLAGS) -cp $(call java_classpath_of,$(filter %.jar,$^)) -d $(basename $@)/ $(filter %.java,$^)
	$(JAR) -cf$(JARFLAGS) $@ -C $(basename $@)/ .

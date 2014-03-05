# Make rules for compiling Java

JAR ?= jar
JAVAC ?= javac

java_classpath_of=$(subst $(eval) ,:,$1)

%.jar: %.compiled
	$(JAR) -cf$(JARFLAGS) $@ -C $* .

%.compiled:
	@mkdir -p $*/
	$(JAVAC) $(JAVACFLAGS) -cp $(call java_classpath_of,$(filter %.jar,$^)) -d $*/ $(filter %.java,$^)
	touch $@

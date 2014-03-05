ipr2mk - Translate IntelliJ project files to Makefile rules
===========================================================

What?
-----

A tool that translates IntelliJ project files to Makefile rules.

Why?
----

The most popular Java build tools* don't work well for projects that use multiple languages, such as a combination of Java & cross-compiled C.  There's usually a lot of awkward jumping between Make, for the C parts, and Ant, for the Java parts.  It's a lot of effort to get the dependencies right for a fast, parallelisable build.  It's much easier if everything is written in Make.

Java programmers work in an IDE.  Professional Java programmers work in IntelliJ.  Maintaining multiple build files 
is a waste of time.  So use the IDE configuration as the master copy and generate Make rules from the IDE configuration.

How?
----

Write a makerule in the project makefile to compile the project's IntelliJ project files to a dependency file Make format.

Include the dependency file in the project makefile.

Make will automatically regenerate the dependency file when developers change the project configuration in the IDE.


\* [Gradle](http://gradle.org) is an exception.

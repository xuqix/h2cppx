Parse c++ header file and generate c++ implement code
-----------------------------------------------------
**Purpose:** Provides "header file to cpp file" capabilities to develop plugin for other platform.

**Required:** python 2.x

**Author:** xiaok

**External module required:** yaml

**Third-party:** pyvisitor CppHeaderParser(modification) 

[Github-Link](https://github.com/xuqix/h2cppx.git)

Help Query:
    
    h2cppx -h

example:
--------

    python h2cppx sample/sample.h

Already includes platform support:
----------------------------------
1. vim support: vim-port branch, just use "git checkout vim-port" to get it.


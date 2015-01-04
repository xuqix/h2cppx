h2cppx(vim-port): parse the c++ header file and generate c++ implement code 
============================================================================
**Purpose:** Parse the c++ header file and generate c++ implement code for vim plugin

**Required:** python 2.x

**Author:** xiaok

**External module required:** cheetah yaml(python package)

**Third-party(the plugin already include):** pyvisitor CppHeaderParser(modification) 

[Github-Link](https://github.com/xuqix/h2cppx.git)

Installation
------------
Before start, make sure you have installed the python package "yaml",
Then run below command:

    git clone 'https://github.com/xuqix/h2cppx.git
    cd  h2cppx
    git checkout vim-port

Now just placed the plugin to the directory "~/.vim/plugin/" and you can start use it.

After the installation is complete, 
You can map the key in .vimrc to quickly use the command.

    e.g:
    nmap <F3>  :H2cppx<ESC>
    nmap <F4>  :H2cppxLine<ESC>
    nmap <F3>p :CpH2cppx<ESC>
    nmap <F4>p :CpH2cppxLine<ESC>
    nmap <F5>  :H2cppxAuto<ESC>

PS:
If the plugin can't find the python path in your computer,
you need set "g:python_path" in the .vimrc file like this:

    let g:python_path = '/usr/bin/python'


Example:
-------

    vim test.h
    :H2cppx  
    Now you can find new file "test.cpp" in your directory

    vim test.h
    :H2cppxLine
    Now you can find defined in your file "test.cpp" from current line of cursor 

    vim test.h
    :CpH2cppx  
    Like :H2cppx, but defined in your clipboard, no file writed, just use "p" to get it.

    vim test.h
    :CpH2cppxLine  
    Like :H2cppxLine, but defined in your clipboard, no file is writed.

    vim test.h
    :H2cppxAuto 
    Auto Contrast header and implementation files, find function 
    declarations in the header file and append the newly added to 
    the implementation file, if the file does not exist to achieve 
    a new file is created!


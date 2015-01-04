if(exists('b:h2cppx')) | finish | endif

let b:h2cppx = 1

if(exists('g:h2cppx'))  
    finish 
endif

let g:h2cppx = 1

let s:python_path = g:python_path
if(system(s:python_path . ' -c "import sys; print sys.version_info[0]"') != "2\n")
    echohl WarningMsg | echomsg "load h2cppx faild,python2.x is must need for h2cppx." | echohl None
    finish
endif

let s:installed_directory = expand('<sfile>:p:h')
let s:h2cppx_dir = s:installed_directory . "/h2cppx"
let s:h2cppx_path= s:h2cppx_dir . "/h2cppx.py"

function s:h2cppx(header_file)
    let cpp_file = expand('%:p:r') . "\.cpp"
    echo cpp_file

    let cmd = printf('%s "%s" "%s" -o "%s"', s:python_path, s:h2cppx_path, a:header_file, cpp_file)
    let content = system(cmd)

    if v:shell_error == 0
        echo content
    elseif v:shell_error == 1
        echohl WarningMsg | echo content | echohl None
    elseif v:shell_error == 2
        echo content 
    elseif v:shell_error == 3
        echo content 
    elseif v:shell_error == 4
        let n = inputdialog("(Warning)Cpp file already exisit, force overwrite it?(yes\no): ")
        if n== "yes"
            echo 'sssssss'
        endif
        echo content 
    elseif v:shell_error == 5
        echo content 
    endif
endfunction

command! -buffer -nargs=0 H2cppx call s:h2cppx(expand('%:p'))


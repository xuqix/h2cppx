if(exists('b:h2cppx')) | finish | endif

let b:h2cppx = 1

if(exists('g:h2cppx'))  
    finish 
endif

let g:h2cppx = 1

if(exists('g:python_path'))
    let s:python_path = g:python_path
else
    let s:python_path = 'python'
endif

if(system(s:python_path . ' -c "import sys; print sys.version_info[0]"') != "2\n")
    echohl WarningMsg | echomsg "load h2cppx faild,python2.x is must need for h2cppx." | echohl None
    finish
endif

let s:installed_directory = expand('<sfile>:p:h')
let s:h2cppx_dir = s:installed_directory . "/h2cppx"
let s:h2cppx_path= s:h2cppx_dir . "/h2cppx.py"
let s:config_file= s:installed_directory . "/config"

"full generate cpp file
function s:h2cppx(header_file, isClipboard)
    let cpp_file = expand('%:p:r') . "\.cpp"

    let cmd = printf('%s "%s" -t "%s" "%s" ', s:python_path, s:h2cppx_path, s:config_file, a:header_file)
    if ! (a:isClipboard == 1)
        let cmd = cmd . " -o " . cpp_file
    endif
    let content = system(cmd)

    while 1
        if v:shell_error == 0
            let filename = expand('%:r') . "\.cpp"
            if a:isClipboard == 1
                call setreg('"+', content )
                echo "Define code already copy to your clipboard,use p to paster!"
            else
                echo "Generate file " . filename . " successful!"
            endif
        elseif v:shell_error == 1
            echo content
        elseif v:shell_error == 2
            echo content 
        elseif v:shell_error == 3
            echo content 
        elseif v:shell_error == 4
            let ans = input("file already exisit, force overwrite it?(yes/no): ")
            if toupper(ans) == "YES" || toupper(ans) == "Y"
                let cmd = printf('%s "%s" "%s" -t "%s" -o "%s" -f', s:python_path, s:h2cppx_path, a:header_file, s:config_file, cpp_file)
                let content = system(cmd)
                continue
            endif
        elseif v:shell_error == 5
            echohl WarningMsg | echo "IO error\n" . content | echohl None
        endif
        break
    endwhile
endfunction

function s:h2cppx_line(header_file, line_number, isClipboard)
    let ln = a:line_number
    let cpp_file = expand('%:p:r') . "\.cpp"

    let cmd = printf('%s "%s" "%s" -t "%s" -ln %d -a', s:python_path, s:h2cppx_path, a:header_file, s:config_file, ln)
    if ! (a:isClipboard == 1)
        let cmd = cmd . " -o " . cpp_file
    endif
    let content = system(cmd)

    while 1
        if v:shell_error == 0
            let filename = expand('%:r') . "\.cpp"
            if a:isClipboard == 1
                call setreg('"+', content . "\n")
                echo "Define code already copy to your clipboard,use p to paster!"
            else
                echo "write file " . filename . " successful!"
            endif
        elseif v:shell_error == 1
            echo content
        elseif v:shell_error == 2
            echohl WarningMsg | echo content | echohl None
        elseif v:shell_error == 3
            echohl WarningMsg | echo content | echohl None
        elseif v:shell_error == 4
            "let ans = input("file already exisit, append to file tail?(yes/no): ")
            "if toupper(ans) == "YES" || toupper(ans) == "Y"
            "    let cmd = printf('%s "%s" "%s" -ln %d -a', s:python_path, s:h2cppx_path, a:header_file, ln)
            "    let content = system(cmd)
            "    continue
            "endif
        elseif v:shell_error == 5
            echohl WarningMsg | echo "IO error\n" . content | echohl None
        endif
        break
    endwhile
endfunction

function H2cppxLine(isClipboard)
    call s:h2cppx_line(expand('%:p'), line('.'), a:isClipboard)
endfunction

function H2cppx(isClipboard)
    call s:h2cppx(expand('%:p'), a:isClipboard)
endfunction

"generate cpp define and put in cpp file
command! -buffer -nargs=0 H2cppx call H2cppx(0)
command! -buffer -nargs=0 H2cppxLine call H2cppxLine(0)
"generate cpp define and put in clipboard
command! -buffer -nargs=0 CpH2cppx call H2cppx(1)
command! -buffer -nargs=0 CpH2cppxLine call H2cppxLine(1)


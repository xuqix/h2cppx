#!/usr/bin/env python

import argparse
from Parser import *
from CodeGeneration import *
from StringIO import StringIO

description = \
"""
    Parse C++ header file and generate c++ implement code. 
"""

usage= \
"""
    h2cpp [-t templatefile] [-o outputfile] [-ln line_number] [-a] header_file
"""

example = \
"""
example:
    h2cppx -hfile sample.h 
    h2cppx -hfile sample.h -t template/template1
    h2cppx -hfile sample.h -o sample.cpp -ln 10
"""

parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        usage = usage,
        description=description,
        epilog = example
        )

parser.add_argument("header_file", help = "special c++ header file")

parser.add_argument(
        "-t", 
        "--template",
        type = str,
        required = False,
        action  = "store",
        default = "template/template1",
        help = "spcial template config file"
        )
#parser.add_argument( "-hfile", "--hfile", type = str, required = True, action = "store", help = "special c++ header file")
parser.add_argument(
        "-o",
        "--output",
        type = str,
        required = False,
        action = "store",
        help = "special cpp output file name, default is stdout"
        )
parser.add_argument(
        "-ln",
        "--line_number",
        type = int,
        required = False,
        action = "store",
        help = "special line number what generate cpp code"
        )
parser.add_argument(
        "-a",
        "--append",
        required = False,
        action = "store_true",
        default = False,
        help = "if cpp file already exist, append to cpp file tail."
        )

def do_action(args):
    Template.init(args.template)

    if not os.path.exists(args.header_file):
        print 'header file not exist!!!'
        return None

    buf = None
    if not args.output:
        buf = sys.stdout
    elif not os.path.exists(args.output):
        buf = open(args.output,'w')
    elif args.append:
        buf = open(args.output, 'a')
    else:
       print 'file already exist, please use "-a" arg to append code to file tail.'
       return None

    node = Header(args.header_file)
    if args.line_number:
        Template.FUNCTION_INTERVAL = Template.VARIABLE_INTERVAL = 1
        node = node.getNodeInLine(args.line_number)
        if not node:
            print 'special line number have not declare was found'
            return None

    visitor= ImplementGenerationVisitor(buf)
    node.accept(visitor)

    if type(buf) == file:
        buf.close()

if __name__=='__main__':
    args = parser.parse_args()
    try:
        do_action(args)
    except IOError,msg:
        print msg


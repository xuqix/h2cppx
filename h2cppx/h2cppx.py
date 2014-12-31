#!/usr/bin/env python

import os
import sys

cur_dir = os.path.split(os.path.realpath(__file__))[0]
sys.path.append(cur_dir)
sys.path.append(cur_dir+'/external')
sys.path.append(cur_dir+'/template')

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
    h2cpp [-t templatefile] [-o outputfile] [-ln line_number] [-a] [-f] header_file
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
        default = cur_dir+"/template/template1",
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
#mutually exclusive optional
group = parser.add_mutually_exclusive_group()
group.add_argument(
        "-a",
        "--append",
        required = False,
        action = "store_true",
        default = False,
        help = "if cpp file already exist, append to cpp file tail."
        )
group.add_argument(
        "-f",
        "--force",
        required = False,
        action = "store_true",
        default = False,
        help = "if cpp file already exist,will force overwrite cpp file!!!"
        )

def do_action(args):
    Template.init(args.template)

    if not os.path.exists(args.header_file):
        print >>sys.stderr,'header file not exist!!!'
        return None

    buf = StringIO()
    node = Header(args.header_file)
    if args.line_number:
        node = node.getNodeInLine(args.line_number)
        if not node:
            print >>sys.stderr,'special line number have not declare was found'
            return None

    # generate implement code
    visitor= ImplementGenerationVisitor(buf)
    node.accept(visitor)

    out = None
    if not args.output:
        out = sys.stdout
    elif not os.path.exists(args.output):
        out = open(args.output,'w')
    elif args.append:
        out = open(args.output, 'a')
    elif args.force:
        out = open(args.output, 'w')
    else:
       print >>sys.stderr,'file already exist, please use "-a" arg to append code to file tail.'
       return None

    #output
    if buf.len:
        out.write(buf.getvalue().lstrip(os.linesep).rstrip(os.linesep))
    else:
        print >>sys.stderr, 'Nothing generation'

    buf.close()
    if type(out) == file:
        buf.close()

if __name__=='__main__':
    args = parser.parse_args()
    try:
        do_action(args)
    except IOError,msg:
        print >>sys.stderr,msg


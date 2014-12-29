#!/usr/bin/env python

'''
    Parse c++ header file and generate c++ implement code
'''

import os
import sys

sys.path.append('external')

import visitor
from Parser import *

class ImplementGenerationVisitor(object):

    @visitor.on('node')
    def visit(self, node):
        """
        This is the generic method that initializes the
        dynamic dispatcher.
        """
        pass

    @visitor.when(Node)
    def visit(self, node):
        """
        Will run for nodes that do specifically match the
        provided type.
        """
        print 'Unrecognized node', node

    @visitor.when(Variable)
    def visit(self, node):
        """ Matches nodes of type variable. """
        comment= node['doxygen']
        if comment: comment+='\n'
        s = comment+((node['typedef']+'::') if node['typedef'] else '') + \
            node['raw_type']+' '+node['owner'] + '::' +  node['name'] +';'
        if node['static']:
            print s,'\n'

    @visitor.when(Function)
    def visit(self, node):
        """ Matches nodes that contain function. """ 
        if node['defined'] or node['inline']:
            return None
        scope = ((node['path']+'::') if node['path'] else '')
        para='('
        for p in node['parameters']:
            para += p['type'] + ' ' + p['name']
            if node['parameters'].index(p) < (len(node['parameters'])-1):
                para += ', '
        para += ')'
        comment= node['doxygen'] 
        print comment+'\n'+node['return_type']+' '+scope+node['name']+para \
                + '\n{\n\n}\n'

    @visitor.when(Class)
    def visit(self, node):
        """ Matches nodes that contain class. """
        for attr in node.attributes:
            attr.accept(self)
        for method in node.methods:
            method.accept(self)

    @visitor.when(Header)
    def visit(self, node):
        """ Matches nodes that contain header. """
        for function in node.functions:
            function.accept(self)
        for cls in node.classes:
            cls.accept(self)

if __name__=='__main__':
    head=Header('sample.h')
    head.accept(ImplementGenerationVisitor())


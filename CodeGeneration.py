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

    def __init__(self, stream=sys.stdout):
        '''
            stream parame specify code output stream,
            you can set it as stdxxx, StringIO or any file object
        '''
        self._stream = stream

    @property
    def stream(self):
        return self._stream

    @visitor.on('node')
    def visit(self, node):
        """
        This is the generic method that initializes the
        dynamic dispatcher.
        """
        pass

    @visitor.on('node')
    def startNode(self, node):
        pass

    @visitor.on('node')
    def endNode(self, node):
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
        if node['static'] and node['owner']:
            self._stream.write( s+'\n')

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
        self._stream.write( comment+'\n'+node['return_type']+' '+scope+node['name']+para \
                + '\n{\n\n}\n')

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

    @visitor.when(Variable)
    def startNode(self, node):
        if node['static'] and node['owner']:
            self._stream.write('start var\n')

    @visitor.when(Variable)
    def endNode(self, node):
        if node['static'] and node['owner']:
            self._stream.write('end var\n')

    @visitor.when(Function)
    def startNode(self, node):
        if node['defined'] or node['inline']:
            return None
        self._stream.write('start function\n')

    @visitor.when(Function)
    def endNode(self, node):
        if node['defined'] or node['inline']:
            return None
        self._stream.write('end function\n')

    @visitor.when(Class)
    def startNode(self, node):
        self._stream.write('start class\n')

    @visitor.when(Class)
    def endNode(self, node):
        self._stream.write('end class\n')

    @visitor.when(Header)
    def startNode(self, node):
        self._stream.write('start header\n')

    @visitor.when(Header)
    def endNode(self, node):
        self._stream.write('end header\n')

# for test
if __name__=='__main__':
    head=Header('sample.h')
    head.accept(ImplementGenerationVisitor())
#    head.functions[1].accept(ImplementGenerationVisitor())


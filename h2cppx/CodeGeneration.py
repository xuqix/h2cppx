#!/usr/bin/env python

'''
    Parse c++ header file and generate c++ implement code
'''

import os
import sys
import yaml

sys.path.append('external')

import visitor
from Parser import *

class Template(object):

    # template key-value 
    template = {}
    # keyword 
    keyword = [ 'TYPE', 'FULLNAME']

    @staticmethod
    def init(filename):
        data = file(filename).read()
        inside = False
        raw_content = ''
        #replace \n to \\n in " "
        for c in data:
            if c=='"':
                inside = not inside
            if inside and c=='\n':
                raw_content += '\\n'
            else:
                raw_content += c
        content = yaml.load(raw_content)
        for k in content:
            v = content[k]
            if type(v) == type(''): 
                k = k.lstrip('\n ').rstrip('\n ')
                v = v.lstrip('\n ').rstrip('\n ')
            Template.template[k] = v
            #dynamic create class attribute
            setattr(Template, k, v)

    @staticmethod
    def getFormatString(key):
        fmt = Template.template[key]
        for k in Template.keyword:
            fmt = fmt.replace(k,'%s')
        return fmt


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
        if (not node['static']) or (not node['owner']):
            return None
        doxy_comment = ''
        if Template.DOXYGEN: doxy_comment = node['doxygen'] + os.linesep
        fmt = Template.getFormatString('VARIABLE')
        var_type = ((node['typedef']+'::') if node['typedef'] else '') + node['raw_type'];
        if node['constant']: var_type = 'const ' + var_type
        var_name = node['owner'] + '::' +  node['name']
        var_def  = fmt % (var_type, var_name)
        self._stream.write( doxy_comment + var_def + 
                Template.VARIABLE_INTERVAL * os.linesep)

    @visitor.when(Function)
    def visit(self, node):
        """ Matches nodes that contain function. """ 
        if node['defined'] or node['inline'] or node['extern'] or \
           node['pure_virtual'] or node['friend']:
            return None
        doxy_comment = ''
        if Template.DOXYGEN: doxy_comment = node['doxygen'] + os.linesep

        ret_type = node['return_type']
        fullname = ((node['path']+'::') if node['path'] else '') + \
                   ('~' if node['destructor'] else '') + node['name']
        parameters=''
        for p in node['parameters']:
            parameters += p['type'] + ' ' + p['name']
            if node['parameters'].index(p) < (len(node['parameters'])-1):
                parameters += ', '
        fmt = Template.getFormatString('FUNCTION')
        fun_def = ''
        if node['constructor'] or node['destructor']:
            fun_def = fmt[3:] % (fullname, parameters)
        else:
            fun_def = fmt % (ret_type, fullname, parameters)
        if node['const']:
            fun_def = fun_def.replace(')', ') const')
        self._stream.write( doxy_comment + fun_def + 
                Template.FUNCTION_INTERVAL * os.linesep )

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
            self._stream.write(Template.VARIABLE_START)

    @visitor.when(Variable)
    def endNode(self, node):
        if node['static'] and node['owner']:
            self._stream.write(Template.VARIABLE_END)

    @visitor.when(Function)
    def startNode(self, node):
        if node['defined'] or node['inline']:
            return None
        self._stream.write(Template.FUNCTION_START)

    @visitor.when(Function)
    def endNode(self, node):
        if node['defined'] or node['inline']:
            return None
        self._stream.write(Template.FUNCTION_END)

    @visitor.when(Class)
    def startNode(self, node):
        self._stream.write(Template.CLASS_START)

    @visitor.when(Class)
    def endNode(self, node):
        self._stream.write(Template.CLASS_END)

    @visitor.when(Header)
    def startNode(self, node):
        self._stream.write(Template.HEADER_START)
        self._stream.write('\n\n#include "'+node['header_file']+'"\n\n')

    @visitor.when(Header)
    def endNode(self, node):
        self._stream.write(Template.HEADER_END)


# for test
if __name__=='__main__':
    Template.init('template/template1')
    head=Header('sample.h')
    print 'Generate all head file implement: '
    head.accept(ImplementGenerationVisitor())
    print 'Generate special line_number %d implement: \n' % 15
    head.getNodeInLine(15).accept(ImplementGenerationVisitor())


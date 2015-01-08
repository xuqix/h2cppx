#!/usr/bin/env python

'''
    Encapsulation CppHeaderParser for Parse c++ header file 
'''

import os
import sys

sys.path.append('external')

from CppHeaderParser import CppHeaderParser

class Node(object):
    '''all parse object base class'''

    def __init__(self, *args):
        self.children = []
        try:
            for child in args:
                if issubclass(child, self.__class__):
                    self.children.append(child)
                else:
                    raise TypeError('args must is subclass from Node')
        except TypeError, msg:
            print 'Exception: ',msg
            sys.exit()

    def accept(self, visitor):
        try:
            visitor.startNode(self)
        except AttributeError:
            pass

        visitor.visit(self)

        try:
            visitor.endNode(self)
        except AttributeError:
            pass

    def __getitem__(self, key):
        return self._info[key]

    def __getattr__(self, name):
        if name in self._info:
            return self._info[name]
        return object.__getattr__(name)


class Variable(Node):
    ''' cpp variable object '''

    def __init__(self, info, access=None):
        super(Variable,self).__init__()
        self._info = {
            'access'   : access,
            'type'     : info['type'],
            'raw_type' : info['raw_type'],
            'typedef'  : info['typedef'],
            'name'     : info['name'],
            'namespace': info['namespace'],
            'owner'    : info['property_of_class'],
            'static'   : True if info['static'] else False,
            'doxygen'  : info['doxygen'] if 'doxygen' in info else '',
            'line_number' : info['line_number'],
            'constant' : True if info['constant'] else False,
            'default_value' : info['default_value'] if 'default_value' in info else '',
        }
        self._info['path'] = self._info['namespace'] + self._info['owner']
        self._info['sign_name'] = self._info['path'] + '::' +  self._info['name']
        self._info['sign_type'] = ((self._info['typedef']+'::') if self._info['typedef'] else '') + self._info['raw_type'];
        if self._info['constant']: 
            self._info['sign_type'] = 'const ' + self._info['sign_type']

class Function(Node):
    ''' 
        cpp function object 
        note: 
        self['parameters'] is a dict of list, dict 
        contains the following keys:
              'line_number', 'constant', 'name', 
              'reference', 'type', 'static' , 'pointer'
    '''

    def __init__(self, info, access=None):
        super(Function, self).__init__()
        self._info = {
            'access' : access,
            'name' : info['name'],
            'debug': info['debug'],
            'returns': info['returns'],
            'return_type': info['rtnType'],
            'namespace' : info['namespace'],
            'parameters' : info['parameters'], 
            'line_number' : info['line_number'],
            'const': True if info['const'] else False,
            'inline': True if info['inline'] else False,
            'extern': True if info['extern'] else False,
            'friend': True if info['friend'] else False,
            'defined': True if info['defined'] else False,
            'path' : info['path'] if 'path' in info else '',
            'operator' : True if info['operator'] else False,
            'virtual' : 'virtual' if info['virtual'] else '',
            'explicit' : 'explicit' if info['explicit'] else '',
            'destructor' : True if info['destructor'] else False,
            'parent' : info['parent'] if 'parent' in info else '',
            'constructor': True if info['constructor'] else False,
            'pure_virtual': 'pure virtual' if info['pure_virtual'] else '',
            'doxygen'  : info['doxygen'] if 'doxygen' in info else '',
        }
        self._info['sign_name'] = \
        ((self._info['path']+'::') if self._info['path'] else '') + \
        ('~' if self._info['destructor'] else '') + self._info['name']


class Class(Node):
    ''' cpp class object '''

    def __init__(self, info):
        super(Class, self).__init__()
        self._info = {
            'inherits' : info['inherits'],
            'line_number' : info['line_number'],
            'forward_declares' : info['forward_declares'],
            'name' : info['name'],
            'namespace' : info['namespace'],
            'declaration_method' : info['declaration_method'],
            'doxygen' : info['doxygen'] if 'doxygen' in info else '',
        }
        self._attrs = []
        self._methods = []
        for access in ['public', 'protected', 'private']:
            for attr in info['properties'][access]:
                self._attrs.append(Variable(attr, access))
            for method in info['methods'][access]:
                self._methods.append(Function(method, access))

    @property
    def methods(self):
        return self._methods

    @property
    def attributes(self):
        return self._attrs

class Header(Node):
    ''' cpp header file object '''

    def __init__(self, header_file):
        super(Header, self).__init__()
        header = CppHeaderParser.CppHeader(header_file)
        self._info = {
            'header_file' : header_file,
            'includes' : header.includes,
        }
        self._functions = [ Function(function) for function in header.functions ]
        self._classes = [ Class(cls) for name,cls in header.classes.items() ]

    @property
    def functions(self):
        return self._functions

    @property
    def classes(self):
        return self._classes

    def getNodeInLine(self, line_number):
        for cls in self._classes:
            for fun in cls.methods:
                if fun['line_number'] == line_number:
                    return fun
            for attr in cls.attributes:
                if attr['line_number'] == line_number:
                    return attr
        for fun in self._functions:
            if fun['line_number'] == line_number:
                return fun
        return None


#test for Parser
if __name__=='__main__':

    h=Header('sample.h')
    for f in h.functions:
        print f['path'], f['return_type'], f['name'], f['parameters'][0]['name'] if len(f['parameters'])>0 else None

    for c in h.classes:
        for f in c.methods:
            print f['path'], f['return_type'], f['name'], f['parameters'][0]['name'] if len(f['parameters'])>0 else None
    

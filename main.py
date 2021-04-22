# -*- coding: utf-8 -*-
#
# Copyright (C) 2019, Carlos Damasceno <damascenodiego@usp.br>

import re
import argparse

import networkx as nx
import networkx.drawing.nx_agraph as nx_agraph

parser = argparse.ArgumentParser()
parser.add_argument('file', type=argparse.FileType('rb'))

arguments = parser.parse_args()


fname = arguments.file.name
print(fname)

kiss_pattern = "(.+)\s+--\s+(.+)\s+/\s+(.+)\s+->\s+(.+)"

_states = set()

with open(fname, newline='\n') as _fname:
    _dot = nx.DiGraph(name='g')   # or DiGraph, MultiGraph, MultiDiGraph, etc
    _initialstate = None
    for _line in _fname.readlines():
        _line=_line.replace("\r","")
        match = re.search(kiss_pattern,_line)
        if match:
            _orig, _in, _out, _dest = match.groups()
            if (not _orig in _states):
                _initialstate = _orig
                _states.add(_orig)
                _dot.add_node(_orig)
            if (not _dest in _states):
                _states.add(_dest)
                _dot.add_node(_dest)
            _dot.add_edge(_orig, _dest,label='{}/{}'.format(_in,_out))
        else:
            print("pattern not found")
    _dot.add_node('__start0', label="", shape="none", width="0", height="0")
    _dot.add_edge('__start0', _initialstate)
    dot_fname = fname.replace('.kiss', '.dot')
    nx_agraph.write_dot(_dot,dot_fname)
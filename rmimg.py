#!/usr/bin/python

import sys, re

orig_data = file(sys.argv[1]).read().split('\n')

OBJ_RE = re.compile(r'^(\d+) \d+ obj$')
TYPE_RE = re.compile(r'/Subtype /(\w+)')
END_RE = re.compile(r'^endobj$')

def scan(data, targs=None):
    obj = None
    in_dict = False
    typ = None

    i = 0
    while i < len(data):
        l = data[i]
        if targs and obj in targs:
            del data[i]
        else:
            i += 1

        m = OBJ_RE.match(l)
        if m:
            # Start of object
            obj = m.group(1)
            if targs and obj in targs:
                del data[i]
            continue

        if l.startswith('<<'):
            in_dict = True
        if in_dict and obj and not typ:
            m = TYPE_RE.search(l)
            if m:
                typ = m.group(1)
                continue
        if l.endswith('>>'):
            in_dict = False

        m = END_RE.match(l)
        if m:
            if targs and obj in targs:
                print 'Deleted', obj
            elif obj and typ:
                print obj, typ
            obj = typ = None
            continue
    
    with open(sys.argv[1], 'w') as fil:
        fil.write('\n'.join(data))

cmd = 'r'
while True:
    if cmd in ('r', 'q'):
        curr_data = list(orig_data)
        scan(curr_data)
    if cmd in ('s', 'q'):
        break
    if cmd[0].isdigit():
        if ',' in cmd:
            targs = [t.strip() for t in cmd.split(',')]
        else:
            targs = cmd.split()
        scan(curr_data, targs)

    print
    print 'R. Revert'
    print 'Q. Revert and Quit'
    print 'S. Save and Quit'
    cmd = raw_input("Enter objs to delete or command: ").lower()

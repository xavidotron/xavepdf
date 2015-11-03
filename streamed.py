#!/usr/bin/python

import sys, re, json

orig_data = file(sys.argv[1]).read().split('\n')

OBJ_RE = re.compile(r'^(\d+) \d+ obj$')
STREAM_RE = re.compile(r'^stream$')
TEXT_RE = re.compile(r'\(((?:[^)]|\\\))+)\)\sTj\b|\[\s\(((?:[^)]|\\\))+)\)\s\d+\.\d+\s\(((?:[^)]|\\\))+)\)\s\]\sTJ\b')
END_STREAM_RE = re.compile(r'^endstream$')
END_RE = re.compile(r'^endobj$')

MAPPING = {}
try:
    with open(sys.argv[1] + '.mapping') as mfil:
        MAPPING = json.load(mfil)
except IOError:
    pass

def scan(data, targs=[]):
    targs = list(targs)
    obj = None
    stream_start = None
    del_txt = None

    i = 0
    while i < len(data):
        l = data[i]
        i += 1

        m = OBJ_RE.match(l)
        if m:
            # Start of object
            obj = m.group(1)
            continue
        
        if obj:
            if stream_start is not None:
                m = END_STREAM_RE.match(l)
                if m:
                    lines = '\n'.join(data[stream_start:i])
                    cnt = 0
                    for m in TEXT_RE.finditer(lines):
                        txt = m.group(1)
                        if txt is None:
                            txt = m.group(2) + m.group(3)
                        txt = txt.replace(r'\(', '(').replace(r'\)', ')')
                        mapped_txt = ""
                        for c in txt:
                            if c in MAPPING:
                                mapped_txt += MAPPING[c]
                            else:
                                mapped_txt += c
                        span = '%s.%s' % (obj, cnt)
                        if span in targs:
                            del_txt = txt
                            lines = lines[:m.start()] + lines[m.end():]
                            data[stream_start:i] = lines.split('\n')
                            targs.remove(span)
                            print 'Deleted', mapped_txt, '(%s)' % txt
                        else:
                            print span, mapped_txt, '(%s)' % txt
                            cnt += 1

                    if cnt > 0:
                        print obj, 'end stream of', cnt
                    stream_start = None
                    continue                
            else:
                m = STREAM_RE.search(l)
                if m:
                    stream_start = i + 1
                    continue
                
                m = END_RE.match(l)
                if m:
                    obj = None
                    continue
    
    with open(sys.argv[1], 'w') as fil:
        fil.write('\n'.join(data))
    
    return del_txt

cmd = 'r'
targs = []
while True:
    if cmd == 'm':
        mapping = ""
        while len(mapping) != len(txt):
            mapping = raw_input('Enter mapping for "%s": ' % txt)
        for i in xrange(len(mapping)):
            MAPPING[txt[i]] = mapping[i]
    if cmd in ('r', 'q', 'm'):
        curr_data = list(orig_data)
        scan(curr_data)
    if cmd in ('s', 'q'):
        break
    if cmd[0].isdigit():
        if ',' in cmd:
            targs = [t.strip() for t in cmd.split(',')]
        else:
            targs = cmd.split()
        txt = scan(curr_data, targs)

    print
    print 'R. Revert'
    print 'Q. Revert and Quit'
    print 'S. Save and Quit'
    if len(targs) == 1:
        print 'M. Map "%s" and Revert' % txt
    cmd = raw_input("Enter string to delete or command: ").lower()

with open(sys.argv[1] + '.mapping', 'w') as mfil:
    json.dump(MAPPING, mfil)

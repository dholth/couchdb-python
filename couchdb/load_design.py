#!/usr/bin/env python
"""
Simple, Python 3 compatible design doc from filesystem loader.
"""

from __future__ import unicode_literals

import os.path
import pprint
import codecs
import json

def load_design(directory, strip_files=False):
    """
    Load a design document from the filesystem.
    
    strip_files: call .strip() on file contents, like couchdbkit
    """
    objects = {}
    
    for (dirpath, dirnames, filenames) in os.walk(directory, topdown=False):
        key = os.path.split(dirpath)[-1]
        ob = {}        
        objects[dirpath] = (key, ob)

        for name in filenames:            
            fkey = os.path.splitext(name)[0]
            fullname = os.path.join(dirpath, name)
            with codecs.open(fullname, 'r', 'utf-8') as f:
                contents = f.read()
                if name.endswith('.json'):                
                    contents = json.loads(contents)
                elif strip_files:
                    contents = contents.strip()
                ob[fkey] = contents

        for name in dirnames:
            if name == '_attachments':
                raise NotImplementedError()
            subkey, subthing = objects[os.path.join(dirpath, name)]
            ob[subkey] = subthing

    return ob

if __name__ == "__main__":
    import sys
    ob = load_design(sys.argv[1])
    pprint.pprint(ob)


import os
import sys

subfolder = sys.argv[1]

if not os.path.isdir(subfolder):
    os.mkdir(subfolder)

with open(subfolder + '/file', 'w') as f:
    f.write('bleh')
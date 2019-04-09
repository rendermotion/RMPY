#!/C:/Program Files/Autodesk/Maya2018/bin mayapy
import os
import sys
sys.path.insert(0, os.path.abspath('C:/Python27/Lib/site-packages'))
import maya.standalone
maya.standalone.initialize(name='python')
import sphinx

if __name__ == '__main__':
    argv = sys.argv[1:]
    print argv
    cwd = os.getcwd()
    argv.insert(0, sphinx.__file__)
    sphinx.main(argv)
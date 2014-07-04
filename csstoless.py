from tempfile import mkstemp
from shutil import move
import os
import sys



def main(argv):
    #main code
    if len(sys.argv) == 1:
        #No path to css folder given
        path = raw_input("Enter the relative path to the css folder")
    else:
        #I also supported you being able to give a path via arguments in the command line (python this_script.py path/to/css)
        path = sys.argv[1]




#Secure we're run as the main script, if so, run main()
if __name__ == "__main__":
    main(sys.argv)
else:
    print "You are trying to run this python script as a module."
    print "This is not supported. Please run " + os.path.basename(__file__)
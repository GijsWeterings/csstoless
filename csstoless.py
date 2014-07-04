from tempfile import mkstemp
import shutil
from shutil import move
import os
import sys

#Restarts the script in case of a fail
def restart():
    python = sys.executable
    os.execl(python,python, * sys.argv)

def replace(file_path, pattern, subst):
    #Creates temporary files to work in
    fh, less_file_path = mkstemp()
    fh2, variables_file_path = mkstemp()
    fh3, result_file_path = mkstemp()

    #open all needed files
    result_file = open(result_file_path,'wb')
    less_file = open(less_file_path,'wb+')
    variables_file = open(variables_file_path, 'wb+')
    css_file = open(file_path, 'rb')

    for line in css_file:
        variables_file.write("variabele ")
        less_file.write(line)#.replace(pattern,subst))
    
    #We're done writing to these files, to concatinate them we need to reopen them in a different mode
    less_file.close()
    variables_file.close()

    #join the variables and rules together in the result file
    shutil.copyfileobj(open(variables_file_path, 'rb'),result_file)
    shutil.copyfileobj(open(less_file_path,'rb'),result_file)

    #Close down result file in preperation of moving
    result_file.close()

    #moves the result file to the created less folder
    modified_file_path = (file_path[:-3] + 'less').split('/',1)[1]
    modified_file_path = 'less/'+modified_file_path
    print modified_file_path
    move(result_file_path, modified_file_path)

    #remove unused tempfile
    os.remove(less_file_path)
    os.remove(variables_file_path)

    #close .css file
    css_file.close()

def main(argv):
    print 'full path =', os.path.abspath(os.path.dirname(sys.argv[0]))
    #main code
    if len(sys.argv) == 1:
        #No path to css folder given
        path = raw_input("Enter the relative path to the css folder: ")
    else:
        #I also supported you being able to give a path via arguments in the command line (python this_script.py folder)
        path = sys.argv[1]
    while not os.path.isdir(path):
        path = raw_input("\nPath is not valid. Please give a valid path: ")

    #create less directory, if not exists
    if not os.path.exists('less'):
        os.mkdir('less')

    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".css"):
                print "Processing " + file
                replace(os.path.join(root,file), "","")#pattern, subst)




#Secure we're run as the main script, if so, run main()
if __name__ == "__main__":
    main(sys.argv)
else:
    print "You are trying to run this python script as a module."
    print "This is not supported. Please run " + os.path.basename(__file__)


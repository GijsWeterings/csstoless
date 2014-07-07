from tempfile import mkstemp
from shutil import move
import os
import sys
import shutil
import re

# Global variables
colorvariables = {}

# Reads a line, and replaces HEX codes with LESS variables.
# Variables are added on top of the resulting LESS file.
def checkColor(line):
    variablerule = ""

    # We search the line for a HEX code with a regex search
    m = re.search(r"#[0-9abcdefABCDEF]{6}", line)

    # We have a hit of a HEX code.
    if m is not None:
        # We extract the found HEX value, and convert it to uppercase to ensure coding standards
        variable = m.group(0).upper()

        # Add new variable to the list if it isn't in it yet
        if variable not in colorvariables:
            colorvariables[variable] = "@color" + str(len(colorvariables))
            variablerule = colorvariables[variable] + ": " + variable + ";\n"

        # Insert the newly created variable in place of the HEX code
        line = line.replace(variable,colorvariables[variable])

    return (variablerule, line)

def process(file_path):
    colorvariables.clear()

    # Creates temporary files to work in
    fh, less_file_path = mkstemp()
    fh2, variables_file_path = mkstemp()
    fh3, result_file_path = mkstemp()

    # Open all needed files
    result_file = open(result_file_path,'wb')
    less_file = open(less_file_path,'wb+')
    variables_file = open(variables_file_path, 'wb+')
    css_file = open(file_path, 'rb')

    for line in css_file:
        variable, lessrule = checkColor(line)
        variables_file.write(variable)
        less_file.write(lessrule)#.replace(pattern,subst))

    # We're done writing to these files,
    # to concatinate them we need to reopen them in a different mode
    less_file.close()
    variables_file.close()

    # Join the variables and rules together in the result file
    shutil.copyfileobj(open(variables_file_path, 'rb'),result_file)
    shutil.copyfileobj(open(less_file_path,'rb'),result_file)

    # Close down result file in preperation of moving
    result_file.close()

    # Moves the result file to the created less folder
    filename = os.path.basename(file_path)

    modified_file_path = (filename[:-3] + 'less')
    modified_file_path = 'less/' + modified_file_path
    print "Writing parsed LESS file to " + modified_file_path + "\n"
    move(result_file_path, modified_file_path)

    # Remove unused tempfiles
    os.remove(less_file_path)
    os.remove(variables_file_path)

    # Close .css file
    css_file.close()

def main(argv):
    # Extract path from either command line arguments or from user input
    if len(sys.argv) == 1:
        # No path to css folder given
        path = raw_input("Enter the relative path to the css folder: ")
    else:
        # I also supported you being able to give a path via arguments in the command line (python this_script.py folder)
        path = sys.argv[1]
    while not os.path.isdir(path):
        path = raw_input("\nPath is not valid. Please give a valid path: ")

    # Create less directory, if not exists
    if not os.path.exists('less'):
        os.mkdir('less')

    # Search trough all subfolders of the given basepath and search for .css files
    for root, _, files in os.walk(path):
        for file in files:
            if file.endswith(".css"):
                print "Reading " + file + " and processing"
                process(os.path.join(root,file))




# Secure we're run as the main script, if so, run main()
if __name__ == "__main__":
    main(sys.argv)
else:
    print "You are trying to run this python script as a module."
    print "This is not supported. Please run " + os.path.basename(__file__)


import sys
import csp_solver as csp

# check validity of arguments
if len(sys.argv) < 4:
    print('Not enough arguments! Use "python main.py <problem.var> <problem.con> <none/fc>"')
    quit()
if len(sys.argv) > 4:
    print('Too many arguments! Use "python main.py <problem.var> <problem.con> <none/fc>"')
    quit()
if sys.argv[3] != "none" and sys.argv[3] != "fc":
    print('Invalid value for consistent-enforcing procedure! Must be "none" or "fc"')
    quit()

# attempt to open files
try:
    var_file = open(sys.argv[1], "r")
except:
    print('Could not open file "' + sys.argv[1] + '".')
    quit()
    
try:
    con_file = open(sys.argv[2], "r")
except:
    print('Could not open file "' + sys.argv[2] + '".')
    quit()
    
# read the var file and make a dict containing the domain of each variable
vars = {}
for line in var_file:
    name = line[0]
    # remove any leading or trailing whitespace, split into a list
    strlist = line[3:].strip().split(' ')
    # convert list of strings into list of integers
    domain = []
    for val in strlist:
        domain.append(int(val))
    vars[name] = domain

# read the con file and make a list containing every constraint
cons = []
for line in con_file:
    # remove any leading or trailing whitespace
    cons.append(line.strip())
    
# set fc
fc = False
if (sys.argv[3] == "fc"):
    fc = True

# now do the thing!
csp.backtrack(cons, vars, {}, fc)
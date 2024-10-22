# Zac Hays

import copy

# checks if a constraint is adhered to
# takes a constraint and a dict of assigned vars
def checkCon(constraint, assigned):
    key1, operator, key2 = constraint.split(' ')
    # if either variable in the constraint isn't in assigned, it will return true
    # it's only looking for direct violations
    if key1 not in assigned or key2 not in assigned:
        return True
    var1 = assigned[key1]
    var2 = assigned[key2]
    
    if operator == '=':
        return var1 == var2
    if operator == '!':
        return var1 != var2
    if operator == '>':
        return var1 > var2
    if operator == '<':
        return var1 < var2
    
# checks that ALL constraints are adhered to
def checkAllCons(constraints, assigned):
    for con in constraints:
        if checkCon(con, assigned) == False:
            return False
    return True

# returns the number of constraints key is a part of, excluding ones with an assigned variable
def howConstraining(key, cons, assigned):
    count = 0
    for constraint in cons:
        key1, operator, key2 = constraint.split(' ')
        if key1 not in assigned and key2 not in assigned:
            if key1 == key or key2 == key:
                count += 1
    return count

# a helper function for finding the least constraining value; returns the sum of possible values for remaining variables
#   to explain a quirk: assigned is the real list of assigned variables, whereas fakeAssigned is a list
#   containing only the variable we are currently checking. this is so other constraints don't apply
def lcvHelper(cons, vars, assigned, fakeAssigned):
    count = 0
    for var in vars:
        if var in assigned: continue
        for value in vars[var]:
            temp = fakeAssigned.copy()
            temp[var] = value
            if checkAllCons(cons, temp):
                count += 1
    return count

# returns an updated version of vars with only valid values in each variable's domain
def doForwardCheck(cons, vars, assigned):
    newVars = copy.deepcopy(vars)
    for var in vars:
        if var in assigned: continue
        for value in vars[var]:
            temp = assigned.copy()
            temp[var] = value
            if not checkAllCons(cons, temp):
                newVars[var].remove(value)
    return newVars

# branch number
branchNo = 0
# print the branch with the correct formatting
def printBranch(assigned, success):
    global branchNo
    branchNo += 1
    out = str(branchNo) + ". "
    for key in assigned:
        out += key + "=" + str(assigned[key]) + ", "
    if (success):
        out = out[0 : -2] + "  solution"
    else:
        out = out[0 : -2] + "  failure"
    print(out)

# recursive backtracking algorithm
def backtrack(cons, vars, assigned, fc):
    
    # do forward checking if enabled
    if fc:
        vars = doForwardCheck(cons, vars, assigned)
    # check for failure
    if not checkAllCons(cons, assigned):
        printBranch(assigned, False)
        return False
    for key in vars:
        if not vars[key]: # variable with an empty domain
            printBranch(assigned, False)
            return False
    # check for success
    if len(vars) == len(assigned):
        printBranch(assigned, True)
        return True
    
    # choose a variable
    curVar = None
    # find most constrain[ed] var(s)
    ed = []
    for key in vars:
        if key in assigned: continue
        if not ed: # ed is empty - just add whatever
            ed.append(key)
        # if they have the same domain size, just append
        elif len(vars[key]) == len(vars[ed[0]]):
            ed.append(key)
        # if the new key is more constrained, kick everyone else out
        elif len(vars[key]) < len(vars[ed[0]]):
            ed.clear()
            ed.append(key) 
    if len(ed) > 1:
        # break ties with most constrain[ing]
        ing = []
        for key in ed:
            if not ing: # ing is empty - just add whatever
                ing.append(key)
            # if they have the same number of constraints, just append
            elif howConstraining(key, cons, assigned) == howConstraining(ing[0], cons, assigned):
                ing.append(key)
            # if the new key is more constraining, kick everyone else out
            elif howConstraining(key, cons, assigned) > howConstraining(ing[0], cons, assigned):
                ing.clear()
                ing.append(key)
        # finally, break ties alphabetically
        curVar = min(ing)
    else:
        curVar = ed[0]
        
    # choose a value - keep trying until it works or runs out!
    tempVars = copy.deepcopy(vars)
    while tempVars[curVar]:
        bestVals = []
        hiScore = -1
        # check the 'lcv score' for each possible value in the domain, pick the maximum
        for val in tempVars[curVar]:
            fakeAssigned = {curVar: val}
            score = lcvHelper(cons, tempVars, assigned, fakeAssigned)
            if not bestVals: # empty - add whatevers
                bestVals.append(val)
                hiScore = score
            # if same score, append
            elif score == hiScore:
                bestVals.append(val)
            # if it beat the high score, kick everyone else out
            elif score > hiScore:
                bestVals.clear()
                bestVals.append(val)
                hiScore = score
        # break ties with lowest value
        curValue = min(bestVals)
        
        # recur with curVar assigned to curValue
        temp = assigned.copy()
        temp[curVar] = curValue
        if backtrack(cons, vars, temp, fc):
            return True
        
        # this value wasn't in the solution. remove it and loop!
        tempVars[curVar].remove(curValue)
        
    # no value worked for this variable!
    return False
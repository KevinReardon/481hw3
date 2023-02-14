import sys
import ast
import random
import astor
import shutil
import os
import time


# Get the current time in seconds since start
current_time = int(time.time())
#print ("Current time", current_time)

# Set the seed for the random number generator using the current time
random.seed(current_time)


class MutantGen(ast.NodeTransformer):
    print("test1")
    # Swap Comparison operators
    def swapComp(self, node):
        print("test2")
        for i, comp in enumerate(node.ops):
            if random.random() < 0.5:
                # Change == to !=
                if comp == ast.Eq:
                    node.ops[i] = ast.NotEq
                # Change >= to <
                elif comp == ast.GtE:
                    node.ops[i] = ast.Lt
                # Change <= to >
                elif comp == ast.LtE:
                    node.ops[i] = ast.Gt

    # Swap Binary Operators
    def swapBinOp(self, node):
        print("test3")
        for i, op in enumerate(node.op):
            if random.random() < 0.5:
                #swap + with -
                if op == ast.Add:
                    node.op[i] = ast.Sub
                #swap + with -
                if op == ast.Sub:
                    node.op[i] = ast.Add
    
    #Delete assignment 25% of the time
    def delAssign(self, node):
        print("test4")
        if isinstance(node, ast.Assign) and random.random() < 0.25:
            return ast.Delete(targets=[ast.Name(id=t.id, ctx=ast.Del()) for t in node.targets])
        return node



def main():
    # Command line arg check
    if len(sys.argv) != 3:
        print("Needs 2 arguments 1st: File, 2nd: # of mutants")
        return
    
    # Get file and # of mutants 
    fileName = sys.argv[1]
    try:
        numMut = int(sys.argv[2])
        if numMut <= 0:
            raise ValueError("Number of mutants must be positive")
    except ValueError:
        print("Invalid number of mutants")
        return


    # Build AST from source file
    with open(fileName, "r") as source:
        sourceTree = ast.parse(source.read())
        
        #print(ast.dump(sourceTree))

    # Save unmodified version of source
    temp = sourceTree
    numMut = int(numMut)

    # Initialize mutant generator
    gen = MutantGen()
    for i in range(numMut):
        # Reset SourceTree to unmodified source
        sourceTree = temp

        # Apply mutation transformations
        mutantTree = gen.visit(sourceTree)
        #mutantTree = gen.delAssign(gen.swapComp(gen.swapBinOp(sourceTree)))
        #mutantTree = gen.delAssign(gen.swapBinOp(gen.swapComp(sourceTree)))


        mutantTreeFix = ast.fix_missing_locations(mutantTree)
        # Transform mutant AST to source
        mutantTreeSource = astor.to_source(mutantTreeFix)

        # Write mutated source to a file
        with open((str(i) + ".py"), "w") as f:
            f.write(mutantTreeSource)

        print("Mutant " + str(i) + " created")

if __name__ == "__main__":
    main()
import sys
import ast
import random
import astor
import shutil
import os

random.seed(0)

class MutantGen(ast.NodeTransformer):
    # Swap Comparison operators
    def swapComp(self, node):
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
        for i, op in enumerate(node.op):
            if random.random() < 0.5:
                #swap + with -
                if op == ast.Add:
                    node.op[i] = ast.Add
                #swap + with -
                if op == ast.Sub:
                    node.op[i] = ast.Add
    
    #Delete assignment 25% of the time
    def delAssign(self, node):
        if random.random() < 0.75:
            return node
        else:
            return None

def main():
    # Command line arg check
    if len(sys.argv) != 3:
        print("Needs 2 arguments 1st: File, 2nd: # of mutants")
        return
    
    # Get file and # of mutants 
    fileName = sys.argv[1]
    numMut = sys.argv[2]

    # Build AST from source file
    with open(fileName, "r") as source:
        sourceTree = ast.parse(source.read())

    # Save unmodified version of source
    temp = sourceTree
    numMut = int(numMut)
    # Initialize mutant generator
    gen = MutantGen()
    for i in range(numMut):
        # Reset  SourceTree to unmodified source
        sourceTree = temp
        # Apply mutation transformations
        mutantTree = gen.visit(sourceTree)
        ast.fix_missing_locations(mutantTree)
        # Transform mutant AST to source
        mutantTreeSource = astor.to_source(mutantTree)

        # Write mutated source to a file
        with open((str(i) + ".py"), "w") as f:
            f.write(mutantTreeSource)

        # Make dir if it does not exits
        #output_dir = "mutDir"
        #if not os.path.exists(output_dir):  
        #    os.makedirs(output_dir)

        # Move file to mutant dir
       #shutil.move((str(i) + ".py"), os.path.join(output_dir, (str(i) + ".py")))

if __name__ == "__main__":
    main()
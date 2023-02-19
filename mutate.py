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



class MutantGen(ast.NodeTransformer):
    def __init__(self, value):
        self.val = value

    def visit(self, node):
        # randomly mutate the node with a small probability
        val = (self.val * .007) + .01
        if random.random() < val:
            node = self.mutate_node(node)
        return self.generic_visit(node)

    def mutate_node(self, node):
        # choose a random mutation to apply to the node
        mutations = [
            self.deleteAssign,
            self.binOp,
            self.compare,
            self.returnSwap,
            
        ]
        mutation = random.choice(mutations)
        return mutation(node)
    
    # Swap Comparison operators
    def compare(self, node):
        if isinstance(node, ast.Compare):
            self.generic_visit(node)
            if isinstance(node.ops, ast.Eq):
                print("test1")
                node.ops = ast.NotEq()
            if isinstance(node.ops, ast.NotEq):
                print("test1")
                node.ops = ast.Eq()
            if isinstance(node.ops, ast.Lt):
                print("test1")
                node.ops = ast.GtE()
            if isinstance(node.ops, ast.Gt):
                print("test1")
                node.ops = ast.LtE()
            if isinstance(node.ops, ast.LtE):
                print("test1")
                node.ops = ast.Gt()
            if isinstance(node.ops, ast.GtE):
                print("test1")
                node.ops = ast.Lt()
        return node
                               
    def binOp(self, node):
        if isinstance(node, ast.BinOp):
            self.generic_visit(node)                
            if isinstance(node.op, ast.Add):
                print("test2")
                node.op = ast.Sub()
            elif isinstance(node.op, ast.Sub):
                print("test2")
                node.op = ast.Add()
            elif isinstance(node.op, ast.Mult):
                print("test2")
                node.op = ast.Div()
            elif isinstance(node.op, ast.Div):
                print("test2")
                node.op = ast.Mult()
        return node
    
    #Delete assignment 25% of the time
    def deleteAssign(self, node):
        if isinstance(node, ast.Assign):
            print("test3")
            return ast.Expr(value=None)
        return node
    
    def returnSwap(self, node):
        if isinstance(node, ast.Return):
            self.generic_visit(node)
            if isinstance(node.value, ast.Num):
                print("test4")
                node.value.n = 481
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
    
    for i in range(numMut):
        random.seed(current_time)
        # Reset SourceTree to unmodified source
        sourceTree = temp
        gen = MutantGen(i)
        # Apply mutation transformations
        mutantTree = gen.visit(sourceTree)

        mutantTreeFix = ast.fix_missing_locations(mutantTree)
        # Transform mutant AST to source
        mutantTreeSource = astor.to_source(mutantTreeFix)

        # Write mutated source to a file
        with open((str(i) + ".py"), "w") as f:
            f.write(mutantTreeSource)

        print("Mutant " + str(i) + " created")

if __name__ == "__main__":
    main()
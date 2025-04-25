
from id3 import *


class Controller:
    def __init__(self) :
        self.decisionTree = self.makeDecisionTree()
        
        
    def setPacman(self, pac):
        self.pacman = pac
    
    def getState(self):
        ghost_close = self.ghostClose(100)
        closePP = self.pelletClose(150)
        
        pelletEaten = self.pacman.eatPellets(self.pacman.allPowerPellets)  
        pelletEatenBool = pelletEaten is not None
        
        #Time is allways 1 at the moment
        time = 1
        currentValues = [ghost_close, pelletEatenBool,closePP,time]
        currentExample = Example(0,currentValues)
        
        st = self.determineState(self.decisionTree, currentExample)
        return st
        

    #Determines pacman state based on pacmans current data
    def determineState(self,tree:DecisionNode, currentExample: Example):

        if len(tree.childNodes) > 0: # Any children?
            index = allAttributes.index(tree.testValue) # atrribute index
            value = currentExample.getValue(index) #Gets value from current example (state)
            
            if value in tree.childNodes: #Finds next branch in childNodes dict
                nextValue = tree.childNodes[value]
                return self.determineState(nextValue,currentExample) #Recursive call
                
            else:
                print("unknown value", value)
                return
        else:
            return tree.action
            


    #Reads file and makes decision tree based on id3
    def makeDecisionTree(self):
        allExamples = []
        allAttributes = []
        filename = "pacman_training_data4.csv"

        with open(filename, newline = "", encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile)
            header = next(reader)
            allAttributes = header[:-1] # all values except last on are attributes
            for row in reader: 
                values = row[:-1]
                action = int (row[-1])
                
                #Converting values. Eiter bool or int
                parsed_values = [value == "True" if value in ["True","False"] else int(value) for value in values]
                allExamples.append(Example(action, parsed_values))
    

    
        tree = DecisionNode()
        makeTree(allExamples, allAttributes, tree)
        tree.print()
        return tree


    # Checks if the closest ghost is closer than some threshold
    def ghostClose(self,distance):
        res = False
        for ghost in self.pacman.ghosts:
          dist = self.pacman.dist(ghost.node.position.asTuple(),self.pacman.position.asTuple())
          if dist < distance:
            res = True
        return res
    
    # Checks if the closest power pellet is closer than some threshold
    def pelletClose(self,distance):
        self.pacman.updatePowerPellets()
        if not self.pacman.powerPellets:
            return False
        
        PP = self.pacman.nearbyPowerPellet()
        dist = self.pacman.dist(PP.position.asTuple(),self.pacman.position.asTuple())
        if dist < distance:
            return True
        return False












        
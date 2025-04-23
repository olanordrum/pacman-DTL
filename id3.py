from math import log2
from typing import Any
import csv

class DecisionNode:
    def __init__(self):
        self.childNodes : dict[str,DecisionNode] = {}  
        self.testValue : str | None = None # Either string or None
        self.possibleValues = [] # All possible values the node can hold
        self.action: int | None = None
        
        
        
    # Recusive function to print the decision tree
    def print(self, level: int = 0):
        space = "  "
        print("\n", space * level, "Level :", level)
        print(space * level, "Test Value :", self.testValue)
        print("Possible Values :", self.possibleValues)
        
        if len(self.childNodes) > 0:
            for attribute in self.childNodes:
                node = self.childNodes[attribute]
                print(space * level, "Attribute : ", attribute)
                node.print(level + 1)
        else:
            print("Leaf Node")
              
                
                
                
class Example: 
    def __init__(self, action: int, values: list[Any]):
        self.action = action # pacman state
        self.values = values #Values of the row
        
        
    def getValue(self, i):
        return self.values[i]
    
    def setValue(self,i, value):
        self.values[i] = value




def makeTree(examples: list[Example], attributes: list [str | None], decisionNode):
    initEntropy = calculateEntropy(examples)
    
    #No entropy -> all examples have same action (leaf)
    if initEntropy <= 0: 
        decisionNode.action = examples[0].action
        return
    
    exampleCount = len(examples)
    
    if all( a is None for a in attributes): #No attributes
        decisionNode.action = examples[0].action
        return
    
    bestInformationGain = 0.0
    bestSplitAttribute = attributes[0]
    attributeIndex = 0
    bestSets = splitByAttribute(examples, attributeIndex)

    for attribute in attributes:
        if attribute is None:
            continue
        
        attributeIndex = attributes.index(attribute)
        sets = splitByAttribute(examples, attributeIndex)
        
        
        overallEntropy = entropyOfSets(sets,exampleCount)
        
        informationGain = initEntropy - overallEntropy
        
        
        if informationGain > bestInformationGain:
            bestInformationGain = informationGain
            bestSplitAttribute = attribute
            bestSets = sets
            
            
        #Start building tree
        decisionNode.testValue = bestSplitAttribute
        bestAttributeIndex = attributes.index(bestSplitAttribute)
        
        decisionNode.possibleValues = []
        
        for example in examples:
            value = example.getValue(bestAttributeIndex)
            if value not in decisionNode.possibleValues:
                decisionNode.possibleValues.append(value)
        
        #Remove used attributes from list to be passed on
        newAttributes = attributes.copy()
        newAttributes[bestAttributeIndex] = None
    
        
        attributeValue = None
        
        for set in bestSets.values():
            attributeValue = set[0].getValue(bestAttributeIndex)
            daughter = DecisionNode()
            decisionNode.childNodes[attributeValue] = daughter

            makeTree(set, newAttributes, daughter)
         
        
        
        
    # Sum of entropy in each group
def splitByAttribute(examples: list[Example], attributeIndex: int):
    sets: dict[Any, list[Example]] = {}
    
    for example in examples:
        value = example.getValue(attributeIndex)
        
        if value in sets:
            sets[value].append(example)
            
        else:
            sets[value] = [example]
            
    return sets
            
            

def entropyOfSets(sets: dict[float, list[Example]], numberOfExamples: int):
    
    entropy = 0.0
    
    for set in sets.values():
        proportion = len(set) / numberOfExamples

        entropy -= proportion * calculateEntropy(set)
        
        
    #Return total entropy
    return entropy 




def calculateEntropy(examples : list[Example]):
    totalCount = len(examples)
    
    if totalCount < 0:
        return 0.0
    
    actionCount : dict[str, int] = {} 
    
    # Counting how many times an action occurs in the dataset
    for example in examples:
        if example.action in actionCount:
            actionCount[example.action] += 1
        else:
            actionCount[example.action] = 1
            
    if len(actionCount) == 0:
        return 0.0
    
    
    # Calculating entropy
    
    entropy = 0.0
    
    for action in actionCount.values():
        proportion = action / totalCount #percentage of this action
        entropy -= proportion * log2(proportion) #Subtracting from the total entropy
        
    return entropy
    
    
    
    
allExamples = []
allAttributes = []
filename = "pacman_training_data.csv"

with open(filename, newline = "", encoding="utf-8") as csvfile:
    reader = csv.reader(csvfile)
    header = next(reader)
    allAttributes = header[:-1] # all values except last on are attributes
    for row in reader: 
        values = row[:-1]
        action = int (row[-1])
        
        #Converting values
        parsed_values = [value == "True" if value in ["True","False"] else int(value) for value in values]
        allExamples.append(Example(action, parsed_values))
    


 
    

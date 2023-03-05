import random


class pubchem:
    """
    Constructor for the pubchem class
    
    @params integer of the pubchem number, An empty list of the foods that have the current pubchem
    @returns None
    """  
    def __init__(self, name, ItemsWith):
        self.name = name
        self.Items = ItemsWith

       
    def getName(self):
        """
        Returns the name of the pubchem
        
        @params 
        @returns String name
        """ 
        return self.name
    
             
    def getCurrentIngredients(self):
        """
        Returns the listof Items that shuld contain a list of all the foods that have the following pubchem
        
        @params none
        @returns None
        """    
        return self.Items


    def add(self, newIngredient):
        """
        Adds the string passed in to the list of foods with the pubchem
        @params string name that will be added to the list
        @returns None
        """ 
        self.Items.append(newIngredient)
     
    def __eq__ (self, other):
        """
        A comparator for the pubchem class
        
        @params string name
        @returns boolean, whether or not the name matches the pubchem
        """     
        if (self.name == other):
            return True
        return self.name == other.name
    
    def __repr__ (self):
        return (self.name + " has " + str(len(self.Items)) + " Foods with the chemical")

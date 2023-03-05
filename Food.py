import random

class Food:
    """
    Constructor for the Food class
    
    @params string name, list of pubchem in strings, string categor of food
    @returns None
    """ 
    def __init__(self, name, items, category):
        self.Listofchem = items
        self.name = name
        self.cat = category
        
                     
    def getList(self):
        """
        Returns the list of pubchems contained inside the food
        
        @params none
        @returns A list of all of the chemicals inside the Food
        """   
        return self.Listofchem
    

    def getName(self):
        """
        Returns the name of the food
        
        @params none
        @returns string of food name
        """  
        return self.name  
       
    def __repr__ (self):
        """
        A toString method for the Food class
           
        @params none
        @returns string name
        """  
        return self.name 
        
        
    def compare(self, otherFood):
        """
        Compares one food to another
        Helps see the similarties in molecular make up
        
        @params instance of food that will be compared
        @returns double, a grade that shows how similar the two moleculars are
        """ 
        original = set(self.Listofchem)     
        try:
            new = set(otherFood.getList())
            numerator = original.intersection(new)
            percent = len(numerator) / len(original)
        except:
            percent = 0
        return percent

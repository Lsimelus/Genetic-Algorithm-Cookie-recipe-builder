import glob
import json
from Pubchem import pubchem
from Food import Food



class Database:
    """
    Constructor Database
    
    Only one instance is created
    @params none
    @returns None
    """  
    def __init__(self):
        self.Fulllist = []
        self.pubBook = {}
        
    def scrape(self):
        """
        Loops through local Json Files containing the dictionaries of each food item
        An instance of the food class is created for every food
        The List of food cakked Fulllist is populated
        
        @params 
        @returns None
        """  
        for filename in glob.glob("JsonFiles/*.json"):
            raw = open(filename, "r")
            data = json.loads(raw.read())
                   
            section = data["molecules"]
            item_name = data["entity_alias_readable"].lower()
            category = data["category_readable"]
                        
            List_of_molecules = []
            for flavor in section:
                for key in flavor:
                    if (key == "pubchem_id"):
                        List_of_molecules.append(flavor[key])    
                        
            CurrentItem = Food(item_name, List_of_molecules, category)
            self.Fulllist.append(CurrentItem)
            self.analyzeIngredients(CurrentItem, List_of_molecules)
     

    def analyzeIngredients(self, wholeIngredient, List_of_molecules):
        """
        Inserts an ingredient into all of the pubchems that it contains
        Before code is ran food is not in any of the pubchem classes


        @params Food item, the newly created food that has. list of pubchem items
        @returns None
        """ 
        for pubchemNum in List_of_molecules:
            if (str(pubchemNum) in self.pubBook):
                temp = self.pubBook[str(pubchemNum)]
                temp.add(wholeIngredient.getName())
            else:
                emptylist = []
                newChem = pubchem(str(pubchemNum), emptylist)
                newChem.add(wholeIngredient.getName())
                self.pubBook[str(pubchemNum)] = newChem
                

    def has(self, moleculestring):
        """
        Returns whether or not a molecule already exists inside the pubchem list
        If the molecule does not exist the pubchem is created then added to the list in another method

        @params string name
        @returns None
        """
        for items in self.pubBook:
            if (items.getName() == moleculestring):
                return -1
        return 0
    


    def get_ingredient(self, food_name):
        """
        @params string name
        @returns None
        """
        ingredient = None
        for item in self.Fulllist:
            if food_name == str(item):
                ingredient = item
        if ingredient is None:
            for item in self.Fulllist:
                if (item.getName() in food_name):
                    ingredient = item
                elif (food_name in item.getName()):
                    ingredient = item
        return ingredient
    

    def get_pubchem(self, pub_string):
        """
        Returns whether or not a molecule already exists inside the pubchem list
        If the molecule does not exist the pubchem is created then added to the list
        
        @params string name
        @returns None
        """
        return self.pubBook[str(pub_string)]
import random
import glob
import json
import urllib.request
import random
from Database import Database
from Recipe import Recipe

 
def main():
    ing = []
    rec = []
    db = Database()
    db.scrape()
    rec = parse_startup(ing, rec, db)    
        
    starter_recipes = randomRecipeGen(rec)
    
    for recipe in starter_recipes:
        for f in recipe.get_foods():
            recipe.delete_none(f)

    num_of_gens = 40
    for x in range(0, num_of_gens):
        rec = generation_production(starter_recipes, db)
        for r in rec:
            random_mutation(r)
            r.gen_new_name()
            
    print("Here is the list of recipes after " + str(num_of_gens) + " generations")
    for items in rec:
        print(items.get_name().title())
        print(items.rate_parity_total())
        print(items.get_foods())
    print()
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("Final recipe:")
    print("-------------")
    nov_rec = []
    for i in rec:
        nov_rec.append(i.rate_parity_avg())
    
    max_nov = rec[nov_rec.index(max(nov_rec))]
    print((max_nov.get_name()).title())
    print(max_nov.rate_parity_total())
    for ing in max_nov.get_foods():
        print((ing.getName()).title())
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")


def parse_startup(ingredients, recipes, database):
    """
    The function that parses the input file for all of the recipes to be used throughout the
    rest of this project. It pulls both data for each recipe in addition to cataloguing all the ingredients found
    in the input folder. 
    @params set ingredients, the set of unique ingredients found in the given input file
    @params list recipes, the list of recipes parsed from the input file 
    @params  db, database with all the food and their chemical compositions
    @returns recipes, the list of recipes for a given run
    """
    infile = open('newcookies2.txt')
    data = infile.readlines()        
    
    count = 0   
    rec_ing = []
    for line in data:
        new_ing = ''
        split_line = line.split()
        if (len(split_line) >= 1 and checkInt(split_line[0][0]) == False):
            if (count != 0):
                for ing in rec_ing:
                    if (ing == None):
                        rec_ing.remove(ing)

                new_recipe = Recipe(recipe_name, database, rec_ing)
                recipes.append(new_recipe)
                rec_ing = []
            recipe_name = ' '.join(split_line)
            count += 1
         
        else:
            if ("/" not in line):
                new_ing = database.get_ingredient(' '.join(split_line[2:]))
                rec_ing.append(new_ing)
                ingredients.append(new_ing)
            elif ("/" in line):
                if (checkInt(split_line[0]) == True):
                    new_ing = database.get_ingredient(' '.join(split_line[3:]))
                else: 
                    new_ing = database.get_ingredient(' '.join(split_line[2:]))
                if (new_ing != None):
                    rec_ing.append(new_ing)
                    ingredients.append(new_ing) 
        
    return recipes


def checkInt(x):
    """
    A helper function for parse_startup(). Basically just checks wehter or not the string value
    from the inputted text file can be converted to an int. If false, this insdicates that 
    it is a string. 
        
    @params x, string being checked
    @return Boolean, true if x can be casted as a string
    """
    try: 
        int(x)
        return True
    except ValueError:
        return False


def randomRecipeGen(recipes):
    """
    A function that cretes the starting generation of recipes by choosing 10 random recuoes from 
    the list of recipes that were created throup parse_startup().
        
    @params recipes, the array of the current population of recipes (Recipe objects)
    @return subsection, a list of 10 recipes that represent the original generation of recipes
    """
    subsection = []
    used_recipes = list(range(0, len(recipes)))
    
    count = 0
    while (count <= 10):
        chosen_rec = random.randint(0, len(recipes))
        if (chosen_rec in used_recipes):
            subsection.append(recipes[chosen_rec])
            count += 1
    return subsection


def generation_production(recipes, db):
    """
    The function that calls the crossover function proportional to the amount of recipes that exist, generating a
    whole new population of recipes (or curret population). 
        
    @params recipes, the array of the current population of recipes (Recipe objects)
            db, database with all the food and their chemical compositions
    @returns new_gen, an array of a new generation of recipes that will replace the originally inputted recipes
    """
    new_gen = [] 
    i = 0
    
    while i < len(recipes):
       
        new_gen.append(crossover(recipes, db))
        i+=1
    return new_gen


def crossover(recipes, db):
    """
    The function that generates a new recipe by combining the first sub-list of the first recipe with the second 
    sub-list of the second recipe, which are chosen based off of their fitness scores.
        
    @params recipes, the array of the current population of recipes (Recipe objects)
            db, database with all the food and their chemical compositions
    @returns new_recipe, a single recipe that was created from two parents of the inputted recipes
    """ 
    empty = []
    new_recipe = Recipe(None, db, empty)
    
    parents_index = choose_recipe(recipes)
    
    first_parent = recipes[parents_index[0]]
    second_parent = recipes[parents_index[1]]    
    
    for i in range(0, min(len(first_parent.get_foods()), len(second_parent.get_foods()))):
    
        if (i == 0 or (i % 2)==0):
            new_recipe.add_food(first_parent.get_foods()[i])
        else: 
            new_recipe.add_food(second_parent.get_foods()[i])
            
    return new_recipe


def choose_recipe(recipes):
    """
    The function that chooses which recipe is the fittest to be the parent of one of the recipes that will
    be apart of the new generation of recipes. The first parent is chosen based off 
    their fitness score of parity, but the second parent is randomized.
        
    @params recipes, the array of the current population of recipes (Recipe objects)
    @return chosen, the recipes who will be used to create a new recipe during crossover
    """
    rec_fs = []
    parents = []
    
    for r in recipes: 
        rec_fs.append(r.rate_parity_avg())
        
    parents.append(rec_fs.index(max(rec_fs)))
    
    second = random.randint(0, len(recipes)-1)
    while (second == parents[0]):
        second = random.randint(0, len(recipes)-1)
    parents.append(second)
    return parents
    
    
def random_mutation(rec):
    """
    Is called on every recipe after it is created
    Has a 20% of creating a mutation
    Every mutation has an equal chance of getting selected
    
    @params List of all of the ingredients
    @returns None
    """   
    type_of_mutation = random.randint(1,15)

    if type_of_mutation == 1:
        rec.mutate_replace_random()

    elif type_of_mutation == 2:
        rec.mutate_add_from_best()
        
    elif type_of_mutation == 3:
        rec.mutate_remove_worst()
main()

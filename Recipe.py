import random
import glob
import json
import urllib.request
import random

class Recipe:
    def __init__(self, name = None, database = None, foods = None):
        self.foods = foods
        self.list_of_chem = []
        for food in self.foods:
            if food is not None:
                self.list_of_chem += list(set(food.getList() + self.list_of_chem))
        self.name = name
        self.recipe_size_lmt = 15
        self.base_foods = ["butter", "sugar", "salt", "vanilla", "egg", "flour"]
        self.database = database
        for food_n in self.base_foods:
            self.add_food_db(food_n)

    
    def get_foods(self):
        """
        Returns the list of ingredients/foods in the recipe

        @returns array, the ingredient list
        """
        return self.foods


    def get_chems(self):
        """
        Returns the list of pubchems in the recipe

        @returns array, the pubchem list
        """
        return self.list_of_chem

    
    def get_name(self):
        """
        Returns the recipe name

        @returns string, recipe name
        """
        return self.name

    
    def get_worst_food(self):
        """
        Returns the worst food/ingredient in the recipe, according to the one that shares the least elements
        with the others

        @returns Food, the least compatible food
        """
        rating_list = []
        least_important = None
        index = 0
        for food in self.foods:
            try:
                if food.getName() in self.base_foods:
                    next
                food_score = 0.0
                for other_food in self.foods:
                    food_score += food.compare(other_food)
                rating_list.append(food_score)
                if least_important is None:
                    least_important = index
                else:
                    if rating_list[least_important] > food_score:
                        least_important = index
            except:
                print()
            finally:
                index += 1
        return self.foods[least_important]


    def get_best_food(self):
        """
        Returns the best food in the recipe, according to the one thats most compatible/
        shares the most elements with the other elements.

        @returns Food, the most compatible food
        """
        rating_list = []
        most_important = None
        index = 0
        for food in self.foods:
            food_score = 0.0
            for other_food in self.foods:
                food_score += food.compare(other_food)
            rating_list.append(food_score)
            if most_important is None:
                most_important = index
            else:
                if rating_list[most_important] < food_score:
                    most_important = index
            index += 1
        return self.foods[most_important]


    def get_best_food_var(self):
        """
        A variant of the get_food function that excludes base food elements from the search

        @returns Food, the most compatible food
        """
        rating_list = []
        most_important = None
        index = 0
        for food in self.foods:
            if food.getName() in self.base_foods:
                next
            food_score = 0.0
            for other_food in self.foods:
                food_score += food.compare(other_food)
            rating_list.append(food_score)
            if most_important is None:
                most_important = index
            else:
                if rating_list[most_important] < food_score:
                    most_important = index
            index += 1
        return self.foods[most_important]


    def add_food(self, new_food):
        """
        Adds a new food to the ingredient list, using an entered food.

        @params Food, new food
        """
        if new_food is not None:
            self.foods.append(new_food)
            self.foods = list(set(self.foods))
            self.list_of_chem = list(set(new_food.getList() + self.list_of_chem))


    def add_food_db(self, food_name):
        """
        Adds a food using an entered food name, that is used to retrieve the cited food
        from the recipe's database, before the food is added to the recipe

        @params string, food name
        """
        new_food = self.database.get_ingredient(food_name)
        self.add_food(new_food)


    def remove_food(self, food_name):
        """
        Removes a food and its relevant pubchems from the recipe using the food's name as
        input

        @params string, food name
        """
        try:
            deleted_food = None
            for food in self.foods:
                
                if food_name  == food.getName():
                    deleted_food = food
                    self.foods.remove(food)
            # removes any molecules that the deleted food has, that none of the remaining foods can account for.
            if deleted_food is not None:
                self.list_of_chem.clear()
                for food in self.foods:
                    self.list_of_chem = list(set(food.getList() + self.list_of_chem))
        except:
                print("Something went wrong")


    def delete_none(self, food):
        """
        A cleanup function that deletes foods with with None values from the ingredient list.
        
        @param Food, food being checked

        """
        if (food == None):
            self.foods.remove(food)


    def check_food(self, food_name):
        """
        Checks whether a given food name is present within the ingredient list.

        @params string, food name
        @returns boolean, whether or not the food is present
        """
        food_present = False
        for food in self.foods:
            if food.getName() == food_name:
                food_present = True
        return food_present


    def rate_parity_total(self):
        """
        Sums the parity total parity of the recipe by iterating through the recipe, and summing
        elements' parities with one another.

        @returns float, the total parity of the recipe
        """
        total_rating = 0
        for food in self.foods:
            food_score = 0.0
            for other_food in self.foods:
                try:
                    food_score += food.compare(other_food)
                except:
                    food_score += 0
            total_rating += food_score
        return total_rating


    def rate_parity_avg(self):
        """
        Returns the average parity, using the length of the ingredient list.

        @returns float, the average parity of the recipe
        """
        return self.rate_parity_total()/len(self.foods)


    def compare_food(self, other_food):
        """
        Compares the pubchem list of the recipe to the pubchems in a given food, returning their parity.

        @params Food, other food
        @returns float, parity/percentage similarity of the two.
        """
        original = set(self.list_of_chem)

        new = set(other_food.getList())
        numerator = original.intersection(new)
        percent = len(numerator) / len(original)
        return percent


    def compare_recipe_foods(self, other_recipe):
        
        """
        Compares the ingredient list of the recipe to the ingredients in another 
        recipe, returning their similarity.

        @params Food, other food
        @returns float, percentage similarity of the two.
        """
        original = set(self.foods)
        new = set(other_recipe.get_foods())
        numerator = original.intersection(new)
        percent = len(numerator) / len(original)
        return percent


    def verify(self):
        """
        A cleanup function that ensures the recipe is at the correct length, and that
        the base ingredients are all present.

        """
        for food_name in self.base_foods:
            if self.check_food(food_name) is False:
                self.add_food_db(food_name)
        while len(self.foods) > self.recipe_size_lmt:
            self.remove_food(self.get_worst_food())


    def mutate_replace_random(self):
        """
        A mutation that replaces a random ingredient in the recipe with another random ingredient,
        based on its pubchem list.

        """
        removed_food_name = "Butter"
        while removed_food_name not in self.base_foods:
            removed_food_name = random.choice(self.foods).getName()
        self.remove_food(removed_food_name)
        rem_food = self.database.get_ingredient(removed_food_name)
        rem_chem_list = rem_food.getList()
        rand_chem = self.database.get_pubchem(random.choice(rem_chem_list))
        new_food_name = random.choice(rand_chem.getCurrentIngredients())
        self.add_food_db(new_food_name)
        self.verify()


    def mutate_add_from_best(self):
        """
        A mutation that adds a new ingredient based on the randomly selecting a linked ingredient
        from the best ingredient's pubchem list.
        """
        rand_best_chem = random.choice(self.get_best_food().getList())
        rand_best_chem = self.database.get_pubchem(rand_best_chem)
        self.add_food_db(random.choice(rand_best_chem.getCurrentIngredients()))
        self.verify()


    def mutate_remove_worst(self):
        """
        A mutation that removes the worst ingredient from the recipe.
        """
        self.remove_food(self.get_worst_food().getName())

    
    def rate_fitness(self, other_recipes):
        """
        A defunct fitness function that decreases total parity based on the highest similarity of the 
        the recipe to a given list of recipes.
        
        @param array, other recipes for checking novelty
        @returns float, final fitness
        """
        strongest_match_parity = 0
        for recipe in other_recipes:
            if self.compare_recipe_foods(recipe) > strongest_match_parity:
                strongest_match_parity = self.compare_recipe_foods(recipe)
        return self.rate_parity_total() - (self.rate_parity_total() * strongest_match_parity)

    
    def gen_new_name(self):
        """
        A function that generates a new name for the recipe.
        """
        adjectives = open("english-adjectives.txt", 'r')
        ends = open("soup-synonyms.txt", 'r')
        adjective_list = []
        ends_list = []
        for adj in adjectives:
            adjective_list.append(adj)
        for end in ends:
            ends_list.append(end)

        new_name = str(random.choice(adjective_list).rstrip()) + " " + str(random.choice(self.foods).getName()) + " & " + str(random.choice(self.foods).getName()) + " " + str(random.choice(ends_list))

        self.name = new_name
        return new_name    
    
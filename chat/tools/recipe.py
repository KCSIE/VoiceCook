from pydantic import BaseModel, Field
from langchain.tools import BaseTool
from typing import Optional, Type

import requests

HF_API_KEY = ""
HF_API_URL = "https://api-inference.huggingface.co/models/flax-community/t5-recipe-generation"

NJ_API_KEY = ""
NJ_API_URL = "https://api.api-ninjas.com/v1/recipe?query={}"

class IngredientsInput(BaseModel):
    """Inputs for recipe_generation"""
    ingredients: str = Field(description="ingredients for generating the recipe, a string like 'ingredient1, ingredient2, ingredient3, ...'")

class RecipeGen(BaseTool):
    name = "recipe_generation"
    description = "useful when you have some ingredients and want to generate a recipe"
    args_schema: Type[BaseModel] = IngredientsInput

    def _run(self, ingredients: str) -> str: 
        response = requests.post(HF_API_URL, headers={"Authorization": f"Bearer {HF_API_KEY}"}, json={"inputs": ingredients}).json()
        recipe = response[0]['generated_text']
        return recipe

class FoodQueryInput(BaseModel):
    """Inputs for recipe_search"""
    food_query: str = Field(description="a specific food's name as the title of recipe, or part of the recipe's title")

class RecipeSearch(BaseTool):
    name = "recipe_search"
    description = "useful when you want to do recipes fuzzy search or full text search based on food's name"
    args_schema: Type[BaseModel] = FoodQueryInput

    def _run(self, food_query: str) -> str: 
        response = requests.get(NJ_API_URL.format(food_query), headers={'X-Api-Key': NJ_API_KEY}).json()
        return str(response[:3])

if __name__ == '__main__':
    # test = RecipeGen()
    # print(test._run("beef, butter, tomato, carrot, cheese"))
    test = RecipeSearch()
    print(test._run("hot wings"))
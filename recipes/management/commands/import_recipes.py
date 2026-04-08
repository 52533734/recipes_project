import csv
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from recipes.models import Recipe, Ingredient


class Command(BaseCommand):
    help = "Import recipes from CSV"

    def handle(self, *args, **kwargs):
        file_path = os.path.join(settings.BASE_DIR, "data", "recipes.csv")

        with open(file_path, newline='', encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
    
                instructions = row["instructions"].replace("; ", "\n")  #convert semicolons to newlines

                recipe = Recipe.objects.create(
                    name=row["name"],
                    cuisine=row["cuisine"],
                    description=row["description"],
                    instructions=instructions
                )

                ingredients_list = row["ingredients"].split(",")

                for ingredient_name in ingredients_list:
                    ingredient, created = Ingredient.objects.get_or_create(
                        name=ingredient_name.strip()
                    )
                    recipe.ingredients.add(ingredient)

        self.stdout.write(self.style.SUCCESS("Recipes imported successfully"))
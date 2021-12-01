with open('input.txt') as file:
    rules = file.read().splitlines()
    foods = []
    for rule in rules:
        aux = rule.split(' (contains ')
        ingredients = set(aux[0].split())
        allergens = set(aux[1][:-1].split(', '))
        foods.append((ingredients, allergens))

    #print(foods)


ingredients_count = {}
possible_allergens = {}

for ingredients, allergens in foods:

    # First, we count the amount of times an ingredient appears in the list
    for ingredient in ingredients:
        if (ingredient in ingredients_count.keys()):
            ingredients_count[ingredient] += 1
        else:
            ingredients_count[ingredient] = 1

    # Then, we create a dict with the allergen as the key and the dict of the posible ingredients containing that allergen as the value
    # If the allergen is not in the dict, we copy all the ingredients that appear on its tuple
    # If appears, we get the union of the values and the ingredients
    for allergen in allergens:
        if (allergen in possible_allergens):
            # &= is the union operator
            possible_allergens[allergen] &= ingredients
        else:
            possible_allergens[allergen] = ingredients.copy()
    

allergic = set()

for ingredient_allergens in possible_allergens.values():
    allergic.update(ingredient_allergens)

#print(ingredients_count)

#print(possible_allergens)

#print(allergic)

total = 0

for ingredient in (ingredients_count.keys() - allergic):
    total += ingredients_count[ingredient]
    #print(ingredients_count[ingredient])

print(total)

#print(ingredients_count.keys() - allergic)

possible = {}

for ingredients, allergens in foods:
    for allergen in allergens:
        if (allergen in possible):
            possible[allergen] &= ingredients
        else:
            possible[allergen] = ingredients.copy()

found = set()

allergen_ingredient = []
while (len(allergen_ingredient) < len(possible.keys())):
    for allergen, ingredients in possible.items():
        if (len(ingredients - found) == 1):
            ingredient = min(ingredients - found)
            allergen_ingredient.append((allergen, ingredient))
            found.add(ingredient)
            break

ingredient_list = ''

for ingredient in sorted(allergen_ingredient):
    ingredient_list += ingredient[1] + ','

print(ingredient_list[:-1])

#print(possible)
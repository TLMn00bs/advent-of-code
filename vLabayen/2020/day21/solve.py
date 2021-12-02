import re

with open('input.txt') as f:
#with open('example.txt') as f:
	foods = [(ingredients.split(' '), allergens.split(', ')) for ingredients,allergens in (re.match('(.*) \(contains (.*)\)', line[:-1]).groups() for line in f)]

	match_options = {}
	for ingredients, allergens in foods:
		for allergen in allergens:
			if allergen not in match_options: match_options[allergen] = []
			match_options[allergen].append(set(ingredients))

	matches = {allergen : set.intersection(*options) for allergen, options in match_options.items()}
	possible_allegen_ingredients = set([ingredient for allergen, ingredients in matches.items() for ingredient in ingredients])

	all_ingredients_raw = [ingredient for ingredients, allergens in foods for ingredient in ingredients]
	all_ingredients = set(all_ingredients_raw)
	non_allegen_ingredients = all_ingredients.difference(possible_allegen_ingredients)

	print(sum(all_ingredients_raw.count(ingredient) for ingredient in non_allegen_ingredients))

	unique_matches = {allergen : ingredients for allergen,ingredients in matches.items()}

	allergen_list = list(sorted(matches, key=lambda k: len(matches[k])))
	removed_allergens = []
	i = 0
	while len(allergen_list) > 0:
		allergen = allergen_list[i]

		for other_allergen in allergen_list[i+1:]:
			unique_matches[other_allergen] = unique_matches[other_allergen].difference(unique_matches[allergen])

		removed_allergens.append(allergen)
		allergen_list = [allergen for allergen in list(sorted(unique_matches, key=lambda k: len(unique_matches[k]))) if allergen not in removed_allergens]

	print(unique_matches)
	print(','.join([list(unique_matches[allergen])[0] for allergen in sorted(unique_matches)]))

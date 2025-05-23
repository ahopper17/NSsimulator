import random
import config

def starting_trait():
    return 1  # Start as slow

def mutate_trait(current_value):
    if random.random() < config.MUTATION_CHANCE:
        if current_value < max(config.POSSIBLE_TRAIT_VALUES):
            return current_value + 1
    return current_value

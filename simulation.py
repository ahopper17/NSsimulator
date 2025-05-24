import config
import random
from organism import Organism
from world import World

#Initialize organism lists
organisms = []
dead_organisms = []

#Create world
world = World(config.WIDTH, config.HEIGHT, config.FOOD_NUMBER)

#Save occupied positions
occupied_positions = set()

def build_organism(x, y, energy):
    trait_name = config.TRAIT_NAME
    mutable_val = config.STARTING_MUTABLE_VALUE
    speed = mutable_val if trait_name == "speed" else 1
    efficiency = mutable_val if trait_name == "efficiency" else 1.0
    return Organism(x, y, speed=speed, energy=energy, efficiency=efficiency)

#Initialize organisms on the grid in random locations
for _ in range(config.NUM_ORGANISMS):
    while True:
        x = random.randint(0, config.WIDTH - 1)
        y = random.randint(0, config.HEIGHT - 1)
        #Check if position occupied, if not place organism
        if (x, y) not in occupied_positions:
            organisms.append(build_organism(x,y, config.STARTING_ENERGY))
            world.place_organism(x, y)
            occupied_positions.add((x, y))
            break

#Get the distribution of the tested trait
def get_trait_distribution(trait_name, possible_values):
    counts = {val: 0 for val in possible_values}
    total = len(organisms)

    for org in organisms:
        value = getattr(org, trait_name)
        if value in counts:
            counts[value] += 1

    return [counts[val] / total if total > 0 else 0 for val in possible_values]


#Run it!
def simulate():
    global organisms, dead_organisms

    #End if all organisms die
    if not organisms:
        return False

    live_organisms = []

    #All organisms will...
    for org in organisms:
        
        #Move and eat
        print(f"Org at ({org.x}, {org.y}) Before move: energy={org.energy}, speed={org.speed}, efficiency={org.efficiency}")
        org.move(world)
        print(f"Org at ({org.x}, {org.y}) After move: energy={org.energy}")

        #Or die.
        if org.check_survival(world):
            world.place_organism(org.x, org.y)

            # Handle reproduction
            offspring = org.reproduce(world)
            if offspring:
                organisms.append(offspring)
                world.place_organism(offspring.x, offspring.y)

            live_organisms.append(org)
        else:
            dead_organisms.append({'x': org.x, 'y': org.y, 'frames_left': config.DEATH_ANIMATION_FRAMES})

    organisms = live_organisms

    #Update dead organism animations
    for corpse in dead_organisms:
        corpse['frames_left'] -= 1
    dead_organisms[:] = [corpse for corpse in dead_organisms if corpse['frames_left'] > 0]

    #Replenish the food sources
    world.replenish_food()

    #Keep going if we have some live organisms
    return True

#Driver when running simulation file
def run():
    for step in range(config.SIMULATION_STEPS):
        if not simulate():
            print(f"Simulation has ended at step {step}.")
            break
        print(f"Step {step}: ")
        for row in world.grid:
            print(row)

if __name__ == "__main__":
    run()
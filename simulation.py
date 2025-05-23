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

#Initialize organisms on the grid in random locations
for _ in range(config.NUM_ORGANISMS):
    while True:
        x = random.randint(0, config.WIDTH - 1)
        y = random.randint(0, config.HEIGHT - 1)
        #Check if position occupied, if not place organism
        if (x, y) not in occupied_positions:
            organisms.append(Organism(x, y, speed=1, energy=config.STARTING_ENERGY))
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
        org.move(world)

        #Or die.
        if org.check_survival(world):
            org.reproduce(world, organisms)
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
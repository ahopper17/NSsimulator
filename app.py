from flask import Flask, render_template, jsonify
from simulation.simulation import simulate, run, organisms, get_trait_distribution, world
from simulation import config


app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/step')
def step():
    alive = simulate()

    # Create blank grids
    grid = [['' for _ in range(config.WIDTH)] for _ in range(config.HEIGHT)]
    food_grid = [[False for _ in range(config.WIDTH)] for _ in range(config.HEIGHT)]

    # Initialize food
    for x in range(config.WIDTH):
        for y in range(config.HEIGHT):
            if world.food[y][x] > 0:
                food_grid[y][x] = True

    # Place organisms into the grid by their position and trait
    for org in organisms:
        grid[org.y][org.x] = str(getattr(org, config.TRAIT_NAME))   

    trait_distribution = get_trait_distribution(config.TRAIT_NAME, 
                                                config.TRAIT_POSSIBLE_VALUES[config.TRAIT_NAME])
    return jsonify({
        'grid': grid,
        'food': food_grid,
        'alive': alive,
        'trait_distribution': trait_distribution
    })

if __name__ == '__main__':
    app.run(debug=True)
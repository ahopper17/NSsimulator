from flask import Flask, render_template, jsonify
from simulation.simulation import simulate, run, organisms, get_trait_distribution
from simulation import config

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/step')
def step():
    alive = simulate()
    grid = [[org.speed for org in organisms]] #grid logic will go here
    trait_distribution = get_trait_distribution(config.TRAIT_NAME, config.MUTATION_CONFIG[config.TRAIT_NAME]["values"])
    return jsonify({
        'grid': grid,
        'alive': alive,
        'trait_distribution': trait_distribution
    })

if __name__ == '__main__':
    app.run(debug=True)
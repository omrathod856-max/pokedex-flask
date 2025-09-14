from flask import Flask, render_template , request
import requests
import random

app = Flask(__name__)
pokedex_url = "https://api.npoint.io/80e109ecf2e6bec2fa29"
all_pkm = requests.get(pokedex_url).json()
selected_pokemon = {}


@app.route('/')
def index():
    return render_template("index.html" ,pokemons=all_pkm)

@app.route('/pokemon/<id>')
def pokemon(id):
    global selected_pokemon
    for pkm in all_pkm:
        if pkm['id'] == int(id):
            selected_pokemon = pkm
            stats = selected_pokemon['stats']
            max_stat = max(stats.values())
            total = selected_pokemon['stats']['hp'] + selected_pokemon['stats']['attack'] + selected_pokemon['stats']['defense'] + selected_pokemon['stats']['special_attack'] + selected_pokemon['stats']['special_defense'] + selected_pokemon['stats']['speed']
    return render_template("details.html" , selected_pokemon=selected_pokemon , total=total , max=max_stat)

@app.route('/my_team/')
def my_team():
    random_team = []
    for i in range(0, 6):
        random_team.append(random.choice(all_pkm))
    return render_template("team.html" , pokemons=random_team)

@app.route("/search")
def search():


    query = request.args.get("q", "").lower()
    results = [pkm for pkm in all_pkm if query in pkm["name"].lower()]
    return render_template("index.html", pokemons=results, query=query)

@app.route("/sort_types")
def sort_types():
    query = request.args.get("t", "").lower()
    results = [pkm for pkm in all_pkm if query in [type.lower() for type in pkm['type']]]
    return render_template("index.html", pokemons=results, query=query)



if __name__ == '__main__':
    app.run(host = "0.0.0.0", port=5000,debug=True)



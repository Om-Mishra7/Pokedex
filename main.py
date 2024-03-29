from flask import Flask, render_template, request, redirect
import requests
import json
from waitress import serve

app = Flask(__name__)

app.secret_key = "BHrTTJ24VkvS7B2pQ15v"
AUTH_HEADER = {"Authorization": "622BEB8354BCDC1C94E1B5B414C66"}


@app.route("/")
def pokemon():
    try:
        if request.args.get("search") == None:
            id = "1"
        else:
            id = request.args.get("search").lower()
            if id.isnumeric():
                if id < "1" or id > "905":
                    id = "1"
        response = requests.get(
            f"https://api.pokemon.project.projectrexa.dedyn.io/pokeapi/{id}",
            headers=AUTH_HEADER,
        )
        data = response.json()

        name = data["name"]
        if data["secondary_type"] == None:
            secondary = "null"
        else:
            secondary = data["secondary_type"]

        if (
            requests.get(
                f"https://img.pokemondb.net/sprites/black-white/anim/normal/{name}.gif"
            ).status_code
        ) == 200:
            link = (
                f"https://img.pokemondb.net/sprites/black-white/anim/normal/{name}.gif"
            )
        else:
            link = f"https://cdn.projectrexa.dedyn.io/pokemon/sprites/{name}.png"

        return render_template(
            "dex.html",
            link=link,
            name=data["name"],
            id=data["id"],
            type_1=data["primary_type"],
            type_2=secondary,
            description=data["description"],
            height=data["height"],
            weight=data["weight"],
            hp=data["hp"],
            attack=data["attack"],
            defence=data["defence"],
            special_attack=data["special_attack"],
            special_defence=data["special_defence"],
            speed=data["speed"],
        )
    except Exception as e:
        print(e)
        return "Not Found"


if __name__ == "__main__":
    app.run(debug=True)

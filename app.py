from flask import Flask, render_template, request, redirect, url_for, session
from back import get_all_stations, get_list_of_equipements, get_all_zdc

app = Flask(__name__)

app.config.from_mapping(SECRET_KEY="dev")  # pour pouvoir utiliser session


# Route principale avec formulaire
@app.route("/", methods=["GET", "POST"])
def form():
    # if request.method == "POST":
    #     # Affiche les données envoyées par le formulaire pour le débogage
    #     print(request.form)  # Vérifie ce qui est envoyé dans le formulaire
    #     # Récupère la valeur soumise par l'utilisateur dans le formulaire
    #     gare = request.form.get("gare")
    #     if gare:  # Si une gare a été choisie
    #         session["gare_choisie"] = gare
    #         return redirect(url_for("about"))
    #     else:
    #         return "Erreur : Aucune gare sélectionnée", 400

    # return render_template("form.html", data=get_all_stations())
    if request.method == "POST":
        session["zdc"] = request.form.get("zdc")
        return redirect(url_for("about"))
    return render_template("form.html", data=get_all_zdc())


# Deuxième route : page "à propos"
@app.route("/about", methods=["GET", "POST"])
def about():
    # On appelle la liste des équipements
    return render_template(
        "station.html", data=get_list_of_equipements(session.get("zdc")).keys()
    )


if __name__ == "__main__":
    app.run(debug=True)

import os
from flask import Flask, flash, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
import psycopg2
import sqlalchemy as db
from web_scrapping import get_elements


app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/' #pour pouvoir utiliser flash methode ()


# C'est très important de garder l'adresse de la BD en toute sécurité, surtout si elle est hébérgé sur un serveur. 
# Bonne Pratique: la définir comme variable d'environement
# sur windows: > $env:DATABASE_URL = "Lien"
# Pour mon cas: > $env:DATABASE_URL = "postgresql://user:password@localhost/subsyy"
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Comment(db.Model):
    
    id = db.Column(db.Integer , primary_key=True)
    comment = db.Column(db.String(200),unique = False)
    customee = db.Column(db.String(200),unique=False)

    def __init__(self, customee, comment):
        
        self.customee = customee
        self.comment = comment

# Tu peux ici créer la table, comme tu peux le faire en ligne de commande :
# >>> from application import db
# >>> db.create_all()   
db.create_all()

# J'ai regroupé les deux fonctions avec les méthodes GET et POST
@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        newcomment = request.form['comment']
        newcustomee = request.form['customee']
        signature = Comment(newcustomee,newcomment)
        db.session.add(signature)
        db.session.commit()
        #Pas mieux qu'un feedback instantané pour l'utilisateur, indiquant que ses données ont été bien ajoutées à la BD, à voir dans home.html comment je l'ai implémenté.
        flash('Votre Commentaire a été bien ajouté, Merci!')
    return render_template('home.html')

#Sraping pour un lien d'un produit amazon pour scraper les reviews {newUser, reviewText}
@app.route('/scrapy', methods=["POST"])
def scrapy_page():
    newURL = request.form['link']
    
    #je fais appel à la fonction get_elements dans le fichier web_scrapping
    newReviews = get_elements(newURL)

    #pour l'affichage je passe la liste obtenue avec le lien à la page scrapy.html
    return render_template('scrapy.html', reviews = newReviews, url = newURL )
    
    return render_template('scrapy.html')

if __name__ =="__main__":
    app.debug=True
    app.run()
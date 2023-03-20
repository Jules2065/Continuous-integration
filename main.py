from flask import *
import time
import threading
import traceback
from gestion_bdd import SqlLogger
from math import floor, ceil
from time import sleep

app = Flask(__name__)



@app.route("/login-page/", methods=['GET', 'POST'])
def login_page():
    print("allo?")
    if request.method == 'POST':
        print("POST")
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
           pass
    return render_template('login-page.html')

@app.route("/create-account", methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        sql_client = SqlLogger()
        if sql_client.connexion():
            try:
                sql_client.ecriture(f"INSERT INTO users VALUES ('{request.form['mail']}', '{request.form['pwd']}', '0', '{request.form['pseudo']}') ")
                return redirect(url_for('login_page'))
            except Exception as e:
                print("Erreur as e : ", e)
            sql_client.deconnexion()
    return render_template('create-account.html')

@app.route("/test/")
def test():
    last_min = True
    nbr_user = 21
    nbr_group = 6
    if last_min:
        while ceil(nbr_user/nbr_group) != (nbr_user - (nbr_group-1) * ceil(nbr_user/nbr_group)) +1:
            nbr_group += 1 
        if nbr_user % nbr_group == 0:
            print(f"total de {nbr_group} groupes")
            print("nombre de personnes dans tous les groupes :", 1)
        else:
            max_nbr_user_group = ceil(nbr_user/nbr_group)
            print(f"total de {nbr_group} groupes")
            print("nombre de personnes dans un groupe simple :", max_nbr_user_group)
            print("nombre de personnes dans le dernier groupe :", nbr_user%max_nbr_user_group)


    else:
        print((nbr_user - (nbr_group-1) * floor(nbr_user/nbr_group)))
        print(floor(nbr_user/nbr_group))
        while (nbr_user - (nbr_group-1) * floor(nbr_user/nbr_group)) != floor(nbr_user/nbr_group) +1 :
            nbr_group +=1
        if nbr_user % nbr_group == 0:
            print(f"total de {nbr_group} groupes")
            print("nombre de personnes dans tous les groupes :", 1)
        else:
            max_nbr_user_group = floor(nbr_user/nbr_group)
            print(f"total de {nbr_group} groupes")
            print("nombre de personnes dans un groupe simple:", max_nbr_user_group)
            print("nombre de personnes dans le dernier groupe :", nbr_user - ((nbr_group-1) * (max_nbr_user_group)))
    return render_template('test.html')  

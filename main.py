from flask import *
import time
import threading
import traceback
from gestion_bdd import SqlLogger
from math import floor, ceil
from time import sleep

app = Flask(__name__)

USERS = ["Tata", "Toto", "Jules", "Idir", "Roger", "Natalie", "Bastien", "Sebastien", "Emilie", "Emile"]


nbr_group = 5
nbr_user = 21
last_min = False
group_list = []
user_list = []
true_nbr_group = 5
user_group = 4
user_group_spe = 5


class Group():
    def __init__(self, name) -> None:
        self.name = name


class User():
    def __init__(self, name, group) -> None:
        self.name = name
        self.group = group



for user in USERS:
    user_list.append(User(user, "Sans groupe"))



@app.route("/login-page/", methods=['GET', 'POST'])
def login_page():
    global user_list
    if request.method == 'POST':
        if request.form['username'] == 'admin':
            #connexion comme utilisateur admin
            return redirect(url_for('main_page_admin'))
        else:
            #connexion comme utilisateur normal
            if request.form['username'] not in USERS:
                USERS.append(request.form['username'])
                user_list.append(User(request.form['username'], None))
            return redirect(url_for('main_page_user'))
    return render_template('login-page.html')

@app.route("/main-page-admin/", methods=['GET', 'POST'])
def main_page_admin():
    global nbr_group
    global nbr_user
    global last_min
    global true_nbr_group
    global group_list

    info = ""
    if request.method == 'POST':
        if request.form['group'] == "":
            nbr_group = 0
        else:
            nbr_group = int(request.form['group'])

        if request.form['user'] == "":
            nbr_user = 0
        else:
            nbr_user = int(request.form['user'])
        
        if request.form['last'] == "":
            last_min = True
        elif request.form['last'] == "lastmin":
            last_min = True
        else:
            last_min = False
    group_list.clear()
    info = calcul_group_user()

    for i in range(true_nbr_group):
        group_list.append(Group(f"Groupe {i+1}"))
    group_list.append(Group("Sans groupe"))
    return render_template('main-page-admin.html', info=info)

@app.route("/main-page-user/", methods=['GET', 'POST'])
def main_page_user():
    global user_list
    global group_list
    info = calcul_group_user()

    
    #Création d'un tableau de dictionnaire pour afficher les groupes sur le site
    print(len(group_list))
    tab = []
    for user in user_list:
        dico = {}
        for group in group_list:
            dico[group.name] = ""
            if user.group == group.name:
                dico[group.name] = user.name
        print("dico")
        tab.append(dico)

    print(tab)
    
    return render_template('main-page-user.html', info=info, tab=tab)




def calcul_group_user():
    global nbr_group
    global nbr_user
    global last_min
    global true_nbr_group
    global user_group
    global user_group_spe
    if nbr_user == 0 or nbr_group == 0:
        info = f"Nombre de groupes maximum = 0 | Nombre de personnes par groupes = 0"
        true_nbr_group = 0
        user_group = 0
        user_group_spe = 0
    else:
        if nbr_user % nbr_group == 0:
            info = f"Nombre de groupes maximum = {nbr_group} | Nombre de personnes par groupes = {int(nbr_user/nbr_group)}"
            true_nbr_group = nbr_group
            user_group = int(nbr_user/nbr_group)
            user_group_spe = 0
        else:
            if last_min:
                while ceil(nbr_user/nbr_group) != (nbr_user - (nbr_group-1) * ceil(nbr_user/nbr_group)) +1:
                    nbr_group += 1 
                if nbr_user % nbr_group == 0:
                    info = f"Nombre de groupes maximum = {nbr_group} | Nombre de personnes par groupes = 1"
                    true_nbr_group = nbr_group
                    user_group = 1
                    user_group_spe = 0

                else:
                    max_nbr_user_group = ceil(nbr_user/nbr_group)
                    info = f"Nombre de groupes maximum = {nbr_group} | Nombre de personnes par groupes simples = {max_nbr_user_group} | Nombre de personnes dans le dernier groupe = {nbr_user%max_nbr_user_group}"
                    true_nbr_group = nbr_group
                    user_group = max_nbr_user_group
                    user_group_spe = nbr_user%max_nbr_user_group

            else:
                while (nbr_user - (nbr_group-1) * floor(nbr_user/nbr_group)) != floor(nbr_user/nbr_group) +1 :
                    nbr_group +=1
                if nbr_user % nbr_group == 0:
                    info = f"Nombre de groupes maximum = {nbr_group} | Nombre de personnes par groupes = 1"
                    true_nbr_group = nbr_group
                    user_group = 1
                    user_group_spe = 0
                else:
                    max_nbr_user_group = floor(nbr_user/nbr_group)
                    info = f"Nombre de groupes maximum = {nbr_group} | Nombre de personnes par groupes simples = {max_nbr_user_group} | Nombre de personnes dans le dernier groupe = {nbr_user - ((nbr_group-1) * (max_nbr_user_group))}"
                    true_nbr_group = nbr_group
                    user_group = max_nbr_user_group
                    user_group_spe = nbr_user - ((nbr_group-1) * (max_nbr_user_group))
    return info
info = calcul_group_user()
print("info :", info)
print('true_nbr_group :', true_nbr_group)
for i in range(true_nbr_group):
    group_list.append(Group(f"Groupe {i+1}"))
group_list.append(Group("Sans groupe"))

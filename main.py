from flask import *
import time
import threading
import traceback
from math import floor, ceil
from time import sleep
from itsdangerous.url_safe import URLSafeTimedSerializer as Serializer
from random import choice

app = Flask(__name__)
app.secret_key = 'BAD_SECRET_KEY'


USERS = ["Tata", "Toto", "Jules", "Idir", "Roger", "Natalie", "Bastien", "Sebastien", "Emilie", "Emile"]


nbr_group = 5
nbr_user = 21
last_min = False
group_list = []
user_list = []
true_nbr_group = 5
user_group = 4
user_group_spe = 5
link_invite=""
erreur=""


class Group():
    def __init__(self, name, number, max_user_number) -> None:
        self.name = name
        self.number = number
        self.nbr_user = 0
        self.max_user_number = max_user_number

    def groupFull(self):
        if self.nbr_user < self.max_user_number:
            return True
        return False
                




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
        session["user"] = request.form['username']
        if request.form['username'] == 'admin':
            #connexion comme utilisateur admin
            return redirect(url_for('main_page_admin'))
        else:
            #connexion comme utilisateur normal
            if request.form['username'] not in USERS:
                USERS.append(request.form['username'])
                user_list.append(User(request.form['username'], "Sans groupe"))
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
    calcul_group_user(nbr_group, nbr_user, last_min)

    group_list.append(Group("Sans groupe", 0, 0))
    return render_template('main-page-admin.html', info=session["user"])

@app.route("/main-page-user/", methods=['GET', 'POST'])
def main_page_user():
    global user_list
    global group_list
    global erreur
    global link_invite
    global nbr_group
    global nbr_user
    global last_min
    info = calcul_group_user(nbr_group, nbr_user, last_min)

    
    #Création d'un tableau de dictionnaire pour afficher les groupes sur le site
    tab = []
    for user in user_list:
        dico = {}
        for group in group_list:
            dico[group.name] = "" 
            if user.group == group.name:
                dico[group.name] = user.name
        tab.append(dico)

    
    return render_template('main-page-user.html', info=session["user"], tab=tab, link_invite=link_invite, erreur=erreur)




def calcul_group_user(nbr_group, nbr_user, last_min):
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

@app.route("/place-random/", methods=['GET', 'POST'])
def place_random():
    global link_invite
    global group_list
    global true_nbr_group
    global erreur
    groupes_possibles = []
    if len(group_list) > 1:
        user_inst = None
        group_inst = None
        for user in user_list:
            if session["user"] == user.name:
                user_inst = user
        #Déterminer quels groupes peuvent être pris puis lancer un random entre tous
        for group in group_list:
            if not group.groupFull():
                groupes_possibles.append(group)
        chosen_group = choice(groupes_possibles)
        print("rand :", chosen_group)
        if user_inst.group == "Sans groupe":
            chosen_group.nbr_user += 1
            user_inst.group = chosen_group.name
        else:
            erreur = "Vous appartenez déjà à un groupe"   
    else:
        erreur = "Aucun groupe n'a été créé"     
    return redirect(url_for('main_page_user'))

@app.route("/create-invite/", methods=['GET', 'POST'])
def create_invite():
    global link_invite
    global group_list
    global true_nbr_group
    global erreur
    global user_group
    global user_group_spe
    
    if len(group_list) < true_nbr_group:
        user_inst = None
        for user in user_list:
            if session["user"] == user.name:
                user_inst = user
        if user_inst.group == "Sans groupe":
            group_nbr_user = user_group
            #Vérifie si le groupe est le dernier
            if len(group_list) == true_nbr_group-1:
                group_nbr_user = user_group_spe
            group_name = f"Groupe {len(group_list)}"
            group_list.append(Group(group_name, len(group_list)), group_nbr_user)
            group_list[-1].nbr_user += 1
            user_inst.group = group_list[-1].name
            url_for('invite', group_name=group_name)
            link_invite=f"localhost:5000/{group_name}/invite"
        else:
            erreur = "Vous appartenez déjà à un groupe"
        
    return redirect(url_for('main_page_user'))

@app.route('/<group_name>/invite', methods=['GET', 'POST'])
def invite(group_name):
    global group_list
    global user_list
    global erreur
    global last_min
    global user_group
    global user_group_spe
    global true_nbr_group
    global nbr_group
    global nbr_user
    print("Groupe name :", group_name)
    user_inst = None
    for user in user_list:
        if session["user"] == user.name:
            user_inst = user
    if user_inst.group == "Sans groupe":
        for group in group_list:
            if group.name == group_name:
                max_nbr_user = 0
                if group.number == true_nbr_group:
                    max_nbr_user = user_group_spe
                else:
                    max_nbr_user = user_group
                
                if group.nbr_user < max_nbr_user:
                    group.nbr_user += 1
                    user_inst.group = group.name

                
                else:
                    erreur = f"Impossible de rejoindre le groupe {group_name} : Il est complet."
    else:
        erreur = "Vous appartenez déjà à un groupe"
                
            
    return redirect(url_for('main_page_user'))


info = calcul_group_user(nbr_group, nbr_user, last_min)
group_list.append(Group("Sans groupe", 0, 0))

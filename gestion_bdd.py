from http import client
import re
from datetime import datetime
import mysql.connector
import traceback


class SqlLogger:
    def __init__(self, host="localhost", user="root", password="", database="continuous_integration", port=3306):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port
        self.connexion_ok = False
        self.session = None

    def connexion(self):
        # try:
            #connexion à la base de données locales
            self.session = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                port=self.port,
                database=self.database
            )
            self.session.autocommit = True
            self.connexion_ok = True
            return True
        # except Exception as e:
        #     self.connexion_ok = False
        # return False
        
    def deconnexion(self):
        try:
            self.session.close()
        except:
            pass
    def ecriture(self, requete, backup = None):
        """
        Tente une ecriture sur la base de données principale et, si une base de données de backup est passée en paramètres, écrit également dans celle ci.
        """
        
        if self.connexion_ok:
            print("Eculé de ta radce")
            if self.session.is_connected():
                print("Eculé de ta radce")
                with self.session.cursor() as c:
                    c.execute(requete)
                    c.close()
                
            else:
                self.connexion_ok = False

                
    def lecture(self, requete, backup = None):
        """
        Tente une lecture sur la base de données principale.
        En cas d'échec, si une base de données de backup est passée en paramètres, celle ci sera interrogée.
        """
        if self.connexion_ok:
            if self.session.is_connected():
                try:
                    with self.session.cursor() as c:
                        c.execute(requete)
                        res = c.fetchall()
                        c.close()
                        return res
                except Exception as e:
                    pass
            else:
                if self.connexion_ok:
                    self.connexion_ok = False


        
        return None

class DatabaseNotConnected(Exception):
    def __init__(self):
        super().__init__("La base de donnée n'est pas connectée")
class NoDatabaseAvailable(Exception):
    def __init__(self, database_name):
        super().__init__("Pas de bases de données disponibles pour " + database_name)
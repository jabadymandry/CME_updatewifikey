# Updatewifikey Cisco Mobility Express : Changement automatiquement de la clé wifi des AP.

- **Fonctionnalité:**
    - Connexion sur Cisco Mobility Express controler 
    
    - Recupère les ssid à modifier le mot de passe
    
    - Génère un mot de passe aléatoire
    
    - Applique le mot de passe comme clé wifi depuis le controlleur
    
    - Met à jour un fichier excel googlesheet partagé avec les utilisateurs ayant accès au fichier.
    
- **Requirements:**
    - Python 3.x. Testé sur version Python 3.7.6
    - module python à installer: gspread, oauth2client, netmiko, pyasn1-modules,loguru
    - Accès en mode ecriture de l'utilisateur utilisé par le script representé dans le fichier json

- **Installation:**
    - Deploiement les codes sur un serveur
    - Créer un cron pour le déclanchement


- **Configuration:**
Le fichier de configuration de l'application se trouve dans /etc/updatewifikey/wifi.conf dont le contenu est le suivant:

#### Section Googlesheet [GOOGLE]
*- Crédentials que j'ai créer pour pouvoir editer le fichier*

**google_credentials = 3531b0eefab4.json**

*- id du fichier sheet recuperer sur l'url du fichier*

**google_sheet_id = 0XnZkjvgkq4M9H6Pmwru6JO3i-ULvq1w**

*- Adresse du controlleur Unifi*

**controller = 192.168.1.250**

*- Utilisateur sur le controlleur avec permission d'edition*

**username = username                                                
password = password**

#### Section Wifi [WIFI]
*- Liste de wifi à modifier séparé par virgule la clé: exemple: ssid = ETE-CONF,SU-Staff*

**ssid = ETE-CONF**

*- Site auxquels sont rattaché les AP séparé par virgule. Par defaut "default"*

**site = default**

*- Les même sssid auront -il le même mot de passe ou non? Il est possible d'avoir le même ssid sur deux ou plusieurs sites différent auxquels il est possible de mettre le même clé ou clé différent.*

**cle_unique = yes**

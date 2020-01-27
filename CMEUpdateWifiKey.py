try:
    import configparser
except:
    import ConfigParser
    
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from CMEController import CMEController
import json


def clearGoogleSheet(google_credentials, google_sheet_id):
    """
    Vider le googlesheet et retourner l'instance du sheet pour mise a jour
    Ajout en tete du tableau
     _______________________
    | WIFI SSID | WIFI KEY  |
    ------------------------
    | ETE-CONF  | $#Nma$#dz |
    -------------------------
    """
    # Definition de credentials pour acces API Google
    credentials = google_credentials
    # Definition scope
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(credentials, scope)
    client = gspread.authorize(creds)
    # Googlesheet a editer
    GoogleSheet_Id = google_sheet_id
    # Ouvrir googlesheet avec ID
    sheet = client.open_by_key(GoogleSheet_Id).sheet1
    sheet.clear()
    sheet.insert_row(["WIFI - SSID", "WIFI - KEY"],1)
    return sheet


def updateGoogleSheet(sheet, data):
    """
    Mise a jour Tableur google sheet en respectant le modele ci-dessous
    """
    #print("Mise a jour googlesheet")
    data = json.loads(data)
    data_in_file = sheet.get_all_values()
    #print("Nombre de lignes dans le fichier: {0}".format(len(data_in_file)))
    #for d in data_in_file:
    #    print(d)
    sheet.insert_row([str(data['ssid']), str(data['key'])], len(data_in_file)+1)

try:
    configFile = "CMEWifi.conf"
    parametre = configparser.ConfigParser()
    parametre.read(configFile)
    controller = parametre['WIFI']['controller']
    username =  parametre['CREDENTIALS']['username']
    password = parametre['CREDENTIALS']['password']
    controller = CMEController(controller,username, password)
    controller.connecter()
    if parametre['WIFI']['cle_unique'] == "yes":
        if controller._session != None:
            gsheet = clearGoogleSheet(parametre['GOOGLE']['google_credentials'], parametre['GOOGLE']['google_sheet_id'])
            wifi_config = json.loads(controller.getWifiConfig())
            for wifi_name in parametre['WIFI']['ssid'].split(','):
                print(wifi_name)
                for wifi in wifi_config:
                    print(wifi)
                    if wifi_name == wifi['Wlan_ssid']:
                        wifi_key = controller.generatePassword()
                        id_wifi = wifi['Wlan_id']
                        commands = ["config wlan disable {0}".format(id_wifi),
                        "config wlan security wpa akm psk set-key ascii {0} {1}".format(wifi_key,id_wifi), 
                        "config wlan enable {0}".format(id_wifi)]
                        print(wifi_key)
                        for cmd in commands:
                            print(controller.exucuterCommande(cmd))
                        sheet_data = json.dumps({'ssid': wifi_name, 'key': wifi_key})
                        updateGoogleSheet(gsheet, sheet_data)
        else:
            print("Erreur de connexion sur le controleur")
            raise "Connexion error"
    else:
        print("Le mode cle unique avec Cisco Mobility Express. yes")
except Exception as error:
    print('Une erreur s\'est produite: {0}'.format(error))
    raise error
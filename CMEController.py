import netmiko
from loguru import logger
import sys
import json
import re
import string
import random


logger.add("logs/log_{time:YYYY-MM-DD}.log",
    format="{time} {level} {message}",
    filter="client",
    level="INFO")

logger.add('logs/log_err_{time:YYYY-MM-DD}.log',
    filter="client",
    level="ERROR")

class CMEController(object):
    """
    Lecture et Ecriture configuration Cisco Mobility Express Controller
    By Bruno Enee <brunoenee@gmail.com>
    16/01/2020
    """

    def __init__(self, controller, username, password, port=22):
        """
        Constructeur et initialisation des variables
        """
        self._controller = controller
        self._username = username
        self._password = password
        self._port = port
        self._session = None

    def connecter(self):
        """
        Connexion sur le controleur des Access Points
        """
        try:
            print("Connexion sur : {0}".format(self._controller))
            self._session = netmiko.ConnectHandler(ip = self._controller,
                            username = self._username,
                            password = self._password,
                            device_type = 'cisco_wlc_ssh')
            if self._session != None:
                logger.info("Connexion [OK]")
            else:
                raise "Connexion [OK]"
        except netmiko.NetMikoAuthenticationException as error:
            logger.info('Authentication failed: Check your credentials!')
            logger.error(error)
            raise error
        finally:
            return self._session

    def deconnecter(self):
        """
        Fermeture de la session SSH sur le controleur
        """
        self._session.close()

    def exucuterCommande(self, cmd):
        """
        Executer une commande sur le controleur Cisco Mobility Express
        """
        if self._session is None:
            self._session = self.connecter()

        print("Execution commande: {0}".format(cmd))
        result = self._session.send_command(cmd)
        return result

    def getWifiConfig(self):
        """
        Recupere la sortie de la commande "show wlan summary" et converti en json
        """
        pattern = "^[1-9][0-9]*"
        regex  = re.compile(pattern)
        wifi = []
        stdout = self.exucuterCommande("show wlan summary")
        for line in stdout.splitlines():
            if regex.search(line):
                wifi.append({
                    'Wlan_id': line.split()[0],
                    'Wlan_profile': line.split()[1],
                    'Wlan_ssid': line.split()[3],
                    'Status': line.split()[4],
                    'Interface_name': line.split()[5]
                })
        return json.dumps(wifi)

    def generatePassword(self, passwd_length=9):
        """
        Generate random password of fixed lenght default 9
        """
        lettres = string.ascii_letters
        chiffres = string.digits
        special_chars = "@!#$"
        pass_chars = lettres+chiffres+special_chars
        password = ''.join(random.choice(pass_chars) for i in range(passwd_length))
        return password

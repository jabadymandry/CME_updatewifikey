#!/usr/bin/python
import configparser
import os

chemin = os.path.abspath('.')
file = os.path.join(chemin,"inventory")

fic = open("section_inventory.txt",'w')
config = configparser.ConfigParser()
config.read(file)
for section in config.sections():
    print("Section : {0}".format(section))
    fic.write(section+"\n")

fic.close()




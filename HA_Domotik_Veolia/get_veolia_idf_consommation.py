from selenium import webdriver
import http.cookiejar
import urllib
import os
import sys
import time
import csv
import logging
from logging.handlers import RotatingFileHandler
from pyvirtualdisplay import Display

# Configuration des logs
logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')
file_handler = RotatingFileHandler('veolia.log', 'a', 1000000, 1)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
steam_handler = logging.StreamHandler()
steam_handler.setLevel(logging.INFO)
steam_handler.setFormatter(formatter)
logger.addHandler(steam_handler)

#URL des pages nécessaires
urlHome = 'https://espace-client.vedif.eau.veolia.fr/s/login/'
urlConso = 'https://espace-client.vedif.eau.veolia.fr/s/historique'

#Informations de connexion
veolia_login = 'sebastien.puteanus@free.fr'
veolia_password = 'genetique77;'

#Emplacement de sauvegarde du fichier à télécharger
downloadPath = '/opt/External_Tools/veolia/'
downloadFile = downloadPath + 'historique_jours_litres.csv'

options = webdriver.FirefoxOptions()
options.add_argument('-headless')
options.add_argument("--no-sandbox")

#Démarre l'affichage virtuel
display = Display(visible=0, size=(800, 600))
display.start()

profile = webdriver.FirefoxProfile()
options = webdriver.FirefoxOptions()
options.headless = True
profile.set_preference('browser.download.folderList', 2)
profile.set_preference('browser.download.manager.showWhenStarting', False)
profile.set_preference('browser.download.dir', downloadPath)
profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'text/csv')

#Bien indiquer l'emplacement de geckodriver
browser = webdriver.Firefox(firefox_profile=profile, options=options, executable_path='/usr/local/bin/geckodriver', service_log_path='/opt/External_Tools/veolia/geckodriver.log')

logger.info('Page de login')
browser.get(('https://espace-client.vedif.eau.veolia.fr/s/login/'))
browser.implicitly_wait(10)

# Recherche et remplis les champs d'identification
idEmail = browser.find_element_by_id('input-3')
idPassword = browser.find_element_by_css_selector('input[type="password"]')

idEmail.clear()
idEmail.send_keys(veolia_login)
time.sleep(3)

idPassword.clear()
idPassword.send_keys(veolia_password)
time.sleep(3)

loginButton = browser.find_element_by_class_name('submit-button')
loginButton.click()
time.sleep(2)

logger.info('Page de consommation')
browser.get(urlConso)
time.sleep(15)

# cherche boutons  Jours et Litres
Btns=browser.find_elements_by_xpath(".//c-icl-button-stateful")

for Btn in Btns:
    #print(Btn.find_element_by_xpath('.//span').text)
    if (Btn.find_element_by_xpath('.//span').text=="Conso"):
        Btn.click()
        time.sleep(3)
 
    if (Btn.find_element_by_xpath('.//span').text=="Jours"):
        Btn.click()
        time.sleep(3)
    if (Btn.find_element_by_xpath('.//span').text=="Litres"):
        Btn.click()
        time.sleep(3)

logger.info('Téléchargement du fichier Consommation en Litres par jours')
downloadFileButton = browser.find_element_by_class_name("slds-button.slds-text-title_caps")
downloadFileButton.click()


for Btn in Btns:
    #print(Btn.find_element_by_xpath('.//span').text)
    if (Btn.find_element_by_xpath('.//span').text=="Conso"):
        Btn.click()
        time.sleep(3)

    if (Btn.find_element_by_xpath('.//span').text=="Jours"):
        Btn.click()
        time.sleep(3)
    if (Btn.find_element_by_xpath('.//span').text=="Euros €"):
        Btn.click()
        time.sleep(3)

logger.info('Téléchargement du fichier Prix en €uros par Jours')
downloadFileButton = browser.find_element_by_class_name("slds-button.slds-text-title_caps")
downloadFileButton.click()


browser.close()

display.stop()

logger.info('Fichier:' + downloadFile)

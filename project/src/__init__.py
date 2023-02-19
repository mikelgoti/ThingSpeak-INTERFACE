from selenium.webdriver.firefox.options import Options
from selenium import webdriver
import requests
import time
import os
import json
import openpyxl


from .utils import Utils
from .thingspeak import ThingSpeak
from .canal import Canal
from .hardware import subir_datos_practica
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.keys import Keys
import time
import os
from dotenv import load_dotenv
load_dotenv()

# Configurar opciones de Edge
edge_options = Options()
edge_options.add_experimental_option("detach", True)  # Mantiene el navegador abierto

browser = webdriver.Edge(options=edge_options)
browser.implicitly_wait(10)
browser.get("https://github.com/")

wait = WebDriverWait(browser, 10)
link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Sign in")))
link.click()

GITHUB_USER = os.getenv("GITHUB_USER")
GITHUB_PASS = os.getenv("GITHUB_PASS")

user_input = browser.find_element(By.ID,"login_field")
pass_input = browser.find_element(By.ID,"password")

user_input.send_keys(GITHUB_USER)#user del env
pass_input.send_keys(GITHUB_PASS)# pass del env
pass_input.send_keys(Keys.RETURN)

time.sleep(3)

# Navegar al perfil
browser.get("https://github.com/settings/profile")

# Esperar a que cargue la pagina del perfil
wait.until(EC.presence_of_element_located((By.ID, "user_profile_name")))

# Extraer información del perfil
try:
    # Nombre del perfil
    profile_name = browser.find_element(By.ID, "user_profile_name").get_attribute("value")
    print(f"Nombre del perfil: {profile_name}")
    
    # Email público (si está disponible)
    try:
        email_element = browser.find_element(By.ID, "user_profile_email")
        email = email_element.get_attribute("value")
        print(f"Email público: {email}")
    except:
        print("Email público: No disponible")
    
    # Bio
    try:
        bio_element = browser.find_element(By.ID, "user_profile_bio")
        bio = bio_element.get_attribute("value")
        print(f"Bio: {bio}")
    except:
        print("Bio: No disponible")
    
    # Ubicación
    try:
        location_element = browser.find_element(By.ID, "user_profile_location")
        location = location_element.get_attribute("value")
        print(f"Ubicación: {location}")
    except:
        print("Ubicación: No disponible")
    
    # Website
    try:
        website_element = browser.find_element(By.ID, "user_profile_blog")
        website = website_element.get_attribute("value")
        print(f"Website: {website}")
    except:
        print("Website: No disponible")
        
except Exception as e:
    print(f"Error al obtener información del perfil: {e}")
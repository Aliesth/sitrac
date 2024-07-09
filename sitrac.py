from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver import Keys
from selenium.common import NoSuchElementException, ElementNotInteractableException, TimeoutException
import time
from selenium.webdriver.support import expected_conditions as EC

with open("C:\\Correos\\SITRAC\\listaRetencion.txt", "r", encoding='utf-8') as file:
    lineas = file.readlines()

driver = webdriver.Chrome() 
options = webdriver.ChromeOptions()
options.add_argument('--start-maximization')
options.add_argument('--disable-extensions')
driver.set_window_position(2000,0)
driver.maximize_window()    
driver.implicitly_wait(4)
driver.get('http://sitrac.correos.cl/')
driver.refresh()

revealed = driver.find_element(By.NAME, 'Usuario')
errors = [NoSuchElementException, ElementNotInteractableException]
wait = WebDriverWait(driver, timeout=60, ignored_exceptions=errors) 
wait.until(lambda d : revealed.send_keys('17414130-4') or True)
driver.find_element(By.NAME,'Clave').send_keys('dana2701')
driver.find_element(By.NAME,'Clave').send_keys(Keys.ENTER)

buttonEscaner = wait.until(EC.element_to_be_clickable((By.ID, 'escaner')))
buttonEscaner.click()

buttonRevisionEscaner = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div[2]/div/nav/div/ul[1]/li[3]/div/a')))
buttonRevisionEscaner.click()

contador = 0

for linea in lineas:
    codigo = linea.strip() 
    try:
        loading_spinner = driver.find_elements(By.XPATH, '//i[contains(@class, "fa-spinner")]')
        if loading_spinner:
            wait.until(EC.invisibility_of_element_located((By.XPATH, '//i[contains(@class, "fa-spinner")]')))
    except TimeoutException:
        print("El spinner sigue siendo visible después del tiempo esperado. Terminando la ejecución.")
        break
    
    codigo_input = driver.find_element(By.NAME, 'Codigo')
    codigo_input.clear()
    codigo_input.send_keys(codigo)
    wait.until(EC.presence_of_element_located((By.NAME, 'Codigo')))
    wait.until(EC.element_to_be_clickable((By.NAME, 'Codigo')))
    codigo_input.send_keys(Keys.ENTER)

    print(f"Procesando envío número {contador}: {codigo}")  
    contador += 1  

    boton_aceptar_presente = EC.presence_of_element_located((By.XPATH, '/html/body/div[4]/div/div/div[3]/button[1]'))
    if wait.until(boton_aceptar_presente, 5):
        try:
            boton_aceptar = driver.find_element(By.XPATH, '/html/body/div[4]/div/div/div[3]/button[1]')
            boton_aceptar.click()
            print("El envío presenta precarga de documentos.")
        except NoSuchElementException:
            print("Sin precarga de documentos.")
            pass
        except ElementNotInteractableException:
            print("Sin precarga de documentos.")
            pass

time.sleep(5)

driver.quit()
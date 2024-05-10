from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.common.exceptions import NoSuchElementException 

remote_debugging_port = 9222

chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress",f"localhost:{remote_debugging_port}")

chrome_driver_path = ChromeDriverManager().install()
service = Service(executable_path=chrome_driver_path)
navegador = webdriver.Chrome(service=service, options=chrome_options)

def localizar_elemento_XPATH(caminhoElemento):
        while not None:
                try:
                        elemento = navegador.find_element(By.XPATH, caminhoElemento)
                        print("elemento encontrado")
                        return elemento
                
                except NoSuchElementException:
                        time.sleep(0.1)
                        print("elemento não encontrado")
                return None


# ao colocar o caminho do elemento coloque sempre em aspas simples ('')
elemento = localizar_elemento_XPATH('teste')


#if elemento: elemento.click()
if elemento: elemento.send_keys("123_teste")
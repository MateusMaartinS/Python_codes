from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
import os
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select




# start chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\Selenium\ChromeTestProfile"
def iniciar_navegador(com_debugging_remoto=True):
    chrome_driver_path = ChromeDriverManager().install()
    chrome_driver_executable = os.path.join(os.path.dirname(chrome_driver_path), 'chromedriver.exe')
    
    #print(f"ChromeDriver path: {chrome_driver_executable}")
    if not os.path.isfile(chrome_driver_executable):
        raise FileNotFoundError(f"O ChromeDriver não foi encontrado em {chrome_driver_executable}")

    service = Service(executable_path=chrome_driver_executable)
    
    chrome_options = Options()
    if com_debugging_remoto:
        remote_debugging_port = 9222
        chrome_options.add_experimental_option("debuggerAddress", f"localhost:{remote_debugging_port}")
    
    navegador = webdriver.Chrome(service=service, options=chrome_options)
    return navegador

navegador = iniciar_navegador(com_debugging_remoto=True)


# aguardar pagina carregar
WebDriverWait(navegador, 90).until(lambda navegador: navegador.execute_script('return document.readyState') == 'complete')

# aguardar elemento carregar
#                                                visibility_of_element_located
elemento = WebDriverWait(navegador, 15).until(EC.presence_of_element_located(
                    (By.XPATH, 'exemplo')))

# elemento do tipo select
anoElement = navegador.find_element(By.XPATH, 'lista')
Select_element = Select(anoElement)

for i in range(10):
    Select_element.select_by_index(i)
    selecao = Select_element.options[i].text
    print(f"selecionado {selecao}")

#trocar de iframe
navegador.switch_to.default_content()
iframe = navegador.find_element(By.XPATH, 'iframe Pagina')
navegador.switch_to.frame(iframe)

xpath = navegador.find_element(By.XPATH, 'iframe Pagina')


'''
o exeucute_script é ate simples de usar
nesse caso ele esta achando o argumento value q esta la no xpath, e esta trocando ele para o arguments[1], que nesse caso é o '2019'
após o ; ele esta definindo que o texto que esta sendo visivel ira receber o arguments[2] que é Dois Mil e Dezenove

então ele vai trocar o valor para 2019 e o texto visivel para Dois Mil e Dezenove
''' 

navegador.execute_script("arguments[0].value = arguments[1]; arguments[0].innerText = arguments[2];", xpath, '2019', 'Dois Mil e Dezenove')


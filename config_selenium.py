from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# configurações para entrar no navegador já istanciado a partir do comando:
# start chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\Selenium\ChromeTestProfile"

remote_debugging_port = 9222

chorme_options = Options()
chorme_options.add_experimental_option("debuggerAddress",f"localhost:{remote_debugging_port}")

chrome_driver_path = ChromeDriverManager().install()
service = Service(executable_path=chrome_driver_path)
navegador = webdriver.Chrome(service=service, options=chorme_options)
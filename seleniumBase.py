import os
import time
import subprocess
import requests
from typing import Optional
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from webdriver_manager.core.os_manager import ChromeType
import tempfile


class ChromeNaoIniciadoError(Exception):
    """Levantada quando não foi possível abrir/anexar ao Chrome de automação (modo debug remoto)."""
    pass


class SeleniumBase:
    def __init__(self, debuggingRemoto: bool = True, porta: int = 9222,
                 pastaPerfilDebug: Optional[str] = None):
        self.debuggingRemoto = debuggingRemoto
        self.porta = porta
        # Perfil persistente usado pelo Chrome de automação (modo debug remoto).
        # Fica fixo em disco de propósito: é o que permite reaproveitar o login
        # (certificado + captcha) entre execuções, sem precisar logar de novo toda hora.
        self.pastaPerfilDebug = pastaPerfilDebug or r"C:\Selenium\ChromeTestProfile"
        self.driver: Optional[webdriver.Chrome] = None

    def startChrome(self) -> webdriver.Chrome:
        print("debuggingRemoto:", self.debuggingRemoto)
        chromeDriverPath = ChromeDriverManager().install()
        pasta_downloads = os.path.abspath(os.path.join(os.path.dirname(__file__),"..","downloads"))
        os.makedirs(pasta_downloads, exist_ok=True)

        if not chromeDriverPath.endswith('chromedriver.exe'):
            chromeDriverExecutable = os.path.join(os.path.dirname(chromeDriverPath), 'chromedriver.exe')
        else:
            chromeDriverExecutable = chromeDriverPath

        if not os.path.isfile(chromeDriverExecutable):
            raise FileNotFoundError(f"ChromeDriver não encontrado em: {chromeDriverExecutable}")

        service = Service(executable_path=chromeDriverExecutable)
        chromeOptions = Options()

        if self.debuggingRemoto:
            # ── Modo automação com login manual: garante que exista um Chrome
            # com debug remoto na porta configurada (abre um se precisar) e
            # então anexa o Selenium nele ────────────────────────────────────
            self._iniciarChromeDebug()
            chromeOptions.add_experimental_option("debuggerAddress", f"localhost:{self.porta}")
            self.driver = webdriver.Chrome(service=service, options=chromeOptions)

        else:

            # Perfil isolado para o Selenium (evita conflito com Chrome aberto)
            pasta_perfil = os.path.abspath(os.path.join(os.path.dirname(__file__),"..","SeleniumProfile"))
            os.makedirs(pasta_perfil, exist_ok=True)

            # -- Headless --
            chromeOptions.add_argument("--headless=new")
            chromeOptions.add_argument("--start-maximized")
            chromeOptions.add_argument("--window-size=1920,1080")
            chromeOptions.add_argument("--disable-gpu")
            chromeOptions.add_argument("--no-sandbox")
            chromeOptions.add_argument("--disable-dev-shm-usage")
            chromeOptions.add_argument("--disable-extensions")
            chromeOptions.add_argument("--log-level=3")

            pasta_perfil = tempfile.mkdtemp(
                prefix="selenium_profile_"
            )

            chromeOptions.add_argument(
                f"--user-data-dir={pasta_perfil}"
            )
            #chromeOptions.add_argument(f"--user-data-dir={pasta_perfil}")

            # -- Camuflagem anti-bot --
            chromeOptions.add_argument("--disable-blink-features=AutomationControlled")
            chromeOptions.add_argument(
                "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/136.0.0.0 Safari/537.36"
            )
            chromeOptions.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
            chromeOptions.add_experimental_option("useAutomationExtension", False)

            # -- Preferências de download --
            prefs = {
                "download.default_directory": pasta_downloads,
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                "safebrowsing.enabled": True,
                "profile.default_content_setting_values.automatic_downloads": 1,
            }
            chromeOptions.add_experimental_option("prefs", prefs)

            self.driver = webdriver.Chrome(service=service, options=chromeOptions)

            # Remove a flag webdriver do navigator (anti-bot extra)
            self.driver.execute_cdp_cmd(
                "Page.addScriptToEvaluateOnNewDocument",
                {"source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"}
            )

            # Libera o download via CDP com caminho absoluto
            self.driver.execute_cdp_cmd(
                "Page.setDownloadBehavior",
                {"behavior": "allow", "downloadPath": pasta_downloads}
            )

            print(f"Downloads configurados em: {pasta_downloads}")

        return self.driver

    def endChrome(self):
        """Fecha o navegador se não estiver em modo debug."""
        if self.driver and not self.debuggingRemoto:
            self.driver.quit()

    # ── Chrome em modo debug remoto (login manual) ─────────────────────────────

    def _debugPortAtiva(self, timeout: float = 2) -> bool:
        """Verifica se já existe um Chrome escutando na porta de debug configurada."""
        try:
            resposta = requests.get(f"http://localhost:{self.porta}/json/version", timeout=timeout)
            return resposta.status_code == 200
        except requests.exceptions.RequestException:
            return False

    def _localizarChromeExe(self) -> str:
        """Localiza o executável do Chrome instalado na máquina."""
        caminhosPossiveis = [
            os.path.join(os.environ.get("PROGRAMFILES", r"C:\Program Files"),
                         "Google", "Chrome", "Application", "chrome.exe"),
            os.path.join(os.environ.get("PROGRAMFILES(X86)", r"C:\Program Files (x86)"),
                         "Google", "Chrome", "Application", "chrome.exe"),
            os.path.join(os.environ.get("LOCALAPPDATA", ""),
                         "Google", "Chrome", "Application", "chrome.exe"),
        ]
        for caminho in caminhosPossiveis:
            if caminho and os.path.isfile(caminho):
                return caminho

        try:
            import winreg
            with winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE,
                r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\chrome.exe"
            ) as chave:
                caminho, _ = winreg.QueryValueEx(chave, None)
                if caminho and os.path.isfile(caminho):
                    return caminho
        except Exception:
            pass

        raise ChromeNaoIniciadoError(
            "Não foi possível localizar o chrome.exe instalado nesta máquina."
        )

    def _iniciarChromeDebug(self, timeoutEspera: int = 30):
        """
        Garante que exista um Chrome com debug remoto na porta configurada.
        Se já houver um (ex: de uma execução anterior, possivelmente já logado),
        reaproveita. Caso contrário, abre um novo processo de Chrome com
        --remote-debugging-port e --user-data-dir, e aguarda ele ficar disponível.
        """
        if self._debugPortAtiva():
            print(f"Chrome de automação já está aberto na porta {self.porta}, reaproveitando sessão/login.")
            return

        chromeExe = self._localizarChromeExe()
        os.makedirs(self.pastaPerfilDebug, exist_ok=True)

        comando = [
            chromeExe,
            f"--remote-debugging-port={self.porta}",
            f"--user-data-dir={self.pastaPerfilDebug}",
            "--remote-allow-origins=*",  # necessário em Chrome recentes p/ o Selenium anexar via CDP
            "--no-first-run",
            "--no-default-browser-check",
        ]

        print(f"Abrindo Chrome de automação (perfil: {self.pastaPerfilDebug}, porta: {self.porta})...")
        flagsCriacao = 0
        if os.name == "nt":
            # Desacopla o Chrome do processo Python: se a automação/API cair,
            # o navegador (e a sessão logada) continua de pé.
            flagsCriacao = subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP

        subprocess.Popen(comando, creationflags=flagsCriacao, close_fds=True)

        tempo = 0
        while tempo < timeoutEspera:
            if self._debugPortAtiva():
                time.sleep(1)  # pequena folga para a primeira aba terminar de montar
                return
            time.sleep(1)
            tempo += 1

        raise ChromeNaoIniciadoError(
            f"O Chrome não respondeu na porta {self.porta} após {timeoutEspera}s."
        )

    # ── Espera de página e elementos ──────────────────────────────────────────

    def pageLoad(self, timeout: int = 90):
        """Aguarda o documento HTML estar completamente carregado."""
        WebDriverWait(self.driver, timeout).until(
            lambda d: d.execute_script('return document.readyState') == 'complete'
        )

    def elementLoadManipulate(self, locator: tuple, timeout: int = 15, type: int = 1):
        """
        Aguarda e retorna um elemento.
        type 1 = presence | type 2 = visibility | type 3 = clickable
        """
        match type:
            case 1:
                return WebDriverWait(self.driver, timeout).until(
                    EC.presence_of_element_located(locator)
                )
            case 2:
                return WebDriverWait(self.driver, timeout).until(
                    EC.visibility_of_element_located(locator)
                )
            case 3:
                return WebDriverWait(self.driver, timeout).until(
                    EC.element_to_be_clickable(locator)
                )

    def findElements(self, locator: tuple) -> list:
        """Retorna todos os elementos que casam com o locator."""
        return self.driver.find_elements(*locator)

    # ── Cliques ───────────────────────────────────────────────────────────────

    def clickWithRetry(self, locator: tuple, tentativas: int = 3, espera: float = 1.5, quantidadeCliques: int = 1):
        """Clica com retry automático. Suporta clique simples, duplo ou N vezes."""
        for i in range(tentativas):
            try:
                elemento = self.elementLoadManipulate(locator, type=3)
                self.pageScroll(action='element', element=elemento)
                time.sleep(0.3)

                if quantidadeCliques == 1:
                    elemento.click()
                elif quantidadeCliques == 2:
                    ActionChains(self.driver).double_click(elemento).perform()
                else:
                    for _ in range(quantidadeCliques):
                        elemento.click()
                        time.sleep(0.1)
                return

            except Exception as e:
                if i == tentativas - 1:
                    raise
                print(f"[Retry {i+1}/{tentativas}] Falha ao clicar: {e}")
                time.sleep(espera)

    def clickByIndex(self, locator, index):
        elementos = self.findElements(locator)

        if index >= len(elementos):
            raise Exception(
                f"Índice {index} não encontrado. "
                f"Foram encontrados apenas {len(elementos)} elementos."
            )

        elemento = elementos[index]
        self.pageScroll(action="element", element=elemento)
        elemento.click()

    def clickByText(self, locator: tuple, texto: str):
        """Clica no primeiro elemento cujo texto seja exatamente igual ao passado."""
        elementos = self.findElements(locator)
        for elemento in elementos:
            if elemento.text.strip() == texto:
                elemento.click()
                return
        raise Exception(f"Elemento com texto '{texto}' não encontrado.")

    def clickJS(self, locator: tuple):
        """Clica via JavaScript — útil quando o clique normal é bloqueado por overlay."""
        elemento = self.elementLoadManipulate(locator, type=3)
        self.driver.execute_script("arguments[0].click();", elemento)

    def rightClick(self, locator: tuple):
        """Clique com botão direito (abre menu de contexto)."""
        elemento = self.elementLoadManipulate(locator, type=3)
        ActionChains(self.driver).context_click(elemento).perform()

    # ── Digitação ─────────────────────────────────────────────────────────────

    def sendKeys(self, locator: tuple, texto: str, clear: bool = True):
        """
        Digita em um campo de input.
        clear=True limpa o campo antes de digitar (padrão).
        """
        elemento = self.elementLoadManipulate(locator, type=3)
        if clear:
            elemento.clear()
        elemento.send_keys(texto)

    def sendKeysAction(self, locator: tuple, texto: str, clear: bool = True):

        elemento = self.elementLoadManipulate(locator, type=3)
        if clear:
            elemento.clear()
        elemento.send_keys(texto)
        ActionChains(self.driver).move_to_element(elemento).double_click(elemento).send_keys(texto).perform()

    # ── Interações especiais ──────────────────────────────────────────────────

    def hover(self, locator: tuple):
        """Move o mouse para cima do elemento sem clicar."""
        elemento = self.elementLoadManipulate(locator)
        ActionChains(self.driver).move_to_element(elemento).perform()

    def dropdownIndex(self, locator: tuple, index: int) -> str:
        """Seleciona uma opção de <select> pelo índice e retorna o texto selecionado."""
        elemento = self.elementLoadManipulate(locator)
        selectElement = Select(elemento)
        selectElement.select_by_index(index)
        return selectElement.options[index].text

    def executeScript(self, locator: tuple, valor: str, texto_visivel: str):
        """Injeta valor via JavaScript — útil para campos com máscara."""
        elemento = self.elementLoadManipulate(locator)
        self.driver.execute_script(
            "arguments[0].value = arguments[1]; arguments[0].innerText = arguments[2];",
            elemento, valor, texto_visivel
        )

    # ── Iframe ────────────────────────────────────────────────────────────────

    def iframeParten(self):
        """Volta para o escopo principal saindo de qualquer iframe."""
        self.driver.switch_to.default_content()

    def iframeAlternate(self, locator: tuple):
        """Muda o contexto para dentro de um iframe específico."""
        iframe = self.elementLoadManipulate(locator)
        self.driver.switch_to.frame(iframe)

    # ── Scroll ────────────────────────────────────────────────────────────────

    def pageScroll(self, action: str, pixels: int = 0, element=None):
        """
        Scroll da página inteira.
        Ações: 'bottom' | 'top' | 'down' | 'up' | 'element'
        """
        match action.lower():
            case 'bottom':
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            case 'top':
                self.driver.execute_script("window.scrollTo(0, 0);")
            case 'down':
                self.driver.execute_script(f"window.scrollBy(0, {pixels});")
            case 'up':
                self.driver.execute_script(f"window.scrollBy(0, -{pixels});")
            case 'element':
                if element is None:
                    raise ValueError("Para 'element', passe o objeto no parâmetro 'element'.")
                self.driver.execute_script(
                    "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
                    element
                )
            case _:
                raise ValueError(f"Ação '{action}' inválida.")

    def containerScroll(self, locator: tuple, action: str, pixels: int = 0):
        """
        Scroll de containers internos (divs, textareas, etc).
        Ações: 'bottom' | 'top' | 'down' | 'up'
        """
        elemento = self.elementLoadManipulate(locator)
        match action.lower():
            case 'bottom':
                self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight;", elemento)
            case 'top':
                self.driver.execute_script("arguments[0].scrollTop = 0;", elemento)
            case 'down':
                self.driver.execute_script("arguments[0].scrollTop += arguments[1];", elemento, pixels)
            case 'up':
                self.driver.execute_script("arguments[0].scrollTop -= arguments[1];", elemento, pixels)
            case _:
                raise ValueError(f"Ação '{action}' inválida.")

    # ── Debug ─────────────────────────────────────────────────────────────────

    def salvarScreenshot(self, nome: str = "debug"):
        """Salva screenshot — essencial para depurar no headless."""
        caminho = os.path.abspath(f"{nome}.png")
        self.driver.save_screenshot(caminho)
        print(f"Screenshot salvo: {caminho}")

    def switchTab(self, index: int):
        self.driver.switch_to.window(
            self.driver.window_handles[index]
        )

    def closeTab(self):
        self.driver.close()

    def closeCurrentTab(self):
        self.driver.close()

        if self.driver.window_handles:
            self.driver.switch_to.window(
                self.driver.window_handles[-1]
            )

    def waitNewTab(self, timeout: int = 10):
        abasAtuais = len(
            self.driver.window_handles
        )

        WebDriverWait(
            self.driver,
            timeout
        ).until(
            lambda d: len(d.window_handles)
            > abasAtuais
        )
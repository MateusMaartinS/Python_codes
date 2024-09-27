from subprocess import Popen
from pywinauto import Desktop
import time

Popen('calc.exe',shell=True)

app = Desktop(backend='uia').window(title='Calculadora')

#app.print_control_identifiers()

app.child_window(title="Um", control_type="Button").click_input()
time.sleep(1)

app.child_window(title="Mais", control_type="Button").click_input()
time.sleep(1)

app.child_window(title="Um", control_type="Button").click_input()
time.sleep(1)

app.child_window(title="Igual a", control_type="Button").click_input()
time.sleep(1)

resultado = app.child_window(auto_id="CalculatorResults", control_type="Text").window_text()
print(resultado)

app.close()
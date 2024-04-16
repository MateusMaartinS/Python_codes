import qrcode
from PIL import Image
from pyzbar.pyzbar import decode as lerqr


# Método para a criação do QRcode (retirado da documentacao)
qr = qrcode.QRCode(version=1,error_correction=qrcode.constants.ERROR_CORRECT_L,box_size=10,border=4,)
qr.add_data('https://www.linkedin.com/in/mateus-martins-da-silva-379008177/')
qr.make(fit=True)

img = qr.make_image(fill_color="black", back_color="white")
img.save('testeQR.png')


# Método para extrair a informacao do QRcode
imagem_qr = lerqr(Image.open('testeQR.png'))

#print(imagem_qr)
print(imagem_qr[0].data.decode("utf-8"))
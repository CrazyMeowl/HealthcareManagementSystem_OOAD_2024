import qrcode
import base64
from io import BytesIO

def generate_qr_code_base64(data):
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_H)
    qr.add_data(data)
    qr.make(fit=True)

    buffered = BytesIO()
    img = qr.make_image(fill='black', back_color='white')
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")
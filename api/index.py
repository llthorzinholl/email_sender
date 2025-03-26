from flask import Flask, request, render_template
from email.message import EmailMessage
import os
import smtplib

app = Flask(__name__, template_folder="../templates", static_folder="../static")
UPLOAD_FOLDER = "/tmp"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        imagem = request.files["imagem"]
        if imagem:
            caminho = os.path.join(UPLOAD_FOLDER, imagem.filename)
            imagem.save(caminho)
            enviar_email_com_anexo(caminho)
            return "Imagem enviada com sucesso!"
    return render_template("index.html")

def enviar_email_com_anexo(caminho_arquivo):
    remetente = os.environ.get("EMAIL_REMETENTE")
    senha = os.environ.get("EMAIL_SENHA")
    destinatario = os.environ.get("EMAIL_DESTINO")

    msg = EmailMessage()
    msg['Subject'] = 'Imagem enviada automaticamente'
    msg['From'] = remetente
    msg['To'] = destinatario
    msg.set_content('Segue imagem em anexo.')

    with open(caminho_arquivo, 'rb') as f:
        msg.add_attachment(f.read(), maintype='image', subtype='jpeg', filename=os.path.basename(caminho_arquivo))

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(remetente, senha)
        smtp.send_message(msg)

# Exporte o app como "app" (Vercel usa isso internamente)
app = app

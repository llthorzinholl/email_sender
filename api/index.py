from flask import Flask, request, render_template, redirect, url_for
from email.message import EmailMessage
from datetime import datetime
import pytz
import os
import smtplib

app = Flask(__name__, template_folder="../templates", static_folder="../static")
UPLOAD_FOLDER = "/tmp"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        nome = request.form.get("nome")
        imagens = []

        # Captura imagens da câmera
        fotos_camera = request.files.getlist("fotos_camera")
        for imagem in fotos_camera:
            if imagem and imagem.filename:
                caminho = os.path.join(UPLOAD_FOLDER, imagem.filename)
                imagem.save(caminho)
                imagens.append(caminho)

        # Captura imagens opcionais
        fotos_opcionais = request.files.getlist("fotos_opcionais")
        for imagem in fotos_opcionais:
            if imagem and imagem.filename:
                caminho = os.path.join(UPLOAD_FOLDER, imagem.filename)
                imagem.save(caminho)
                imagens.append(caminho)

        # Envia todas as imagens por e-mail
        for caminho in imagens:
            enviar_email_com_anexo(caminho, nome)

        return redirect(url_for("index"))

    return render_template("index.html")



def enviar_email_com_anexo(caminho_arquivo, nome):
    remetente = os.environ.get("EMAIL_REMETENTE")
    senha = os.environ.get("EMAIL_SENHA")
    destinatario = os.environ.get("EMAIL_DESTINO")

    fuso_aus = pytz.timezone("Australia/Sydney")
    agora_aus = datetime.now(fuso_aus)
    data_hoje = agora_aus.strftime("%B").strip() + f" {agora_aus.day}"

    msg = EmailMessage()
    msg['Subject'] = f"Timesheet {nome} - {data_hoje}"
    msg['From'] = remetente
    msg['To'] = destinatario
    msg.set_content(
        f"In attachment, you will find the timesheet for {data_hoje} sent by {nome}. "
        "Let me know if you have any questions."
    )

    with open(caminho_arquivo, 'rb') as f:
        msg.add_attachment(f.read(), maintype='image', subtype='jpeg', filename=os.path.basename(caminho_arquivo))

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(remetente, senha)
        smtp.send_message(msg)

# Vercel precisa disso
app = app

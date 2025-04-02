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
        imagem_camera = request.files.get("foto_camera")
        imagem_arquivo = request.files.get("arquivo_opcional")

        imagens = []

        if imagem_camera:
            caminho = os.path.join(UPLOAD_FOLDER, imagem_camera.filename)
            imagem_camera.save(caminho)
            imagens.append(caminho)

        if imagem_arquivo and imagem_arquivo.filename:
            caminho_opcional = os.path.join(UPLOAD_FOLDER, imagem_arquivo.filename)
            imagem_arquivo.save(caminho_opcional)
            imagens.append(caminho_opcional)

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

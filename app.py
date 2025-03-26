import os
import smtplib
from flask import Flask, request, render_template, send_from_directory, redirect, url_for
from email.message import EmailMessage

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
EMAIL_DESTINO = 'twofng@gmail.com'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

HTML_FORM = '''
    <h2>Tirar foto e enviar por e-mail</h2>
<form method="POST" enctype="multipart/form-data">
    <input type="file" name="imagem" accept="image/*" capture="environment" required>
    <br><br>
    <button type="submit">Tirar foto / Enviar</button>
</form>
'''

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        imagem = request.files["imagem"]
        if imagem:
            caminho = os.path.join(UPLOAD_FOLDER, imagem.filename)
            imagem.save(caminho)
            enviar_email_com_anexo(caminho)

        return redirect(url_for("index"))

    return render_template("index.html")

def enviar_email_com_anexo(para, caminho_arquivo):
    remetente = 'ghsilva2895@gmail.com'
    senha = 'wzpi sdgn onff qqjx'  # Use senha de app do Gmail, não sua senha normal

    msg = EmailMessage()
    msg['Subject'] = 'Imagem enviada automaticamente'
    msg['From'] = remetente
    msg['To'] = para
    msg.set_content('Segue imagem em anexo.')

    with open(caminho_arquivo, 'rb') as f:
        conteudo = f.read()
        nome_arquivo = os.path.basename(caminho_arquivo)
        msg.add_attachment(conteudo, maintype='image', subtype='jpeg', filename=nome_arquivo)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(remetente, senha)
        smtp.send_message(msg)

if __name__ == '__main__':
    app.run(debug=True)
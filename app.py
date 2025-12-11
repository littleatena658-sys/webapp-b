from flask import Flask, render_template_string, request
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)

HTML_FORM = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Formulário - WebApp B</title>
</head>
<body>
    <h1>Formulário - WebApp B</h1>
    <form method="POST" action="/enviar">
        <label>Seu nome:</label><br>
        <input type="text" name="nome" required><br><br>

        <label>Seu email:</label><br>
        <input type="email" name="email" required><br><br>

        <label>Mensagem:</label><br>
        <textarea name="mensagem" required></textarea><br><br>

        <button type="submit">Enviar</button>
    </form>
</body>
</html>
"""

HTML_SUCESSO = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Enviado!</title>
</head>
<body>
    <h1>Mensagem enviada com sucesso!</h1>
    <p>Obrigado por enviar sua mensagem.</p>
</body>
</html>
"""


# CONFIGURAR SEU E-MAIL AQUI
SMTP_EMAIL = "SEU_EMAIL_AQUI"
SMTP_PASSWORD = "SUA_SENHA_DE_APLICATIVO_AQUI"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587


@app.route("/")
def index():
    return render_template_string(HTML_FORM)


@app.route("/enviar", methods=["POST"])
def enviar():
    nome = request.form["nome"]
    email = request.form["email"]
    mensagem = request.form["mensagem"]

    # Conteúdo do e-mail
    corpo_email = f"""
    Nova mensagem enviada pelo formulário (WebApp B):

    Nome: {nome}
    Email: {email}
    Mensagem:
    {mensagem}
    """

    msg = MIMEText(corpo_email)
    msg["Subject"] = "Nova mensagem do formulário"
    msg["From"] = SMTP_EMAIL
    msg["To"] = SMTP_EMAIL  # envia para você mesmo

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_EMAIL, SMTP_PASSWORD)
            server.send_message(msg)
        return render_template_string(HTML_SUCESSO)

    except Exception as e:
        return f"Erro ao enviar email: {e}"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

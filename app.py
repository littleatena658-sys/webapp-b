import os
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
<style>
    body {
        margin: 0;
        padding: 0;
        font-family: Arial, Helvetica, sans-serif;
        background: linear-gradient(135deg, #e74a3b, #f6c23e);
        height: 100vh;
        display: flex;
        justify-content: center;
        align-items: center;
    }
    .card {
        background: white;
        padding: 30px;
        width: 350px;
        border-radius: 12px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.2);
        text-align: center;
    }
    h1 {
        margin-bottom: 20px;
        color: #e74a3b;
    }
    input, textarea {
        width: 100%;
        padding: 10px;
        margin: 8px 0;
        border-radius: 6px;
        border: 1px solid #ccc;
        font-size: 16px;
    }
    button {
        width: 100%;
        padding: 12px;
        margin-top: 10px;
        background: #e74a3b;
        color: white;
        border: none;
        border-radius: 6px;
        font-size: 18px;
        cursor: pointer;
        transition: 0.2s;
    }
    button:hover {
        background: #c0392b;
    }
</style>
</head>
<body>
    <div class="card">
        <h1>WebApp B</h1>
        <form method="POST" action="/enviar">
            <input type="text" name="nome" placeholder="Seu nome" required>
            <input type="email" name="email" placeholder="Seu e-mail" required>
            <textarea name="mensagem" placeholder="Sua mensagem" rows="4" required></textarea>
            <button type="submit">Enviar</button>
        </form>
    </div>
</body>
</html>
"""

HTML_SUCESSO = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Sucesso!</title>
<style>
    body {
        font-family: Arial, Helvetica, sans-serif;
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
        background: #f8f9fc;
        margin: 0;
    }
    .card {
        background: white;
        text-align: center;
        padding: 40px;
        border-radius: 12px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.15);
    }
    h1 {
        color: #1cc88a;
    }
</style>
</head>
<body>
    <div class="card">
        <h1>Mensagem enviada!</h1>
        <p>Obrigado pelo contato.</p>
    </div>
</body>
</html>
"""

# 🔐 SEGURANÇA: Pegando variáveis de ambiente
SMTP_EMAIL = os.environ.get("SMTP_EMAIL")
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD")
SMTP_SERVER = "smtp.office365.com"
SMTP_PORT = 587


@app.route("/")
def index():
    return render_template_string(HTML_FORM)


@app.route("/enviar", methods=["POST"])
def enviar():
    nome = request.form["nome"]
    email = request.form["email"]
    mensagem = request.form["mensagem"]

    corpo_email = f"""
    Nova mensagem enviada pelo formulário (WebApp B):

    Nome: {nome}
    Email: {email}
    Mensagem:
    {mensagem}
    """

    msg = MIMEText(corpo_email)
    msg["Subject"] = "Nova mensagem do formulário (WebApp B)"
    msg["From"] = SMTP_EMAIL
    msg["To"] = SMTP_EMAIL

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

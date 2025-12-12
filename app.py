import os
from flask import Flask, render_template_string, request
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

app = Flask(__name__)

HTML_FORM = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Contato – WebApp B</title>

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
        padding: 35px;
        width: 380px;
        border-radius: 14px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.25);
        text-align: center;
    }
    h1 {
        margin-bottom: 20px;
        color: #e74a3b;
        font-size: 26px;
    }
    input, textarea {
        width: 100%;
        padding: 12px;
        margin: 8px 0;
        border-radius: 7px;
        border: 1px solid #ccc;
        font-size: 15px;
    }
    button {
        width: 100%;
        padding: 14px;
        margin-top: 10px;
        background: #e74a3b;
        color: white;
        border: none;
        border-radius: 7px;
        font-size: 18px;
        cursor: pointer;
        transition: 0.2s;
    }
    button:hover { background: #c0392b; }
</style>

</head>
<body>
  <div class="card">
    <h1>WebApp B – Contact Form</h1>
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
<title>Mensagem enviada</title>

<style>
    body {
        margin: 0;
        padding: 0;
        font-family: Arial, Helvetica, sans-serif;
        background: #f8f9fc;
        height: 100vh;
        display: flex;
        justify-content: center;
        align-items: center;
    }
    .box {
        background: white;
        padding: 45px;
        border-radius: 14px;
        text-align: center;
        box-shadow: 0 8px 25px rgba(0,0,0,0.18);
    }
    h1 { color: #1cc88a; }
</style>

</head>
<body>
  <div class="box">
    <h1>Mensagem enviada com sucesso!</h1>
    <p>Obrigado pelo contato. Retornaremos em breve.</p>
  </div>
</body>
</html>
"""

SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY")
EMAIL_SENDER = os.environ.get("EMAIL_SENDER")

@app.route("/")
def index():
    return render_template_string(HTML_FORM)

@app.route("/enviar", methods=["POST"])
def enviar():
    if not SENDGRID_API_KEY or not EMAIL_SENDER:
        return "Erro: SENDGRID_API_KEY ou EMAIL_SENDER não configurados.", 500

    nome = request.form["nome"]
    email_usuario = request.form["email"]
    mensagem = request.form["mensagem"]

    # ----- Email para VOCÊ -----
    subject_admin = "Nova mensagem (WebApp B)"
    content_admin = f"""
    Nova mensagem recebida via WebApp B:

    Nome: {nome}
    Email: {email_usuario}

    Mensagem:
    {mensagem}
    """

    msg_admin = Mail(
        from_email=EMAIL_SENDER,
        to_emails=EMAIL_SENDER,
        subject=subject_admin,
        plain_text_content=content_admin
    )

    # ----- Email para USUÁRIO -----
    subject_user = "Recebemos sua mensagem – WebApp B"
    content_user = f"""
Olá, {nome}!

Obrigado por entrar em contacto. Aqui está uma cópia da sua mensagem:

"{mensagem}"

Nossa equipa irá analisar e responder o mais rapidamente possível.

Atenciosamente,  
WebApp B
"""

    msg_user = Mail(
        from_email=EMAIL_SENDER,
        to_emails=email_usuario,
        subject=subject_user,
        plain_text_content=content_user
    )

    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        sg.send(msg_admin)
        sg.send(msg_user)
        return render_template_string(HTML_SUCESSO)
    except Exception as e:
        return f"Erro ao enviar via SendGrid: {e}", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

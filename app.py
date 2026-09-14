from flask import Flask, render_template, request
from crypto_system import encrypt_message, decrypt_token

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/encrypt", methods=["GET", "POST"])
def encrypt():
    secure_token = None
    error = None
    if request.method == "POST":
        message = request.form.get("message", "").strip()
        if not message:
            error = "Please enter a message to encrypt."
        else:
            secure_token = encrypt_message(message)
    return render_template("encrypt.html", secure_token=secure_token, error=error)

@app.route("/decrypt", methods=["GET", "POST"])
def decrypt():
    decrypted_message = None
    error = None
    if request.method == "POST":
        token = request.form.get("secure_token", "").strip()
        if not token:
            error = "Please enter the secure token."
        else:
            success, result = decrypt_token(token)
            if success:
                decrypted_message = result
            else:
                error = result
    return render_template("decrypt.html", decrypted_message=decrypted_message, error=error)

if __name__ == "__main__":
    app.run(debug=True)

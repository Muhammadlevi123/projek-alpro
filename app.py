from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def dashboard():
    return render_template("index.html")

@app.route("/kasir")
def orders():
    return render_template("kasir.html")

# @app.route("/photo-salons")
# def photo_salons():
#     return render_template("photo_salons.html")

# @app.route("/users")
# def users():
#     return render_template("users.html")

# @app.route("/requests")
# def requests():
#     return render_template("requests.html")

# @app.route("/billing")
# def billing():
#     return render_template("billing.html")

if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
# ⚠️ WICHTIG: Ersetze den String durch einen echten zufälligen Secret Key
app.secret_key = "7f1e8b3d41c8e4a997e3b6a48f2f9cdd"

# Ordner für Bilder
IMAGE_FOLDER = "static/images"
os.makedirs(IMAGE_FOLDER, exist_ok=True)

# --------------------
# Startseite (Username & Profilbild)
# --------------------
@app.route("/", methods=["GET", "POST"])
def index():
    # Profilbilder: nur die, die "profilepic" im Namen haben
    profilepics = [f for f in os.listdir(IMAGE_FOLDER) if "profilepic" in f]

    if request.method == "POST":
        session["username"] = request.form.get("username", "user123")
        session["profilepic"] = request.form.get("profilepic", profilepics[0])

        # Bedingungen & Bildmodus aus URL übernehmen
        session["p"] = request.args.get("p", "1")  # 1=selfies, 2=neutral
        session["cond"] = request.args.get("c", "i")  # i=inclusion, e=exclusion

        return redirect(url_for("select"))

    return render_template("index.html", profilepics=profilepics)


# --------------------
# Bildauswahl
# --------------------
@app.route("/select", methods=["GET", "POST"])
def select():
    pic_mode = session.get("p", "1")

    if pic_mode == "1":
        imgs = [f for f in os.listdir(IMAGE_FOLDER) if f.startswith("self_")]
        headline = "Bitte wähle das Bild, das dir am ähnlichsten sieht."
    else:
        imgs = [f for f in os.listdir(IMAGE_FOLDER) if f.startswith("neutral_")]
        headline = "Bitte wähle das Bild, das dir am besten gefällt."

    imgs.sort()

    if request.method == "POST":
        session["chosen_image"] = request.form.get("chosen_image")
        return redirect(url_for("post"))

    return render_template("select.html", images=imgs, headline=headline)


# --------------------
# Caption schreiben
# --------------------
@app.route("/post", methods=["GET", "POST"])
def post():
    chosen = session.get("chosen_image")

    if request.method == "POST":
        session["caption"] = request.form.get("caption", "")
        return redirect(url_for("feed"))

    return render_template("post.html", chosen=chosen)


# --------------------
# Feed
# --------------------
@app.route("/feed")
def feed():
    cond = session.get("cond", "i")
    chosen = session.get("chosen_image")
    username = session.get("username", "user123")
    profilepic = session.get("profilepic", "profilepic.png")
    caption = session.get("caption", "")

    if cond in ["i", "1"]:  # Inklusion
        likes = 1148
        comments = ["wow 😍", "Love this!", "wie toll!!", "sehr schön 😊"]
        cond_js = "inclusion"
    else:  # Exklusion
        likes = 4
        comments = []
        cond_js = "exclusion"

    return render_template(
        "feed.html",
        chosen_image=chosen,
        likes=likes,
        comments=comments,
        cond=cond_js,
        username=username,
        profilepic=profilepic,
        caption=caption,
    )


if __name__ == "__main__":
    app.run(debug=True)

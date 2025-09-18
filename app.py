from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

# Ordner für Bilder
IMAGE_FOLDER = "static/images"
os.makedirs(IMAGE_FOLDER, exist_ok=True)

# --------------------
# Startseite (Username & Profilbild)
# --------------------
@app.route("/", methods=["GET", "POST"])
def index():
    profilepics = [f for f in os.listdir(IMAGE_FOLDER) if "profilepic" in f]

    p = request.args.get("p", "1")  # 1=selfies, 2=neutral
    c = request.args.get("c", "i")  # i=inclusion, e=exclusion

    if request.method == "POST":
        username = request.form.get("username", "user123")
        profilepic = request.form.get("profilepic", profilepics[0])

        return redirect(
            url_for("select", p=p, c=c, username=username, profilepic=profilepic)
        )

    return render_template("index.html", profilepics=profilepics)


# --------------------
# Bildauswahl
# --------------------
@app.route("/select", methods=["GET", "POST"])
def select():
    p = request.args.get("p", "1")
    c = request.args.get("c", "i")
    username = request.args.get("username", "user123")
    profilepic = request.args.get("profilepic", "profilepic.png")

    if p == "1":
        imgs = [f for f in os.listdir(IMAGE_FOLDER) if f.startswith("self_")]
        headline = "Bitte wähle das Bild, das dir am ähnlichsten sieht."
    else:
        imgs = [f for f in os.listdir(IMAGE_FOLDER) if f.startswith("neutral_")]
        headline = "Bitte wähle das Bild, das dir am besten gefällt."

    imgs.sort()

    if request.method == "POST":
        chosen_image = request.form.get("chosen_image")
        return redirect(
            url_for(
                "post",
                p=p,
                c=c,
                username=username,
                profilepic=profilepic,
                chosen_image=chosen_image,
            )
        )

    return render_template(
        "select.html",
        images=imgs,
        headline=headline,
        pic_mode=p,
        username=username,
        profilepic=profilepic,
        p=p,
        c=c,
    )


# --------------------
# Caption schreiben
# --------------------
@app.route("/post", methods=["GET", "POST"])
def post():
    p = request.args.get("p", "1")
    c = request.args.get("c", "i")
    username = request.args.get("username", "user123")
    profilepic = request.args.get("profilepic", "profilepic.png")
    chosen = request.args.get("chosen_image")

    if request.method == "POST":
        caption = request.form.get("caption", "")
        return redirect(
            url_for(
                "feed",
                p=p,
                c=c,
                username=username,
                profilepic=profilepic,
                chosen_image=chosen,
                caption=caption,
            )
        )

    return render_template(
        "post.html",
        chosen=chosen,
        username=username,
        profilepic=profilepic,
        p=p,
        c=c,
    )


# --------------------
# Feed
# --------------------
@app.route("/feed")
def feed():
    p = request.args.get("p", "1")
    c = request.args.get("c", "i")
    username = request.args.get("username", "user123")
    profilepic = request.args.get("profilepic", "profilepic.png")
    chosen = request.args.get("chosen_image")
    caption = request.args.get("caption", "")

    if c in ["i", "1"]:  # Inklusion
        likes = 1148
        comments = ["wow 😍", "Love this!", "wie toll!!", "sehr schön 😊"]
        cond_js = "inclusion"
    else:  # Exklusion
        likes = 4
        comments = []
        cond_js = "exclusion"

    # LimeSurvey-Redirect-Link (anpassen!)
    limesurvey_url = "https://umfrage.umit-tirol.at/index.php/123456?finish=1"

    return render_template(
        "feed.html",
        chosen_image=chosen,
        likes=likes,
        comments=comments,
        cond=cond_js,
        username=username,
        profilepic=profilepic,
        caption=caption,
        limesurvey_url=limesurvey_url,
    )


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)


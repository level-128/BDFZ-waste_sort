import os
import re
import random
from datetime import datetime
from bdfztrash.lib.image_tagging_achieve import recognize_image
from classfier import decode_from_api, classify

from flask import (Flask, flash, redirect, render_template, request,
                   send_from_directory, url_for)

import webbrowser

# from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = ["jpg", "jpeg", "png"]
UPLOAD_FOLDER = "user_uploads"

app = Flask(__name__)
app.secret_key = bytes([random.randint(0, 255) for i in range(24)])

if not os.path.exists(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


def allowed_file(name):
    return "." in name and name.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=["GET", "POST"])
def upload_page():
    if request.method == "POST":
        # check if there's file
        fl = request.files["file"]
        if fl.filename == "":
            flash("Didn't select file")
            return redirect(request.url)

        if allowed_file(fl.filename):
            extension = fl.filename.rsplit(".", 1)[1].lower()
            name = datetime.now().strftime("%Y-%m-%d %H-%M-%S-%f") + "." + extension
            fl.save(os.path.join(app.config["UPLOAD_FOLDER"], name))
            return redirect(url_for("result_page", filename=name))
    # GET
    return render_template("upload_page.html")


@app.route("/uploaded/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


@app.route("/fake-result/<filename>")
def fake_result_page(filename):
    return render_template("result_page_fake.html", filename=filename)


@app.route("/result/<filename>")
def result_page(filename):
    real_img_dir = os.path.join("user_uploads/", filename)
    api_result = recognize_image(real_img_dir)
    tags = decode_from_api(api_result)
    result = classify(tags)

    if result is None:
        return render_template(
            "result_page.html",
            filename=filename,
            successful=False,
            tags=[tag[0] for tag in tags],
        )

    tag, category, confidence = result
    # TODO: generate description
    # position = ""
    return render_template(
        "result_page.html",
        filename=filename,
        successful=True,
        tag=tag,
        category=category,
        confidence=confidence,
        # location="请将垃圾扔到" + location if len(location) > 0 else "",
        location=""
    )


if __name__ == "__main__":
    app.jinja_env.auto_reload = True
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.config["ENV"] = "development"
    print("Will Run on http://127.0.0.1:5000")
    webbrowser.open_new_tab("http://127.0.0.1:5000")
    app.run(debug=True, host="0.0.0.0", port=5000)
    

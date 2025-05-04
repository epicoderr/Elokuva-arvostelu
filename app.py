import secrets
import sqlite3
from flask import Flask
from flask import abort, redirect, render_template, request, make_response
from flask import session
from werkzeug.security import  check_password_hash, generate_password_hash
import db
import config
import items
import re
import users
import markupsafe

app = Flask(__name__)
app.secret_key = config.secret_key

def require_login():
    if "user_id" not in session:
        abort(403)

def check_csrf():
    if "csrf_token" not in request.form:
        abort(403)
    if request.form["csrf_token"] != session["csrf_token"]:
        abort(403)

@app.template_filter()
def show_lines(content):
    content = str(markupsafe.escape(content))
    content = content.replace("\n", "<br />")
    return markupsafe.Markup(content)

@app.route("/")
def index():
    all_items = items.get_items()
    return render_template("index.html", items=all_items)

@app.route("/user/<int:user_id>")
def show_user(user_id):
    user = users.get_user(user_id)
    if not user:
        abort(404)
    items = users.get_items(user_id)
    return render_template("show_user.html", user=user, items=items)

@app.route("/find_item")
def find_item():
    query = request.args.get("query")
    if query:
        results = items.find_items(query)
    else:
        query = ""
        results = []
    return render_template("find_item.html", query= query, results=results)

@app.route("/item/<int:item_id>")
def show_item(item_id):
    item = items.get_item(item_id)
    if not item:
        abort(404)
    classes = items.get_classes(item_id)
    comments = items.get_comments(item_id)
    images = items.get_images(item_id)
    return render_template("show_item.html", item=item, classes=classes, comments=comments, images=images)

@app.route("/images/<int:item_id>")
def edit_images(item_id):
    require_login()
    item = items.get_item(item_id)
    if not item:
        abort(404)
    if item["user_id"] != session["user_id"]:
        abort(403)

    images = items.get_images(item_id)
    
    return render_template("images.html", item=item, images=images)

@app.route("/add_image", methods=["POST"])
def add_image():
    require_login()
    check_csrf()

    item_id = request.form["item_id"]
    item = items.get_item(item_id)
    if not item:
        abort(404)
    if item["user_id"] != session["user_id"]:
        abort(403)

    file = request.files["image"]
    if not file.filename.endswith(".png"):
        return "VIRHE: väärä tiedostomuoto"

    image = file.read()
    if len(image) > 100 * 1024:
        return "VIRHE: liian suuri kuva"

    items.add_image(item_id, image)
    return redirect("/images/" + str(item_id))

@app.route("/image/<int:image_id>")
def show_image(image_id):
    image = items.get_image(image_id)
    if not image:
        abort(404)
    
    response = make_response(bytes(image))
    response.headers.set("Content-Type", "image/png")
    return response
 
@app.route("/remove_images", methods=["POST"])
def remove_images():
    require_login()
    check_csrf()

    item_id = request.form["item_id"]
    item = items.get_item(item_id)
    if not item:
        abort(404)
    if item["user_id"] != session["user_id"]:
        abort(403)

    for image_id in request.form.getlist("image_id"):
        items.remove_image(item_id, image_id)

    return redirect("/images/" + str(item_id))

@app.route("/new_item")
def new_item():
    require_login()
    return render_template("new_item.html")

@app.route("/create_item", methods=["POST"])
def create_item():
    require_login()
    check_csrf()

    title = request.form["title"]
    if not title or len(title) > 80:
        abort(403)
    description = request.form["description"]
    if not description or len(description) > 1000:
        abort(403)
    review = request.form["review"]
    if not re.search("^([0-9]|10)$", review):
        abort(403)
    user_id = session["user_id"]

    classes = []
    genre = request.form["genre"] 
    if genre:
        classes.append(("Genre", genre))

    items.add_item(title, description, review, user_id, classes)

    return redirect("/")

@app.route("/create_comment/<int:item_id>", methods=["POST"])
def create_comment(item_id):
    require_login()
    check_csrf()

    content = request.form["content"]
    user_id = session["user_id"]

    items.add_comment(item_id, user_id, content)

    return redirect(f"/item/{item_id}")

@app.route("/remove_comment/<int:comment_id>", methods=["GET", "POST"])
def remove_comment(comment_id):
    require_login()

    comment = items.get_comment(comment_id)
    if not comment:
        abort(404)
    if comment["user_id"] != session["user_id"]:
        abort(403)

    if request.method == "GET":
        return render_template("remove_comment.html", comment=comment)
    
    if request.method == "POST":
        check_csrf()
        if "remove" in request.form:
            items.remove_comment(comment_id)
            return redirect(f"/item/{comment['item_id']}")
        else:
            return redirect(f"/item/{comment['item_id']}")

@app.route("/edit_item/<int:item_id>")
def edit_item(item_id):
    require_login()
    item = items.get_item(item_id)
    if not item:
        abort(404)
    if item["user_id"] != session["user_id"]:
        abort(403)
    return render_template("edit_item.html", item=item)

@app.route("/update_item", methods=["POST"])
def update_item():
    require_login()
    check_csrf()

    item_id = request.form["item_id"]
    item = items.get_item(item_id)
    if item["user_id"] != session["user_id"]:
        abort(403)

    title = request.form["title"]
    description = request.form["description"]
    review = request.form["review"]

    items.update_item(item_id, title, description, review)

    return redirect("/item/" + str(item_id))

@app.route("/remove_item/<int:item_id>", methods=["GET", "POST"])
def remove_item(item_id):
    require_login()

    item = items.get_item(item_id)
    if item["user_id"] != session["user_id"]:
        abort(403)

    if request.method == "GET":
        return render_template("remove_item.html", item=item)
    
    if request.method == "POST":
        check_csrf()
        if "remove" in request.form:
            items.remove_item(item_id)
            return redirect("/")
        else:
            return redirect("/item/" + str(item_id))
    
@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        return "VIRHE: salasanat eivät ole samat"
    
    try:
        users.create_user(username, password1)
    except sqlite3.IntegrityError:
        return "VIRHE: tunnus on jo varattu"
    
    return "Tunnus luotu"

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user_id = users.check_login(username, password)
        if user_id:
            session["user_id"] = user_id
            session["username"] = username
            session["csrf_token"] = secrets.token_hex(16)
            return redirect("/")
        else:
            return "VIRHE: väärä tunnus tai salasana"

@app.route("/logout")
def logout():
    if "user_id" in session:
        del session["user_id"]
    if "username" in session:
        del session["username"]

    return redirect("/")
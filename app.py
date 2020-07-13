from flask import Flask, render_template, request, url_for, redirect
from helpers import list_entries, save_entry, get_entry

import markdown2
import random

app = Flask(__name__)

@app.route("/")
def index():
    entries = list_entries()
    return render_template("index.html", entries=entries)


@app.route("/wiki/<string:title>")
def wiki(title):
    html = ""
    if get_entry(title) == None:
        return render_template("error.html", message=f'We didn\'t find this entry: {title}, maybe <a href="/new">create one</a> instead?')
    content = get_entry(title).split("\n")
    for line in content:
        html += markdown2.markdown(line)
    return render_template("entry.html", contents=html, title=title)


@app.route("/search")
def search():
    if request.args.get("s"):
        if request.args.get("s") in list_entries():
            return redirect(url_for("wiki", title=request.args.get("s")))
        valids = [e for e in list_entries() if request.args.get("s") in e]
        return render_template("searched.html", valids=valids, name=request.args.get("s"))


@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        if request.form.get("title") in list_entries():
            return render_template("error.html", message=f"{request.form.get('title')} already exist. You can read it at <a href=\"wiki/{request.form.get('title')}\">here</a>.")
        save_entry(request.form.get("title"), request.form.get("contents"))
        return redirect(url_for("wiki", title=request.form.get("title")))
    else:
        return render_template("create.html")


@app.route("/edit/<string:title>", methods=["GET", "POST"])
def edit(title):
    if request.method == "POST":
        save_entry(title, request.form.get("contents"))
        return redirect(url_for("wiki", title=title))
    else:
        try:
            contents = get_entry(title)
        except:
            return render_template("error.html", message="Invalid entry. Entry doesn't exist, probably create one first?")
        return render_template("edit.html", title=title, contents=contents)


@app.route("/random")
def random_page():
    return redirect(url_for("wiki", title=random.choice(list_entries())))
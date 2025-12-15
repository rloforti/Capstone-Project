from flask import Flask, render_template, request, redirect, url_for
import json
from datetime import datetime

app = Flask(__name__)
DATA_FILE = "data.json"

def load_data():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"topics": [], "posts": []}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

@app.route("/")
def index():
    data = load_data()
    posts = data["posts"][-3:]  # show last 3 posts
    return render_template("index.html", posts=posts)

@app.route("/topics", methods=["GET", "POST"])
def topics():
    data = load_data()
    if request.method == "POST":
        topic = request.form["topic"]
        if topic and topic not in data["topics"]:
            data["topics"].append(topic)
            save_data(data)
        return redirect(url_for("topics"))
    return render_template("topics.html", topics=data["topics"])

@app.route("/add_post", methods=["GET", "POST"])
def add_post():
    data = load_data()
    if request.method == "POST":
        # ✅ use .get() instead of ["topic"] to avoid KeyError
        topic = request.form.get("topic")
        content = request.form.get("content")

        if topic and content:
            post = {
                "id": len(data["posts"]) + 1,
                "topic": topic,
                "content": content,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            data["posts"].append(post)
            save_data(data)
        return redirect(url_for("index"))

    return render_template("add_post.html", topics=data["topics"])

@app.route("/post/<int:post_id>")
def post(post_id):
    data = load_data()
    post = next((p for p in data["posts"] if p["id"] == post_id), None)
    return render_template("post.html", post=post)

if __name__ == "__main__":
    app.run(debug=True)

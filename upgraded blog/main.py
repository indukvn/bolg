from flask import Flask, render_template, request
import requests
import smtplib

email = "newmail002244@gmail.com"
password = "vncdnqzamtgsrfdz"

posts = requests.get("https://api.npoint.io/efb6c12ee2cd10c1d838").json()

app = Flask(__name__)


@app.route('/')
def get_all_posts():
    return render_template("index.html", all_posts=posts)


@app.route("/post/<int:index>")
def show_post(index):
    requested_post = None
    for blog_post in posts:
        if blog_post["id"] == index:
            requested_post = blog_post
    return render_template("post.html", post=requested_post)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact", methods=['POST', 'GET'])
def contact():
    if request.method == "POST":
        data = request.form
        send_msg(data["name"], data["email"], data["phone"], data["message"])
        return render_template("contact.html", msg_sent=True)
    return render_template("contact.html", msg_sent=False)


def send_msg(name, email_sent, phone, message):
    email_msg = f"Subject:New Message\n\nName: {name}\nEmail: {email_sent}\nPhone: {phone}\nMessage: {message}"
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(email, password)
        connection.sendmail(from_addr=email, to_addrs=email, msg=email_msg)


if __name__ == "__main__":
    app.run(debug=True)
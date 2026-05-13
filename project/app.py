from flask import Flask, flash,render_template,request,redirect,url_for,jsonify
from flask_wtf.csrf import CSRFProtect
from project.models import Comment
from project import db

app = Flask(__name__)
app.config["SECRET_KEY"] = "dev-secret-key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
csrf = CSRFProtect(app)
with app.app_context():
    db.create_all()



@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods = ["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        flash(f"Login requested for {username}")
        return redirect(url_for("index"))
    
    return render_template("login.html")



@app.route("/signup", methods =["GET","POST"])
def signup():
    if request.method == "POST":
        email = request.form.get("email")
        flash(f"Sign up requsted for {email}")
        return redirect(url_for("login"))
    return render_template("signup.html")

@app.route("/comments", methods=["POST"])
def add_comment():
    content = request.form.get("content")
    print("Comment received by backend:", content,flush=True)

    if not content:
        flash("Comment cannot be empty.")
        return redirect(request.referrer or url_for("index"))


    new_comment = Comment(content = content)
    db.session.add(new_comment)
    db.session.commit()

    flash("Comment added successfully.")
    return redirect(request.referrer or url_for("index"))

@app.route("/api/charts")
def chart_data():
    return jsonify({
        "popular_majors":{
            "labels":["Computer Science", "Data Science", "Software Engineering"],
            "values":[12,8,10]
        },
        "choice_reasons":{
            "labels":["Job opportunities", "Interest", "Salary", "Enjoy coding"],
            "values":[9,6,5,8]
        }
    })


@app.route("/settings")
def settings():
    return render_template("settings.html")


@app.route("/computer-science")
def computer_science():
    return render_template("computer_science.html")

@app.route("/data-science")
def data_science():
    return render_template("data_science.html")

@app.route("/software-engineering")
def software_engineering():
    return render_template("software_engineering.html")

@app.route("/survey", methods=["GET", "POST"])
def survey():
    if request.method == "POST":
        q1 = request.form.get("q1")
        q2 = request.form.get("q2")
        q3 = request.form.get("q3")
        q4 = request.form.get("q4")
        q5 = request.form.get("q5")
        q6 = request.form.get("q6")
        q7 = request.form.get("q7")

        if not all([q1, q2, q3, q4, q5, q6, q7]):
            flash("Please answer all questions.")
            return redirect(url_for("survey"))

        # TODO: save survey answers to database here

        flash("Survey submitted.")
        return redirect(url_for("index"))

    return render_template("survey.html")
if __name__ == "__main__":
    app.run(debug = True)
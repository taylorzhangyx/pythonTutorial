from application import app, db
from application.modules.user import User
from application.modules.course import Course
from application.modules.enrollment import Enrollment
from flask import render_template, request, Response, json, redirect, flash
from application.forms import LoginForm, RegisterForm
from application.login import verify_identity

# courseData = [
#     {
#         "courseID": "1111",
#         "title": "PHP 111",
#         "description": "Intro to PHP",
#         "credits": "3",
#         "term": "Fall, Spring",
#     },
#     {
#         "courseID": "2222",
#         "title": "Java 1",
#         "description": "Intro to Java Programming",
#         "credits": "4",
#         "term": "Spring",
#     },
#     {
#         "courseID": "3333",
#         "title": "Adv PHP 201",
#         "description": "Advanced PHP Programming",
#         "credits": "3",
#         "term": "Fall",
#     },
#     {
#         "courseID": "4444",
#         "title": "Angular 1",
#         "description": "Intro to Angular",
#         "credits": "3",
#         "term": "Fall, Spring",
#     },
#     {
#         "courseID": "5555",
#         "title": "Java 2",
#         "description": "Advanced Java Programming",
#         "credits": "4",
#         "term": "Fall",
#     },
# ]


@app.route("/", methods=["GET"])
@app.route("/index", methods=["GET"])
@app.route("/home", methods=["GET"])
def index():
    return render_template("index.html", index=True)


@app.route("/courses/<term>", methods=["GET"])
@app.route("/courses", methods=["GET"])
def courses(term="spring 2020"):
    courseData = Course.objects.all()
    return render_template(
        "courses.html", term=term, courseData=courseData, courses=True
    )


@app.route("/register", methods=["GET"])
def register():
    form = RegisterForm()
    return (
        render_template("register.html", register=True, title="Register", form=form),
    )


@app.route("/login", methods=["GET", "POST"])
def login():
    print(f"login {request.method} {request.form}")
    form = LoginForm()
    email = form.email.data
    password = form.password.data
    if form.validate_on_submit():
        if verify_identity(email=email, password=password):
            flash("good login", "success")
            return redirect("/index")
        else:
            flash("something went wrong.", "danger")
    return render_template("login.html", title="Login", form=form, login=True)


@app.route("/enrollment", methods=["POST"])
def enrollment():
    courseId = request.form.get("courseId")
    title = request.form.get("title")
    term = request.form.get("term")
    print(request.form)
    return render_template(
        "enrollment.html",
        enrollment=True,
        course={"courseId": courseId, "title": title, "term": term},
    )


@app.route("/api")
@app.route("/api/<idx>", methods=["GET", "POST"])
def api(idx=None):
    if idx == None:
        jData = Course.objects.all()
    else:
        jData = Course.objects.all()[int(idx)]

    return Response(json.dumps(jData), mimetype="application/json", status=200)


@app.route("/users")
def users():
    userData = User.objects.all()
    if userData.count() == 0:
        firstnames = [
            "John",
            "Jane",
            "Adam",
            "Kevin",
            "Ryan",
            "Cindy",
            "George",
            "James",
            "Paul",
        ]
        for i in range(1, len(firstnames)):
            User(
                userId=str(i),
                firstName=firstnames[i],
                password="1234qwer",
                email=f"{firstnames[i]}@test.com",
            ).save()
        userData = User.objects.all()
    return render_template("users.html", userData=userData, users=True)

from application import app, db
from application.modules.user import User
from application.modules.course import Course
from application.modules.enrollment import Enrollment
from flask import render_template, request, Response, json, redirect, flash, url_for
from application.forms import LoginForm, RegisterForm
from application.login import verify_identity
from application.enrollment import enrollment_query


@app.route("/", methods=["GET"])
@app.route("/index", methods=["GET"])
@app.route("/home", methods=["GET"])
def index():
    return render_template("index.html", index=True)


@app.route("/courses/<term>", methods=["GET"])
@app.route("/courses", methods=["GET"])
def courses(term="spring 2020"):
    courseData = Course.objects.order_by("-courseId")
    return render_template(
        "courses.html", term=term, courseData=courseData, courses=True
    )


@app.route("/register", methods=["GET", "POST"])
def register():
    print(f"request {request.method} {request.form}")
    form = RegisterForm()
    print(f"request2 {request.method} {request.form}")
    if form.validate_on_submit():
        print(f"request3 {request.method} {request.form}")
        user_id = User.objects.count() + 1
        email = form.email.data
        password = form.password.data
        firstName = form.firstName.data
        lastName = form.lastName.data

        user = User(userId=user_id, firstName=firstName, email=email, lastName=lastName)
        user.set_password(password)
        user.save()
        flash("User is successfully registered!", "success")
        print("User is successfully registered")
        return redirect(url_for("index"))
    return render_template("register.html", register=True, title="Register", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    print(f"login {request.method} {request.form}")
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        if verify_identity(email=email, password=password):
            flash("good login", "success")
            return redirect("/index")
        else:
            flash("something went wrong.", "danger")
    return render_template("login.html", title="Login", form=form, login=True)


@app.route("/enrollment", methods=["POST", "GET"])
def enrollment():
    userId = 1
    course = None
    if request.method == "POST":
        courseId = request.form.get("courseId")
        title = request.form.get("title")
        term = request.form.get("term")
        course = {"courseId": courseId, "title": title, "term": term}

        Enrollment(courseId=courseId, userId=userId).save()

    enrolledCourses = User.objects.aggregate(enrollment_query(userId))
    print(f"enrolled courses #: {enrolledCourses}")
    return render_template(
        "enrollment.html",
        course=course,
        enrolledCourses=enrolledCourses,
        enrollment=True,
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
    return render_template("users.html", userData=userData, users=True)

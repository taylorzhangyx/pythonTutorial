from application import app, db, api
from application.modules.user import User
from application.modules.course import Course
from application.modules.enrollment import Enrollment
from flask import (
    render_template,
    request,
    Response,
    json,
    jsonify,
    redirect,
    flash,
    url_for,
    session,
)
from application.forms import LoginForm, RegisterForm
from application.login import verify_identity
from application.enrollment import enrollment_query
from flask_restx import Resource


@app.route("/", methods=["GET"])
@app.route("/index", methods=["GET"])
@app.route("/home", methods=["GET"])
def index():
    logged_in = session.get("email")
    return render_template("index.html", index=True, logged_in=logged_in)


@app.route("/courses/<term>", methods=["GET"])
@app.route("/courses", methods=["GET"])
def courses(term="spring 2020"):
    courseData = Course.objects.order_by("-courseId")
    return render_template(
        "courses.html", term=term, courseData=courseData, courses=True
    )


@app.route("/register", methods=["GET", "POST"])
def register():
    if session.get("email"):
        return redirect("/index")

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
        return redirect(url_for("index"))
    return render_template("register.html", register=True, title="Register", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("email"):
        return redirect("/index")

    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        if verify_identity(email=email, password=password):
            session["email"] = email
            flash("good login", "success")
            return redirect("/index")
        else:
            flash("something went wrong.", "danger")
    return render_template("login.html", title="Login", form=form, login=True)


@app.route("/enrollment", methods=["POST", "GET"])
def enrollment():
    userEmail = session.get("email")
    if not userEmail:
        return redirect("/login")
    else:
        userId = User.objects(email=userEmail)
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


@app.route("/users")
def users():
    userData = User.objects.all()
    return render_template("users.html", userData=userData, users=True)


@app.route("/logout")
def logout():
    session.pop("email", None)
    session["email"] = False
    return redirect("index")


##############################################
# API section


##############################################


@api.route("/api/users", "/api/users/")
class GetUsers(Resource):
    def get(self):
        return jsonify(User.objects.all())

    def post(self):
        userData = api.payload
        print(userData)
        user_id = User.objects.count() + 1
        email = userData["email"]
        password = userData["password"]
        firstName = userData["firstName"]
        lastName = userData["lastName"]

        user = User(userId=user_id, firstName=firstName, email=email, lastName=lastName)
        user.set_password(password)
        user.save()

        return jsonify(User.objects(email=email))


@api.route("/api/users/<idx>")
class GetUsers(Resource):
    def get(self, idx):
        return jsonify(User.objects(userId=idx))

    def put(self, idx):
        data = api.payload
        User.objects(userId=idx).update(**data)
        return jsonify(User.objects(userId=idx))

    def delete(self, idx):
        matchedUser = User.objects(userId=idx)
        if matchedUser:
            matchedUser.delete()
            return "deleted"
        else:
            return "failed", 404


# @app.route("/api")
# @app.route("/api/<idx>", methods=["GET", "POST"])
# def api(idx=None):
#     if idx == None:
#         jData = Course.objects.all()
#     else:
#         jData = Course.objects.all()[int(idx)]

#     return Response(json.dumps(jData), mimetype="application/json", status=200)

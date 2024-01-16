from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField
from datetime import date

'''
Make sure the required packages are installed: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from the requirements.txt for this project.
'''

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)
date_time = date.today().strftime("%B %w, %Y")
ckeditor = CKEditor(app)

# Create add post form
class BlogPostForm(FlaskForm):
    title = StringField(label="Blog Post Title", validators={DataRequired()})
    subtitle = StringField(label="Subtitle", validators=[DataRequired()])
    author = StringField(label="Your Name", validators=[DataRequired()])
    blog_img_url = StringField(label="Blog Image URL", validators=[DataRequired(), URL()])
    body = CKEditorField(label="Blog Content", validators=[DataRequired()])
    submit = SubmitField(label="Submit Post")

# CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy()
db.init_app(app)


# CONFIGURE TABLE
class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)


with app.app_context():
    db.create_all()


@app.route('/')
def get_all_posts():
    # Query the database for all the posts. Convert the data to a python list.
    response = db.session.execute(db.select(BlogPost).order_by(BlogPost.title)).scalars()
    posts = [post for post in response]
    return render_template("index.html", all_posts=posts)

# Add a route so that you can click on individual posts.
@app.route('/post')
def show_post():
    # Retrieve a BlogPost from the database based on the post_id
    post_id = request.args.get("post_id")
    requested_post = db.get_or_404(BlogPost, post_id)
    return render_template("post.html", post=requested_post)


# add_new_post() to create a new blog post
@app.route("/new-post", methods=["GET", "POST"])
def add_post():
    form = BlogPostForm()
    if form.validate_on_submit():
        new_post = BlogPost(
            title = form.title.data,
            subtitle = form.subtitle.data,
            date = date_time,
            body = form.body.data,
            author = form.author.data,
            img_url = form.blog_img_url.data
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("get_all_posts"))
    return render_template("make-post.html", form=form)

# TODO: edit_post() to change an existing blog post

# TODO: delete_post() to remove a blog post from the database

# Below is the code from previous lessons. No changes needed.
@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True, port=5003)

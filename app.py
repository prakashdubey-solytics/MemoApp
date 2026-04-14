from flask import Flask, render_template, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Model
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    body = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'body': self.body,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

# Create database tables
with app.app_context():
    db.create_all()

# Routes
@app.route("/")
def home():
    search = request.args.get('search', '')
    if search:
        posts = Post.query.filter(
            db.or_(
                Post.title.ilike(f'%{search}%'),
                Post.body.ilike(f'%{search}%')
            )
        ).order_by(Post.created_at.desc()).all()
    else:
        posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template("index.html", posts=posts, search=search)

@app.route("/create", methods=["POST"])
def create_post():
    title = request.form.get("title", "").strip()
    body = request.form.get("body", "").strip()

    if not title or not body:
        return redirect("/?error=Title and body are required")

    post = Post(title=title, body=body)
    db.session.add(post)
    db.session.commit()

    return redirect("/")

@app.route("/edit/<int:post_id>", methods=["GET", "POST"])
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        body = request.form.get("body", "").strip()

        if not title or not body:
            return render_template("edit.html", post=post, error="Title and body are required")

        post.title = title
        post.body = body
        db.session.commit()

        return redirect("/")

    return render_template("edit.html", post=post)

@app.route("/delete/<int:post_id>", methods=["POST"])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect("/")

@app.route("/api/posts", methods=["GET"])
def get_posts_api():
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return jsonify([post.to_dict() for post in posts])

@app.route("/api/posts/<int:post_id>", methods=["GET"])
def get_post_api(post_id):
    post = Post.query.get_or_404(post_id)
    return jsonify(post.to_dict())

@app.route("/api/posts", methods=["POST"])
def create_post_api():
    data = request.get_json()
    
    if not data or not data.get('title') or not data.get('body'):
        return jsonify({"error": "Title and body are required"}), 400

    post = Post(title=data['title'], body=data['body'])
    db.session.add(post)
    db.session.commit()

    return jsonify(post.to_dict()), 201

@app.route("/api/posts/<int:post_id>", methods=["PUT"])
def update_post_api(post_id):
    post = Post.query.get_or_404(post_id)
    data = request.get_json()

    if data.get('title'):
        post.title = data['title']
    if data.get('body'):
        post.body = data['body']

    db.session.commit()
    return jsonify(post.to_dict())

@app.route("/api/posts/<int:post_id>", methods=["DELETE"])
def delete_post_api(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return jsonify({"message": "Post deleted"}), 200

@app.route("/run-test")
def run_test():
    # Test that database is working
    try:
        posts = Post.query.all()
        return jsonify({
            "status": "passed",
            "total_posts": len(posts),
            "database": "SQLite Local Database"
        })
    except Exception as e:
        return jsonify({"status": "failed", "error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
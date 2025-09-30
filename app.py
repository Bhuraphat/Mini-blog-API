from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///blog.db"
db = SQLAlchemy(app)

# สร้าง Model สำหรับโพสต์
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)

# สร้างตารางใน database
with app.app_context():
    db.create_all()

# อ่านโพสต์ทั้งหมด
@app.route("/posts", methods=["GET"])
def get_posts():
    posts = Post.query.all()
    return jsonify([{"id": p.id, "title": p.title, "content": p.content} for p in posts])

# อ่านโพสต์เดียว
@app.route("/posts/<int:post_id>", methods=["GET"])
def get_post(post_id):
    post = Post.query.get(post_id)
    if post:
        return jsonify({"id": post.id, "title": post.title, "content": post.content})
    return jsonify({"error": "Post not found"}), 404

# เพิ่มโพสต์ใหม่
@app.route("/posts", methods=["POST"])
def add_post():
    data = request.get_json()
    post = Post(title=data["title"], content=data["content"])
    db.session.add(post)
    db.session.commit()
    return jsonify({"id": post.id, "title": post.title, "content": post.content}), 201

# แก้ไขโพสต์
@app.route("/posts/<int:post_id>", methods=["PUT"])
def update_post(post_id):
    post = Post.query.get(post_id)
    if not post:
        return jsonify({"error": "Post not found"}), 404
    data = request.get_json()
    post.title = data.get("title", post.title)
    post.content = data.get("content", post.content)
    db.session.commit()
    return jsonify({"id": post.id, "title": post.title, "content": post.content})

# ลบโพสต์
@app.route("/posts/<int:post_id>", methods=["DELETE"])
def delete_post(post_id):
    post = Post.query.get(post_id)
    if not post:
        return jsonify({"error": "Post not found"}), 404
    db.session.delete(post)
    db.session.commit()
    return jsonify({"message": "Post deleted"})

if __name__ == "__main__":
    app.run(debug=True)

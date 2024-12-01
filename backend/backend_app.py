from flask import Flask, jsonify, request
from flask_cors import CORS
import uuid

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


@app.route('/api/posts', methods=['GET'])
def get_posts():
    return jsonify(POSTS)


@app.route('/api/posts', methods=["POST"])
def create_posts():
    data = request.get_json(POSTS)
    
    if "title" not in data and "content" not in data:
        return jsonify({"error": "Both 'title' and 'content' are required"}), 400
    
    new_id = uuid.uuid4().int
    
    new_post = {
        "id": new_id,
        "title": data["title"],
        "content": data["content"]
    }
    
    POSTS.append(new_post)
    
    return jsonify(new_post), 201


@app.route("/api/posts/<int:id>", methods=['DELETE'])
def delete_post(id):
    for post in POSTS:
        if post["id"] == int(id):
            POSTS.remove(post)
            return jsonify({"message": f"Post with id {id} has been deleted successfully."}), 200
        
    return jsonify({"error:": "Post not found"}), 404



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)

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


@app.route("/api/posts/<int:id>", methods=["PUT"])
def update_post(id):
    
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "Invalid input. JSON data is required."}), 400

    for post in POSTS:
        if post["id"] == id:
            # Update only the provided fields
            post["title"] = data.get("title", post["title"])
            post["content"] = data.get("content", post["content"])
            
            return jsonify({
                "id": post["id"],
                "title": post["title"],
                "content": post["content"]
                }), 200
            
    return jsonify({"error": "Post not found"}), 404


@app.route("/api/posts/search", methods=["GET"])
def search_post():
    title_query = request.args.get("title", "").lower()
    content_query = request.args.get("content", "").lower()

    filtered_posts = filter( lambda post: title_query in post["title"].lower() 
    and content_query in post["content"].lower(),POSTS)
    
    if not filtered_posts:
        return jsonify({"error": "No posts match the search criteria."}), 404

    return jsonify(list(filtered_posts)), 200



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)

from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Temporary in-memory storage for products
products_list = []

# Endpoint to fetch data from Dummy JSON API and populate initial products list
def fetch_initial_products():
    global products_list
    try:
        response = requests.get("https://dummyjson.com/products")
        response.raise_for_status()
        products_list = response.json().get("products", [])
    except requests.exceptions.RequestException as e:
        products_list = []
        print(f"Error fetching initial products: {e}")

# Fetch initial products on app start
fetch_initial_products()

@app.route("/products", methods=["GET", "POST"])
def products():
    global products_list

    if request.method == "GET":
        if not products_list:
            return jsonify({"error": "Failed to fetch products from the external API."}), 500
        return jsonify(products_list)

    elif request.method == "POST":
        # Validate incoming product data
        data = request.json
        if not data:
            return jsonify({"error": "Invalid request body."}), 400

        required_fields = ["title", "price", "category"]
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields: title, price, and category."}), 400

        # Add new product to the list
        new_product = {
            "id": len(products_list) + 1,
            "title": data["title"],
            "price": data["price"],
            "category": data["category"],
            "description": data.get("description", ""),
            "images": data.get("images", [])
        }
        products_list.append(new_product)

        return jsonify(products_list), 201

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found."}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error."}), 500

if __name__ == "__main__":
    app.run(debug=True)

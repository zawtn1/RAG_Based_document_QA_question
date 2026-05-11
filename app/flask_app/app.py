from flask import Flask, request, jsonify, render_template
from app.rag.qa_chain import build_qa_chain

app = Flask(__name__)

qa_chain = build_qa_chain()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/ask", methods=["POST"])
def ask():
    try:
        data = request.json
        query = data.get("query", "")
        
        print(f"Received query: {query}")  # Debug log
        
        if not query:
            return jsonify({"error": "No query provided"}), 400
        
        response = qa_chain.invoke(query)
        
        print(f"Response: {response}")  # Debug log
        
        return jsonify({"answer": response})
    
    except Exception as e:
        print(f"Error: {str(e)}")  # Debug log
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
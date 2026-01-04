from flask import Flask, request, render_template_string
import pandas as pd

app = Flask(__name__)

# Load datasets
recs = pd.read_csv("data/MovieRecommendations.csv")

# 🔧 CLEAN TITLES (THIS FIXES EVERYTHING)
recs["title"] = recs["title"].astype(str).str.strip().str.strip("'").str.lower()

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Movie Recommender</title>
    <style>
        body {
            font-family: 'Segoe UI', sans-serif;
            background: linear-gradient(120deg, #0f2027, #203a43, #2c5364);
            height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
        }
        .card {
            background: white;
            color: #222;
            width: 460px;
            padding: 35px;
            border-radius: 16px;
            box-shadow: 0 25px 60px rgba(0,0,0,0.35);
            text-align: center;
        }
        h2 {
            margin-bottom: 5px;
        }
        p {
            color: #666;
            font-size: 14px;
        }
        input {
            width: 100%;
            padding: 14px;
            margin-top: 20px;
            border-radius: 8px;
            border: 1px solid #ccc;
            font-size: 15px;
        }
        button {
            width: 100%;
            background: linear-gradient(135deg, #ff416c, #ff4b2b);
            border: none;
            color: white;
            padding: 14px;
            margin-top: 18px;
            border-radius: 8px;
            font-size: 16px;
            cursor: pointer;
        }
        ul {
            list-style: none;
            padding: 0;
            margin-top: 25px;
        }
        li {
            background: #f4f4f4;
            margin: 8px 0;
            padding: 12px;
            border-radius: 8px;
            font-size: 15px;
        }
        .error {
            color: red;
            margin-top: 15px;
        }
        footer {
            margin-top: 20px;
            font-size: 12px;
            color: #888;
        }
    </style>
</head>
<body>

<div class="card">
    <h2>🎬 Movie Recommender</h2>
    <p>Discover movies you’ll love</p>

    <form method="post">
        <input type="text" name="movie" placeholder="Enter a movie name (e.g. toy)" required>
        <button type="submit">Get Recommendations</button>
    </form>

    {% if error %}
        <p class="error">{{ error }}</p>
    {% endif %}

    {% if recommendations %}
        <ul>
            {% for r in recommendations %}
                <li>{{ r }}</li>
            {% endfor %}
        </ul>
    {% endif %}

    <footer>Powered by Flask • Pandas • Docker • Cloud</footer>
</div>

</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    recommendations = []
    error = None

    if request.method == "POST":
        user_movie = request.form["movie"].strip().lower()

        match = recs[recs["title"].str.contains(user_movie)]

        if match.empty:
            error = "Movie not found. Try another title."
        else:
            row = match.iloc[0]
            recommendations = [
                row["FirstMovieRecommendation"],
                row["SecondMovieRecommendation"],
                row["ThirdMovieRecommendation"],
                row["FourthMovieRecommendation"],
            ]

    return render_template_string(
        HTML,
        recommendations=recommendations,
        error=error
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

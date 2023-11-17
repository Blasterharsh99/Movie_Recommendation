from flask import Flask, request, jsonify, render_template
from Movie_Recommendation import recommend,get_suggestions
# Your existing code for movie recommendation

app = Flask(__name__)

@app.route('/')
def index():
    suggestions = get_suggestions()
    return render_template('home.html',suggestions=suggestions)

@app.route('/recommend', methods=['GET'])
def recommend_movies():
    movie_name = request.args.get('title')
    if movie_name:
        movies,ids = recommend(movie_name)
        return render_template('recommend.html',recommend_movies=movies)
    else:
        return jsonify({"error": "Movie title parameter ('title') is required."})

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, request
from db_config import get_db_connection

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/movies")
def list_movies():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM MOVIES")
    movies = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("movie_list.html", movies=movies)


@app.route('/search', methods=['GET'])
def search_movies():
    query = request.args.get('query', '')
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    sql = """
        SELECT * FROM movies
        WHERE title LIKE %s OR director LIKE %s
    """
    cursor.execute(sql, (f'%{query}%', f'%{query}%'))
    movies = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('movie_list.html', movies=movies)


@app.route('/filter', methods=['GET'])
def filter_movies():
    genre = request.args.get('genre', '')
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM movies WHERE genre = %s", (genre,))
    movies = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('movie_list.html', movies=movies)


@app.route('/movie/<int:movie_id>', methods=['GET'])
def movie_details(movie_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT * 
        FROM movies 
        WHERE movie_id = %s
    """, (movie_id,))
    
    movie = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if not movie:
        return render_template('404.html'), 404  
    
    return render_template('movie_details.html', movie=movie)


@app.route('/director/<int:director_id>', methods=['GET'])
def director_page(director_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM directors
        JOIN movies ON directors.director_id = movies.director_id
        WHERE directors.director_id = %s
    """, (director_id,))  

    director_and_movies = cursor.fetchall()
    conn.close()

    if not director_and_movies:
        return render_template('404.html'), 404

    return render_template('director_page.html', director_and_movies=director_and_movies)


if __name__ == '__main__':
    app.run(debug=True)
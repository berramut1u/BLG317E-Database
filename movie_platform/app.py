from flask import Flask, render_template, request
from db_config import get_db_connection

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/movies")
def list_movies():
    # SQL query to fetch movies along with genres and posters
    query = """
        SELECT 
            movies.id, 
            movies.movie_name, 
            movies.movie_date, 
            movies.movie_length, 
            movies.movie_rating,
            GROUP_CONCAT(DISTINCT genres.genre SEPARATOR ', ') AS genres,  -- Get the genres for the movie
            GROUP_CONCAT(DISTINCT languages.film_language SEPARATOR ', ') AS languages,
            MAX(posters.link) AS poster_link  -- Get one poster link (if available)
        FROM movies
        LEFT JOIN genres ON movies.id = genres.id  -- Join with genres table
        LEFT JOIN languages ON movies.id = languages.id        
        LEFT JOIN posters ON movies.id = posters.id  -- Join with posters table
        GROUP BY movies.id  -- Group by movie ID to avoid duplicate rows
    """
    
    # Connect to the database
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query)
    movies = cursor.fetchall()
    cursor.close()
    conn.close()

    # Pass the movies data to the template
    return render_template("movie_list.html", movies=movies)




@app.route('/search', methods=['GET'])
def search_movies():
    query = request.args.get('query', '')
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # SQL query to fetch movies along with genres, languages, and posters
    sql = """
        SELECT 
            movies.id, 
            movies.movie_name, 
            movies.movie_date, 
            movies.movie_length, 
            movies.movie_rating,
            GROUP_CONCAT(DISTINCT genres.genre SEPARATOR ', ') AS genres,  -- Get the genres for the movie
            GROUP_CONCAT(DISTINCT languages.film_language SEPARATOR ', ') AS languages,  -- Get the languages for the movie
            MAX(posters.link) AS poster_link  -- Get one poster link (if available)
        FROM movies
        LEFT JOIN genres ON movies.id = genres.id  -- Join with genres table
        LEFT JOIN languages ON movies.id = languages.id  -- Join with languages table (assuming 'film_language' is the column name)
        LEFT JOIN posters ON movies.id = posters.id  -- Join with posters table
        WHERE movies.movie_name LIKE %s  -- Filter by movie name
        GROUP BY movies.id  -- Group by movie ID to avoid duplicate rows
    """
    
    cursor.execute(sql, (f'%{query}%',))
    movies = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('movie_list.html', movies=movies)


@app.route('/filter', methods=['GET'])
def filter_movies():
    genre = request.args.get('genre', '')
    language = request.args.get('language', '')
    year_min = request.args.get('year_min', None, type=int)
    year_max = request.args.get('year_max', None, type=int)
    runtime_min = request.args.get('runtime_min', None, type=int)
    runtime_max = request.args.get('runtime_max', None, type=int)
    rating_min = request.args.get('rating_min', None, type=float)
    rating_max = request.args.get('rating_max', None, type=float)

    query = """
        SELECT 
            movies.id, 
            movies.movie_name, 
            movies.movie_date, 
            movies.movie_length, 
            movies.movie_rating,
            GROUP_CONCAT(DISTINCT genres.genre SEPARATOR ', ') AS genres,
            GROUP_CONCAT(DISTINCT languages.film_language SEPARATOR ', ') AS languages,
            MAX(posters.link) AS poster_link  -- Add poster link to query
        FROM movies
        LEFT JOIN genres ON movies.id = genres.id
        LEFT JOIN languages ON movies.id = languages.id
        LEFT JOIN posters ON movies.id = posters.id  -- Join with posters table
        WHERE 1=1
    """
    params = []

    # Apply filters dynamically
    if genre:
        query += """
            AND movies.id IN (
                SELECT id FROM genres WHERE genre = %s
            )
        """
        params.append(genre)

    if language:
        query += " AND languages.film_language = %s"
        params.append(language)

    if year_min is not None:
        query += " AND movies.movie_date >= %s"
        params.append(year_min)

    if year_max is not None:
        query += " AND movies.movie_date <= %s"
        params.append(year_max)

    if runtime_min is not None:
        query += " AND movies.movie_length >= %s"
        params.append(runtime_min)

    if runtime_max is not None:
        query += " AND movies.movie_length <= %s"
        params.append(runtime_max)

    if rating_min is not None:
        query += " AND movies.movie_rating >= %s"
        params.append(rating_min)

    if rating_max is not None:
        query += " AND movies.movie_rating <= %s"
        params.append(rating_max)

    # Ensure movies appear only once
    query += " GROUP BY movies.id"

    # Connect to the database and execute the query
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query, tuple(params))
    movies = cursor.fetchall()
    cursor.close()
    conn.close()

    # Pass the movies data to the template (including the poster_link)
    return render_template('movie_list.html', movies=movies)





@app.route('/movie/<int:id>', methods=['GET'])
def movie_details(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT * 
        FROM movies 
        WHERE id = %s
    """, (id,))
    
    movies = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if not movies:
        return render_template('404.html'), 404  
    
    
    return render_template('movie_detail.html', movies=movies)


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
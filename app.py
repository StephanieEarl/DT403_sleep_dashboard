from flask import Flask, jsonify, render_template, abort, Response, make_response 
import sqlite3
import pathlib
import logging
import requests

# Setup logging
logging.basicConfig(filename="app.log", level=logging.DEBUG)

working_directory = pathlib.Path(__file__).parent.absolute()
DATABASE = working_directory / 'sleep_dashboard.db'

def query_db(query: str, args=()) -> list:
    try:
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, args).fetchall()
        return result
    except sqlite3.Error as e:
        logging.error("Database error: %s", e)
        abort(500, description="Database error occurred.")

app = Flask(__name__)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({"error": "Not found"}), 404)

@app.errorhandler(500)
def internal_error(error):
    return make_response(jsonify({"error": "Internal server error"}), 500)

@app.route('/')
def index() -> str:
    return render_template("dashboard.html")

@app.route("/api/temperature_over_time", methods=["GET"])
def temperature_over_time():
    # Fetching the date range from Sessions
    query = """
SELECT MIN(session_date), MAX(session_date)
FROM Sessions;
"""
    try:
        result = query_db(query)
        start_date, end_date = result[0]

        # Making an API call to fetch temperature data
        API_ENDPOINT = "https://archive-api.open-meteo.com/v1/archive"
        params = {
            "latitude": 50.6053,  # London UK
            "longitude": -3.5952,
            "start_date": start_date,
            "end_date": end_date,
            "daily": "temperature_2m_max",
            "timezone": "GMT",
        }
        response = requests.get(API_ENDPOINT, params=params)
        response.raise_for_status()

        return jsonify(response.json())
    except Exception as e:
        logging.error("Error in /api/temperature_over_time: %s", e)
        abort(500, description="Error fetching temperature data.")

@app.route("/api/participants_per_age")
def participants_per_age() -> Response:
    query = """
    SELECT age, COUNT(person_ID) AS num_participants
    FROM Participant
    GROUP BY age
    ORDER BY age ASC;
    """
    try:
        result = query_db(query)
        age = [row[0] for row in result]
        num_participants = [row[1] for row in result]
        return jsonify({"age": age, "num_participants": num_participants})
    except Exception as e:
        logging.error("Error in /api/participants_per_age: %s", e)
        abort(500, description="Error processing data.")

@app.route("/api/clinic_status")
def clinic_status() -> Response:
    query = """
    SELECT clinic_status, COUNT(DISTINCT person_ID) AS total_participants
    FROM Sessions
    GROUP BY clinic_status
    ORDER BY total_participants DESC;
    """
    try:
        result = query_db(query)
        status = [row[0] for row in result]
        counts = [row[1] for row in result]
        return jsonify({"status": status, "counts": counts})
        
    except Exception as e:
        logging.error("Error in /api/clinic_status: %s", e)
        abort(500, description="Error processing data.")

@app.route("/api/sessions_attended")
def sessions_attended() -> Response:
    query = """
    SELECT strftime ('%Y-%m', session_date) AS month, COUNT(session_ID) AS session_attended
    FROM Sessions
    WHERE session_status = 'Attended' 
    GROUP BY month
    ORDER BY month;
    """
    
    try:
        result = query_db(query)
        dates = [row[0] for row in result]
        attended = [row[1] for row in result]
        return jsonify({"dates": dates, "attended": attended})
    except Exception as e:
        logging.error("Error in /api/session_attended: %s", e)
        abort(500, description="Error processing data.")

@app.route("/api/sessions_dna")
def sessions_dna() -> Response:
    query = """
    SELECT strftime ('%Y-%m', session_date) AS month, COUNT(session_ID) AS session_dna
    FROM Sessions
    WHERE session_status <> 'Attended'
    GROUP BY month
    ORDER BY month;
    """
    
    try:
        result = query_db(query)
        logging.debug("Query result: %s", result)
        dates = [row[0] for row in result]
        dna = [row[1] for row in result]
        return jsonify({"dates": dates, "dna": dna})
    except Exception as e:
        logging.error("Error in /api/session_dna: %s", e)
        abort(500, description="Error processing data.")


@app.route("/api/sleep_disorder")
def sleep_disorder() -> Response:
    query = """
    SELECT sleep_disorder, COUNT(person_ID) AS count_disorders
    FROM Sleep
    GROUP BY sleep_disorder
    ORDER BY count_disorders DESC;
    """
    result = query_db(query)

    disorders = [row[0] for row in result]
    counts = [row[1] for row in result]
    return jsonify({"disorders": disorders, "counts": counts})

# THIS NEEDS TO GO AT THE END
if __name__ == "__main__":
    app.run(debug=True)


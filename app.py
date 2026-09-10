from flask import Flask, render_template
import subprocess
from flask import jsonify


app=Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/start-game")
def start_game():
    try:
        subprocess.Popen(["python", "alien_invasion.py"]) 
        return jsonify({"status": "success", "message": "Game Launching..."})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
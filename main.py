from flask import Flask, request, redirect, render_template, send_file
import os
from functions import melody_maker, save_song_data, random_id

app = Flask(__name__)

@app.route("/")
def index():
  return render_template("form.html")

@app.route("/", methods=['POST', 'GET'])
def melody_maker_post():
  if request.method == 'POST':
    tonality = request.form['tonality']
    id = random_id()
    melody = melody_maker(tonality)
    save_song_data(melody, f"melodies/{id}.wav")
    return redirect(f"/view_melody/{id}")
  else:
    return redirect("/")

@app.route("/view_melody/<id>")
def view_melody(id):
  if os.path.exists(f"melodies/{id}.wav"):
    return render_template("melody.html", id=id)

@app.route("/melody_url/<id>")
def melody_url(id):
  return send_file(f"melodies/{id}.wav")

app.run(host='0.0.0.0', port=8080)

# save_song_data(melody_maker("major"), "major.wav")
# save_song_data(melody_maker("minor"), "minor.wav")
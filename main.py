from flask import Flask, render_template, request, redirect, send_file
from scrapper import get_so_jobs
from exporter import save_to_file

app = Flask("JobScrapper")

db = {}


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/report")
def report():
    word = request.args.get("word")
    if word:
        word = word.lower()
        fromDB = db.get(word)
        if fromDB:
            jobs = fromDB
        else:
            jobs = get_so_jobs(word)
            db[word] = jobs
    else:
        return redirect("/")
    return render_template(
        "report.html", resultNumber=len(jobs), searchingBy=word, jobs=jobs)

@app.route("/export")
def export():
  try:
    word = request.args.get("word")
    
    if not word:
      raise Exception()

    word = word.lower()
    jobs = db.get(word)

    if not jobs:
      raise Exception()

    save_to_file(word, jobs)

    return send_file(
      f"{word}_jobs.csv",
      as_attachment=True,
      attachment_filename=f"{word}_jobs.csv"
      )

  except:
    return redirect("/")

app.run(host="0.0.0.0")

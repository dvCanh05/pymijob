from flask import Flask, render_template
from requests_html import HTMLSession
import sqlite3


session = HTMLSession()
app = Flask(__name__)
conn = sqlite3.connect("jobdata.db")
c = conn.cursor()
c.execute('''CREATE TABLE Jobs 
				(jobname text, joburl text)''')

myjobs = []
i = 1
while i < 7:
    resp = session.get(
        "https://github.com/awesome-jobs/vietnam/issues?page={}&q=is%3Aissue+is%3Aopen".format(
            i
        )
    )
    page_html = resp.html
    jobs = page_html.find("div.flex-auto.min-width-0.p-2.pr-3.pr-md-2")
    for job in jobs:
        it_job = job.find("a", first=True).text
        job_link = "https://github.com/" + job.find("a", first=True).attrs["href"]
        c.execute('''INSERT INTO Jobs VALUES(?,?)''', (it_job, job_link))
        myjobs.append({"name": it_job, "link": job_link})
    i += 1
	
conn.commit()
conn.close()
@app.route("/")
def job():
	return render_template("index.html", jobs = myjobs)

if __name__ == "__main__":
    app.run(debug=True)


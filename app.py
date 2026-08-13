from flask import Flask, render_template, request
from pypdf import PdfReader
import re

app = Flask(__name__)


def extract_text_from_pdf(file):
    text = ""

    reader = PdfReader(file)

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


def find_skills(text):
    skills = [
        "python",
        "java",
        "c",
        "c++",
        "javascript",
        "html",
        "css",
        "sql",
        "mysql",
        "firebase",
        "flask",
        "django",
        "react",
        "node.js",
        "machine learning",
        "artificial intelligence",
        "data structures",
        "git",
        "github",
        "cloud",
        "aws",
        "docker"
    ]

    text = text.lower()

    found = []

    for skill in skills:
        if re.search(r"\b" + re.escape(skill.lower()) + r"\b", text):
            found.append(skill)

    return found


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():

    resume = request.files.get("resume")
    job_description = request.form.get("job_description", "")

    if not resume:
        return "Please upload a resume."

    try:
        resume_text = extract_text_from_pdf(resume)
    except Exception as e:
        return f"Error reading PDF: {e}"

    resume_skills = find_skills(resume_text)
    job_skills = find_skills(job_description)

    if job_skills:
        matched_skills = [
            skill for skill in job_skills
            if skill.lower() in [x.lower() for x in resume_skills]
        ]

        missing_skills = [
            skill for skill in job_skills
            if skill.lower() not in [x.lower() for x in resume_skills]
        ]

        score = int((len(matched_skills) / len(job_skills)) * 100)

    else:
        matched_skills = resume_skills
        missing_skills = []
        score = 0

    return render_template(
        "result.html",
        score=score,
        found_skills=resume_skills,
        matched_skills=matched_skills,
        missing_skills=missing_skills
    )


if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask, redirect, url_for, request, render_template, send_from_directory
import exercises_generation
import os

app = Flask(__name__)


def generate_exercise(category):
    return exercises_generation.main(category)


@app.route("/")
def index():
    return render_template("index.html")


@app.route('/generation', methods = ['POST'])
def exercise_generation():
    if request.method == 'POST':
        resource = request.form['select_corpus']
        instances = request.form['select_instances']
        difficulty = request.form['select_difficulty']
        exercise_type = request.form['exerciseType']
        teaching_goal = request.form['teachGoal']
        extra_options = request.form.getlist('extra_checkbox')

        category = str(resource)+"_"+str(instances)+"_"+str(difficulty)+"_"+str(exercise_type)+"-"+str(teaching_goal)+"_"+str(extra_options)
        generate_exercise(category)

        return redirect(url_for('semigramex_generation'))


@app.route("/semigramex_generation/")
def semigramex_generation():
    workingdir = os.path.abspath(os.getcwd())
    filepath = workingdir + '/static/files/generations/'
    return send_from_directory(filepath, 'generated_exercises.pdf')


@app.route("/semigramex_documentation/")
def semigramex_documentation():
    workingdir = os.path.abspath(os.getcwd())
    filepath = workingdir + '/static/files/'
    return send_from_directory(filepath, 'SemiGrammEx_thesis.pdf')


if __name__ == "__main__":
    app.run(debug=True)
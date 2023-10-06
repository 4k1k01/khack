from flask import Flask, render_template, request
import urllib.request as ur
import json

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        game_id = request.form['game_id']
        url = "https://play.kahoot.it/rest/kahoots/" + game_id
        try:
            q = json.loads(ur.urlopen(url).read())["questions"]
            colours = ["RED", "BLUE", "YELLOW", "GREEN"]
            questions = []

            for index, slide in enumerate(q):
                if slide.get("type") == "quiz":
                    for i in range(len(slide.get("choices"))):
                        if slide["choices"][i]["correct"]:
                            colours_list = colours[:2][::-1] if len(slide.get("choices")) == 2 else colours
                            formatted_question = "{}. {}".format(index + 1, colours_list[i])
                            questions.append(formatted_question)

            return render_template('index.html', questions=questions)
        except Exception as e:
            return render_template('index.html', error="Error fetching data. Please check the game ID.")

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

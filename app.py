from flask import Flask, render_template, request
import openai

app = Flask(__name__)
app.static_folder = 'static'
openai.api_key = ""

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    historyText = request.args.get('history')
    _list = historyText.split('#%#')
    newlist = [{"role": "system","content": "you are a helpful assistant"}]
    c = 1
    for x in _list[1:]:
        if (c & 1) != 0:
            newlist.append({"role": "user","content": x})
        else:
            newlist.append({"role": "assistant","content": x})
        c += 1
    try:
        newlist.append({"role": "user", "content": userText})

        completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        temperature=0.5,
        messages=newlist
        )
        return str(completion["choices"][0]["message"]["content"])
    except Exception as e:
        print(e)
        return e

if __name__ == "__main__":
    app.run(
      host='0.0.0.0',
      debug=True
    )
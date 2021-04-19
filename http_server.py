from flask import Flask

app = Flask(__name__)

@app.route('/<file>')
def get_file(file):
    return "File name: {}".format(file)


if __name__ == "__main__":
    app.run()
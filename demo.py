from flask import Flask

app=Flask(__name__)

@app.route('/Edit')
def edit():
    return

if __name__ == '__main__':
    app.run(debug=True)
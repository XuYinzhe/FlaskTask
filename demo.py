from flask import Flask
from flask import render_template

app=Flask(__name__)

@app.route('/edit')
def edit():
    return render_template('edit.html')

if __name__ == '__main__':
    app.run(debug=True)
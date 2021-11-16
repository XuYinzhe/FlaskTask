from flask import Flask, render_template
from markupsafe import escape

app = Flask(__name__)
'''
@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return f'User {escape(username)}'

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return f'Post {post_id}'

@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    # show the subpath after /path/
    return f'Subpath {escape(subpath)}'
'''

@app.route('/')
def hello():
    return 'hello!'

@app.route('/h1')
def hello_h1():
    return '<h1>hello!</h1>'

@app.route('/user/<username>')
def user(username):
    return f'<h1>This is {username}</h1>'

@app.route('/render')
def render():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, request, session, redirect, url_for, render_template
from scripts.vote_manager import save_vote

app = Flask(__name__)
app.secret_key = "e06d50f1d183727eba706a0ec8086620987edb1df4ce629adea2554e8708ede5"


def valid_login(username, password):
    return username == "toto" and password == "toto"


def log_the_user_in(username):
    session['username'] = username
    return redirect(url_for('index'))


@app.route('/')
def index():
    if 'username' in session:
        return render_template('index.html', logged_in=True, username=session["username"])
    return render_template('index.html', logged_in=False)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        if valid_login(request.form['username'], request.form['password']):
            return log_the_user_in(request.form['username'])
        else:
            error = 'Invalid username/password'
            return render_template('login.html', error=error)
    return render_template('login.html')


@app.route('/signin', methods=['POST', 'GET'])
def signin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        return f"Utilisateur {username} inscrit avec succès !"
    return render_template('signin.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route('/vote', methods=['POST', 'GET'])
def vote():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == "POST":
        email = request.form.get('email')
        composer = request.form.get('composer')
        username = session['username']
        if email and composer:
            save_vote(username, email, composer)
            return redirect(url_for('vote_confirmation', composer=composer))
        else:
            return "Veuillez remplir tous les champs.", 400
    return render_template('vote.html')

@app.route('/vote/confirmation')
def vote_confirmation():
    composer = request.args.get('composer', 'inconnu')
    return render_template('confirmation.html', composer=composer)

if __name__ == '__main__':
    app.run(debug=True)

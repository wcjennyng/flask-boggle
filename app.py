from flask import Flask, request, render_template, session, jsonify
from boggle import Boggle

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'

boggle_game = Boggle()

@app.route('/')
def homepage():
    """Display board"""
    board = boggle_game.make_board()
    session['board'] = board
    highscore = session.get('highscore', 0)
    playcount = session.get('playcount', 0)

    return render_template('form.html', board=board, highscore=highscore, playcount=playcount)

@app.route('/check-word')
def check_word():   
    """Checks if word is in dictionary"""
    word = request.args['word']
    board = session['board']
    result = boggle_game.check_valid_word(board, word)

    #returns JSON response
    return jsonify({'result': result})

@app.route('/score', methods=["POST"])
def post_score():
    """Posts score, displays times played, updates highest score"""
    #data sent as JSON when making axios request, using .json instead of .form
    score = request.json['score']
    highscore = session.get('highscore', 0)
    playcount = session.get('playcount', 0)

    session['highscore'] = max(score, highscore)
    session['playcount'] = playcount + 1

    return jsonify(newHighScore = score > highscore)
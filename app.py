from flask import Flask, render_template, url_for, request, redirect
from utilities import predict
from utilities.predict import predict_score
from utilities.predict import tree, forest, neural_nets
from utilities.predict import MODEL_INFO

app = Flask(__name__)
TEAM_CODE = [
				'Chennai Super Kings',
				'Delhi Capitals',
				'Kings XI Punjab',
				'Kolkata Knight Riders',
				'Mumbai Indians',
				'Rajasthan Royals',
				'Royal Challengers Bangalore',
				'Sunrisers Hyderabad'
			 ]
MODELS = {
	'Random Forest Regressor' : forest,
	'Decision Tree Regressor' : tree,
	'Neural Networks Regression' : neural_nets
}

predicted_score = None
total_predictions = 0
@app.route('/')
def index():
	return render_template('index.html', teams=TEAM_CODE, models=MODELS, score=predicted_score, info=MODEL_INFO, total=total_predictions)

@app.route('/predict', methods=['GET', 'POST'])
def predict():
	global predicted_score
	global total_predictions
	if request.method == 'POST':
		total_predictions += 1
		req = request.form
		batting_team = req['batting_team']
		bowling_team = req['bowling_team']
		runs = int(req['runs'])
		overs = float(req['overs'])
		wickets = int(req['wickets'])
		runs_last_5 = int(req['runs_last_5'])
		wickets_last_5 = int(req['wickets_last_5'])
		model = MODELS[req['model']]
		predicted_score = str(predict_score(batting_team, bowling_team, runs, wickets, overs, runs_last_5, wickets_last_5, model))
		return render_template('predict.html', score=predicted_score, info=dict(req), model=MODEL_INFO, total=total_predictions)

@app.errorhandler(404)
def error(e):
	return render_template("404.html", msg=e)

if __name__ == '__main__':
	app.run(debug=True, port=8000)
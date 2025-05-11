from flask import Flask, render_template, request
from car_recommendation import get_top_similar_cars_user_input

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/results', methods=['POST'])
def recommend():
    if request.method == 'POST':
        user_input = {
            'Make': request.form['make'],
            'Model': request.form['model'],
            'Age': int(request.form['age']),
            "KM's driven": int(request.form['kms_driven']),
            'Price': int(request.form['price']),
            'Fuel': request.form['fuel'],
            'Car Documents': request.form['car_documents'],
            'Assembly': request.form['assembly'],
            'Transmission': request.form['transmission'],
            'Air Conditioning': int(request.form.get('air_conditioning', 0)),
            'AM/FM Radio': int(request.form.get('am_fm_radio', 0)),
            'Power Steering': int(request.form.get('power_steering', 0)),
            'Front Speakers': int(request.form.get('front_speakers', 0)),
            'Power Locks': int(request.form.get('power_locks', 0))
        }

        limit = int(request.form['limit'])
        recommendations = get_top_similar_cars_user_input(user_input, limit=limit)
        return render_template('results.html', recommendations=recommendations)

if __name__ == '__main__':
    app.run(debug=True)

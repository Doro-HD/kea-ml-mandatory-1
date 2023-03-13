from flask import Flask, render_template, request
from tensorflow.keras.models import load_model
import numpy as np

app = Flask(__name__)


@app.route('/', methods=['post', 'get'])
def index_predict():
    # the nand.h5 file was created in Colab, downloaded and uploaded using Filezilla model = load_model('nand_gate.h5')
    model = load_model('NAND_GATE.h5')

    # get the two numbers from the request object
    num_one = request.form.get('num-one')
    num_two = request.form.get('num-two')

    result = None
    if num_one is not None and num_two is not None:
        arr = np.array([[float(num_one), float(num_two)]])
        result = model.predict(arr)[0][0]
        result = result > 0.5

    return render_template('index.html', result=str(result))


# will use get for the first page-load, post for the form-submit
@app.route('/james', methods=['post', 'get'])
# this function can have any name
def predict():
    translator = {
        # gender
        'Female': [1, 0],
        'Male': [0, 1],

        # religion
        'Pres': [1, 0, 0],
        'Cath': [0, 1, 0],
        'Other': [0, 0, 1],

        # politics
        '100': 'Dem',
        '010': 'Rep',
        '001': 'Ind'
    }

    # the nand.h5 file was created in Colab, downloaded and uploaded using Filezilla
    model = load_model('James_McCaffrey.h5')

    # get the two numbers from the request object
    age = request.form.get('age')
    income = request.form.get('income')
    sex = request.form.get('sex')
    religion = request.form.get('religion')

    result = 'No input(s)'
    # check if any number is missing
    if age is not None or income is not None or sex is not None or religion is not None:
        age = float('0.' + age)
        income = float('0.' + income)
        sex = translator[sex]
        religion = translator[religion]

        arr = np.array([
            [
                age,
                income,
                sex[0],
                sex[1],
                religion[0],
                religion[1],
                religion[2]

            ]
        ])
        # cast string to decimal number, and make 2d numpy array.

        predictions = model.predict(arr)
        # make new prediction

        # round the outputs and convert them a string for translation
        politics = [round(output) for output in predictions[0]]
        politics = ''.join([str(output) for output in politics])

        politics = translator[politics]

        result = politics

    return render_template('james.html', result=str(result))
    # the result is set, by asking for row=0, column=0. Then cast to string


if __name__ == '__main__':
    app.run(debug=True)

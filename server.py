import pandas as pd
import dill
from flask import Flask, jsonify, request, abort

# Load model
dill._dill._reverse_typemap['ClassType'] = type
with open('./models/predict_churn_pipeline.pkl', 'rb') as f:
    classifier = dill.load(f)

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health():
    if request.method == 'GET':
        return 'OK'

@app.route('/predict', methods=['POST'])
def apicall():
    """API Call

    Pandas dataframe (sent as a payload) from API Call
    """
    try:
        json_data = request.get_json()
        if isinstance(json_data, dict):
            json_data = [json_data]
        df = pd.DataFrame(json_data)

        #Getting the Loan_IDs separated out
        customer_ids = df['CustomerId']

    except Exception as e:
        raise e

    if df.empty:
        abort(400, 'The data is empty')
    else:
        predictions = classifier.predict(df)
        final_predictions = pd.DataFrame(list(zip(customer_ids, predictions)), 
            columns=['CustomerId', 'ExitPrediction'])

        responses = jsonify(predictions=final_predictions.to_json(orient="records"))
        responses.status_code = 200

        return (responses)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
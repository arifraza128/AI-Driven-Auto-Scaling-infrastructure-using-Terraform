from flask import Flask, render_template
import os
import socket

from autoscaling_model import build_prediction_payload, get_cloudwatch_metrics

app = Flask(__name__)

@app.route('/')
def home():
    metrics_history = get_cloudwatch_metrics()
    prediction = build_prediction_payload(metrics_history)
    return render_template("index.html", hostname=socket.gethostname(), prediction=prediction)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv("PORT", "5000")))

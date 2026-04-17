from datetime import datetime, timedelta
from functools import lru_cache
from math import pi
import os
import urllib.error
import urllib.request

import boto3
import numpy as np


SEQUENCE_LENGTH = 12
FEATURE_NAMES = ("cpu_utilization", "network_in", "network_out")
ACTION_LABELS = {
    0: "Keep current capacity",
    1: "Scale up",
    2: "Scale down",
}
DEFAULT_REGION = os.getenv("AWS_REGION", "ap-south-1")


def demo_cloudwatch_metrics():
    """Return a CloudWatch-like history that trends upward before a spike."""

    return [
        {"cpu_utilization": 41.0, "network_in": 820.0, "network_out": 540.0},
        {"cpu_utilization": 44.0, "network_in": 860.0, "network_out": 570.0},
        {"cpu_utilization": 47.0, "network_in": 915.0, "network_out": 605.0},
        {"cpu_utilization": 50.0, "network_in": 980.0, "network_out": 640.0},
        {"cpu_utilization": 53.0, "network_in": 1040.0, "network_out": 675.0},
        {"cpu_utilization": 56.0, "network_in": 1115.0, "network_out": 710.0},
        {"cpu_utilization": 60.0, "network_in": 1190.0, "network_out": 755.0},
        {"cpu_utilization": 64.0, "network_in": 1275.0, "network_out": 805.0},
        {"cpu_utilization": 68.0, "network_in": 1365.0, "network_out": 860.0},
        {"cpu_utilization": 72.0, "network_in": 1450.0, "network_out": 920.0},
        {"cpu_utilization": 76.0, "network_in": 1545.0, "network_out": 980.0},
        {"cpu_utilization": 81.0, "network_in": 1635.0, "network_out": 1045.0},
    ]


def _get_metadata_value(path):
    request = urllib.request.Request(f"http://169.254.169.254/latest/{path}")
    token_request = urllib.request.Request(
        "http://169.254.169.254/latest/api/token",
        method="PUT",
        headers={"X-aws-ec2-metadata-token-ttl-seconds": "21600"},
    )

    try:
        with urllib.request.urlopen(token_request, timeout=1) as response:
            token = response.read().decode("utf-8")
        request.add_header("X-aws-ec2-metadata-token", token)
    except (urllib.error.URLError, ValueError):
        pass

    with urllib.request.urlopen(request, timeout=1) as response:
        return response.read().decode("utf-8")


def _get_instance_id():
    return os.getenv("EC2_INSTANCE_ID") or _get_metadata_value("meta-data/instance-id")


def _get_cloudwatch_client():
    session = boto3.session.Session(region_name=DEFAULT_REGION)
    return session.client("cloudwatch")


def _fetch_metric_series(client, metric_name, instance_id):
    response = client.get_metric_statistics(
        Namespace="AWS/EC2",
        MetricName=metric_name,
        Dimensions=[{"Name": "InstanceId", "Value": instance_id}],
        StartTime=datetime.utcnow() - timedelta(hours=2),
        EndTime=datetime.utcnow(),
        Period=300,
        Statistics=["Average"],
    )

    datapoints = sorted(response.get("Datapoints", []), key=lambda item: item["Timestamp"])
    return datapoints[-SEQUENCE_LENGTH:]


def get_cloudwatch_metrics():
    try:
        instance_id = _get_instance_id()
        client = _get_cloudwatch_client()
        cpu_points = _fetch_metric_series(client, "CPUUtilization", instance_id)
        network_in_points = _fetch_metric_series(client, "NetworkIn", instance_id)
        network_out_points = _fetch_metric_series(client, "NetworkOut", instance_id)

        if not cpu_points or not network_in_points or not network_out_points:
            return demo_cloudwatch_metrics()

        combined_rows = []
        for index in range(min(len(cpu_points), len(network_in_points), len(network_out_points))):
            combined_rows.append(
                {
                    "cpu_utilization": float(cpu_points[index]["Average"]),
                    "network_in": float(network_in_points[index]["Average"]),
                    "network_out": float(network_out_points[index]["Average"]),
                }
            )

        return combined_rows[-SEQUENCE_LENGTH:]
    except Exception:
        return demo_cloudwatch_metrics()


def _generate_training_data(sample_count=1500, seed=42):
    rng = np.random.default_rng(seed)
    features = np.zeros((sample_count, SEQUENCE_LENGTH, len(FEATURE_NAMES)), dtype=np.float32)
    labels = np.zeros((sample_count,), dtype=np.int64)

    for sample_index in range(sample_count):
        baseline_cpu = rng.uniform(18, 85)
        trend = rng.uniform(-1.8, 2.2)
        season_frequency = rng.uniform(0.08, 0.22)
        phase = rng.uniform(0, 2 * pi)
        network_multiplier = rng.uniform(10.0, 18.0)
        network_balance = rng.uniform(0.7, 1.2)

        latest_cpu = baseline_cpu
        latest_network_in = baseline_cpu * network_multiplier
        latest_network_out = latest_network_in * network_balance

        for step_index in range(SEQUENCE_LENGTH):
            seasonal_shift = 8.5 * np.sin(phase + step_index * season_frequency)
            latest_cpu = np.clip(baseline_cpu + trend * step_index + seasonal_shift + rng.normal(0, 4.2), 0, 100)
            latest_network_in = max(20.0, latest_cpu * network_multiplier + rng.normal(0, 55))
            latest_network_out = max(15.0, latest_network_in * network_balance + rng.normal(0, 32))
            features[sample_index, step_index] = [latest_cpu, latest_network_in, latest_network_out]

        future_cpu = np.clip(latest_cpu + trend * 2.5 + rng.normal(0, 5.5), 0, 100)
        future_network_in = max(20.0, latest_network_in + trend * 38 + rng.normal(0, 95))
        future_network_out = max(15.0, latest_network_out + trend * 28 + rng.normal(0, 65))

        if future_cpu >= 70 or future_network_in >= 1500:
            labels[sample_index] = 1
        elif future_cpu <= 35 and future_network_in <= 650:
            labels[sample_index] = 2
        else:
            labels[sample_index] = 0

    return features, labels


def _build_model():
    return _NeuralScaler()


class _NeuralScaler:
    def __init__(self):
        self.input_size = SEQUENCE_LENGTH * len(FEATURE_NAMES)
        self.hidden_size = 24
        self.output_size = len(ACTION_LABELS)
        rng = np.random.default_rng(42)
        self.w1 = rng.normal(0, 0.15, size=(self.input_size, self.hidden_size)).astype(np.float32)
        self.b1 = np.zeros((self.hidden_size,), dtype=np.float32)
        self.w2 = rng.normal(0, 0.15, size=(self.hidden_size, self.output_size)).astype(np.float32)
        self.b2 = np.zeros((self.output_size,), dtype=np.float32)

    @staticmethod
    def _relu(values):
        return np.maximum(values, 0.0)

    @staticmethod
    def _relu_grad(values):
        return (values > 0).astype(np.float32)

    @staticmethod
    def _softmax(logits):
        shifted = logits - np.max(logits, axis=1, keepdims=True)
        exp_values = np.exp(shifted)
        return exp_values / np.sum(exp_values, axis=1, keepdims=True)

    def fit(self, features, labels, epochs=20, learning_rate=0.0025):
        flat_features = features.reshape(features.shape[0], -1)
        one_hot = np.eye(self.output_size, dtype=np.float32)[labels]

        for _ in range(epochs):
            hidden_pre = flat_features @ self.w1 + self.b1
            hidden = self._relu(hidden_pre)
            logits = hidden @ self.w2 + self.b2
            probabilities = self._softmax(logits)

            error = (probabilities - one_hot) / flat_features.shape[0]
            grad_w2 = hidden.T @ error
            grad_b2 = np.sum(error, axis=0)
            grad_hidden = (error @ self.w2.T) * self._relu_grad(hidden_pre)
            grad_w1 = flat_features.T @ grad_hidden
            grad_b1 = np.sum(grad_hidden, axis=0)

            self.w2 -= learning_rate * grad_w2
            self.b2 -= learning_rate * grad_b2
            self.w1 -= learning_rate * grad_w1
            self.b1 -= learning_rate * grad_b1

    def predict(self, features, verbose=0):
        flat_features = features.reshape(features.shape[0], -1)
        hidden = self._relu(flat_features @ self.w1 + self.b1)
        logits = hidden @ self.w2 + self.b2
        return self._softmax(logits)


@lru_cache(maxsize=1)
def get_trained_model():
    features, labels = _generate_training_data()
    model = _build_model()
    model.fit(features, labels, epochs=35, learning_rate=0.002)
    return model


def _normalize_metrics(metrics_history):
    if not metrics_history:
        metrics_history = demo_cloudwatch_metrics()

    rows = []
    for metric in metrics_history[-SEQUENCE_LENGTH:]:
        rows.append([
            float(metric["cpu_utilization"]),
            float(metric["network_in"]),
            float(metric["network_out"]),
        ])

    while len(rows) < SEQUENCE_LENGTH:
        rows.insert(0, rows[0])

    return np.asarray(rows, dtype=np.float32)


def build_prediction_payload(metrics_history):
    model = get_trained_model()
    input_batch = _normalize_metrics(metrics_history)[np.newaxis, ...]
    probabilities = model.predict(input_batch, verbose=0)[0]
    action_index = int(np.argmax(probabilities))
    latest_metrics = metrics_history[-1] if metrics_history else demo_cloudwatch_metrics()[-1]

    return {
        "action_label": ACTION_LABELS[action_index],
        "confidence": f"{float(probabilities[action_index]) * 100:.1f}%",
        "latest_cpu": f"{float(latest_metrics['cpu_utilization']):.1f}",
        "latest_network_in": f"{float(latest_metrics['network_in']):.0f}",
        "latest_network_out": f"{float(latest_metrics['network_out']):.0f}",
    }
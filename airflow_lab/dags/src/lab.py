import pandas as pd # type: ignore
from sklearn.preprocessing import MinMaxScaler # type: ignore
from sklearn.cluster import KMeans # type: ignore
from kneed import KneeLocator # type: ignore
import pickle
import os
import base64
import json
from datetime import datetime
from sklearn.metrics import silhouette_score # type: ignore

def load_data():
    """
    Loads data from a CSV file, serializes it, and returns the serialized data.
    Returns:
        str: Base64-encoded serialized data (JSON-safe).
    """
    print("We are here")
    df = pd.read_csv(os.path.join(os.path.dirname(__file__), "../data/file.csv"))
    serialized_data = pickle.dumps(df)                    # bytes
    return base64.b64encode(serialized_data).decode("ascii")  # JSON-safe string

def data_preprocessing(data_b64: str):
    """
    Deserializes base64-encoded pickled data, performs preprocessing,
    and returns base64-encoded pickled clustered data.
    """
    # decode -> bytes -> DataFrame
    data_bytes = base64.b64decode(data_b64)
    df = pickle.loads(data_bytes)

    df = df.dropna()
    clustering_data = df[["BALANCE", "PURCHASES", "CREDIT_LIMIT"]]

    min_max_scaler = MinMaxScaler()
    clustering_data_minmax = min_max_scaler.fit_transform(clustering_data)

    # bytes -> base64 string for XCom
    clustering_serialized_data = pickle.dumps(clustering_data_minmax)
    return base64.b64encode(clustering_serialized_data).decode("ascii")


def build_save_model(data_b64: str, filename: str):
    """
    Builds a KMeans model on the preprocessed data and saves it.
    Returns the SSE list (JSON-serializable).
    """
    # decode -> bytes -> numpy array
    data_bytes = base64.b64decode(data_b64)
    df = pickle.loads(data_bytes)

    kmeans_kwargs = {"init": "random", "n_init": 10, "max_iter": 300, "random_state": 42}
    sse = []
    for k in range(1, 50):
        kmeans = KMeans(n_clusters=k, **kmeans_kwargs)
        kmeans.fit(df)
        sse.append(kmeans.inertia_)

    # NOTE: This saves the last-fitted model (k=49), matching your original intent.
    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "model")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, filename)
    with open(output_path, "wb") as f:
        pickle.dump(kmeans, f)

    return sse  # list is JSON-safe


def load_model_elbow(filename: str, sse: list):
    """
    Loads the saved model and uses the elbow method to report k.
    Returns the first prediction (as a plain int) for test.csv.
    """
    # load the saved (last-fitted) model
    output_path = os.path.join(os.path.dirname(__file__), "../model", filename)
    loaded_model = pickle.load(open(output_path, "rb"))

    # elbow for information/logging
    kl = KneeLocator(range(1, 50), sse, curve="convex", direction="decreasing")
    print(f"Optimal no. of clusters: {kl.elbow}")

    # predict on raw test data (matches your original code)
    df = pd.read_csv(os.path.join(os.path.dirname(__file__), "../data/test.csv"))
    pred = loaded_model.predict(df)[0]

    # ensure JSON-safe return
    try:
        return int(pred)
    except Exception:
        # if not numeric, still return a JSON-friendly version
        return pred.item() if hasattr(pred, "item") else pred
    
def generate_dashboard(data_b64: str, sse: list, optimal_k: int):
    """
    Generates an HTML dashboard with elbow curve, cluster distribution,
    and model metrics.
    """
    import plotly.graph_objects as go # type: ignore
    from plotly.subplots import make_subplots # type: ignore

    # Decode data
    data_bytes = base64.b64decode(data_b64)
    data = pickle.loads(data_bytes)

    # Compute silhouette score using optimal_k
    kmeans_final = KMeans(n_clusters=optimal_k, init="random", n_init=10,
                          max_iter=300, random_state=42)
    labels = kmeans_final.fit_predict(data)
    sil_score = silhouette_score(data, labels)

    # Cluster distribution counts
    unique, counts = zip(*sorted(
        zip(*[list(x) for x in [range(optimal_k),
        [list(labels).count(i) for i in range(optimal_k)]]])
    ))

    # Build subplots
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=("Elbow Curve", "Cluster Distribution")
    )

    # Elbow curve
    fig.add_trace(go.Scatter(
        x=list(range(1, 50)), y=sse,
        mode='lines+markers', name='SSE',
        line=dict(color='royalblue')
    ), row=1, col=1)
    fig.add_vline(x=optimal_k, line_dash="dash", line_color="red",
                  annotation_text=f"k={optimal_k}", row=1, col=1)

    # Cluster distribution
    fig.add_trace(go.Bar(
        x=[f"Cluster {i}" for i in unique],
        y=list(counts), name='Points per Cluster',
        marker_color='teal'
    ), row=1, col=2)

    fig.update_layout(
        title_text=f"Airflow_Lab1 — K-Means Dashboard | Run: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC",
        height=500
    )

    # Metrics summary
    metrics_html = f"""
    <div style="font-family:Arial; padding:20px; background:#f4f4f4; border-radius:8px; margin:20px;">
        <h2>Model Metrics</h2>
        <table style="border-collapse:collapse; width:400px;">
            <tr><td style="padding:8px;"><b>Optimal K (Elbow)</b></td><td>{optimal_k}</td></tr>
            <tr><td style="padding:8px;"><b>Silhouette Score</b></td><td>{sil_score:.4f}</td></tr>
            <tr><td style="padding:8px;"><b>Min SSE</b></td><td>{min(sse):.4f}</td></tr>
            <tr><td style="padding:8px;"><b>Max SSE</b></td><td>{max(sse):.4f}</td></tr>
            <tr><td style="padding:8px;"><b>Generated At</b></td><td>{datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC</td></tr>
        </table>
    </div>
    """

    full_html = fig.to_html(full_html=True, include_plotlyjs='cdn').replace(
        "</body>", metrics_html + "</body>"
    )

    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "dashboard")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "dashboard.html")
    with open(output_path, "w") as f:
        f.write(full_html)

    print(f"Dashboard saved to {output_path}")
    return output_path
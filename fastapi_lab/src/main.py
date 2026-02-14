from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
from predict import predict_data, predict_proba, get_model

app = FastAPI(title="Iris Classifier API", version="1.0.0")

# Class mapping for Iris dataset
SPECIES = {0: "setosa", 1: "versicolor", 2: "virginica"}

class IrisData(BaseModel):
    """
    Request body schema for Iris measurements.
    """
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float

class IrisResponse(BaseModel):
    """
    Response schema returned by /predict.
    """
    class_id: int
    species: str
    probabilities: list[float]
    confidence: float

@app.get("/", status_code=status.HTTP_200_OK)
async def health_ping():
    """
    Simple health check endpoint.
    """
    return {"status": "healthy"}

@app.get("/model-info")
async def model_info():
    """
    Returns model metadata and hyperparameters.
    """
    model = get_model()
    return {
        "model_type": type(model).__name__,
        "params": model.get_params()
    }

@app.post("/predict", response_model=IrisResponse)
async def predict_iris(iris_features: IrisData):
    """
    Predict the iris flower species based on measurements.
    """
    try:
        X = [[
            iris_features.sepal_length,
            iris_features.sepal_width,
            iris_features.petal_length,
            iris_features.petal_width
        ]]

        pred = int(predict_data(X)[0])
        probs = predict_proba(X)[0].tolist()
        conf = float(max(probs))

        return IrisResponse(
            class_id=pred,
            species=SPECIES[pred],
            probabilities=probs,
            confidence=conf
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
# FastAPI Lab 1 — Iris Decision Tree API (Enhanced Version)

## Lab Overview

This lab demonstrates how to expose a trained Machine Learning model as a REST API using **FastAPI** and serve it with **Uvicorn**.

The project involves:

1. Training a Decision Tree Classifier on the Iris dataset.
2. Saving the trained model as `iris_model.pkl`.
3. Building API endpoints to serve predictions.
4. Testing the API using Swagger UI (`/docs`).

After completing the base lab requirements, additional enhancements were implemented to improve performance, usability, and professionalism of the API.

---

# Part 1 — Base Lab Implementation

## Objective

The goal of the base lab was to:

- Train a Decision Tree Classifier on the Iris dataset
- Save the model as a `.pkl` file
- Create a FastAPI application
- Expose a `/predict` endpoint
- Serve the application using `uvicorn`


## Base Workflow Followed

### 1. Train the Model

Inside `train.py`:

- Loaded Iris dataset
- Trained a `DecisionTreeClassifier`
- Saved model to: 'model/iris_model.pkl'

### 2. Create FastAPI Application

In main.py:

	•	Created FastAPI instance
  
	•	Defined request body using Pydantic
  
	•	Defined /predict endpoint
  
	•	Loaded model and returned class prediction

  ### 3. Run the Server
  uvicorn main:app --reload
  Swagger UI accessed at: http://127.0.0.1:8000/docs

  ### 4. Outcome (Without Enhancements)
  
  The base implementation successfully:

  {
  "sepal_length": 5.1,
  "sepal_width": 3.5,
  "petal_length": 1.4,
  "petal_width": 0.2
}


Returned predicted class:


{
  "response": 0
}


Where:

	•	0 = setosa
  
	•	1 = versicolor
  
	•	2 = virginica
  

The API worked correctly and returned HTTP 200 responses.


![image1](https://github.com/user-attachments/assets/ec8807ae-ee3b-4c2a-814e-be0ea07d636e)

![image2](https://github.com/user-attachments/assets/6fd8e38a-b15f-402b-8b0d-bc4683db62d2)

![image3](https://github.com/user-attachments/assets/189df2f3-ff09-45cc-836f-355248fccbc1)

![image4](https://github.com/user-attachments/assets/e5dfe03b-1020-424b-8e8d-ed1d3f34e409)

![image5](https://github.com/user-attachments/assets/39c0bb92-54f3-4648-a05d-e3e7d732e3a3)


### Part 2 — Enhancements Added

After completing the lab requirements, the API was improved with multiple enhancements.

###  Enhancement 1 — Model Caching (Performance Optimization)

Problem: Originally, the model was loaded on every prediction request.


Solution: Used @lru_cache(maxsize=1) to load the model once and reuse it.


Implemented In: src/predict.py


Code Improvement:

@lru_cache(maxsize=1)
def get_model():
    return joblib.load(MODEL_PATH)


Benefit:

	•	Reduced unnecessary disk reads
  
	•	Improved performance
  
	•	Production-ready pattern

### Enhancement 2 — Enhanced Prediction Response

Problem: Base lab only returned: { "response": 0 } - This is not user-friendly.

Solution: Enhanced /predict to return:

	•	class_id
  
	•	species name
  
	•	probabilities
  
	•	confidence score
  

Implemented In: src/main.py

New Response Format:

{
  "class_id": 0,
  "species": "setosa",
  "probabilities": [1.0, 0.0, 0.0],
  "confidence": 1.0
}

Benefit:

	•	More informative
  
	•	More interpretable
  
	•	More realistic ML API response

### Enhancement 3 — Added /model-info Endpoint

Purpose:

Expose model metadata and hyperparameters.

Endpoint: GET /model-info

Implemented In: src/main.py

{
  "model_type": "DecisionTreeClassifier",
  "params": {
    "criterion": "gini",
    "max_depth": null,
    ...
  }
}

Benefit:
	•	Transparency
	•	Debugging support
	•	Production-style monitoring endpoint

### Enhancement 4 — Health Check Endpoint

Endpoint: GET /

Purpose:

Quick API status check.

Response: {
  "status": "healthy"
}

Implemented In: src/main.py

### Outcomes After Enhancements

With enhancements, the API now:

	• Loads model only once
  
	•	Returns interpretable predictions
  
	•	Provides probability distribution
  
	•	Returns confidence score
  
	•	Exposes model hyperparameters
  
	•	Includes health check endpoint
  
	•	Follows production-ready API design patterns


![image6](https://github.com/user-attachments/assets/36fcfed2-2165-46cb-aaf2-6494295e3c98)

![image7](https://github.com/user-attachments/assets/7ee7a3e1-7faa-489c-a647-a86a527c435b)

![image8](https://github.com/user-attachments/assets/c6c7fef6-ba3b-411b-8073-b0642b14fc04)







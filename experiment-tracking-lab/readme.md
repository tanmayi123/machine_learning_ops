Experiment Tracking with Weights & Biases and XGBoost

Overview

This lab demonstrates experiment tracking for a machine learning workflow using Weights & Biases (W&B). An XGBoost multi-class classifier is trained on the UCI Dermatology dataset, and experiments are tracked, compared, and analyzed.

The goal is to build a reproducible and structured experimentation pipeline similar to real-world ML workflows.

Project Structure

.
├── notebook.ipynb
├── README.md

Dataset

	1. Source: UCI Machine Learning Repository
  
	2. Dataset: Dermatology
  
	3. Task: Multi-class classification (6 classes)
  
	4. Preprocessing:
  
	5. Missing values handled
  
	6. Labels converted to 0–5 range
  


Replication of Original Lab

The following steps were implemented to replicate the base lab:

	•	Installed required libraries (wandb, xgboost, scikit-learn)
  
	•	Logged into Weights & Biases

	•	Downloaded and loaded the dataset
  
	•	Split the dataset into training and testing sets
  
	•	Trained an XGBoost model using default hyperparameters
  
	•	Logged:
  
	•	Training and testing loss (mlogloss)
  
	•	Accuracy
  
	•	Error rate
  
	•	Training vs testing performance curves



Enhancements

1. Improved Data Handling

	•	Used train_test_split with stratification to preserve class distribution
	•	Added fixed random_state for reproducibility



2. Advanced Evaluation Metrics

Additional evaluation metrics were included:
	•	Precision (weighted)
	•	Recall (weighted)
	•	F1-score (weighted)
	•	Error rate



3. Hyperparameter Experimentation

Multiple experiments were conducted using different combinations of:
	•	Learning rate (eta): 0.01, 0.1, 0.3
	•	Max depth: 3, 5, 7

Each configuration was tracked as a separate W&B run for comparison.



4. Experiment Tracking with W&B

The following were tracked and visualized:
	•	Train vs test loss curves
	•	Accuracy, precision, recall, and F1-score
	•	Error rate
	•	Comparison across multiple runs



5. Feature Importance
	•	Logged feature importance for trained models
	•	Enabled interpretability of model decisions



6. Model Versioning (Artifacts)
	•	Saved trained models
	•	Logged models as W&B artifacts
	•	Enabled reproducibility and version control



Results

	•	Higher learning rates (0.3) with deeper trees (depth = 7) performed best
  
	•	Lower learning rates resulted in more stable but slower convergence
  
	•	Slight overfitting observed in deeper models (train loss < test loss)
  
	•	F1-score remained stable across top-performing configurations



Tech Stack
	•	Python
	•	XGBoost
	•	Scikit-learn
	•	Weights & Biases (W&B)
	•	NumPy

How to Run
  Install dependencies : pip install wandb xgboost scikit-learn numpy pandas
  Login to W&B : wandb login
  Run the notebook : wb_lab.ipynb

  Conclusion

This lab demonstrates a complete experiment tracking workflow, including:
	•	Model training
	•	Metric logging
	•	Hyperparameter comparison
	•	Visualization
	•	Model versioning

It reflects a practical approach to managing machine learning experiments in a structured and reproducible manner.

How to Run

1. Install dependencies = pip install wandb xgboost scikit-learn numpy pandas
2. Login to W&B = wandb login
3. Run the notebook = wb_lab.ipynb

![WhatsApp Image 2026-03-28 at 2 28 15 PM](https://github.com/user-attachments/assets/5f7b772b-e1bb-4fd9-9b03-281557c3e2e4)

<img width="1512" height="820" alt="Screenshot 2026-03-28 at 3 53 10 PM" src="https://github.com/user-attachments/assets/247c0a93-44a4-482e-a300-416026f3ffa1" />



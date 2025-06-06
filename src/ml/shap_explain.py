from shap import TreeExplainer
import numpy as np

def explain_model_predictions(model, X, feature_names):
    """
    Explain model predictions using SHAP values.

    Parameters:
    - model: The trained machine learning model.
    - X: The input features for which to explain predictions.
    - feature_names: The names of the features.

    Returns:
    - shap_values: The SHAP values for the input features.
    - feature_importance: The mean absolute SHAP values for feature importance.
    """
    explainer = TreeExplainer(model)
    shap_values = explainer.shap_values(X)

    # Calculate feature importance as the mean absolute SHAP values
    feature_importance = np.abs(shap_values).mean(axis=0)

    return shap_values, feature_importance

def summarize_explanation(shap_values, feature_names):
    """
    Summarize SHAP values for a single prediction.

    Parameters:
    - shap_values: The SHAP values for a single prediction.
    - feature_names: The names of the features.

    Returns:
    - summary: A dictionary summarizing the SHAP values and feature contributions.
    """
    summary = {}
    for i, feature in enumerate(feature_names):
        summary[feature] = shap_values[i]
    
    return summary
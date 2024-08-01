import streamlit as st
import pandas as pd
import numpy as np

# Generate a dataframe with the required columns
data = {
    'member_id': range(1, 101),
    'age': np.random.randint(18, 85, size=100),
    'gender': np.random.choice(['Male', 'Female'], 100),
    'allowed_pmpm': np.random.uniform(100, 5000, size=100)
}

df = pd.DataFrame(data)

# Define a list of real chronic conditions
chronic_conditions = [
    'Diabetes', 'Hypertension', 'Chronic Kidney Disease', 'Asthma', 
    'COPD', 'Heart Failure', 'Depression', 'Arthritis'
]

# Assign real chronic condition names to the dataframe
df['chronic_condition'] = np.random.choice(chronic_conditions, 100)

# Define criteria for categorizing claimants
def categorize_claimant(row):
    if row['allowed_pmpm'] > 3000:
        return 'Impactable high cost claimant'
    elif row['allowed_pmpm'] > 2000:
        return 'Unavoidable high cost claimant'
    elif row['allowed_pmpm'] > 1000:
        return 'Future high cost claimant'
    else:
        return 'Stable low cost claimant'

df['claimant_category'] = df.apply(categorize_claimant, axis=1)

# Add a column for predicted high cost level
np.random.seed(42)  # For reproducibility
df['predicted_high_cost_level'] = np.random.rand(100)

# Adjust predicted high cost level based on category
def adjust_prediction(row):
    if row['claimant_category'] == 'Impactable high cost claimant':
        return np.random.uniform(0.3, 0.6)
    elif row['claimant_category'] == 'Unavoidable high cost claimant':
        return np.random.uniform(0.7, 1.0)
    elif row['claimant_category'] == 'Future high cost claimant':
        return np.random.uniform(0.7, 1.0)
    else:
        return np.random.uniform(0.0, 0.3)

df['predicted_high_cost_level'] = df.apply(adjust_prediction, axis=1)
df['predicted_high_cost_level'] = df['predicted_high_cost_level'].round(2)

# Streamlit application
st.title('Healthcare Data Analysis')

# Select chronic condition
chronic_condition = st.selectbox('Select Chronic Condition', options=chronic_conditions)

# Select high cost category
high_cost_categories = [
    'Impactable high cost claimant', 'Unavoidable high cost claimant', 
    'Future high cost claimant', 'Stable low cost claimant'
]
high_cost_category = st.selectbox('Select High Cost Category', options=high_cost_categories)

# Filter the dataframe based on selections
filtered_df = df[(df['chronic_condition'] == chronic_condition) & (df['claimant_category'] == high_cost_category)]

# Display the filtered dataframe
st.dataframe(filtered_df)

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
st.title('High Cost Claimants')

st.markdown("""
Below is high cost clamaint prediction demo. We predict the probability of a being a high cost claimant (e.g., higiher allowed PMPM relative to their peers). We created four categories to help users identify which members are impactable:

Impactable high cost claimant: Currently high cost claimant; however, predicted to drop in the future. Users should target these members as they are likely to have lower costs in the future.

Unavoidable high cost claimant: Members who are currently high cost and predicted to stay high cost. These are members users may want to consider ignoring since there is little opportunity for improvement.

Future high cost claimants: Members who current low cost; however, are predicted to become high cost. Users may want to target these members as they could become high cost claimants in the future.

Stable low cost members: Members with current low costs and predicted to stay low. No intervention with these members is likely necessary.
""")


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

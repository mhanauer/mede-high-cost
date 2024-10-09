import streamlit as st
import pandas as pd
import numpy as np

# Set a seed for reproducibility
np.random.seed(42)

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

# Calculate the default 75th percentile for allowed_pmpm
default_high_cost_threshold = np.percentile(df['allowed_pmpm'], 75)

# Allow the user to set the allowed PMPM threshold
allowed_pmpm_threshold = st.number_input(
    'Set the allowed PMPM threshold for high cost claimants',
    min_value=0.0,
    value=float(default_high_cost_threshold),
    step=100.0
)

# Add a column for current high cost claimant based on user-defined threshold
df['current_high_cost_claimant'] = df['allowed_pmpm'] > allowed_pmpm_threshold

# Generate 'predicted_allowed_pmpm' by applying a random growth factor
df['predicted_allowed_pmpm'] = df['allowed_pmpm'] * (1 + np.random.normal(0, 0.1, size=100))

# Ensure representation in all categories
# Manually set values for some rows to guarantee all categories
df.loc[0:10, 'allowed_pmpm'] = allowed_pmpm_threshold + 1000  # Currently high cost
df.loc[0:5, 'predicted_allowed_pmpm'] = allowed_pmpm_threshold - 1000  # Predicted to drop below threshold
df.loc[6:10, 'predicted_allowed_pmpm'] = allowed_pmpm_threshold + 1000  # Predicted to stay above threshold
df.loc[11:20, 'allowed_pmpm'] = allowed_pmpm_threshold - 1000  # Currently low cost
df.loc[11:15, 'predicted_allowed_pmpm'] = allowed_pmpm_threshold + 1000  # Predicted to rise above threshold
df.loc[16:20, 'predicted_allowed_pmpm'] = allowed_pmpm_threshold - 1000  # Predicted to stay below threshold

# Define criteria for categorizing claimants based on user-selected threshold
def categorize_claimant(row):
    if row['current_high_cost_claimant']:
        if row['predicted_allowed_pmpm'] <= allowed_pmpm_threshold:
            return 'Wait and see high cost claimant'
        else:
            return 'Unavoidable high cost claimant'
    else:
        if row['predicted_allowed_pmpm'] > allowed_pmpm_threshold:
            return 'Impactable high cost claimant'
        else:
            return 'Stable low cost claimant'

# Apply the categorization
df['claimant_category'] = df.apply(categorize_claimant, axis=1)

# Streamlit application
st.title('High Cost Claimants')

st.markdown(f"""
Below is a high-cost claimant prediction demo. We predict the future allowed PMPM for members. We created categories to help users identify which members are impactable:

- **Wait and see high cost claimant**: Currently high-cost (allowed PMPM greater than **{allowed_pmpm_threshold}**) and predicted to drop below the threshold in the future. Users can leave these members alone as they are likely to get better on their own.
- **Unavoidable high cost claimant**: Currently high-cost (allowed PMPM greater than **{allowed_pmpm_threshold}**) and

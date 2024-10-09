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

# Add a column for predicted high cost level
df['predicted_high_cost_level'] = np.random.uniform(0, 1, size=100)

# Ensure representation in all categories
# Manually set values for some rows to guarantee all categories
df.loc[0:10, 'allowed_pmpm'] = default_high_cost_threshold + 1000  # Ensure they are high cost
df.loc[0:5, 'predicted_high_cost_level'] = 0.6  # Wait and see high cost
df.loc[6:10, 'predicted_high_cost_level'] = 0.8  # Unavoidable high cost
df.loc[11:20, 'allowed_pmpm'] = default_high_cost_threshold - 1000  # Ensure they are low cost
df.loc[11:15, 'predicted_high_cost_level'] = 0.8  # Impactable high cost
df.loc[16:20, 'predicted_high_cost_level'] = 0.6  # Stable low cost

# Streamlit application
st.title('High Cost Claimants')

# Allow the user to set the allowed PMPM threshold
allowed_pmpm_threshold = st.number_input(
    'Set the allowed PMPM threshold for current high cost claimants',
    min_value=0.0,
    value=float(default_high_cost_threshold),
    step=100.0
)

# Allow the user to set the prediction threshold
prediction_threshold = st.number_input(
    'Set the prediction threshold for future high cost claimants (0 to 1)',
    min_value=0.0,
    max_value=1.0,
    value=0.7,
    step=0.01
)

# Add a column for current high cost claimant based on user-defined threshold
df['current_high_cost_claimant'] = df['allowed_pmpm'] > allowed_pmpm_threshold

st.markdown(f"""
Below is a high-cost claimant prediction demo. We predict the probability of being a high-cost claimant (e.g., higher allowed PMPM relative to their peers). We created categories to help users identify which members are impactable:

- **Wait and see high cost claimant**: Currently high-cost (allowed PMPM greater than **{allowed_pmpm_threshold}**) and predicted to drop in the future (prediction value is below the selected threshold of **{prediction_threshold}**). Users can leave these members alone as they are likely to get better on their own.
- **Unavoidable high cost claimant**: Currently high-cost (allowed PMPM greater than **{allowed_pmpm_threshold}**) and predicted to stay high-cost (prediction value is at or above the selected threshold of **{prediction_threshold}**). Users may target these members for case management or "laser" them in stop loss.
- **Impactable high cost claimants**: Currently low-cost (allowed PMPM less than or equal to **{allowed_pmpm_threshold}**) but predicted to become high-cost in the future (prediction value is at or above the selected threshold of **{prediction_threshold}**). Users may want to target these members as they could become high-cost claimants.
- **Stable low cost members**: Currently low-cost (allowed PMPM less than or equal to **{allowed_pmpm_threshold}**) and predicted to stay low (prediction value is below the selected threshold of **{prediction_threshold}**). No intervention with these members is likely necessary.
""")

# Define criteria for categorizing claimants based on user-selected thresholds
def categorize_claimant(row):
    if row['current_high_cost_claimant']:
        if row['predicted_high_cost_level'] < prediction_threshold:
            return 'Wait and see high cost claimant'
        else:
            return 'Unavoidable high cost claimant'
    else:
        if row['predicted_high_cost_level'] >= prediction_threshold:
            return 'Impactable high cost claimant'
        else:
            return 'Stable low cost claimant'

# Apply the categorization
df['claimant_category'] = df.apply(categorize_claimant, axis=1)

# Select chronic condition
chronic_condition = st.selectbox('Select Chronic Condition', options=chronic_conditions)

# Select high cost category
high_cost_categories = [
    'Wait and see high cost claimant', 'Unavoidable high cost claimant', 
    'Impactable high cost claimant', 'Stable low cost claimant'
]
high_cost_category = st.selectbox('Select High Cost Category', options=high_cost_categories)

# Filter the dataframe based on selections
filtered_df = df[
    (df['chronic_condition'] == chronic_condition) & 
    (df['claimant_category'] == high_cost_category)
].round(2)

# Display the filtered dataframe
st.dataframe(filtered_df)

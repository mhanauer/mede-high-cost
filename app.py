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

# Generate predicted_allowed_pmpm
df['predicted_allowed_pmpm'] = df['allowed_pmpm'] * np.random.uniform(0.8, 1.2, size=100)

# Ensure representation in all categories
# Manually set values for some rows to guarantee all categories

# For 'Wait and see high cost claimant': currently high cost, predicted low cost
df.loc[0:5, 'allowed_pmpm'] = default_high_cost_threshold + 1000  # High cost now
df.loc[0:5, 'predicted_allowed_pmpm'] = default_high_cost_threshold - 1000  # Predicted low cost

# For 'Unavoidable high cost claimant': currently high cost, predicted high cost
df.loc[6:10, 'allowed_pmpm'] = default_high_cost_threshold + 1000  # High cost now
df.loc[6:10, 'predicted_allowed_pmpm'] = default_high_cost_threshold + 1000  # Predicted high cost

# For 'Impactable high cost claimant': currently low cost, predicted high cost
df.loc[11:15, 'allowed_pmpm'] = default_high_cost_threshold - 1000  # Low cost now
df.loc[11:15, 'predicted_allowed_pmpm'] = default_high_cost_threshold + 1000  # Predicted high cost

# For 'Stable low cost claimant': currently low cost, predicted low cost
df.loc[16:20, 'allowed_pmpm'] = default_high_cost_threshold - 1000  # Low cost now
df.loc[16:20, 'predicted_allowed_pmpm'] = default_high_cost_threshold - 1000  # Predicted low cost

# Streamlit application
st.title('High Cost Claimants')

# Allow the user to set the allowed PMPM threshold
allowed_pmpm_threshold = st.number_input(
    'Set the allowed PMPM threshold for high cost claimants',
    min_value=0.0,
    value=float(default_high_cost_threshold),
    step=100.0
)

# Add a column for current high cost claimant based on user-defined threshold
df['current_high_cost_claimant'] = df['allowed_pmpm'] > allowed_pmpm_threshold

# Add a column for predicted high cost claimant based on predicted_allowed_pmpm
df['predicted_high_cost_claimant'] = df['predicted_allowed_pmpm'] > allowed_pmpm_threshold

st.markdown(f"""
Below is a high-cost claimant prediction demo. We predict the allowed PMPM for each member. We created categories to help users identify which members are impactable:

- **Wait and see high cost claimant**: Currently high-cost (allowed PMPM greater than **{allowed_pmpm_threshold}**) and predicted to drop in the future (predicted allowed PMPM is less than or equal to the threshold **{allowed_pmpm_threshold}**). Users can leave these members alone as they are likely to get better on their own.
- **Unavoidable high cost claimant**: Currently high-cost (allowed PMPM greater than **{allowed_pmpm_threshold}**) and predicted to stay high-cost (predicted allowed PMPM is greater than **{allowed_pmpm_threshold}**). Users may target these members for case management or "laser" them in stop loss.
- **Impactable high cost claimants**: Currently low-cost (allowed PMPM less than or equal to **{allowed_pmpm_threshold}**) but predicted to become high-cost in the future (predicted allowed PMPM is greater than **{allowed_pmpm_threshold}**). Users may want to target these members as they could become high-cost claimants.
- **Stable low cost members**: Currently low-cost (allowed PMPM less than or equal to **{allowed_pmpm_threshold}**) and predicted to stay low (predicted allowed PMPM is less than or equal to **{allowed_pmpm_threshold}**). No intervention with these members is likely necessary.
""")

# Define criteria for categorizing claimants based on user-selected threshold
def categorize_claimant(row):
    if row['current_high_cost_claimant']:
        if row['predicted_high_cost_claimant']:
            return 'Unavoidable high cost claimant'
        else:
            return 'Wait and see high cost claimant'
    else:
        if row['predicted_high_cost_claimant']:
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

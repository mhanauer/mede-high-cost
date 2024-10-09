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
    'allowed_pmpm': np.random.uniform(5000, 15000, size=100)  # Adjusted range to center around 10,000
}

df = pd.DataFrame(data)

# Round 'allowed_pmpm' to the nearest dollar
df['allowed_pmpm'] = df['allowed_pmpm'].round(0).astype(int)

# Define a list of real chronic conditions
chronic_conditions = [
    'Diabetes', 'Hypertension', 'Chronic Kidney Disease', 'Asthma',
    'COPD', 'Heart Failure', 'Depression', 'Arthritis'
]

# Assign real chronic condition names to the dataframe
df['chronic_condition'] = np.random.choice(chronic_conditions, 100)

# Generate 'predicted_allowed_pmpm' and round to the nearest dollar
df['predicted_allowed_pmpm'] = df['allowed_pmpm'] * np.random.uniform(0.8, 1.2, size=100)
df['predicted_allowed_pmpm'] = df['predicted_allowed_pmpm'].round(0).astype(int)

# Ensure representation in all categories
# For 'Unavoidable high cost claimant': currently high cost, predicted high cost
df.loc[0:4, 'allowed_pmpm'] = 15000  # High cost now (>10,000)
df.loc[0:4, 'predicted_allowed_pmpm'] = 15000  # Predicted high cost (>10,000)

# For 'Impactable high cost claimant': currently low cost, predicted high cost
df.loc[5:9, 'allowed_pmpm'] = 8000  # Low cost now (≤10,000)
df.loc[5:9, 'predicted_allowed_pmpm'] = 15000  # Predicted high cost (>10,000)

# For 'Wait and see high cost claimant': currently high cost, predicted low cost
df.loc[10:14, 'allowed_pmpm'] = 15000  # High cost now (>10,000)
df.loc[10:14, 'predicted_allowed_pmpm'] = 8000  # Predicted low cost (≤10,000)

# For 'Stable low cost claimant': currently low cost, predicted low cost
df.loc[15:19, 'allowed_pmpm'] = 8000  # Low cost now (≤10,000)
df.loc[15:19, 'predicted_allowed_pmpm'] = 8000  # Predicted low cost (≤10,000)

# Streamlit application
st.title('High Cost Claimants')

# Allow the user to set the allowed PMPM threshold
allowed_pmpm_threshold = st.number_input(
    'Set the allowed PMPM threshold for high cost claimants',
    min_value=0.0,
    value=10000.0,
    step=100.0
)

# Convert threshold to integer for consistency
allowed_pmpm_threshold = int(allowed_pmpm_threshold)

# Add a column for current high cost claimant based on user-defined threshold
df['current_high_cost_claimant'] = df['allowed_pmpm'] > allowed_pmpm_threshold

# Add a column for predicted high cost claimant based on predicted_allowed_pmpm
df['predicted_high_cost_claimant'] = df['predicted_allowed_pmpm'] > allowed_pmpm_threshold

st.markdown(f"""
Below is a high-cost claimant prediction demo. We predict the allowed PMPM for each member. We created categories to help users identify which members are impactable:

- **Wait and see high cost claimant**: Currently high-cost (allowed PMPM greater than **{allowed_pmpm_threshold:,}**) and predicted to drop in the future (predicted allowed PMPM is less than or equal to **{allowed_pmpm_threshold:,}**). Users can leave these members alone as they are likely to get better on their own.
- **Unavoidable high cost claimant**: Currently high-cost (allowed PMPM greater than **{allowed_pmpm_threshold:,}**) and predicted to stay high-cost (predicted allowed PMPM is greater than **{allowed_pmpm_threshold:,}**). Users may target these members for case management or "laser" them in stop loss.
- **Impactable high cost claimants**: Currently low-cost (allowed PMPM less than or equal to **{allowed_pmpm_threshold:,}**) but predicted to become high-cost in the future (predicted allowed PMPM is greater than **{allowed_pmpm_threshold:,}**). Users may want to target these members as they could become high-cost claimants.
- **Stable low cost members**: Currently low-cost (allowed PMPM less than or equal to **{allowed_pmpm_threshold:,}**) and predicted to stay low (predicted allowed PMPM is less than or equal to **{allowed_pmpm_threshold:,}**). No intervention with these members is likely necessary.
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
]

# Display the filtered dataframe
st.dataframe(filtered_df)

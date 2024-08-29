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

# Calculate the 75th percentile for allowed_pmpm
high_cost_threshold = np.percentile(df['allowed_pmpm'], 75)

# Add a column for current high cost claimant based on the 75th percentile
df['current_high_cost_claimant'] = df['allowed_pmpm'] > high_cost_threshold

# Add a column for predicted high cost level
np.random.seed(42)  # For reproducibility
df['predicted_high_cost_level'] = np.random.uniform(0, 1, size=100)

# Define criteria for categorizing claimants
def categorize_claimant(row):
    if row['current_high_cost_claimant']:
        if row['predicted_high_cost_level'] < 0.7:
            return 'Wait and see high cost claimant'
        else:
            return 'Unavoidable high cost claimant'
    elif not row['current_high_cost_claimant']:
        if row['predicted_high_cost_level'] >= 0.7:
            return 'Impactable high cost claimant'
        else:
            return 'Stable low cost claimant'

df['claimant_category'] = df.apply(categorize_claimant, axis=1)

# Streamlit application
st.title('High Cost Claimants')
st.markdown("""
Below is a high-cost claimant prediction demo. We predict the probability of being a high-cost claimant (e.g., higher allowed PMPM relative to their peers). We created categories to help users identify which members are impactable:

- **Current high-cost claimant**: Members who are in the 75th percentile or above for allowed PMPM. These members are considered high-cost based on current data.
- **Wait and see high cost claimant**: Currently high-cost and predicted to drop in the future (prediction value is at or above the 70th percentile). Users can leave these members alone as they are likely to get better on their own.
- **Recurring high cost claimant**: Currently high-cost and predicted to stay high-cost (member predicted to be between 70th and 100th percentile of predicted costs). Users may target these members for case management or "laser" them in stop loss.
- **Impactable high cost claimants**: Currently low-cost but predicted to become high-cost in the future (ember predicted to be between 70th and 100th percentile of predicted costs). Users may want to target these members as they could become high-cost claimants.
- **Stable low cost members**: Currently low-cost and predicted to stay low (member predicted to be in lower than 70% percent of all members). No intervention with these members is likely necessary.
""")

# Select chronic condition
chronic_condition = st.selectbox('Select Chronic Condition', options=chronic_conditions)

# Select high cost category
high_cost_categories = [
    'Wait and see high cost', 'Unavoidable high cost claimant', 
    'Impactable high cost claimant', 'Stable low cost claimant'
]
high_cost_category = st.selectbox('Select High Cost Category', options=high_cost_categories)

# Filter the dataframe based on selections
filtered_df = df[(df['chronic_condition'] == chronic_condition) & (df['claimant_category'] == high_cost_category)].round(2)

# Display the filtered dataframe
st.dataframe(filtered_df)

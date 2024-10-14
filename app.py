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

# Calculate 'allowed_dollars' and 'predicted_allowed_dollars'
df['allowed_dollars'] = df['allowed_pmpm'] * 12
df['predicted_allowed_dollars'] = df['predicted_allowed_pmpm'] * 12

# Streamlit application
st.title('High Cost Claimants')

# Allow the user to set the total allowed dollars threshold
allowed_dollars_threshold = st.number_input(
    'Set the total allowed dollars threshold for high cost claimants',
    min_value=0.0,
    value=100000.0,
    step=1000.0
)

# Convert threshold to integer for consistency
allowed_dollars_threshold = int(allowed_dollars_threshold)
half_threshold = allowed_dollars_threshold * 0.5

# Dynamic values based on the user-defined threshold
high_cost_value = allowed_dollars_threshold  # 100% of the threshold
low_cost_value = half_threshold  # 50% of the threshold
moderate_cost_value = (low_cost_value + high_cost_value) / 2  # Midpoint between low and high cost

# Ensure representation in all categories based on dynamic threshold
# For 'Unavoidable high cost claimant': currently high cost, predicted high cost
df.loc[0:9, 'allowed_dollars'] = high_cost_value  # High cost now
df.loc[0:9, 'predicted_allowed_dollars'] = high_cost_value  # Predicted high cost

# For 'Impactable high cost claimant': currently low cost, predicted high cost
df.loc[10:19, 'allowed_dollars'] = low_cost_value  # Low cost now
df.loc[10:19, 'predicted_allowed_dollars'] = high_cost_value  # Predicted high cost

# For 'Wait and See high cost claimant': currently high cost, predicted low cost
df.loc[20:29, 'allowed_dollars'] = high_cost_value  # High cost now
df.loc[20:29, 'predicted_allowed_dollars'] = low_cost_value  # Predicted low cost

# For 'Stable low cost member': currently low cost, predicted low cost
df.loc[30:59, 'allowed_dollars'] = low_cost_value  # Low cost now
df.loc[30:59, 'predicted_allowed_dollars'] = low_cost_value  # Predicted low cost

# For 'Stable moderate cost member': currently moderate cost, predicted moderate cost
df.loc[60:89, 'allowed_dollars'] = moderate_cost_value  # Moderate cost now
df.loc[60:89, 'predicted_allowed_dollars'] = moderate_cost_value  # Predicted moderate cost

# Recalculate 'allowed_pmpm' and 'predicted_allowed_pmpm'
df['allowed_pmpm'] = (df['allowed_dollars'] / 12).round(0).astype(int)
df['predicted_allowed_pmpm'] = (df['predicted_allowed_dollars'] / 12).round(0).astype(int)

# Add a column for current high cost claimant based on user-defined threshold
df['current_high_cost_claimant'] = df['allowed_dollars'] > allowed_dollars_threshold

# Add a column for predicted high cost claimant based on predicted_allowed_dollars
df['predicted_high_cost_claimant'] = df['predicted_allowed_dollars'] > allowed_dollars_threshold

st.markdown(f"""
Below is a high-cost claimant prediction demo. We predict the allowed dollars for each member. We created categories to help users identify which members are impactable:

- **Wait and See high cost claimant**: Currently high-cost (allowed dollars greater than **{allowed_dollars_threshold:,.0f}**) and predicted to drop in the future (predicted allowed dollars less than or equal to **{allowed_dollars_threshold:,.0f}**). Users can leave these members alone as they are likely to get better on their own.

- **Unavoidable high cost claimant**: Currently high-cost (allowed dollars greater than **{allowed_dollars_threshold:,.0f}**) and predicted to stay high-cost (predicted allowed dollars greater than **{allowed_dollars_threshold:,.0f}**). Users may target these members for case management or "laser" them in stop loss.

- **Impactable high cost claimant**: Currently low-cost (allowed dollars less than or equal to **{allowed_dollars_threshold:,.0f}**) but predicted to become high-cost in the future (predicted allowed dollars greater than **{allowed_dollars_threshold:,.0f}**). Users may want to target these members as they could become high-cost claimants.

- **Stable moderate cost member**: Currently moderate-cost (allowed dollars between **{half_threshold:,.0f}** and **{allowed_dollars_threshold:,.0f}**) and predicted to stay moderate (predicted allowed dollars between **{half_threshold:,.0f}** and **{allowed_dollars_threshold:,.0f}**). It is possible intervention may be needed.

- **Stable low cost member**: Currently low-cost (allowed dollars less than **{half_threshold:,.0f}**) and predicted to stay low (predicted allowed dollars less than **{half_threshold:,.0f}**). No intervention with these members is likely necessary.
""")

# Define criteria for categorizing claimants based on user-selected threshold
def categorize_claimant(row):
    current_allowed = row['allowed_dollars']
    predicted_allowed = row['predicted_allowed_dollars']
    
    if current_allowed > allowed_dollars_threshold:
        if predicted_allowed > allowed_dollars_threshold:
            return 'Unavoidable high cost claimant'
        else:
            return 'Wait and See high cost claimant'
    elif half_threshold <= current_allowed <= allowed_dollars_threshold:
        if half_threshold <= predicted_allowed <= allowed_dollars_threshold:
            return 'Stable moderate cost member'
        else:
            return 'Impactable high cost claimant'
    elif current_allowed < half_threshold:
        if predicted_allowed < half_threshold:
            return 'Stable low cost member'
        else:
            return 'Impactable moderate cost claimant'
    else:
        return 'Other'

# Apply the categorization
df['claimant_category'] = df.apply(categorize_claimant, axis=1)

# Select chronic condition (optional)
chronic_conditions_with_all = ['All'] + chronic_conditions
chronic_condition = st.selectbox('Select Chronic Condition (optional)', options=chronic_conditions_with_all)

# Select high cost category
high_cost_categories = [
    'Wait and See high cost claimant', 'Unavoidable high cost claimant',
    'Impactable high cost claimant', 'Stable low cost member', 'Stable moderate cost member'
]
high_cost_category = st.selectbox('Select High Cost Category', options=high_cost_categories)

# Filter the dataframe based on selections
if chronic_condition != 'All':
    filtered_df = df[
        (df['chronic_condition'] == chronic_condition) &
        (df['claimant_category'] == high_cost_category)
    ]
else:
    filtered_df = df[
        df['claimant_category'] == high_cost_category
    ]

# Display the filtered dataframe
st.dataframe(filtered_df)

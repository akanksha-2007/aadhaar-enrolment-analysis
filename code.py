# main analysis script
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set working directory
os.chdir(r"C:\Users\akank\Downloads\api_data_aadhar_enrolment\api_data_aadhar_enrolment")

# Load CSVs
files = [
    "api_data_aadhar_enrolment_0_500000.csv",
    "api_data_aadhar_enrolment_500000_1000000.csv",
    "api_data_aadhar_enrolment_1000000_1006029.csv"
]

df = pd.concat([pd.read_csv(f) for f in files], ignore_index=True)

# ✅ Clean state names
df['state'] = df['state'].astype(str).str.strip().str.upper()

# ✅ Remove invalid state names (non-alphabetic or numeric garbage)
df = df[df['state'].str.match(r'^[A-Z &]+$')]
# Age group totals
age_group_totals = df[['age_0_5', 'age_5_17', 'age_18_greater']].sum().reset_index()
age_group_totals.columns = ['Age_Group', 'Total_Enrolments']


# ✅ Remove rows with missing or zero enrolment
df = df[df['age_5_17'] > 0]

# ✅ State-wise total enrolments
state_counts = df.groupby('state', as_index=False)['age_5_17'].sum()
state_counts = state_counts.sort_values(by='age_5_17', ascending=False)

# ✅ Chart 1: State-wise Aadhaar Enrolments (Age 05–17)
plt.figure(figsize=(14,6))
sns.barplot(x='state', y='age_5_17', data=state_counts, palette="crest")
plt.xticks(rotation=90)
plt.title("State-wise Aadhaar Enrolments (Age 05–17)")
plt.ylabel("Total Enrolments")
plt.xlabel("State")
plt.tight_layout()
plt.show()

# ✅ Chart 2: Year-wise Aadhaar Enrolments (Age 05–17)
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ✅ Fix date formatting and extract year
df['date'] = pd.to_datetime(df['date'], errors='coerce', dayfirst=True)
df = df[df['date'].notnull()]   # remove invalid dates
df['Year'] = df['date'].dt.year.astype(int)

# ✅ Group by year and sum enrolments
year_counts = df.groupby('Year', as_index=False)['age_5_17'].sum()
print(df['Year'].value_counts().sort_index())

# ✅ Plot year-wise trend
plt.figure(figsize=(10,5))
sns.lineplot(x='Year', y='age_5_17', data=year_counts, marker='o', color="darkblue")
plt.title("Year-wise Aadhaar Enrolments (Age 05–17)")
plt.ylabel("Total Enrolments")
plt.xlabel("Year")
plt.grid(True, linestyle="--", alpha=0.6)
plt.tight_layout()
plt.show()

# ✅ Quick check: print table for insights
print(year_counts)


# ✅ Chart 3: Top 5 States by Child Enrolment
top5 = state_counts.head(5)
plt.figure(figsize=(8,5))
sns.barplot(x='state', y='age_5_17', data=top5, palette="viridis")
plt.title("Top 5 States by Child Enrolment (Age 05–17)")
plt.ylabel("Total Enrolments")
plt.xlabel("State")
plt.tight_layout()
plt.show()

# ✅ Chart 4: Bottom 5 States by Child Enrolment


# ✅ Sort states by enrolment
sorted_states = state_counts.sort_values(by='age_5_17', ascending=True)

# ✅ Bottom 5 states chart
bottom5 = sorted_states.head(5)

plt.figure(figsize=(10,5))
sns.barplot(x='state', y='age_5_17', data=bottom5, palette="mako")
plt.title("Bottom 5 States by Child Enrolment (Age 05–17)")
plt.ylabel("Total Enrolments")
plt.xlabel("State")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# ✅ Chart 5: Age Group Comparison (0–5 vs 5–17 vs 18+)
age_group_totals = df[['age_0_5', 'age_5_17', 'age_18_greater']].sum().reset_index()
age_group_totals.columns = ['Age_Group', 'Total_Enrolments']

plt.figure(figsize=(7,5))
sns.barplot(x='Age_Group', y='Total_Enrolments', data=age_group_totals, palette="rocket")
plt.title("Comparison of Aadhaar Enrolments by Age Groups")
plt.ylabel("Total Enrolments")
plt.xlabel("Age Group")
plt.tight_layout()
plt.show()

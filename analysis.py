import pandas as pd
import matplotlib.pyplot as plt


df1 = pd.read_csv("data/api_data_aadhar_enrolment_0_500000.csv")
df2 = pd.read_csv("data/api_data_aadhar_enrolment_500000_1000000.csv")
df3 = pd.read_csv("data/api_data_aadhar_enrolment_1000000_1006029.csv")

df = pd.concat([df1, df2, df3], ignore_index=True)

print(df.head())
print(df.shape)
df['state'] = df['state'].str.strip().str.title()
df['district'] = df['district'].str.strip().str.title()
df['district'] = (
    df['district']
    .str.replace('*', '', regex=False)
    .str.strip()
)


df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y')
print(df.dtypes)
df['total_enrolments'] = (
    df['age_0_5'] +
    df['age_5_17'] +
    df['age_18_greater']
)
print(df[['age_0_5','age_5_17','age_18_greater','total_enrolments']].head())
# Create month column
df['month'] = df['date'].dt.to_period('M')

district_month = df.groupby(
    ['state', 'district', 'month'],
    as_index=False
).agg({
    'age_0_5': 'sum',
    'age_5_17': 'sum',
    'age_18_greater': 'sum',
    'total_enrolments': 'sum'
})

print("district_month shape:", district_month.shape)
print(district_month.head())
# Remove numeric-only state/district entries (data quality fix)
district_month = district_month[
    district_month['state'].apply(lambda x: isinstance(x, str)) &
    district_month['district'].apply(lambda x: isinstance(x, str))
]
print("district_month shape after cleaning:", district_month.shape)
# Proper cleaning: remove numeric-only state/district values
district_month = district_month[
    ~district_month['state'].str.isnumeric() &
    ~district_month['district'].str.isnumeric()
]

print("district_month shape after REAL cleaning:", district_month.shape)
print(district_month.head())
avg_monthly = district_month.groupby(
    ['state', 'district'],
    as_index=False
)['total_enrolments'].mean()

lowest_5 = avg_monthly.sort_values(
    'total_enrolments'
).head(5)

print("Lowest 5 districts by average monthly enrolment:")
print(lowest_5)
age_sum = district_month.groupby(
    ['state', 'district'],
    as_index=False
).agg({
    'age_0_5': 'sum',
    'age_5_17': 'sum',
    'age_18_greater': 'sum'
})

age_sum['dominant_group'] = age_sum[
    ['age_0_5', 'age_5_17', 'age_18_greater']
].idxmax(axis=1)
age_counts = age_sum['dominant_group'].value_counts()

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")
os.makedirs(OUTPUT_DIR, exist_ok=True)

plt.figure(figsize=(6, 4))
age_counts.plot(kind="bar")

plt.title("Dominant Age Group Across Districts")
plt.xlabel("Age Group")
plt.ylabel("Number of Districts")

plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "dominant_age_group.png"))
plt.close()

print("Bar chart saved: outputs/dominant_age_group.png")

print(age_counts)
import matplotlib.pyplot as plt

plt.figure()
age_counts.plot(kind='bar')
plt.title("Dominant Aadhaar Enrolment Age Group by District")
plt.xlabel("Age Group")
plt.ylabel("Number of Districts")
plt.tight_layout()
plt.show()
import os
os.makedirs("outputs", exist_ok=True)
avg_monthly = district_month.groupby(
    ['state', 'district'],
    as_index=False
)['total_enrolments'].mean()
lowest_10 = avg_monthly.sort_values(
    'total_enrolments',
    ascending=True
).head(10)
lowest_10 = lowest_10.rename(
    columns={'total_enrolments': 'avg_monthly_enrolments'}
)
print("\nTable 1: Lowest 10 Districts by Average Monthly Aadhaar Enrolment\n")
print(lowest_10)
lowest_10.to_csv("outputs/lowest_10_districts.csv", index=False)

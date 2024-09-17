# Import required libraries
import pandas as pd
import mysql.connector
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Connect to MySQL
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="telco_churn"  # Adjust the database name as per your MySQL Workbench
)

# Create a cursor object
cursor = connection.cursor()

# SQL query to fetch data
query = "SELECT * FROM telco_customers"
cursor.execute(query)

# Fetch all results
result = cursor.fetchall()

# Define column names (these must match with your actual column names in the database)
columns = ['customerID', 'gender', 'SeniorCitizen', 'Partner', 'Dependents', 'tenure', 'PhoneService', 
           'MultipleLines', 'InternetService', 'OnlineSecurity', 'OnlineBackup', 'DeviceProtection', 
           'TechSupport', 'StreamingTV', 'StreamingMovies', 'Contract', 'PaperlessBilling', 
           'PaymentMethod', 'MonthlyCharges', 'TotalCharges', 'Churn']

# Load data into a Pandas DataFrame
df = pd.DataFrame(result, columns=columns)

# Display first few rows of the DataFrame
print(df.head())

# 2. Churn Distribution
plt.figure(figsize=(8,6))
sns.countplot(x='Churn', data=df)
plt.title('Churn Distribution')
plt.show()

# 3. Tenure vs Monthly Charges by Churn (Scatter plot)
plt.figure(figsize=(10,6))
sns.scatterplot(x='tenure', y='MonthlyCharges', hue='Churn', data=df)
plt.title('Tenure vs Monthly Charges by Churn')
plt.show()

# 4. Churn by Payment Method (Count plot)
plt.figure(figsize=(10,6))
sns.countplot(x='PaymentMethod', hue='Churn', data=df)
plt.title('Churn by Payment Method')
plt.xticks(rotation=45)  # Rotate labels for better readability
plt.show()

# 5. Churn Percentage by Gender (Pie Chart)
plt.figure(figsize=(8,6))
gender_churn = df.groupby('gender')['Churn'].value_counts(normalize=True).unstack()
gender_churn.plot(kind='pie', subplots=True, autopct='%1.1f%%', startangle=90)
plt.title('Churn Percentage by Gender')
plt.ylabel('')
plt.show()

# 6. Descriptive Statistics
print("\nDescriptive Statistics:\n")
print(df.describe())

# 7. Export the DataFrame to a CSV file for further analysis
df.to_csv('telco_customers_analysis.csv', index=False)

# Close the cursor and connection
cursor.close()
connection.close()

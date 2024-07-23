import argparse
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import seaborn as sns

sns.set_context("paper")
sns.set_theme(style='white')

# Read data
parser = argparse.ArgumentParser()
parser.add_argument('--filename', type=str, default='SGA1-2_summary2.xlsx', nargs='?')
args = parser.parse_args()
file_name =  args.filename
df = pd.read_excel(file_name)
file_name = os.path.basename(file_name)

# Extract unique values
classes = df['Class'].unique()
types = sorted(df['Type'].unique())
types.append(types.pop(types.index('Satisfaction')))
save_name = ""
if file_name in ['SGA1-2_summary2.xlsx', 'YRE Surveys_SGA1-2_summary.xlsx']:
    categories = ['Failed', 'Insufficient', 'Sufficient', 'Satisfactory', 'Good', 'Excellent']
    save_name = f"conf_ratings_sga1-sga2_deviation.pdf" if file_name == 'SGA1-2_summary2.xlsx' else f'YRE_deviations_sga1-2.pdf'
else:
    categories = ["Very poor", "Poor", "Fair", "Good", "Excellent"]
    save_name = f"conf_deviations_sga3.pdf" if file_name =='SGA3_summary.xlsx' else f'YRE_deviations_sga3.pdf'

# Calculate mean ratings for each type-class combination
ratings_dict = {}
for c in classes:
    df_class = df[df['Class'] == c]
    if not df_class.empty:
        std = df_class.sum(numeric_only=True)
        ratings_dict[c] = std

# Convert dictionary to DataFrame
ratings_df = pd.DataFrame(ratings_dict)
# sort by class name
ratings_df.sort_index(axis=1, inplace=True)
sns.catplot(kind='box', data=ratings_df, errorbar="sd",  height=6, aspect=1.3, orient='h', palette='Reds')
# Save figure
# plt.savefig(save_name, dpi=600, bbox_inches='tight', pad_inches=0.1)
plt.show()
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
parser.add_argument('--total_deviation', default=False, action='store_true',
                    help='Additionally shows boxplot indicating success rates.')
parser.add_argument('--save', default=False, action='store_true',
                    help='Additionally shows boxplot indicating success rates.')
args = parser.parse_args()
file_name =  args.filename
save = args.save
df = pd.read_excel(file_name)
file_name = os.path.basename(file_name)

# Extract unique values
classes = df['Class'].unique()
types = sorted(df['Type'].unique())
types.append(types.pop(types.index('Satisfaction')))
save_name = ""
if file_name in ['SGA1-2_summary2.xlsx', 'YRE Surveys_SGA1-2_summary.xlsx']:
    categories = ['Failed', 'Insufficient', 'Sufficient', 'Satisfactory', 'Good', 'Excellent']
    save_name = f"conf_ratings_sga1-sga2_deviation.eps" if file_name == 'SGA1-2_summary2.xlsx' else f'YRE_deviations_sga1-2.eps'
else:
    categories = ["Very poor", "Poor", "Fair", "Good", "Excellent"]
    save_name = f"conf_deviations_sga3.eps" if file_name =='SGA3_summary.xlsx' else f'YRE_deviations_sga3.eps'

# Sum up responses for each class
ratings_dict = {}
for c in classes:
    df_class = df[df['Class'] == c]
    if not df_class.empty:
        ratings_dict[c] = df_class.sum(numeric_only=True)

# Convert dictionary to DataFrame
ratings_df = pd.DataFrame(ratings_dict)
# sort by class name
ratings_df.sort_index(axis=1, inplace=True)
# Set the font size globally
plt.rcParams['xtick.labelsize'] = 13
plt.rcParams['ytick.labelsize'] = 13
g = sns.catplot(kind='box', data=ratings_df, errorbar="sd",  height=6, aspect=1.3, orient='h', palette='Reds')
g.set_xlabels('Response', size=13)
if args.total_deviation:
    # sns.catplot(kind='box', data=df.select_dtypes('number'), errorbar="sd",  height=6, aspect=1.3, orient='h', palette='Blues')
    p = sns.catplot(kind='box', data=ratings_df.T.reset_index(), errorbar="sd",  height=6, aspect=1.3, orient='h', palette='vlag')
    if file_name == 'YRE Surveys_SGA1-2_summary.xlsx':
        sn = 'total_deviation_sga1-2.eps'
    else:
        sn = 'total_deviation_sga3.eps'
    if save:
        p.savefig(sn, dpi=600, bbox_inches='tight', pad_inches=0.1)

# Save figure
if save:
    g.savefig(save_name, dpi=600, bbox_inches='tight', pad_inches=0.1)
plt.show()

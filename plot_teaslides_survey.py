import argparse
import matplotlib.pyplot as plt
import os
import pandas as pd
import plot_likert
import seaborn as sns

sns.set_context("paper")
sns.set_theme(style='white', palette='vlag', rc={'grid.linestyle': 'dotted'})

# Read data
 # Read data
parser = argparse.ArgumentParser()
parser.add_argument('--filename', type=str, default='HBPTeaandSlides_overall_satisfaction.xlsx', nargs='?')
parser.add_argument('--total_mean', default=False, action='store_true',
                    help='Shows mean of participants')
parser.add_argument('--plot_type', type=str, default='stacked', nargs='?',
                    help='Defines the type of plot. Likert graph or stacked histograms')
parser.add_argument('--percentage', default=False, action='store_true',
                    help='Defines whether percentage or absolute value will be plotted')
args = parser.parse_args()
file_name =  args.filename
plot_type = args.plot_type
total_mean = args.total_mean
percentage = args.percentage
df = pd.read_excel(file_name)
file_name = os.path.basename(file_name)

# Convert the series to a DataFrame and transpose it
mean = df.mean(numeric_only=True)
if percentage and plot_type == 'stacked':
    percent = mean * 100 / mean.sum()
    new_df = pd.DataFrame(percent).T
else:
    new_df = pd.DataFrame(mean).T

if total_mean:
    print(df.sum(numeric_only=True))
    print(df.sum(numeric_only=True).mean())

# Plot the stacked histogram
fig, ax = plt.subplots(1, 1, figsize=(8, 6))
if plot_type == 'stacked':
    new_df.plot(kind='barh', stacked=True, ax=ax)
else:
    colors = sns.color_palette(palette='vlag', n_colors=len(new_df.columns))
    colors.insert(0, "#ffffff00")
    plot_likert.plot_counts(new_df.round(decimals=0), new_df.columns, ax=ax,
                                 bar_labels=False, bar_labels_color="#31464c",
                                 # plot_percentage=True,
                                 colors=colors,
                                 )
colors = sns.color_palette(palette='vlag', n_colors=len(new_df.columns))
ax.set_title('Overall Satisfaction', fontsize=15)
ax.set_xlabel(None)
ax.set_ylabel(None)
ax.set_yticklabels("")
ax.legend_.remove()
if plot_type == 'stacked':
    for container in ax.containers:
        labels = ax.bar_label(container, label_type='center',
                              fmt='%.0f'+("%%" if percentage else ""),
                              color='#31464c', padding=0, fontsize=11)
        for label in labels:
            label_text = label.get_text()
            label_text = label_text.rstrip("%")
            number = float(label_text)
            if number < 6:
                label.set_text("")

legend_props = {'ncols': len(new_df.columns),
                'loc':'upper left', 'frameon':True}
ax.legend(**legend_props)
# plt.savefig(f'TA_ratings_{plot_type}.pdf', dpi=600, bbox_inches='tight', pad_inches=0.1)
# plt.show()

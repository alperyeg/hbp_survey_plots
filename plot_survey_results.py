import argparse
import matplotlib.pyplot as plt
import os
import pandas as pd
import plot_likert
import seaborn as sns

from matplotlib.transforms import ScaledTranslation

sns.set_context("paper")
sns.set_theme(style='white', palette='vlag')

# Read data
 # Read data
parser = argparse.ArgumentParser()
parser.add_argument('--filename', type=str, default='SGA1-2_summary2.xlsx', nargs='?')
parser.add_argument('--total_mean', default=False, action='store_true',
                    help='Shows mean of participants')
parser.add_argument('--plot_type', type=str, default='stacked', nargs='?',
                    help='Defines the type of plot. Likert graph or stacked histograms')
parser.add_argument('--percentage', default=False, action='store_true',
                    help='Defines whether percentage or absolute value will be plotted')
args = parser.parse_args()
file_name =  args.filename
plot_type = args.plot_type
percentage = args.percentage
df = pd.read_excel(file_name)
file_name = os.path.basename(file_name)

# Extract unique values
classes = df['Class'].unique()
types = sorted(df['Type'].unique())
types.append(types.pop(types.index('Satisfaction')))
save_name = ""
if file_name in ['SGA1-2_summary2.xlsx', 'YRE Surveys_SGA1-2_summary.xlsx']:
    categories = ['Failed', 'Insufficient', 'Sufficient', 'Satisfactory', 'Good', 'Excellent']
    save_name = f"conf_ratings_sga1-sga2_{plot_type}.pdf" if file_name == 'SGA1-2_summary2.xlsx' else f'YRE_ratings_sga1-2_{plot_type}.pdf'
    adjust_subplot = {'top':0.88, 'bottom':0.11, 'left':0.125, 'right':0.9, 'hspace':0.2, 'wspace':0.8}
    ax_index = 1
    last_index = -1
    subplot_props =  {'nrows':1, 'ncols':len(types), 'figsize':(20, 4)}
    legend_props = {'bbox_to_anchor':(-1.1, 1.1), 'ncols':len(df.columns[2:]),
                    'loc':'lower left', 'frameon':True}
else:
    categories = ["Very poor", "Poor", "Fair", "Good", "Excellent"]
    save_name = f"conf_ratings_sga3_{plot_type}.pdf" if file_name =='SGA3_summary.xlsx' else f'YRE_ratings_sga3_{plot_type}.pdf'
    subplot_props =  {'nrows':2, 'ncols':2, 'figsize':(20, 8)}
    adjust_subplot = {'top':0.880, 'bottom':0.110, 'left':0.140, 'right':0.900, 'hspace':0.33, 'wspace':0.360}
    ax_index = (0, 0)
    last_index = (-1, -1)
    legend_props = {'bbox_to_anchor':(0.6, 1.1), 'ncols':len(df.columns[2:]),
                    'loc':'lower left', 'frameon':True}

# Calculate mean ratings for each type-class combination
ratings_dict = {}
total_mean = []
for t in types:
    for c in classes:
        df_class = df[(df['Type'] == t) & (df['Class'] == c)]
        if not df_class.empty:
            mean = df_class.mean(numeric_only=True)
            total_mean.append(mean)
            if percentage and plot_type == 'stacked':
                percent = mean * 100 / mean.sum()
                ratings_dict[(t, c)] = percent
            else:
                ratings_dict[(t, c)] = mean

if args.total_mean:
    import numpy as np
    print('Total mean: ', np.mean([i.sum() for i in total_mean]))

# Convert dictionary to DataFrame
ratings_df = pd.DataFrame(ratings_dict).T.reset_index()
ratings_df.columns = ['Type', 'Class'] + categories

# Plotting
fig, axes = plt.subplots(**subplot_props)
fontsize = 15
sublabels = ['A', 'B', 'C', 'D']
j = 0
for i, t in enumerate(types):
    if file_name in ['SGA1-2_summary2.xlsx', 'YRE Surveys_SGA1-2_summary.xlsx']:
        ax = axes[i]
    else:
        j = 1 if i > 1 else 0
        ax = axes[j, i % 2]
    # Per type
    new_df = ratings_df[ratings_df['Type'] == t]
    # print(new_df)
    # Likert graph
    if plot_type == 'likert':
        # Need to define color range
        colors = sns.color_palette(palette='vlag', n_colors=len(ratings_df.columns[2:]))
        colors.insert(0, "#ffffff00")
        pl = plot_likert.plot_counts(new_df.iloc[:,2:].round(decimals=0), new_df.columns[2:], ax=ax,
                                 bar_labels=True, bar_labels_color="#31464c",
                                 plot_percentage=percentage,
                                 colors=colors)
    # Stacked histogram
    else:
        new_df.plot(kind='barh', stacked=True, ax=ax)
    # Axes edits
    ax.set_title(t, fontsize=fontsize)
    ax.text(0.0, 1.0, sublabels[i],
            transform=(ax.transAxes + ScaledTranslation(-20/72, +7/72, fig.dpi_scale_trans)),
            fontsize=fontsize, va='bottom', weight='demibold')
    ax.set_xlabel(None)
    ax.set_ylabel(None)
    ax.tick_params(axis='y', labelsize=12.5)
    ax.tick_params(axis='x', labelsize=13)
    # set category `class` names as labels
    ax.set_yticklabels(new_df['Class'].to_list())
    ax.legend_.remove()
    # Set bar labels
    if plot_type == 'stacked':
        for container in ax.containers:
            labels = ax.bar_label(container, label_type='center',
                                  fmt='%.0f'+("%%" if percentage else ""),
                                  color='#31464c', padding=0, fontsize=11)
            for label in labels:
                label_text = label.get_text()
                label_text = label_text.rstrip("%")
                number = float(label_text)
                # remove percentage less than 6 %
                if number < 6:
                    label.set_text("")

# Move legend
axes[ax_index].legend(**legend_props)
# Change title and remove label of last subplot
axes[last_index].set_title('Overall Satisfaction', fontsize=fontsize)
axes[last_index].set_yticklabels("")
plt.subplots_adjust(**adjust_subplot)
# Save figure
# plt.subplot_tool()
# plt.savefig(save_name, dpi=600, bbox_inches='tight', pad_inches=0.1)
plt.show()

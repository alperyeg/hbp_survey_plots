import argparse
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import plot_likert
import seaborn as sns

from matplotlib.transforms import ScaledTranslation

sns.set_context("paper")
sns.set_theme(style='white', palette='vlag')


parser = argparse.ArgumentParser()
parser.add_argument('--percentage', default=False, action='store_true',
                    help='Defines whether percentage or absolute value will be plotted')
args = parser.parse_args()
sheet = [0, 1]
fontsize = 15
sublabels = ['A', 'B']
percentage = args.percentage
titles = ['Based on your experience as a speaker/tutor at an HBP Education Programme Event,\n please rate how important you consider the following aspects \n when teaching multidisciplinary audiences?',
          'How often did you encounter the following challenges when teaching \n a multidisciplinary audience in the context of HBP Education Programme events?']
adjust_subplot = {'top':0.880, 'bottom':0.110, 'left':0.140, 'right':0.900, 'hspace':0.4, 'wspace':0.360}
subplot_props =  {'nrows':len(sheet), 'ncols':1, 'figsize':(12, 12)}
# Plotting
# 2 rows 1 column
fig, axes = plt.subplots(**subplot_props)
for s in sheet:
    ax = axes[s]
    xls = pd.read_excel('PI Survey_Data.xlsx', s)
    df = xls.select_dtypes('number')
    if percentage:
        df = df.div(df.sum(axis=1), axis=0) * 100
    legend_props = {'bbox_to_anchor':(0.15, -0.2), 'ncols':len(df.columns),
                    'loc':'lower left', 'frameon':True}

    df.plot(kind='barh', stacked=True, ax=ax)
    # Axes edits
    ax.set_title(titles[s], fontsize=fontsize)
    ax.text(0.0, 1.0, sublabels[s],
            transform=(ax.transAxes + ScaledTranslation(-7.5, +35/72, fig.dpi_scale_trans)),
            fontsize=fontsize, va='bottom', weight='demibold')
    ax.set_xlabel(None)
    ax.set_ylabel(None)
    ax.tick_params(axis='y', labelsize=12.5)
    ax.tick_params(axis='x', labelsize=13)
    ax.set_yticklabels(xls['Class'].to_list())
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
    ax.legend(**legend_props)
plt.subplots_adjust(**adjust_subplot)
# plt.subplot_tool()
# plt.savefig('pi_survey.eps', dpi=600, bbox_inches='tight', pad_inches=0.1)
plt.show()

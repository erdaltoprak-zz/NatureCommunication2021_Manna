import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import LogFormatterMathtext
from Colors import tmpcolor, v041color, change_width, mw_tmp, mw_v041

colors = [tmpcolor, v041color]
palette = sns.color_palette(colors)

df1 = pd.read_csv('IC95_2019_09_19.csv')
df2 = pd.read_csv('IC95_2019_09_20.csv')
dff = pd.concat([df1, df2], axis='rows')
collist = [1, 2, -1]
cellorder = ['WT', 'I5F', 'M20I', 'P21L', 'A26T', 'D27E', 'L28R',
             'W30R', 'W30G', 'I94L', 'R98P', 'F153S']
IC95 = dff.iloc[:, collist]

IC95_2 = pd.concat([IC95.loc[IC95['CellType'] == i] for i in cellorder], axis='rows')
IC95_2.loc[IC95_2['Drug'] == 'V041', 'Drug'] = '4\'-DTMP'

fig, ax = plt.subplots()
sns.set_style('ticks')
sns.despine()

sns.barplot(x='CellType', y='IC95', hue='Drug', data=IC95_2,
            palette=palette, ax=ax, capsize=.05, ci='sd',
            errwidth=1.5, edgecolor='k', errcolor='k')
change_width(ax, .3)
ax.set_yscale('log')
ax.set_ylim(.3, 4000)
ax.set_xlabel('DHFR Variants')
ax.set_ylabel('IC$_{95}$ (µM)')
ax.set_yticks([1e0, 1e1, 1e2, 1e3])
ax.set_yticklabels(['', '10$^1$', '', '10$^3$'])
ax.legend(frameon=False, loc=1, fontsize=8)  # , ncol=2)
ax.set_xticklabels(ax.get_xticklabels(), rotation=90, horizontalalignment='center', fontsize=8)
fig.set_size_inches(4.4, 2.0)
fig.tight_layout(pad=0.95)
# fig.savefig('BarPlot_IC95-AllSingleMutants.pdf', dpi=600)
# fig.savefig('BarPlot_IC95-AllSingleMutants.png', transparent=True, dpi=600)

########## Convert concentration to ug/mL ############
IC95_2['IC95_ug'] = 0
IC95_2.loc[IC95_2.Drug == 'TMP', 'IC95_ug'] = IC95_2.loc[IC95_2.Drug == 'TMP', 'IC95'] * mw_tmp * 1e-3
IC95_2.loc[IC95_2.Drug == "4\'-DTMP", 'IC95_ug'] = IC95_2.loc[IC95_2.Drug == "4\'-DTMP", 'IC95'] * mw_v041 * 1e-3
fig, ax = plt.subplots()
sns.set_style('ticks')
sns.despine()

sns.barplot(x='CellType', y='IC95_ug', hue='Drug', data=IC95_2,
            palette=palette, ax=ax, capsize=.05, ci='sd',
            errwidth=1.5, edgecolor='k', errcolor='k')
change_width(ax, .3)
xms = sorted([-0.35, 0.65, 1.65, 2.65, 3.65, 4.65, 5.65, 6.65, 7.65, 8.65, 9.65, 10.65, 0.05, 1.05, 2.05, 3.05, 4.05, 5.05,
       6.05, 7.05, 8.05, 9.05, 10.05, 11.05])
c = 0
for strain in IC95_2.CellType.unique():
    for drug in IC95_2.Drug.unique():
        yvals = IC95_2.loc[(IC95_2.CellType == strain) & (IC95_2.Drug == drug), 'IC95_ug'].values
        xvals = np.ones(len(yvals)) * xms[c] + (np.random.random(len(yvals)) - .5) * .2 + .15
        # print(strain, drug, xvals, yvals)
        ax.plot(xvals, yvals, 'o', color='k', markersize=2, alpha=.3)
        c += 1

ax.set_yscale('log')
ax.set_xlabel('DHFR Variants')
ax.set_ylabel('IC$_{95}$ (µg/mL)')
ax.set_yticks([1e0, 1e1, 1e2, 1e3])
ax.set_yticklabels([1e0, 1e1, 1e2, 1e3])
ax.yaxis.set_major_formatter(LogFormatterMathtext())
# ax.set_yticklabels(['10$^{-1}$', '', '10$^1$', '', '10$^3$'])
ax.set_ylim(.6, 1000)
ax.legend(frameon=False, loc=1, fontsize=8, ncol=2, bbox_to_anchor=(1.05, 1.05))
ax.set_xticklabels(ax.get_xticklabels(), rotation=90, horizontalalignment='center', fontsize=8)
fig.set_size_inches(4.4, 2.0)
fig.tight_layout(pad=0.95)
fig.savefig('BarPlot_IC95-AllSingleMutants_ug_wDots.pdf', dpi=600)
fig.savefig('BarPlot_IC95-AllSingleMutants_ug_wDots.png', transparent=True, dpi=600)

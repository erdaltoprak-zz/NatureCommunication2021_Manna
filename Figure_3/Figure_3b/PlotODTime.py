import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import scipy.stats as ss
from Colors import tmpcolor, v041color, change_width

df = pd.read_excel('Evolution of Mixed Mutants_OD Values.xlsx', 'ODs')
dfm = df.groupby('Selection').mean().drop('Replica', axis='columns')
dfs = df.groupby('Selection').std().drop('Replica', axis='columns')
pall = ["w", tmpcolor, v041color]
paldict = {'No Drug': 'w', 'TMP': tmpcolor, '4\'-DTMP': v041color}

df2 = pd.read_excel('Evolution of Mixed Mutants_OD Values.xlsx', 'GenTimes')
df21 = df2.set_index(['Selection', 'Replica']).stack().reset_index()
df21.columns = ['Selection', 'Replica', 'Interval', 'Generations/hour']
df21['Time'] = df21['Interval'].apply(lambda x: int(x.split('->')[1]))
df21.loc[df21['Selection']=='V041','Selection']='4\'-DTMP'
fig2, ax2 = plt.subplots()
sns.set_style('ticks')
sns.despine()
sns.barplot(x='Time', y='Generations/hour', hue='Selection', ci='sd',
            data=df21, capsize=.05, errwidth=1.5, edgecolor='k',
            palette=pall, ax=ax2)
change_width(ax2,.23)

xms = sorted([-0.38,  0.62, 1.62, 2.62, 3.62, 4.62, -0.12, 0.88, 1.88, 2.88,
              3.88, 4.88, 0.15, 1.15, 2.15, 3.15, 4.15, 5.15])
c = 0
for strain in df21.Time.unique():
    for drug in df21.Selection.unique():
        yvals = df21.loc[(df21.Time == strain) & (df21.Selection == drug), 'Generations/hour'].values
        xvals = np.ones(len(yvals)) * xms[c] + (np.random.random(len(yvals)) - .5) * .2 + .115
        # print(strain, drug, xvals, yvals)
        ax2.plot(xvals, yvals, 'o', color='k', markersize=2, alpha=.5)
        c += 1

ax2.set_xticklabels(['0-4','4-8','8-12','20-24','24-28','28-32'])
ax2.set_xlabel('Time (h)')
ax2.legend(frameon=False, loc=1, ncol=3, bbox_to_anchor=(1, 1.1))
ax2.set_ylim(0,1.8)
ax2.set_yticks([0,.3,.6,.9,1.2,1.5,1.8])
fig2.set_size_inches(5, 2)
fig2.tight_layout(pad=.5)
fig2.savefig('GenTimevsIntervals_wDots.pdf', dpi=600, transparent=True)
fig2.savefig('GenTimevsIntervals_wDots.png', dpi=600, transparent=True)

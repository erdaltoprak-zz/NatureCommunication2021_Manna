import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from Colors import tmpcolor, v041color, change_width

df = pd.read_excel('KiData2.xlsx', 'Sheet1')
fig, ax = plt.subplots()
sns.set_style('ticks')
sns.despine()
sns.barplot(x='Mutant', y='Ki (nM)', hue='Drug',
            hue_order=['TMP', '4\'-DTMP'],
            palette=[tmpcolor, v041color],
            data=df, ax=ax, capsize=0.05, ci='sd',
            errwidth=1.5, edgecolor='k', errcolor='k')
change_width(ax, 0.35)
xms = sorted([-0.38, 0.63, 0.03, 1.02])
c = 0
for strain in df.Mutant.unique():
    for drug in df.Drug.unique():
        yvals = df.loc[(df.Mutant == strain) & (df.Drug == drug), 'Ki (nM)'].values
        xvals = np.ones(len(yvals)) * xms[c] + (np.random.random(len(yvals)) - .5) * .25 + .175
        # print(strain, drug, xvals, yvals)
        ax.plot(xvals, yvals, 'o', color='k', markersize=3, alpha=.5)
        c += 1
# ax.plot([0-.175, .175], [10, 10], '-k')
# ax.plot([1-.175, 1.175], [100, 100], '-k')
ax.set_ylim(1, 200)
ax.set_yscale('log')
ax.set_ylabel('K$_i$ (nM)')
ax.legend(frameon=False, loc=2)
fig.set_size_inches(4, 3)
fig.tight_layout(pad=.5)
fig.savefig('KiData_updated_wDots.pdf',dpi=600, transparent=True)
fig.savefig('KiData_updated_wDots.png',dpi=600, transparent=True)

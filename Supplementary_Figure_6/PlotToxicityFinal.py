import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from Colors import tmpcolor, v041color, change_width

palette = [tmpcolor, v041color]

cosmetics = dict(capsize=.05, errwidth=1.5, edgecolor='k',
                 errcolor='k', ci='sd', hue_order=['TMP', '4\'-DTMP'],
                 palette=palette, )
df = pd.read_excel('ToxicityAllDataCombined.xlsx', 'Summary')
df = df.loc[df.Time == 24, :]
celltypelist=['ARPE-19','ARPE-19','293A','CHO-DHFR']
assaytypelist=['Confluent','Dividing','Dividing','Dividing']
titles = [['ARPE-19 / Confluent', 'ARPE-19 / Dividing'],
          ['293A / Dividing', 'CHO-DHFR / Dividing']]
fig, ax = plt.subplots(2, 2, sharex=True, sharey=True)
sns.set_style('ticks')
sns.despine()
xms=[[sorted([-0.38, 0.63, 1.62, 2.62, 3.62, 4.62, 5.62,
       0.03, 1.02, 2.02, 3.02, 4.03, 5.03, 6.02]),
      sorted([-0.38, 0.63, 1.62, 2.62, 3.62, 4.62, 5.62,
       0.03, 1.02, 2.02, 3.02, 4.03, 5.03, 6.02])],
     [sorted([-0.38, 0.63, 1.62, 2.62, 3.62, 4.62, 5.62, 6.62,
       0.03, 1.02, 2.02, 3.02, 4.03, 5.03, 6.02, 7.02]),
      sorted([-0.38, 0.63, 1.62, 2.62, 3.62, 4.62, 5.62, 6.62,
       0.03, 1.02, 2.02, 3.02, 4.03, 5.03, 6.02, 7.02])]]
cx=0
# for celltype in celltypelist:
#     for assaytype in assaytypelist:
for m in range(4):
    celltype=celltypelist[m]
    assaytype= assaytypelist[m]
    dfnow=df.loc[(df.CellType == celltype) &
                 (df.CellCycleType == assaytype), :]
    sns.barplot(x='Concentration', y='Growth', hue='Drug',
                data=dfnow, ax=ax[cx//2, cx%2], **cosmetics)
    c=0
    for strain in dfnow.Concentration.unique():
        for drug in dfnow.Drug.unique():
            yvals = dfnow.loc[(dfnow.Concentration == strain) & (dfnow.Drug == drug), 'Growth'].values
            xvals = np.ones(len(yvals)) * xms[cx//2][cx%2][c] + (np.random.random(len(yvals)) - .5) * .25 + .175
            print(strain, drug, xvals, yvals)
            ax[cx//2, cx%2].plot(xvals, yvals, 'o', color='k', markersize=3, alpha=.5)
            c += 1
    cx += 1
# sns.barplot(x='Concentration', y='Growth', hue='Drug',
#             data=df.loc[(df.CellType == 'ARPE-19') &
#                         (df.CellCycleType == 'Dividing'), :],
#             ax=ax[0, 1], **cosmetics)
# sns.barplot(x='Concentration', y='Growth', hue='Drug',
#             data=df.loc[(df.CellType == '293A') &
#                         (df.CellCycleType == 'Dividing'), :],
#             ax=ax[1, 0], **cosmetics)
# sns.barplot(x='Concentration', y='Growth', hue='Drug',
#             data=df.loc[(df.CellType == 'CHO-DHFR') &
#                         (df.CellCycleType == 'Dividing'), :],
#             ax=ax[1, 1], **cosmetics)
for i in range(2):
    for j in range(2):
        if i == 0 and j == 0:
            handles, labels = ax[i, j].get_legend_handles_labels()
            ax[i, j].legend(handles, labels, ncol=2, loc=1,
                            frameon=False, bbox_to_anchor=(1, 1))
        else:
            ax[i, j].get_legend().remove()
        if i==0:
            ax[i, j].set_xlabel('')
        else:
            ax[i, j].set_xlabel('[Drug] (µM)')
        change_width(ax[i, j], 0.35)

        ax[i, j].set_title(titles[i][j])
        ax[i, j].set_ylim(0, 150)
        ax[i, j].set_yticks(np.arange(0,160,25))
        xticklabels = ax[i, j].get_xticklabels()
        ax[i, j].set_xticklabels(xticklabels, rotation=30, horizontalalignment='right')
        ax[i, j].set_ylabel('')

ax[0, 0].set_ylabel('ATP content at 24h\n(relative to DMSO)')
ax[1, 0].set_ylabel('ATP content at 24h\n(relative to DMSO)')
fig.set_size_inches(7, 5)
fig.tight_layout(pad=.95)
fig.savefig('ToxicitySummaryFinal_wDots.png', dpi=600, transparent=False)
fig.savefig('ToxicitySummaryFinal_wDots.pdf', dpi=600, transparent=False)

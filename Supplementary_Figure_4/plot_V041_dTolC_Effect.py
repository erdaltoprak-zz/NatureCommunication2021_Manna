import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from Colors import change_width, mw_v041, mw_tmp


def findIC95(concs, ODs):
    ODthr = max(ODs) * .05
    ODbool = ODs < ODthr
    IC95 = min(concs[ODbool])
    return IC95


colors = ["gray", "olivedrab"]
palette = sns.color_palette(colors)

drugconc = [round(9000 * ((1 / 3) ** i), 2) for i in range(12)]
# drugconc.append(0)
df = pd.read_excel('2019-09-14-WT-dTolC-TMP-V041.xlsx', 'Raw Data')

wt_TMP = df.iloc[:8, 1:]
wt_V041 = df.iloc[9:17, 1:]
dT_TMP = df.iloc[18:26, 1:]
dT_V041 = df.iloc[27:, 1:]

wt_TMP -= wt_TMP.iloc[-1, :]
wt_V041 -= wt_V041.iloc[-1, :]
dT_TMP -= dT_TMP.iloc[-1, :]
dT_V041 -= dT_V041.iloc[-1, :]

wt_TMP[wt_TMP < 0] = 0
wt_V041[wt_V041 < 0] = 0
dT_TMP[dT_TMP < 0] = 0
dT_V041[dT_V041 < 0] = 0

wt_TMP.columns = drugconc
wt_V041.columns = drugconc
dT_TMP.columns = drugconc
dT_V041.columns = drugconc

wt_TMP = wt_TMP.iloc[:-1, :]
wt_V041 = wt_V041.iloc[:-1, :]
dT_TMP = dT_TMP.iloc[:-1, :]
dT_V041 = dT_V041.iloc[:-1, :]

d1 = wt_TMP.stack().reset_index()
d1['CellType'] = 'WT'
d1['Drug'] = 'TMP'
d2 = wt_V041.stack().reset_index()
d2['CellType'] = 'WT'
d2['Drug'] = '4\'-DTMP'
d3 = dT_TMP.stack().reset_index()
d3['CellType'] = '∆TolC'
d3['Drug'] = 'TMP'
d4 = dT_V041.stack().reset_index()
d4['CellType'] = '∆TolC'
d4['Drug'] = '4\'-DTMP'
dd = pd.concat([d1, d2, d3, d4], axis=0)

dd.columns = ['Replicate', 'Concentration', 'OD', 'CellType', 'Drug']
titles = ['TMP', '4\'-DTMP']
df5 = dd.set_index(['CellType', 'Drug', 'Replicate']).pivot(columns='Concentration')
df5.columns = drugconc[:12][::-1]
df5['IC95'] = np.nan
for i in range(len(df5)):
    df5.iloc[i, -1] = findIC95(df5.columns.values, df5.iloc[i, :].values)
IC95 = df5['IC95'].reset_index()
IC95['IC95_ug'] = 0
IC95.loc[IC95.Drug == 'TMP', 'IC95_ug'] = IC95.loc[IC95.Drug == 'TMP', 'IC95'] * mw_tmp * 1e-3
IC95.loc[IC95.Drug == '4\'-DTMP', 'IC95_ug'] = IC95.loc[IC95.Drug == '4\'-DTMP', 'IC95'] * mw_v041 * 1e-3

fig, ax = plt.subplots()
sns.set_style('ticks')
sns.despine()

sns.barplot(x='Drug', y='IC95_ug', hue='CellType', order=['TMP', '4\'-DTMP'], data=IC95,
            palette=palette, ax=ax, capsize=.05, ci='sd', errwidth=1.5, edgecolor='k', errcolor='k')
change_width(ax, .35)
xms = sorted([-0.375, 0.625, 0.025, 1.025])
c = 0
for drug in ['TMP', '4\'-DTMP']:
    for strain in IC95.CellType.unique():
        yvals = IC95.loc[(IC95.Drug == drug) & (IC95.CellType == strain), 'IC95_ug'].values
        xvals = np.ones(len(yvals)) * xms[c] + (np.random.random(len(yvals)) - .5) * .3 + .175
        print(strain, drug, xvals, yvals)
        ax.plot(xvals, yvals, 'o', color='k', markersize=3, alpha=.5)
        c += 1
ax.set_yscale('log')
ax.set_xlabel('Drugs')
ax.set_yticks([0.1, 1, 10])
ax.set_yticklabels([0.1, 1, 10])
ax.set_ylabel('IC$_{95}$ (µg/ml)')
ax.set_ylim(.1, 2)
ax.legend(frameon=False, loc=1)
fig.set_size_inches(3, 2)
fig.tight_layout(pad=0.95)
fig.savefig('BarPlot_IC95-WTdTolC_TMP-V041_ug_wDots.pdf',dpi=600)
fig.savefig('BarPlot_IC95-WTdTolC_TMP-V041_ug_wDots.png',dpi=600)

# dcolors=[ "#386CB0", "#F0027F"]

fig2, ax2 = plt.subplots(1, 2, sharex=True, sharey=True)
sns.set_style('ticks')
sns.despine()
df6 = df5.iloc[:, :-1]
celltype = ['WT', '∆TolC']
drugs = ['TMP', '4\'-DTMP']
mws = [mw_tmp, mw_v041]
for i in [0, 7, 14, 21]:
    c = ((i % 2) + 1) % 2
    x = df6.columns.values * mws[c] * 1e-3
    y = df6.iloc[i, :]
    ax2[c].plot(x, y, '-o', color=colors[i // 14], label=celltype[i // 14], ms=5)
    ax2[c].set_xscale('log')
    ax2[c].set_xlim(1e-2, 1e4)
    ax2[c].set_xticks([0.01, 1, 100, 10000])
    ax2[c].set_xticklabels([0.01, 1, 100, 10000])
    ax2[c].set_xlabel('[' + drugs[c] + '] (µg/ml)')
    ax2[c].set_ylabel('OD$_{600}$')
ax2[0].legend(frameon=False, loc=1)
fig2.set_size_inches(5, 2)
fig2.tight_layout(pad=0.95)
# fig2.savefig('ReprLines_ug.pdf',dpi=600)
# fig2.savefig('ReprLines_ug.png',dpi=600)

# fig,ax=plt.subplots(2,1,sharex=True)
# sns.set_style('ticks')
# sns.despine()
# data1=dd.loc[dd['Drug']=='TMP'].iloc[:,1:]
# sns.lineplot(x='Concentration',y='OD',hue='CellType',markers=True,data=data1,ax=ax[0])
# data2=dd.loc[dd['Drug']=='V041'].iloc[:,1:]
# sns.lineplot(x='Concentration',y='OD',hue='CellType',markers=True,data=data2,ax=ax[1])
# for i in range(2):
#     ax[i].set_xscale('log')
#     ax[i].set_title(titles[i])
#
# # fig.savefig('WT-dTolC_TMP-V041.pdf',dpi=600)

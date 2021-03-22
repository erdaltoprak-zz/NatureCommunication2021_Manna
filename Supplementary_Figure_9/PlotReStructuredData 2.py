import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from Colors import tmpcolor, v041color, mw_tmp, mw_v041, change_width

df = pd.read_csv('AllDataRestructured.csv')
df2 = pd.read_csv('../2020_01_31_MorbPopulations_MIC/All_Data_Restructured_02_04_2020.csv')
df3 = df2.loc[(df2['Day#'] == 21) & (df2['TimeMeasured'] == 24), :].drop(['TimeMeasured', 'Day#'], axis='columns')
df3['MeasuredIn'] = np.nan
df3.loc[df3['EvolvedIn'] == 'TMP', 'MeasuredIn'] = 'TMP'
df3.loc[df3['EvolvedIn'] == 'V041', 'MeasuredIn'] = 'V041'
df3['Replica'] = 1.0
df4 = pd.concat([df, df3], axis='rows', sort=True)

dfSum = df4.loc[:, ['Name', 'EvolvedIn', 'MeasuredIn', 'IC95', 'IC75', 'IC50']].sort_values(
    ['Name', 'EvolvedIn', 'MeasuredIn'])
dfSum.loc[dfSum.EvolvedIn == 'V041', 'EvolvedIn'] = "4'-DTMP"
dfSum.loc[dfSum.MeasuredIn == 'V041', 'MeasuredIn'] = "4'-DTMP"
dfSum['NewName'] = dfSum.Name.str.replace('D21', '')
dfSum['NewName'] = dfSum.NewName.str.replace('T', 'TMP-')
dfSum['NewName'] = dfSum.NewName.str.replace('V', '4\'-DTMP-')
mwdict = {'TMP': mw_tmp * 1e-3, '4\'-DTMP': mw_v041 * 1e-3}
dfSum['mws'] = dfSum.MeasuredIn.apply(lambda x: mwdict[x])

dfSum['IC95_ug'] = dfSum.IC95 * dfSum.mws
dfSum['IC75_ug'] = dfSum.IC75 * dfSum.mws
dfSum['IC50_ug'] = dfSum.IC50 * dfSum.mws

colors = sns.set_palette([tmpcolor, v041color])
collist = [tmpcolor, v041color]
#
fig, ax = plt.subplots(2, 1)
sns.set_style('ticks')
sns.despine()

# sns.barplot(x='NewName',y='IC95',hue='MeasuredIn',palette=colors,
#             data=dfSum.loc[dfSum['EvolvedIn']=='TMP'],
#             ax=ax[0],capsize=.05,ci='sd',errwidth=1.5,edgecolor='k', errcolor='k')
drugorder = ['TMP', "4'-DTMP"]
xms = [sorted([-0.375, 0.625, 1.625, 2.625, 3.625, 4.625, 5.625,
               0.025, 1.025, 2.025, 3.025, 4.025, 5.025, 6.025]),
       sorted([-0.375, 0.625, 1.625, 2.625, 3.625, 4.625, 5.625, 6.625,
               0.025, 1.025, 2.025, 3.025, 4.025, 5.025, 6.025, 7.025])]
for i in range(2):
    dfnow=dfSum.loc[dfSum['EvolvedIn'] == drugorder[i],:]
    sns.barplot(x='NewName', y='IC95_ug', hue='MeasuredIn', palette=colors,
                data=dfnow, ax=ax[i], capsize=.05, ci='sd', errwidth=1.5,
                edgecolor='k', errcolor='k')
    c = 0
    for drug in dfnow.NewName.unique():
        for strain in dfnow.MeasuredIn.unique():
            yvals = dfnow.loc[(dfnow.NewName == drug) & (dfnow.MeasuredIn == strain), 'IC95_ug'].values
            xvals = np.ones(len(yvals)) * xms[i][c] + (np.random.random(len(yvals)) - .5) * .3 + .175
            print(strain, drug, xvals, yvals)
            ax[i].plot(xvals, yvals, 'o', color='k', markersize=3, alpha=.5)
            c += 1
for currax in ax:
    currax.set_yscale('log')
    currax.set_ylim([1, 1e4])
    currax.set_ylabel('IC$_{95}$ (µg/ml)')
    currax.set_xlabel('')
    currax.get_legend().remove()
    currax.set_xticklabels(currax.get_xticklabels(), fontsize=9)
    change_width(currax, 0.35)
currax.legend(frameon=False, loc=1, ncol=2)
fig.set_size_inches(7, 4)
fig.tight_layout(pad=.5)
fig.savefig('LastDays_AllMICValues_SelfCross_IC95ug_wDots.pdf', transparent=True, dpi=600)
fig.savefig('LastDays_AllMICValues_SelfCross_IC95ug_wDots.png', transparent=True, dpi=600)
# df5=dfSum.loc[:,['Name','MeasuredIn','IC95']].set_index('Name')
# df6=df5.pivot(columns='MeasuredIn')

df7 = df.set_index(['Name', 'Replica'])
df8 = df3.set_index(['Name', 'Replica'])

df9 = pd.concat([df7, df8.loc[:, ['IC95', 'IC75', 'IC50']]], axis='columns')
df9.columns = ['EvolvedIn', 'MeasuredIn', 'Culture#', 'IC95-Cross', 'IC75-Cross', 'IC50-Cross', '0.04',
               '0.66', '1.64', '4.1', '10.2', '25.6', '64.0', '160.0', '400.0',
               '1000.0', '1750.0', '2500.0', 'IC95-Self', 'IC75-Self', 'IC50-Self']
for icx in [95, 75, 50]:
    df9['IC' + str(icx) + '-TMP'] = np.nan
    df9.loc[(df9['EvolvedIn'] == 'TMP'), 'IC' + str(icx) + '-TMP'] = df9.loc[
        (df9['EvolvedIn'] == 'TMP'), 'IC' + str(icx) + '-Self']
    df9.loc[(df9['EvolvedIn'] == '4\'-DTMP'), 'IC' + str(icx) + '-TMP'] = df9.loc[
        (df9['EvolvedIn'] == 'V041'), 'IC' + str(icx) + '-Cross']

    df9['IC' + str(icx) + '-V041'] = np.nan
    df9.loc[(df9['EvolvedIn'] == 'V041'), 'IC' + str(icx) + '-4\'-DTMP'] = df9.loc[
        (df9['EvolvedIn'] == '4\'-DTMP'), 'IC' + str(icx) + '-Self']
    df9.loc[(df9['EvolvedIn'] == '4\'-DTMP'), 'IC' + str(icx) + '-4\'-DTMP'] = df9.loc[
        (df9['EvolvedIn'] == 'TMP'), 'IC' + str(icx) + '-Cross']

df10 = df9.loc[:, ['IC95-TMP', 'IC95-4\'-DTMP', 'IC75-TMP', 'IC75-4\'-DTMP', 'IC50-TMP', 'IC50-4\'-DTMP']].reset_index()
np.random.seed(1234)
fig, ax = plt.subplots()
sns.despine()
sns.set_style('ticks')

for name in list(set(df10['Name'])):
    if name[0] == 'T':
        color = collist[0]
    else:
        color = collist[1]
    x = df10.loc[(df10['Name'] == name), 'IC75-TMP'].mean(skipna=True) + np.random.random(1) * -1 ** (
        int(np.random.random(1) * 10)) * 50
    y = df10.loc[(df10['Name'] == name), 'IC75-4\'-DTMP'].mean(skipna=True) + np.random.random(1) * -1 ** (
        int(np.random.random(1) * 10)) * 50
    xerr = df10.loc[(df10['Name'] == name), 'IC75-TMP'].std(skipna=True) / np.sqrt(
        df10.loc[(df10['Name'] == name) & ~(df10['IC75-TMP'].isnull()), 'IC75-TMP'].count())
    yerr = df10.loc[(df10['Name'] == name), 'IC75-4\'-DTMP'].std(skipna=True) / np.sqrt(
        df10.loc[(df10['Name'] == name) & ~(df10['IC75-4\'-DTMP'].isnull()), 'IC75-4\'-DTMP'].count())
    ax.errorbar(x, y, xerr, yerr, marker='o', color=color, markerfacecolor='w', capsize=2)
    print(name, x, y, xerr, yerr)
# sns.scatterplot('IC95-TMP','IC95-V041',hue='EvolvedIn',
#                 x_jitter=10,y_jitter=10,data=df9,ax=ax)

ax.plot([1e2, 1e4], [1e2, 1e4], '--r', alpha=.3)
ax.set_xscale('log')
ax.set_yscale('log')
ax.axis('square')
ax.set_xlim(1e2, 1e4)
ax.set_ylim(1e2, 1e4)

ax.set_xlabel('IC$_{75}$(Trimethoprim) (µg/mL)')
ax.set_ylabel('IC$_{75}$(4\'-DTMP) (µg/mL)')
fig.set_size_inches(5, 5)
# fig.tight_layout(pad=.5)
# fig.savefig('IC75-Scatterplot-TMP-V041.pdf',transparent=True,dpi=600)

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from Colors import colorsall


def despineme(currax, bottom=True):
    if bottom:
        sns.despine(ax=currax)
    else:
        sns.despine(ax=currax, bottom=True)
        currax.xaxis.set_tick_params(width=0, which='both')
        currax.set_xlabel('')
    return None


fakex = -5
fakey = -5

df = pd.read_csv('MutantFrequenciesTime.csv')
df = df.loc[(df['Mutation'].isin(colorsall)) | (df['Freq'] > 1), :]

df1 = df.loc[:, ['Mutation', 'Part1(%)', 'Time', 'Drug', 'Replica']] \
    .set_index(['Drug', 'Replica', 'Mutation'])
df1Piv = df1.pivot(columns='Time')
df1Piv.columns = [0, 4, 8, 12, 20, 24, 28]
df1Piv.reset_index(inplace=True)

df2 = df.loc[:, ['Mutation', 'Freq', 'Time', 'Drug', 'Replica']]
df2['Freq'] /= 100
df3 = df2.groupby(['Mutation', 'Time', 'Drug']).mean()
df4 = df2.groupby(['Mutation', 'Time', 'Drug']).std()
df5 = pd.concat([df3, df4], axis='columns') \
    .reset_index() \
    .drop('Replica', axis='columns') \
    .sort_values(['Drug', 'Mutation', 'Time'], ascending=True)
df5.columns = ['Mutation', 'Time', 'Drug', 'meanFreq(%)', 'stdFreq(%)']

df6 = df3.loc[:, 'Freq'].reset_index() \
    .set_index(['Mutation', 'Drug']) \
    .pivot(columns='Time') \
    .reset_index()
df7 = df4.loc[:, 'Freq'].reset_index() \
    .set_index(['Mutation', 'Drug']) \
    .pivot(columns='Time') \
    .reset_index()
df6.columns = ['Mutation', 'Drug', 0, 4, 8, 12, 20, 24, 28]
df7.columns = ['Mutation', 'Drug', 0, 4, 8, 12, 20, 24, 28]
df7.loc[:, [0, 28]] /= np.sqrt(3)
df7.loc[df7['Drug'].isin(['TMP', 'V041']), [4, 8, 12, 20, 24]] /= np.sqrt(7)
df7.loc[(df7['Drug'] == 'ND'), [4, 8, 12, 20, 24]] /= np.sqrt(3)

titlelabels = {'ND': 'No Drug', 'TMP': 'TMP', 'V041': '4\'-DTMP'}
mutantsall=['c-35t','g-31a','I5F','D27E','D27K','L28R','W30R','I94L','R98P','F153S']
fig, ax = plt.subplots(3, 1, sharey=True, sharex=True)
sns.set_style('ticks')
sns.despine()

c = 0
for drugnow in ['ND', 'TMP', 'V041']:
    currax = ax[c]
    mdfnow = df6.loc[df6['Drug'] == drugnow, :]
    sdfnow = df7.loc[df7['Drug'] == drugnow, :]
    for mutant in mdfnow['Mutation'].values:
        kwknowns = dict(marker='o', markeredgecolor='k', linewidth=.75, linestyle='-', capsize=3, markersize=6,
                        ecolor='k')
        if mutant in colorsall:
            currax.errorbar(mdfnow.columns[2:], mdfnow.loc[mdfnow['Mutation'] == mutant, :].values[0][2:],
                            sdfnow.loc[sdfnow['Mutation'] == mutant, :].values[0][2:],
                            color=colorsall[mutant], **kwknowns)
    currax.set_ylabel('Frequency - ' + titlelabels[drugnow])
    currax.set_xlim(-1, 30)
    currax.set_ylim(-.1, 1.05)
    if c == 2:
        currax.set_xlabel('Time (h)')
    if drugnow == 'TMP':
        for m in mutantsall:
            currax.errorbar(fakex, fakey, yerr=1, color=colorsall[m], label=m, **kwknowns)
        currax.legend(frameon=False, loc=1,
                      ncol=2, bbox_to_anchor=(1, .85),
                      fontsize=8, markerscale=.75)
    c += 1
fig.set_size_inches(4, 5)
fig.tight_layout(pad=.5)
fig.savefig('FreqTimeSumm.png', dpi=600, transparent=True)
fig.savefig('FreqTimeSumm.pdf', dpi=600, transparent=True)

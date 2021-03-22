import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from Colors import tmpcolor, v041color

df = pd.read_csv('4AB/All_Data_Restructured_02_04_2020.csv')
wts = df.loc[df['Name'] == 'TB194', :]
dff = df.loc[~(df['Name'].isin(['B', 'TB194'])), :].reset_index(drop=True)
dff.loc[(dff['Name'] == 'T7D21'), 'IC50'] = 2500
icsTMP24 = wts.loc[(wts['EvolvedIn'] == 'TMP') &
                   (wts['TimeMeasured'] == 24), ['IC95', 'IC75', 'IC50']].median()
icsTMP48 = wts.loc[(wts['EvolvedIn'] == 'TMP') &
                   (wts['TimeMeasured'] == 48), ['IC95', 'IC75', 'IC50']].median()
icsV04124 = wts.loc[(wts['EvolvedIn'] == 'V041') &
                    (wts['TimeMeasured'] == 24), ['IC95', 'IC75', 'IC50']].median()
icsV04148 = wts.loc[(wts['EvolvedIn'] == 'V041') &
                    (wts['TimeMeasured'] == 48), ['IC95', 'IC75', 'IC50']].median()
for i in range(1, 8):
    newname = 'T' + str(i) + 'D0'
    dff.loc[len(dff)] = [newname, 'TMP', i, 0, 24, icsTMP24.values[0], icsTMP24.values[1], icsTMP24.values[2], np.nan,
                         np.nan,
                         np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan]
    dff.loc[len(dff)] = [newname, 'TMP', i, 0, 48, icsTMP48.values[0], icsTMP48.values[1], icsTMP48.values[2], np.nan,
                         np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan,
                         np.nan, np.nan]
for i in range(1, 9):
    newname = 'V' + str(i) + 'D0'
    dff.loc[len(dff)] = [newname, 'V041', i, 0, 24, icsV04124.values[0], icsV04124.values[1], icsV04124.values[2],
                         np.nan, np.nan,
                         np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan]
    dff.loc[len(dff)] = [newname, 'V041', i, 0, 48, icsV04148.values[0], icsV04148.values[1], icsV04148.values[2],
                         np.nan,
                         np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan,
                         np.nan, np.nan]

colors = [tmpcolor, v041color]
colors_r=[v041color]
for timemeas in ['IC50']:  # 'IC95', ,'IC50'
    dff2 = dff.loc[dff['TimeMeasured'] == 24, :]
    dff2.sort_values(by=['Culture#', 'TimeMeasured', 'EvolvedIn', 'Day#'], inplace=True)
    fig, ax = plt.subplots()
    sns.set_style('ticks')
    sns.despine()
    currax = ax  # [0]
    sns.lineplot(x='Day#', y=timemeas, hue='EvolvedIn', err_style='bars', ci=0,
                 markers=True, palette=colors, marker='o', markersize=6, markeredgewidth=0, lw=3,
                 data=dff2, legend=False, ax=currax)
    sns.lineplot(x='Day#', y=timemeas, hue='EvolvedIn', units='Culture#',
                 estimator=None, palette=colors, lw=.5, data=dff2, ax=currax, **dict(alpha=.8))
    currax.set_xlabel('Time (d)')
    currax.set_ylabel('IC$_{50}$ (µg/mL)')
    currax.set_yscale('log')

    handles, labels = currax.get_legend_handles_labels()
    currax.legend(handles[1:], ['TMP', '4\'-DTMP'], frameon=False, loc=4, fontsize=10)

    fig.set_size_inches(3.6, 2.4)
    fig.tight_layout()
    fig.savefig(timemeas + 'TwoTimePoints-3x2.pdf', dpi=600)
    fig.savefig(timemeas + 'TwoTimePoints-3x2.png', transparent=True, dpi=600)

legendbool = ['full']+[False]*3+['full']+[False]*3
fig2, ax2 = plt.subplots(2, 4)
sns.set_style('ticks')

for i in range(8):
    row, col = (i // len(ax2[0]), i % len(ax2[0]))
    currax = ax2[row, col]
    if i==7:
        df = dff2.loc[(dff2['Culture#'] == i + 1), :]
        sns.lineplot(x='Day#', y='IC75', hue='EvolvedIn',
                     palette=colors_r, markers=True, marker='o', data=df, ax=currax, legend=legendbool[i])
    else:
        df = dff2.loc[(dff2['Culture#'] == i+1), :]
        sns.lineplot(x='Day#', y='IC75', hue='EvolvedIn',
                     palette=colors, data=df, markers=True, marker='o', ax=currax,legend=legendbool[i])
    currax.set_yscale('log')
    currax.set_ylabel('IC$_{75}$ (µg/mL)')
    currax.set_xlabel('Time (d)')
    currax.set_ylim(6e-1,7e3)
    # currax.set_title('Culture-'+str(i+1),y=.9)
    if i in [0, 4]:
        sns.despine(ax=currax)
        handles, labels = currax.get_legend_handles_labels()
        currax.legend(handles[1:], ['TMP', '4\'-DTMP'], frameon=False, loc=4, bbox_to_anchor=(1.1,-.1))
    else:
        sns.despine(ax=currax, left=True)
        currax.set_yticklabels([])
        currax.yaxis.set_tick_params(width=0,which='both')
        currax.set_ylabel('')
    if i<4:
        currax.set_xlabel('')
fig2.set_size_inches(6.8,3)
fig2.tight_layout(pad=.5)
# fig2.savefig(timemeas + 'IndividualCultures.pdf', dpi=600)
# fig2.savefig(timemeas + 'IndividualCultures.png', transparent=True, dpi=600)



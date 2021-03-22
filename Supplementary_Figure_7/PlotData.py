import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from Colors import change_width, mw_tmp, mw_v041
#
# def change_width(ax, new_value):
#     for patch in ax.patches:
#         current_width = patch.get_width()
#         diff = current_width - new_value
#         # we change the bar width
#         patch.set_width(new_value)
#         # we recenter the bar
#         patch.set_x(patch.get_x() + diff * .5)


def findIC95(ODs):
    # print(ODs,ODs.index)
    concs = ODs.index
    ODs = ODs.values
    ODthr = max(ODs) * .05
    ODbool = ODs < ODthr
    IC95 = min(concs[ODbool])
    return IC95


# df=pd.read_excel('TMPMorbPopulations_MIC_TMP-V041_2019_10_23.xlsx','BgCorrected')
df = pd.read_excel('TMPMorbPopulations_MIC_TMP-V041_2019_10_23_48h.xlsx', 'BgCorrected')

conc = [9000 * ((1 / 3) ** i) for i in range(12)] * 8
drugs = ['TMP'] * 48 + ['4\'-DTMP'] * 48
reps = [1] * 12 + [2] * 12 + [3] * 12 + [4] * 12 + [1] * 12 + [2] * 12 + [3] * 12 + [4] * 12
df['Concentration'] = conc
df['Drug'] = drugs
df['Replica'] = reps
df2 = df.set_index(['Concentration', 'Drug', 'Replica']).stack().reset_index()
df2.columns = ['Concentration', 'Drug', 'Replica', 'Population', 'OD']
colors = ["darkgrey", "teal"]
palette = sns.color_palette(colors)
fig, ax = plt.subplots(2, 3, sharey=True, sharex=True)
sns.set_style('ticks')
sns.despine()
c = 0
# gentitle='Observed Mutants\n'
domgenotypes = ['- c-35t/D27E\n- c-35t/F153S', '- g-31a/R98P', '- c-35t/L28R',
                '- c-35t/W30R', '- c-35t/W30R\n- c-35t/I5F', '- c-35t/I94L']
legendBool = [False, 'brief', False, False, False, False]  # ['full']+[False]*7
for i in list(set(df2['Population'])):
    if i in [6, 8]:
        continue
    axnow = ax[c // len(ax[0]), c % len(ax[0])]
    # row,col=(c//len(ax[0]), c%len(ax[0]))
    df3 = df2.loc[df2['Population'] == i]
    df3.loc[(df3.Concentration>500)&(df3.Drug=='4\'-DTMP'),'OD']=0
    df3['Concentration_ug']=0
    df3.loc[df3.Drug=='TMP','Concentration_ug'] = df3.loc[df3.Drug=='TMP','Concentration'] * mw_tmp * 1e-3
    df3.loc[df3.Drug == '4\'-DTMP', 'Concentration_ug'] = df3.loc[df3.Drug == '4\'-DTMP', 'Concentration'] * mw_v041 * 1e-3
    sns.lineplot(x='Concentration_ug', y='OD', hue='Drug', ci='sd',
                 markers=True, marker='o',
                 ms=5, palette=palette,
                 legend=legendBool[c], data=df3, ax=axnow)
    axnow.set_xscale('log')
    axnow.set_ylim(-0.01, 0.5)
    # axnow.set_xticks([1e-2, 1, 100, 10000])
    axnow.axvline(500, *[0, 1], linestyle='--',
                  color='k', zorder=0, alpha=.8, lw=.75)
    axnow.set_xlabel('')
    axnow.text(axnow.get_xlim()[0] * 2, axnow.get_ylim()[0] + .01,
               domgenotypes[c], horizontalalignment='left',
               verticalalignment='bottom', fontsize=9)#, fontweight='bold')  # gentitle+
    axnow.set_xlim(1e-2,1e4)
    if c == 1:
        handles, labels= axnow.get_legend_handles_labels()
        axnow.legend(handles[1:],labels[1:], frameon=False, loc='upper center', ncol=2)
        # legend = axnow.legend(frameon=False, loc='upper center', bbox_to_anchor=(0.28, 1.1), ncol=3, fontsize=8)
        # legend.texts[0].set_text('')
    if c//len(ax[0]) == 1:
        axnow.set_xlabel('[Drug] (µg/ml)')
    if c%len(ax[0]) == 0 :
        axnow.set_ylabel( 'OD$_{600}$')

    c += 1
# g=sns.FacetGrid(data=df2,col='Population',col_wrap=4)
# g.map(sns.lineplot,'Concentration','OD')
fig.set_size_inches(6, 3)
fig.tight_layout(pad=.5)
fig.savefig('MIC_MorbPopulations_48h_2r3c_ug.pdf', dpi=600)
# fig.savefig('MIC_MorbPopulations_48h_6r1c.png',dpi=600)

df4 = df2.set_index(['Drug', 'Replica', 'Population']).pivot(columns='Concentration')
df4.columns = conc[:12][::-1]
df4['IC95'] = df4.apply(findIC95, axis=1)

IC95 = df4['IC95'].reset_index()
IC95.columns = ['Drug', 'Replica', 'Population', 'IC95']
IC95 = IC95.loc[~(IC95.Population.isin([6, 8])), :]
IC95['IC95_ug'] = 0
IC95.loc[IC95.Drug == 'TMP', 'IC95_ug'] = IC95.loc[IC95.Drug == 'TMP', 'IC95'] * mw_tmp * 1e-3
IC95.loc[IC95.Drug == '4\'-DTMP', 'IC95_ug'] = IC95.loc[IC95.Drug == '4\'-DTMP', 'IC95'] * mw_v041 * 1e-3

fig2, ax2 = plt.subplots()
sns.set_style('ticks')
sns.despine()
sns.barplot(x='Population', y='IC95_ug', hue='Drug',
            capsize=.05,errcolor='k',ci='sd',
            edgecolor='k',errwidth=1, data=IC95,
            hue_order=['TMP','4\'-DTMP'],
            palette=palette, ax=ax2)
ax2.set_yscale('log')
ax2.set_ylim(1, 1e4)
ax2.set_xlabel('Dominant Genotype(s)')
ax2.set_ylabel('IC$_{95}$ (µg/ml)')
ax2.set_xticklabels([f.replace('-','') for f in domgenotypes])
ax2.legend(frameon=False, loc=1, ncol=2, bbox_to_anchor=(1,1.2))
change_width(ax2, .35)

xms = sorted([-0.375, 0.625, 1.625, 2.625, 3.625, 4.625,
              0.025, 1.025, 2.025, 3.025, 4.025, 5.025])
c = 0
for strain in IC95.Population.unique():
    for drug in ['TMP','4\'-DTMP']:
        yvals = IC95.loc[(IC95.Population == strain) & (IC95.Drug == drug), 'IC95_ug'].values
        xvals = np.ones(len(yvals)) * xms[c] + (np.random.random(len(yvals)) - .5) * .25 + .175
        # print(strain, drug, xvals, yvals)
        ax2.plot(xvals, yvals, 'o', color='k', markersize=3, alpha=.5)
        c += 1
fig2.set_size_inches(6, 2)
fig2.tight_layout(pad=.5)
fig2.savefig('MIC_MorbPopulations_IC95_48h_ug_wDots.pdf',dpi=600)

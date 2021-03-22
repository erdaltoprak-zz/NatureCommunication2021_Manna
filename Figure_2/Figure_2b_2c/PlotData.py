import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from Colors import tmpcolor, v041color, change_width, mw_tmp, mw_v041

palette = [tmpcolor, v041color]
df = pd.read_csv('IC95.csv')
df = df.set_index(['strain', 'drug']).stack().reset_index()
df.columns = ['Strain', 'Drug', 'Replica', 'IC_95']
df['IC_95'] *= 1000
df.loc[df['Drug'] == 'V-041', 'Drug'] = '4\'-DTMP'
fig, ax = plt.subplots()
sns.set_style('ticks')
sns.despine()
sns.barplot(x='Strain', y='IC_95', hue='Drug', data=df,
            palette=palette, capsize=.05,
            ci='sd', errwidth=1.5, edgecolor='k')
sns.pointplot(x='Strain', y='IC_95', hue='Drug', data=df, palette=palette,edgecolor='k')
change_width(ax, 0.35)
ax.set_yscale('log')
ax.set_ylabel('$IC_{95}$ (µM)')
ax.legend(frameon=False, loc=2, fontsize=8)
ax.set_xlabel('DHFR Variant')
ax.set_ylim(1e0, 1e4)
fig.set_size_inches(2.33, 2)
fig.tight_layout(pad=.95)
# fig.savefig('WT-L28R-TMP-V041-Barplot.png', transparent=True, dpi=600)
# fig.savefig('WT-L28R-TMP-V041-Barplot.pdf', dpi=600)

df2 = pd.read_csv('RepresentativeLines.csv')
df2['Concentration'] *= 1000
df2.loc[df2['Concentration'] == 0, 'Concentration'] = 4.23e-2
df2['FinalValue'] -= 0.0432
df2.loc[df2['FinalValue'] < 1e-2, 'FinalValue'] = 1e-2
df2.loc[(df2['Drug'] == 'V-041') & (df2['Concentration'] > 833), 'FinalValue'] = 1e-2
df2.loc[df2['Drug'] == 'V-041', 'Drug'] = '4\'-DTMP'

titles = ['WT', 'L28R']
fig, ax = plt.subplots(1, 2, sharey=True)
sns.set_style('ticks')
sns.despine()
sns.lineplot(x='Concentration', y='FinalValue', hue='Drug', data=df2.loc[df2['Strain'] == 'WT', :],
             marker='o', palette=palette, ax=ax[0])
sns.lineplot(x='Concentration', y='FinalValue', hue='Drug', data=df2.loc[df2['Strain'] == 'L28R', :],
             marker='o', legend=False, palette=palette, ax=ax[1])
for i in range(2):
    ax[i].set_xscale('log')
    ax[i].set_yscale('log')
    ax[i].set_xlim(4.23e-2, 1e4)
    ax[i].set_xticks([4.23e-2, 1e-1, 1e0, 1e1, 1e2, 1e3, 1e4])
    ax[i].set_xticklabels(['0', '', '1', '', '$10^2$', '', '$10^4$'])
    ax[i].set_yticks([1e-2, 1e-1, 1])
    ax[i].set_yticklabels(['0', '0.1', '1'])
    ax[i].set_ylim(8e-3, 1)
    ax[i].set_ylabel('OD$_{600}$')
    ax[i].set_xlabel('Drug (µM)')
    ax[i].set_title(titles[i], fontweight='bold')
handles, labels = ax[0].get_legend_handles_labels()
ax[0].legend(handles=handles[1:], labels=labels[1:], frameon=False, fontsize=8)

fig.set_size_inches(4.67, 2)
fig.tight_layout(pad=.95)
fig.savefig('WT-L28R-ReprLines.png', transparent=True, dpi=600)
fig.savefig('WT-L28R-ReprLines.pdf', dpi=600)

######## Convert Concentration to ug/mL ############
df['IC_95_ug']=0
df.loc[df.Drug=='TMP','IC_95_ug']=df.loc[df.Drug=='TMP','IC_95'] * mw_tmp * 1e-3
df.loc[df.Drug=="4\'-DTMP",'IC_95_ug']=df.loc[df.Drug=="4\'-DTMP",'IC_95'] * mw_v041 * 1e-3


fig, ax = plt.subplots()
sns.set_style('ticks')
sns.despine()
sns.barplot(x='Strain', y='IC_95_ug', hue='Drug', data=df,
            palette=palette, capsize=.05,
            ci='sd', errwidth=1.5, edgecolor='k')
# sns.swarmplot(x='Strain', y='IC_95_ug', hue='Drug',
#               data=df, palette=palette,edgecolor='k', zorder=10)
change_width(ax, 0.35)
xms=[-.2, .2, .8, 1.2]
c=0
for strain in df.Strain.unique():
    for drug in df.Drug.unique():
        yvals= df.loc[(df.Strain==strain)&(df.Drug==drug),'IC_95_ug'].values
        xvals= np.ones(len(yvals))*xms[c] + (np.random.random(len(yvals))-.5)*.2
        ax.plot(xvals, yvals, 'o', color='k', markersize=2, alpha=.3)
        c+=1

ax.set_yscale('log')
ax.set_ylabel('IC$_{95}$ (µg/mL)')
ax.legend(frameon=False, loc=2, fontsize=8, bbox_to_anchor=(0.,1.1))
ax.set_xlabel('DHFR Variant')
ax.set_ylim(3e-1, 1e4)
ax.set_yticks([1e0, 1e2, 1e4])
fig.set_size_inches(2.33, 2)
fig.tight_layout(pad=.95)
fig.savefig('WT-L28R-TMP-V041-Barplot_ug_wDots.png', transparent=True, dpi=600)
fig.savefig('WT-L28R-TMP-V041-Barplot_ug_wDots.pdf', dpi=600)


df2['Concentration_ug']=0
df2.loc[df2.Drug=='TMP','Concentration_ug']=df2.loc[df2.Drug=='TMP','Concentration'] * mw_tmp * 1e-3
df2.loc[df2.Drug=="4\'-DTMP",'Concentration_ug']=df2.loc[df2.Drug=="4\'-DTMP",'Concentration'] * mw_v041 * 1e-3
fig, ax = plt.subplots(1, 2, sharey=True)
sns.set_style('ticks')
sns.despine()
sns.lineplot(x='Concentration_ug', y='FinalValue', hue='Drug', data=df2.loc[df2['Strain'] == 'WT', :],
             marker='o', palette=palette, ax=ax[0])
sns.lineplot(x='Concentration_ug', y='FinalValue', hue='Drug', data=df2.loc[df2['Strain'] == 'L28R', :],
             marker='o', legend=False, palette=palette, ax=ax[1])
for i in range(2):
    ax[i].set_xscale('log')
    ax[i].set_yscale('log')
    ax[i].set_xlim(4.23e-2, 1e4)
    ax[i].set_xticks([4.23e-2, 1e-1, 1e0, 1e1, 1e2, 1e3, 1e4])
    ax[i].set_xticklabels(['0', '', '1', '', '$10^2$', '', '$10^4$'])
    ax[i].set_yticks([1e-2, 1e-1, 1])
    ax[i].set_yticklabels(['0', '0.1', '1'])
    ax[i].set_ylim(8e-3, 1)
    ax[i].set_ylabel('OD$_{600}$')
    ax[i].set_xlabel('Drug (µg/mL)')
    ax[i].set_title(titles[i], fontweight='bold')
handles, labels = ax[0].get_legend_handles_labels()
ax[0].legend(handles=handles[1:], labels=labels[1:], frameon=False, fontsize=8)

fig.set_size_inches(4.67, 2)
fig.tight_layout(pad=.95)
fig.savefig('WT-L28R-ReprLines_ug.png', transparent=True, dpi=600)
fig.savefig('WT-L28R-ReprLines_ug.pdf', dpi=600)
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


df=pd.read_csv('All_Data_Restructured_02_04_2020.csv')
wts=df.loc[df['Name']=='TB194',:]
dff=df.loc[~(df['Name'].isin(['B','TB194'])) ,:].reset_index(drop=True)
dff.loc[(dff['Name']=='T7D21'),'IC50']=2500
icsTMP24=wts.loc[(wts['EvolvedIn']=='TMP')&
               (wts['TimeMeasured']==24),['IC95','IC75','IC50']].median()
icsTMP48=wts.loc[(wts['EvolvedIn']=='TMP')&
               (wts['TimeMeasured']==48),['IC95','IC75','IC50']].median()
icsV04124=wts.loc[(wts['EvolvedIn']=='V041')&
               (wts['TimeMeasured']==24),['IC95','IC75','IC50']].median()
icsV04148=wts.loc[(wts['EvolvedIn']=='V041')&
               (wts['TimeMeasured']==48),['IC95','IC75','IC50']].median()
for i in range(1,8):
    newname='T'+str(i)+'D0'
    dff.loc[len(dff)]=[newname,'TMP',i,0,24,icsTMP24.values[0],icsTMP24.values[1],icsTMP24.values[2],np.nan,np.nan,
                       np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan]
    dff.loc[len(dff)] = [newname, 'TMP', i, 0, 48, icsTMP48.values[0], icsTMP48.values[1], icsTMP48.values[2], np.nan,
                         np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan,
                         np.nan, np.nan]
for i in range(1,9):
    newname='V'+str(i)+'D0'
    dff.loc[len(dff)]=[newname,'V041',i,0,24,icsV04124.values[0],icsV04124.values[1],icsV04124.values[2],np.nan,np.nan,
                       np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan]
    dff.loc[len(dff)] = [newname, 'V041', i, 0, 48, icsV04148.values[0], icsV04148.values[1], icsV04148.values[2], np.nan,
                         np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan,
                         np.nan, np.nan]

colors=sns.set_palette([ "#386CB0", "#F0027F"])
# grid=sns.FacetGrid(data=dff, col='Culture#',hue='EvolvedIn',
#                    col_wrap=4,subplot_kws=dict(yscale='log'))
# grid.map(sns.lineplot,'Day#','IC95',markers=True,marker='o',palette=colors)
# plt.savefig('AllCultures_IC95_TMP_V041_24h.pdf',transparent=True,dpi=600)
# grid=sns.FacetGrid(data=dff, col='Culture#',hue='EvolvedIn',
#                    col_wrap=4,subplot_kws=dict(yscale='log'))
# grid.map(sns.lineplot,'Day#','IC75',markers=True,marker='o',palette=colors)
# plt.savefig('AllCultures_IC75_TMP_V041_24h.pdf',transparent=True,dpi=600)
# grid=sns.FacetGrid(data=dff, col='Culture#',hue='EvolvedIn',
#                    col_wrap=4,subplot_kws=dict(yscale='log'))
# grid.map(sns.lineplot,'Day#','IC50',markers=True,marker='o',palette=colors)
# plt.savefig('AllCultures_IC50_TMP_V041_24h.pdf',transparent=True,dpi=600)
for timemeas in ['IC95','IC75','IC50']:
    dff2=dff.loc[dff['TimeMeasured']==24,:]
    dff2.sort_values(by=['Culture#','TimeMeasured','EvolvedIn','Day#'],inplace=True)
    fig,ax=plt.subplots(1,2,sharey=True)
    sns.set_style('ticks')
    sns.despine()
    sns.lineplot(x='Day#',y=timemeas,hue='EvolvedIn',err_style='bars',ci=0,data=dff2,legend=False,ax=ax[0])
    sns.lineplot(x='Day#',y=timemeas,hue='EvolvedIn',units='Culture#',estimator=None,lw=.25,data=dff2,**dict(alpha=.5),ax=ax[0])
    ax[0].set_xlabel('Time (days)')
    ax[0].set_ylabel(timemeas+' (µg/mL)')

    ax[0].set_yscale('log')
    ax[0].set_title('Time Measured=24h')
    # fig.savefig('AllInOnePlotIC50.pdf',transparent=True,dpi=600)


    dff3=dff.loc[dff['TimeMeasured']==48,:]
    dff3.sort_values(by=['Culture#','TimeMeasured','EvolvedIn','Day#'],inplace=True)
    # fig,ax=plt.subplots()
    # sns.set_style('ticks')
    # sns.despine()
    sns.lineplot(x='Day#',y=timemeas,hue='EvolvedIn',err_style='bars',ci=0,data=dff3,legend=False,ax=ax[1])
    sns.lineplot(x='Day#',y=timemeas,hue='EvolvedIn',units='Culture#',estimator=None,lw=.25,data=dff3,**dict(alpha=.5),ax=ax[1])
    ax[1].set_xlabel('Time (days)')
    ax[1].set_ylabel(timemeas+' (µg/mL)')

    ax[1].set_yscale('log')
    ax[1].set_title('Time Measured=48h')

    for i in range(2):
        ax[i].set_ylim(.5,1e4)
    fig.set_size_inches(6,3)
    fig.tight_layout()
    fig.savefig(timemeas+'TwoTimePoints.pdf',transparent=True,dpi=600)
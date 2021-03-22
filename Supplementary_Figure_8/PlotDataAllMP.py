import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
global icfact
def findIC95(ODs):
    # print(ODs,ODs.index)
    concs=ODs.index
    ODs=ODs.values
    ODthr=max(ODs)*icfact
    ODbool=ODs<ODthr
    if sum(ODbool)<1:
        IC95 = 6250#max(concs)
    else:
        IC95 = min(concs[ODbool])
    return IC95

def parsename(name):
    dd=name.split('D')
    if len(dd)==2:
        day=int(dd[1])
        culture=int(dd[0].replace('T',''))
    else:
        if name=='TB194':
            day=0
            culture='WT'
        elif name=='B':
            day=np.nan
            culture=np.nan
    return day,culture

# def hillfit(x,y):
#     f=1/(1+e^((EC50-x)/h))
#     return

icfact=.5
# df1=pd.read_excel('MIC_of_Master_Plate1_T1_to_T4_48h.xlsx','BgCorrected')
# df2=pd.read_excel('MIC_of_Master_Plate2_T5_to_T7_48h.xlsx','BgCorrected')

df1=pd.read_excel('MIC_of_Master_Plate1_T1_to_T4_24h.xlsx','BgCorrected')
df2=pd.read_excel('MIC_of_Master_Plate2_T5_to_T7_24h.xlsx','BgCorrected')
df1.columns=[.04,.1,.26,.66,1.64,4.1,10.2,25.6,64,160,400,1000,1750,2500]
df2.columns=[.04,.1,.26,.66,1.64,4.1,10.2,25.6,64,160,400,1000,1750,2500]

platelayout=pd.read_excel('/Users/ytalhatamerlab/Dropbox/DHFR Project/12. Morbidostat_MSM_2020/MIC/96 Well Plate Overlay_Master Plate1_Rearranged.xlsx','Sheet2')


# fig,ax=plt.subplots(4,24,sharex=True,sharey=True)
# sns.set_style('ticks')
# sns.despine()
# fig2,ax2=plt.subplots(4,24,sharex=True,sharey=True)
# sns.set_style('ticks')
# sns.despine()
# c=0
# for i in range(4):
#     for j in range(24):
#         axnow1=ax[i,j]
#         axnow2=ax2[i,j]
#         axnow1.semilogx(df1.columns,df1.loc[c,:],'-b')
#         axnow2.semilogx(df2.columns, df2.loc[c, :], '-k')
#         # axnow1.set_xlabel(df1.columns[j%12])
#         # axnow2.set_xlabel(df2.columns[j % 12])
#         axnow1.set_xticks([.1,10,1000])
#         axnow2.set_xticks([.1, 10, 1000])
#         c+=1
#
# fig.suptitle('Master Plate 1')
# fig2.suptitle('Master Plate 2')
# fig.set_size_inches(12,4)
# fig.savefig('MP1-OD_vs_Time_48h.pdf',dpi=500)
#
# fig2.set_size_inches(12,4)
# fig2.savefig('MP2-OD_vs_Time_48h.pdf',dpi=500)
#


################## MIC Calculation and Visualization ##################
mp1=pd.DataFrame(np.zeros((96,3)),index=range(96),columns=['Culture#','Day#','IC95'])
mp2=pd.DataFrame(np.zeros((96,3)),index=range(96),columns=['Culture#','Day#','IC95'])
mp1['EvolvedIn']='TMP'
mp2['EvolvedIn']='TMP'

platelayout=pd.read_excel('/Users/ytalhatamerlab/Dropbox/DHFR Project/12. Morbidostat_MSM_2020/MIC/96 Well Plate Overlay_Master Plate1_Rearranged.xlsx','Sheet2')
platelayout2=pd.read_excel('/Users/ytalhatamerlab/Dropbox/DHFR Project/12. Morbidostat_MSM_2020/MIC/96 Well Plate Overlay_Master Plate2_Rearranged.xlsx','Sheet2')

mp1['Name']=platelayout['MasterPlate-1']
mp2['Name']=platelayout2['MasterPlate-2']
for i in range(96):
    print()
for i in range(96):
    ods=df1.loc[i,:]
    mp1['Day#'][i],mp1['Culture#'][i]=parsename(platelayout.loc[i, "MasterPlate-1"])
    if max(ods)<0.01:
        mp1['IC95'][i]=0
    else:
        mp1['IC95'][i]=findIC95(ods)

    ods2=df2.loc[i,:]
    mp2['Day#'][i], mp2['Culture#'][i] = parsename(platelayout2.loc[i, "MasterPlate-2"])
    if max(ods2)<0.01:
        mp2['IC95'][i]=0
    else:
        mp2['IC95'][i]=findIC95(ods2)

WT=pd.concat([mp1.loc[mp1['Culture#']=='WT',:],mp2.loc[mp1['Culture#']=='WT',:]],axis='rows')
alldata=pd.concat([mp1,mp2],axis='rows')
alldata=alldata.loc[~(alldata['Name'].isin(['TB194','B'])),:]
for i in range(1,8):
    alldata.loc[len(alldata)]=[i,0,WT['IC95'].mean(),'TMP','T'+str(i)+'D0']
alldata.sort_values(by=['Culture#','Day#'],ascending=True,inplace=True)

# alldata.loc[(alldata['Culture#']==7)&(alldata['Day#']==21),'IC95']=2500
# fig,ax=plt.subplots(2,4,sharex=True,sharey=True)
# sns.set_style('ticks')
# sns.despine()
#
# for i in range(1,8):
#     axnow=ax[(i-1)//len(ax[0]),(i-1)%len(ax[0])]
#     df=alldata.loc[alldata['Culture#']==i,:]
#     sns.lineplot(x='Day#',y='IC95',markers=True,marker='o',data=df,ax=axnow)
#     axnow.set_yscale('log')
#     axnow.set_xlabel('Time (days)')
#     axnow.set_ylabel('$IC_{50}$ (µg/mL)')
#     axnow.set_title('Culture #: {0}'.format(i))
#
# ax[1,3].axis('off')
# fig.set_size_inches(8,4)
# fig.savefig('MorbidostatPopulations_Days_24h_IC50.pdf',transparent=True,dpi=600)



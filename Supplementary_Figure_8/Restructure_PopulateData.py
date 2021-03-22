import pandas as pd
import numpy as np

def parsename(name):
    dd=name.split('D')
    if len(dd)==2:
        day=int(dd[1])
        culture=int(dd[0].replace('T','').replace('V',''))
    else:
        if name=='TB194':
            day=0
            culture=0
        elif name=='B':
            day=np.nan
            culture=np.nan
    return day,culture

def findICx(ODs):
    concs=ODs.index
    ODs=ODs.values
    ODthr=max(ODs)*(1-icx)
    ODbool=ODs<ODthr
    if sum(ODbool)<1:
        ICx = 6250#max(concs)
    else:
        ICx = min(concs[ODbool])
    return ICx

def reshapedata(df_results,platelayout,timemeasurement,evolvedin):
    global icx
    df=pd.DataFrame(index=platelayout,columns=['EvolvedIn','Culture#','Day#','TimeMeasured','IC95','IC75','IC50'])
    df['TimeMeasured']=timemeasurement
    df['EvolvedIn']=evolvedin
    days,cultures=np.transpose(list(map(parsename,platelayout)))
    df['Day#']=days
    df['Culture#']=cultures
    for icx in [0.95,0.75,0.5]:
        df['IC'+str(int(icx*100))]=df_results.apply(findICx, axis='columns')
    dfall=pd.concat([df,df_results],axis='columns')
    dfall.index.name='Name'
    dfall.reset_index(inplace=True)
    dfall['Culture#'].astype('float',inplace=True)
    dfall['Day#'].astype('float', inplace=True)
    dfall.sort_values(by=['Culture#','Day#'], inplace=True)

    return dfall




dflayouts=pd.read_excel('PlateLayouts.xlsx','Sheet1')
concs=[.04,.1,.26,.66,1.64,4.1,10.2,25.6,64,160,400,1000,1750,2500]

mp1=pd.read_excel('MIC_of_Master_Plate1_T1_to_T4_24h.xlsx','BgCorrected').set_index(dflayouts[1])
mp1.columns=concs
df1=reshapedata(mp1,mp1.index,24,'TMP')

mp2=pd.read_excel('MIC_of_Master_Plate2_T5_to_T7_24h.xlsx','BgCorrected').set_index(dflayouts[2])
mp2.columns=concs
df2=reshapedata(mp2,mp2.index,24,'TMP')

mp3=pd.read_excel('MIC_of_Master_Plate3_V1_to_V4_24h.xlsx','BgCorrected').set_index(dflayouts[3])
mp3.columns=concs
df3=reshapedata(mp3,mp3.index,24,'V041')

mp4=pd.read_excel('MIC_of_Master_Plate4_V5_to_V8_24h.xlsx','BgCorrected').set_index(dflayouts[4])
mp4.columns=concs
df4=reshapedata(mp4,mp4.index,24,'V041')

mp5=pd.read_excel('MIC_of_Master_Plate1_T1_to_T4_48h.xlsx','BgCorrected').set_index(dflayouts[1])
mp5.columns=concs
df5=reshapedata(mp5,mp5.index,48,'TMP')

mp6=pd.read_excel('MIC_of_Master_Plate2_T5_to_T7_48h.xlsx','BgCorrected').set_index(dflayouts[2])
mp6.columns=concs
df6=reshapedata(mp6,mp6.index,48,'TMP')

mp7=pd.read_excel('MIC_of_Master_Plate3_V1_to_V4_48h.xlsx','BgCorrected').set_index(dflayouts[3])
mp7.columns=concs
df7=reshapedata(mp7,mp7.index,48,'V041')

mp8=pd.read_excel('MIC_of_Master_Plate4_V5_to_V8_48h.xlsx','BgCorrected').set_index(dflayouts[4])
mp8.columns=concs
df8=reshapedata(mp8,mp8.index,48,'V041')

df=pd.concat([df1, df2,df3,df4,df5,df6,df7,df8], axis='rows')
df.sort_values(by=['Culture#','TimeMeasured','EvolvedIn','Day#'],inplace=True)
df.to_csv('All_Data_Restructured_02_04_2020.csv',index=False)

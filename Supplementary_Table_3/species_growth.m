%2/4/2021: plotting bacterial growth for Madhu
%{
There are total 16 strains, one WT (8 replicates), 7 strains evolved in TMP (T1 to T7, 4 replicates each) 
and 8 strains evolved in 4'-DTMP (DTMP1 to DTMP8, 4 replicates each). 
Attached are the plate layout (96-well plate) and the data from our plate reader.
We need the individual OD600 vs time curve along with the growth rates. 
%}
%% Export data to matlab 
clearvars; close all; clc
tbl_OD=readtable('Day21_NoDrug_2021_02_02.xlsx'); %this gets the numeric parts, convenient for OD measurements
tbl_OD=table2array(tbl_OD(1:96,1:end));
tbl_OD2=readcell('Day21_NoDrug_2021_02_02.xlsx');%this reads everything, I want to get time from this 
timeh=tbl_OD2(2,1:end); %241 time points, cell 
timeh_num=zeros(1,length(timeh));
for i=1:length(timeh)
    time_char=char(timeh(i)); %convert to char so that it is not 1x1
    time_char(end)=[]; %remove 's'
    timeh_num(i)=str2double(time_char);
    clear time_char
end
timeh_hour=timeh_num./3600; %convert seconds to hour 
%timeh2=0:300:240*300; %no need, I figured how to pull it from the excel sheet 
%% Subtract background 
%Wells that have media: 
%A1,6,8,
%B5,7,12
%C1,6,8
%D5,7,12
%E1,6,8
%F5,7,12
%G1,6,8
%H1,4,5,7,8,11,12
%I need to figure the row numbers in tbl_OD that corresponds to these wells.

media_rows=[1 6 8, ... %A
    12+5 12+7 12+12,...  %B
    2*12+1 2*12+6 2*12+8, ... %C
    3*12+5, 3*12+7, 3*12+12,... %D
    4*12+1 4*12+6 4*12+8,... %E
    5*12+5, 5*12+7, 5*12+12,... %F
    6*12+1 6*12+6 6*12+8,... %G
    7*12+1 7*12+4 7*12+5 7*12+7 7*12+8 7*12+11 7*12+12];

media_OD=tbl_OD(media_rows,:);
%plot(media_OD,'*') %visually check for outliers 
mean_media_OD=mean(media_OD(:)); %use this for bg subtraction 
std_media_OD=std(media_OD(:));
medeian_media_OD=median(media_OD(:)); 
%% Background subtraction 
OD_bg_corr=tbl_OD-mean_media_OD; %OD background corrected 
OD_bg_corr(OD_bg_corr<0)=0; %correct for negative numbers 
%% Pull strain data 
%WT: A7, B6, C7, D6, E7, F6, G7, H6
wt_rows=[7 12+6 2*12+7 3*12+6 4*12+7 5*12+6 6*12+7 7*12+6];
wt_OD=OD_bg_corr(wt_rows,:); 

tmp1_OD=OD_bg_corr(2:5,:);
tmp2_OD=OD_bg_corr(9:12,:);
tmp3_OD=OD_bg_corr(12+1:12+4,:);
tmp4_OD=OD_bg_corr(12+8:12+11,:);
tmp5_OD=OD_bg_corr(12*2+2:12*2+5,:);
tmp6_OD=OD_bg_corr(12*2+9:12*2+12,:);
tmp7_OD=OD_bg_corr(12*3+1:12*3+4,:);
dtmp1_OD=OD_bg_corr(12*3+8:12*3+11,:);
dtmp2_OD=OD_bg_corr(12*4+2:12*4+5,:);
dtmp3_OD=OD_bg_corr(12*4+9:12*4+12,:);
dtmp4_OD=OD_bg_corr(12*5+1:12*5+4,:);
dtmp5_OD=OD_bg_corr(12*5+8:12*5+11,:);
dtmp6_OD=OD_bg_corr(12*6+2:12*6+5,:);
dtmp7_OD=OD_bg_corr(12*6+9:12*6+12,:);
dtmp8_OD=OD_bg_corr([12*7+2:12*7+3 12*7+9:12*7+10],:);
%% Plot 
x=timeh_hour;
plot(x,wt_OD)
hold on 
plot(x,tmp1_OD)
plot(x,tmp2_OD)
plot(x,tmp3_OD)
plot(x,tmp4_OD)
plot(x,tmp5_OD)
plot(x,tmp6_OD)
plot(x,tmp7_OD)
plot(x,dtmp1_OD)
plot(x,dtmp2_OD)
plot(x,dtmp3_OD)
plot(x,dtmp4_OD)
plot(x,dtmp5_OD)
plot(x,dtmp6_OD)
plot(x,dtmp7_OD)
plot(x,dtmp8_OD)
legend('wt','tmp1','tmp2','tmp3','tmp4','tmp5','tmp6','tmp7',...
    'dtmp1','dtmp2','dtmp3','dtmp4','dtmp5','dtmp6','dtmp7','dtmp8')
%% 
figure 
x=timeh_hour;
plot(x,wt_OD,'b','LineWidth',2)
xlabel('Time [h]')
ylabel('OD')
title('WT')
xlim([0 20])
ylim([0 0.7])
saveas(gcf,['WT.png'])

all_data=[tmp1_OD; tmp2_OD; tmp3_OD; tmp4_OD; tmp5_OD; tmp6_OD; tmp7_OD; dtmp1_OD; ...
    dtmp2_OD; dtmp3_OD; dtmp4_OD; dtmp5_OD; dtmp6_OD; dtmp7_OD; dtmp8_OD];

labelsh={'tmp1','tmp2','tmp3','tmp4','tmp5','tmp6','tmp7',...
    'dtmp1','dtmp2','dtmp3','dtmp4','dtmp5','dtmp6','dtmp7','dtmp8'};

for i=1:15 %15 strains 
    figure
    datah=all_data((i-1)*4+1:(i-1)*4+4,:);
    plot(x,datah,'b','LineWidth',2)
    xlabel('Time [h]')
    ylabel('OD')
    title(labelsh(i))
    xlim([0 20])
    ylim([0 0.7])
    saveas(gcf,cell2mat(strcat(labelsh(i), '.png')))
end

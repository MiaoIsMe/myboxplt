#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
class myplt():
    def cal_Quantile(da):
        if da.count()%2==0:
            p_50=(da[int(da.count()/2-0.5)]+da[int(da.count()/2)])/2
            da1=da[:int(da.count()/2)]
        else:
            p_50=da[int(da.count()/2)]
            da1=da[:int((da.count()+1)/2)]
        if da1.count()%2==0:
            p_75=(da1[int(da1.count()/2-0.5)]+da1[int(da1.count()/2)])/2
            da2=da[int(da.count()/2):]
        else:
            p_75=da1[int(da1.count()/2)]
            da2=da[int((da.count()+1)/2):]
        da2.reset_index(drop=True, inplace=True)
        if da2.count()%2==0:
            p_25=(da2[int(da2.count()/2-0.5)]+da2[int(da2.count()/2)])/2
        else:
            p_25=da2[int(da2.count()/2)]
        da3=da[int(da1.count()/2):(int(da2.count()/2)+int(da.count()/2))]
        da3.reset_index(drop=True, inplace=True)
        return (p_25,p_50,p_75,da3)
    def cal_max_min(da,p_25,p_75):
        ma=da[da<(p_75+(p_75-p_25)*1.5)].max()
        mi=da[da>(p_25-(p_75-p_25)*1.5)].min()
        return (ma,mi)
    def find_ex_point(data):
        da=pd.Series(data).astype(int)
        da=da.sort_values(ascending=False)
        da.reset_index(drop=True, inplace=True)
        p_25,p_50,p_75=myplt.cal_Quantile(da)[:3]
        da_ex=da[(da<(p_25-(p_75-p_25)*1.5)) | (da>(p_75+(p_75-p_25)*1.5))]
        return da_ex
    def cul_all_max_min(data_l):
        data_l=[[int(i) for i in k] for k in data_l]
        return (max([max(i) for i in data_l]),min([min(i) for i in data_l]))
    def cul_step(da_ma,da_mi):
        n=(da_ma-da_mi)/4
        count=0
        while n>10:
            count+=1
            n/=10
        step=int(n)*10**count
        return step
    def info_boxplot(ax,data_l,multiplebox=True,linecolor='black',pointcolor='black'):
        ax.cla()
        lenth=len(data_l)
        ax.set_xlim((0,lenth+1))
        tick_x=range(1,lenth+1)
        ax.set_xticks(tick_x)
        ax.set_xticklabels([str(i) for i in tick_x])
        def cal_per5(da3):
            per_5=[]
            add=da3.count()*0.1
            count=0
            for i in range(9):
                count+=add
                per_5.append(da3[int(count-1)])
            return per_5
        def draw_boxplot(ax,mi,ma,p_25,p_50,p_75,multiplebox,da_ex,per_5,k,linecolor='black',pointcolor='black'):
            ax.vlines(k,mi,p_25,color=linecolor,linewidth=1)
            ax.vlines(k,p_75,ma,color=linecolor,linewidth=1)
            ax.hlines(mi,k-0.15,k+0.15,color=linecolor,linewidth=1)
            ax.hlines(ma,k-0.15,k+0.15,color=linecolor,linewidth=1)
            rect = plt.Rectangle((k-0.25,p_25),0.5,p_75-p_25,linewidth=1, edgecolor=linecolor, facecolor='none')
            ax.add_patch(rect)
            #异常点
            for i in da_ex.values:
                ax.text(k,i , "o",color=pointcolor, fontsize=5, verticalalignment="center",horizontalalignment='center')
                #ax.scatter(k,i,color='white', marker='o', edgecolors='black')
            ax.vlines(k,da_ex.min(),da_ex.max(),color='white',linewidth=1,zorder=0)
            if (not multiplebox):
                ax.hlines(p_50,k-0.25,k+0.25,color=linecolor,linewidth=1)
            else:
                #5%
                for i in per_5:
                    ax.hlines(i,k-0.25,k+0.25,color=linecolor,linewidth=1)
                ax.hlines(p_50,k-0.25,k+0.25,color=linecolor,linewidth=3)
        def main_box(ax,data,multiplebox,k,linecolor,pointcolor):
            da=pd.Series(data).astype(int)
            da=da.sort_values(ascending=False)
            da.reset_index(drop=True, inplace=True)
            p_25,p_50,p_75,da3=myplt.cal_Quantile(da)
            per_5=cal_per5(da3)
            per_5[4]=p_50
            ma,mi=myplt.cal_max_min(da,p_25,p_75)
            da_ex=da[(da<(p_25-(p_75-p_25)*1.5)) | (da>(p_75+(p_75-p_25)*1.5))]
            draw_boxplot(ax,mi,ma,p_25,p_50,p_75,multiplebox,da_ex,per_5,k,linecolor,pointcolor)
        for k in range(lenth):
            main_box(ax,data_l[k],multiplebox,k+1,linecolor,pointcolor)
    def histobox_plot(ax, data_l,linecolor='black',pointcolor='black',boxcolor='lavender'):
        ax.cla()
        lenth=len(data_l)
        ax.set_xlim((0,lenth+1))
        tick_x=range(1,lenth+1)
        ax.set_xticks(tick_x)
        ax.set_xticklabels([str(i) for i in tick_x])
        def normal_his(da,Rec_begin):
            his_l=[]
            for i in range(len(Rec_begin)-1):
                his_l.append(da[(da<Rec_begin[i+1]) & (da>=Rec_begin[i])].count())
            his_l.append(da[da>=Rec_begin[len(Rec_begin)-1]].count())
            ma_l=max(his_l)
            mi_l=min(his_l)
            his_nor=[((i-mi_l)/(ma_l-mi_l))*0.55 for i in his_l]
            #标准化 [0,1]*0.55
            return his_nor
        def draw_histobox(ax,mi,ma,p_25,p_50,p_75,da_ex,Rec_begin,his_nor,da_m,da_n,k,linecolor='black',pointcolor='black',boxcolor='lavender'):
            ax.vlines(k,mi,ma,color=linecolor,linewidth=1)
            ax.hlines(mi,k-0.15,k,color=linecolor,linewidth=1)
            ax.hlines(ma,k-0.15,k,color=linecolor,linewidth=1)
            ax.hlines(p_50,k-0.25,k,color=linecolor,linewidth=1)
            rect = plt.Rectangle((k-0.25,p_25),0.25,p_75-p_25,linewidth=1, edgecolor=linecolor, facecolor='none')
            ax.add_patch(rect)
            for i in da_ex.values:
                ax.text(k,i , "o", fontsize=5,color=pointcolor, verticalalignment="center",horizontalalignment='center')
                #ax.scatter(k,i,color='white', marker='o', edgecolors='black')
            ax.vlines(k,da_ex.min(),da_ex.max(),color='white',linewidth=1,zorder=0)
            for i in range(len(Rec_begin)):
                rect = plt.Rectangle((k,Rec_begin[i]),0.15+his_nor[i],(da_m-da_n)/10,linewidth=1,edgecolor=linecolor, facecolor=boxcolor)
                ax.add_patch(rect)
        def main_box(ax,data,k,linecolor,pointcolor,boxcolor):
            da=pd.Series(data).astype(int)
            da=da.sort_values(ascending=False)
            da.reset_index(drop=True, inplace=True)
            p_25,p_50,p_75=myplt.cal_Quantile(da)[:3]
            ma,mi=myplt.cal_max_min(da,p_25,p_75)
            da_ex=da[(da<(p_25-(p_75-p_25)*1.5)) | (da>(p_75+(p_75-p_25)*1.5))]
            #这里改
            Rec_begin=np.arange(da.min(),da.max(),(da.max()-da.min())/10)
            his_nor=normal_his(da,Rec_begin)
            draw_histobox(ax,mi,ma,p_25,p_50,p_75,da_ex,Rec_begin,his_nor,da.max(),da.min(),k,linecolor,pointcolor,boxcolor)
        for k in range(lenth):
            main_box(ax,data_l[k],k+1,linecolor,pointcolor,boxcolor)
    def creative_boxplot(ax, data_l,linecolor='black',pointcolor='black',boxcolor='lavender'):
        ax.cla()
        lenth=len(data_l)
        ax.set_xlim((0,lenth*3+1))#lenth+lenth*2+1
        tick_x=range(1,lenth*3+1)
        his_x=list(tick_x)[:lenth]
        sim_x=[j for j in list(tick_x)[lenth:] if j%2==0]
        ax.set_xticks(his_x+sim_x)
        ax.set_xticklabels([str(i) for i in his_x]+["zoom"+str(i) for i in his_x])
        da_ma,da_mi=myplt.cul_all_max_min(data_l)
        step=myplt.cul_step(da_ma,da_mi)
        tick_y=list(range(da_mi-(da_mi%step),da_ma+step*2,step))
        ax.set_ylim((tick_y[0]-step/6,tick_y[-1]+step/6))
        ax.set_yticks(tick_y)
        ax.set_yticklabels([str(i) for i in tick_y])
        def normal_his(da,Rec_begin):
            his_l=[]
            for i in range(len(Rec_begin)-1):
                his_l.append(da[(da<Rec_begin[i+1]) & (da>=Rec_begin[i])].count())
            his_l.append(da[da>=Rec_begin[len(Rec_begin)-1]].count())
            ma_l=max(his_l)
            mi_l=min(his_l)
            his_nor=[((i-mi_l)/(ma_l-mi_l))*0.55 for i in his_l]
            #标准化 [0,1]*0.55
            return his_nor
        def draw_histobox(ax,mi,ma,p_25,p_50,p_75,da_ex,Rec_begin,his_nor,da_m,da_n,k,linecolor='black',pointcolor='black',boxcolor='lavender'):
            ax.vlines(k,mi,ma,color=linecolor,linewidth=1)
            ax.hlines(mi,k-0.15,k,color=linecolor,linewidth=1)
            ax.hlines(ma,k-0.15,k,color=linecolor,linewidth=1)
            ax.hlines(p_50,k-0.25,k,color=linecolor,linewidth=1)
            rect = plt.Rectangle((k-0.25,p_25),0.25,p_75-p_25,linewidth=1, edgecolor=linecolor, facecolor='none')
            ax.add_patch(rect)
            for i in da_ex.values:
                ax.text(k,i , "o", fontsize=5,color=pointcolor, verticalalignment="center",horizontalalignment='center')
                #ax.scatter(k,i,color='white', marker='o', edgecolors='black')
            ax.vlines(k,da_ex.min(),da_ex.max(),color='white',linewidth=1,zorder=0)
            for i in range(len(Rec_begin)):
                rect = plt.Rectangle((k,Rec_begin[i]),0.15+his_nor[i],(da_m-da_n)/10,linewidth=1,edgecolor=linecolor, facecolor=boxcolor)
                ax.add_patch(rect)
        def draw_y_axis(mi,ma,step,step1,lenth,tick_y,ratio,k):
            tick_y1=list(range(mi-(mi%step1),ma+step1*2,step1))
            while len(tick_y1)!=len(tick_y):
                if (len(tick_y1)<len(tick_y)):
                    tick_y1.append(tick_y1[-1]+step1)
                else:
                    tick_y1.pop()
            ax.vlines(lenth+2*k-1,(tick_y1[0]-step/6)*ratio,(tick_y1[-1]+step/6)*ratio,color='black',linewidth=1)
            for i in tick_y1:
                ax.hlines(i*ratio,lenth+2*k-1-0.05,lenth+2*k-1,color='black',linewidth=1)
                ax.text(lenth+2*k-1-0.05, i*ratio , str(i), fontsize=10, verticalalignment="center",horizontalalignment='right')
        def draw_sim_box(ax,mi,ma,p_25,p_50,p_75,ratio,k,lenth,linecolor='black'):
            ax.vlines(lenth+2*k,mi*ratio,p_25*ratio,color=linecolor,linewidth=1)
            ax.vlines(lenth+2*k,p_75*ratio,ma*ratio,color=linecolor,linewidth=1)
            ax.hlines(mi*ratio,lenth+2*k-0.15,lenth+2*k+0.15,color=linecolor,linewidth=1)
            ax.hlines(ma*ratio,lenth+2*k-0.15,lenth+2*k+0.15,color=linecolor,linewidth=1)
            rect = plt.Rectangle((lenth+2*k-0.25,p_25*ratio),0.5,(p_75-p_25)*ratio,linewidth=1, edgecolor=linecolor, facecolor='none')
            ax.add_patch(rect)
            ax.hlines(p_50*ratio,lenth+2*k-0.25,lenth+2*k+0.25,color=linecolor,linewidth=3)
        def main_box(ax,data,k,linecolor,pointcolor,boxcolor):
            da=pd.Series(data).astype(int)
            da=da.sort_values(ascending=False)
            da.reset_index(drop=True, inplace=True)
            p_25,p_50,p_75=myplt.cal_Quantile(da)[:3]
            ma,mi=myplt.cal_max_min(da,p_25,p_75)
            step1=myplt.cul_step(ma,mi)
            ratio=step/step1
            da_ex=da[(da<(p_25-(p_75-p_25)*1.5)) | (da>(p_75+(p_75-p_25)*1.5))]
            Rec_begin=np.arange(da.min(),da.max(),(da.max()-da.min())/10)
            his_nor=normal_his(da,Rec_begin)
            draw_histobox(ax,mi,ma,p_25,p_50,p_75,da_ex,Rec_begin,his_nor,da.max(),da.min(),k,linecolor,pointcolor,boxcolor)
            draw_y_axis(mi,ma,step,step1,lenth,tick_y,ratio,k)
            draw_sim_box(ax,mi,ma,p_25,p_50,p_75,ratio,k,lenth,linecolor)
        for k in range(lenth):
            main_box(ax,data_l[k],k+1,linecolor,pointcolor,boxcolor)
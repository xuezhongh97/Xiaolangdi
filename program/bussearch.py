# -*- coding: utf-8 -*-
"""
小浪底大区公共交通查询系统源码 
版权所有：薛中涵
邮箱：zhonghan.xue@foxmail.com
"""
import os
import datetime
import calendar
import time
import math
import cv2 as cv
import matplotlib.pyplot as plt # plt 用于显示图片
import matplotlib.image as mpimg # mpimg 用于读取图片
import numpy as np
import random as rd
from PIL import Image, ImageDraw, ImageFont

fast_normal_timetable=[]
for i in range(5*60,22*60,6):
    fast_normal_timetable.append(i)
for i in range(22*60,24*60,12):
    fast_normal_timetable.append(i)    
for i in range(7*60+3,9*60,6):
    fast_normal_timetable.append(i)
for i in range(17*60+3,19*60,6):
    fast_normal_timetable.append(i)
for i in range(0*60,5*60,30):
    fast_normal_timetable.append(i)
fast_normal_timetable.sort()

main_normal_timetable=[]
for i in range(5*60,22*60,10):
    main_normal_timetable.append(i)
for i in range(22*60,24*60,20):
    main_normal_timetable.append(i)
for i in range(7*60+5,9*60,10):
    main_normal_timetable.append(i)
for i in range(17*60+5,19*60,10):
    main_normal_timetable.append(i)
for i in range(0*60,5*60,30):
    main_normal_timetable.append(i)
main_normal_timetable.sort()

slow_normal_timetable=[]
for i in range(5*60,23*60+1,20):
    slow_normal_timetable.append(i)
for i in range(7*60+10,9*60,20):
    slow_normal_timetable.append(i)
for i in range(17*60+10,19*60,20):
    slow_normal_timetable.append(i)
slow_normal_timetable.sort()

long_normal_timetable=[]
for i in range(5*60,22*60+1,40):
    long_normal_timetable.append(i)
for i in range(7*60+20,9*60,40):
    long_normal_timetable.append(i)
for i in range(17*60+20,19*60,40):
    long_normal_timetable.append(i)
long_normal_timetable.sort()

fast_sunday_timetable=[]
for i in range(7*60,23*60+1,9):
    fast_sunday_timetable.append(i)

middle_sunday_timetable=[]
for i in range(7*60,22*60+1,15):
    middle_sunday_timetable.append(i)

slow_sunday_timetable=[]
for i in range(7*60,21*60+1,30):
    slow_sunday_timetable.append(i)

long_sunday_timetable=[]
for i in range(7*60,20*60+1,60):
    long_sunday_timetable.append(i)

list_station=[]
list_line=[]

class busline:
    def __init__(self,numero,starttime=5,endtime=22,proprity=1,time=1,price=1,timetable1=slow_normal_timetable,timetable2=slow_sunday_timetable):
        self.__numero=numero
        self.__starttime=starttime
        self.__endtime=endtime
        self.__proprity=proprity
        self.__station=[]
        self.__price=price
        self.__time=time
        self.__timetable1=timetable1
        self.__timetable2=timetable2
        self.__linecolor=(np.random.randint(0,255), np.random.randint(0,255), np.random.randint(0,255))
        self.__stationcolor=(np.random.randint(0,255), np.random.randint(0,255), np.random.randint(0,255))
        
        
    def get_numero(self):
        return self.__numero
    
    def get_station(self):
        return self.__station
    
    def get_proprity(self):
        return self.__proprity
    
    def get_price(self):
        return self.__price
    
    def get_linecolor(self):
        return self.__linecolor

    def get_stationcolor(self):
        return self.__stationcolor

    def get_time(self):
        return self.__time
    
    def add_station(self,station):
        self.__station=station
        for i in station:
            flag=0
            for j in list_station:
                if j.get_name()==i:
                    j.add_line(self.get_numero())
                    flag=1
            if flag==0: list_station.append(Station(i,self.get_numero()))
            
        
    def get_info(self):
        if self.__station[0]=="外环" or self.__station[0]=="内环":
            print(self.get_numero(),"\n",self.__station[1]," 环线")
        else:
            print(self.get_numero(),"\n",self.__station[0],"<--->",self.__station[-1])
        if self.__proprity==1:
            print("电车公司运营")
            print("监督电话030-41224100")
        elif self.__proprity==2:
            print("巴士股份公司运营") 
            print("监督电话030-41224200")
           
        elif self.__proprity==3:
            print("公交三公司运营")
            print("监督电话030-41224105")
        else:
            print("郊区公交公司运营")
            print("监督电话030-45882155")           
        print("首班车",self.__starttime,"点")
        print("末班车",self.__endtime,"点")
        print("站点")
        connectiontemp2=0
        for m in self.__station:
            for n in list_station:
                if m==n.get_name():
                    if connectiontemp2==1:
                        pass#print("|")                        
                    print("*",n.get_zone()," ",m)
                    connectiontemp2=1
        print("平均每站",self.__time,"分钟")
        self.affichage_timetable()
    
    def get_starttime(self):
        return self.__starttime
    
    def get_endtime(self):
        return self.__endtime
    
    def affichage_timetable(self):
        print("\n发车时刻表")
        hourtemp=-1
        if issunday==1:
            for i in self.__timetable2:
                if i//60!=hourtemp:
                    print("\n",i//60,"\t",end="")
                print(i%60,end=" ")
                hourtemp=i//60
        else:
            for i in self.__timetable1:
                if i//60!=hourtemp:
                    print("\n",i//60,"\t",end="")
                print(i%60,end=" ")
                hourtemp=i//60
    
    def get_timetable(self):
        if issunday==1:
            return self.__timetable2
        else:
            return self.__timetable1

class Station:
    def __init__(self,name,line,zone=1):
        self.__name=name
        self.__line=[]
        self.__line.append(line)
        self.__neighborhood=[]
        self.__timetable=[]
        self.__position=[1,1,1,1]
        self.__zone=zone
        self.__shortname=[]
    def get_name(self):
        return self.__name
        
    def add_line(self,line):
        self.__line.append(line)
    
    def get_line(self):
        return self.__line

    def get_zone(self):
        return self.__zone


    def get_position(self):
        return self.__position

    def add_position(self,position,zone):
        self.__position=position
        self.__zone=zone
        
    def get_shortname(self):
        return self.__shortname
    
    def add_shortname(self,shortname):
        self.__shortname=shortname
    
    def get_info(self):
        print(self.get_name())
        print(self.get_zone(),"区车站")
        print("停靠巴士")
        print(self.get_line())
        self.get_timetable()
        
    def initialiser(self):
        for i in self.__line:
            for j in list_line:
                if i==j.get_numero():
                    liste_de_line=j.get_station()
                    for k in liste_de_line:
                        if k!=self.get_name():
                            self.__neighborhood.append((k,j.get_time()*abs(liste_de_line.index(k)-liste_de_line.index(self.get_name())),j.get_numero()))
        self.__neighborhoodsorted=sorted(self.__neighborhood, key=lambda s: s[-1])
        for i in self.__line:
            for j in list_line:
                if i==j.get_numero():
                    direction=j.get_station()[0]
                    delay=j.get_time()*abs(len(j.get_station())-j.get_station().index(self.get_name()))
                    timetableexact=[]
                    for i in j.get_timetable():
                        timetableexact.append(i+delay)
                    self.__timetable.append((j.get_numero(),direction,timetableexact))
                    direction=j.get_station()[-1]
                    delay=j.get_time()*abs(0-j.get_station().index(self.get_name()))
                    timetableexact=[]
                    for i in j.get_timetable():
                        timetableexact.append(i+delay)
                    self.__timetable.append((j.get_numero(),direction,timetableexact))
  
    def get_neighbor(self):
        return self.__neighborhoodsorted
    
    def get_timetable(self):
        for i in self.__timetable:
            for j in i[2]:
                time_rest=j-timenow
                if j>timenow:
                    break
            if time_rest<0:
                print(i[0],"(",i[1],")","停止运营")
            else:
                print(i[0],"(",i[1],")\t -",int(time_rest))
    def give_timetable(self):
        return self.__timetable



now = (datetime.datetime.utcnow() + datetime.timedelta(hours=8))

# 判断今天是否为周末
def is_week_lastday():
    # 假如今天是周日
    sunday = now.weekday()
    # 如果今天是周日，则返回True
    if sunday == 6:
        return True
    else:
        pass


    
def searchline():
    try:
        line=int(input("线路号\n"))
    except ValueError:
        print("")
    os.system("clear")    
    for i in list_line:
        if line==i.get_numero():
            i.get_info()
                
        
def searchstation():
    station=input("站点名\n输入汉语全称或者拼音首字母\n")
    os.system("clear")
    for i in list_station:
        if station==i.get_name() or station==i.get_shortname():
            i.get_info()

def drawline(station1,station2,line):
    global linemap
    for i in list_station:
        if station1==i.get_name() or station1==i.get_shortname():
            Station1=i
    for i in list_station:
        if station2==i.get_name() or station1==i.get_shortname():
            Station2=i
    n1,y1,x1,z1=Station1.get_position()
    n2,y2,x2,z1=Station2.get_position()
    cv.line(linemap, (y1, x1), (y2, x2), line.get_linecolor(), 5) #9

def drawpoint(station,line,isblackened):
    global linemap
    for i in list_station:
        if station==i.get_name():
            Station=i
    n1,y1,x1,z1=Station.get_position()
    cv.circle(linemap, (y1,x1), 5, colorbar[Station.get_zone()-1], 5) #33
    img_PIL = Image.fromarray(cv.cvtColor(linemap, cv.COLOR_BGR2RGB))
    if isblackened==1:
        sizefont=25
    else:
        sizefont=15
    font = ImageFont.truetype('wqy-microhei.ttc', sizefont)
    fillColor = line.get_stationcolor()
    position = (y1+10,x1-5)
    str = station
    draw = ImageDraw.Draw(img_PIL)
    draw.text(position, str, font=font, fill=fillColor)
    linemap = cv.cvtColor(np.asarray(img_PIL),cv.COLOR_RGB2BGR)
    
def searchroute(startstation,endstation,line,timenow1,ticketflag):
    stations=[]
    for i in list_station:
        if startstation==i.get_name() or startstation==i.get_shortname():
            stationstarted=i
        if endstation==i.get_name() or endstation==i.get_shortname():
            stationended=i
    mintime=3000
    for j in list_line:
        if line==j.get_numero():
            linetemp=j
            found=0
            circle=0
            if linetemp.get_station()[1]==linetemp.get_station()[-1]:
                circle=1
            for k in linetemp.get_station():
                if k==stationstarted.get_name():
                    stationnum1=linetemp.get_station().index(k)
                if k==stationended.get_name():
                    stationnum2=linetemp.get_station().index(k)
                    found=1                
            if found==1:
                if stationnum1<=stationnum2:
                    direction=linetemp.get_station()[-1]
                else:
                    direction=linetemp.get_station()[0]
                if circle:
                    if stationnum1==1:
                        if abs(stationnum2-1)>abs(len(linetemp.get_station())-stationnum2):
                            direction=linetemp.get_station()[-1]
                            stationnum1=len(linetemp.get_station())-1
                        else:
                            direction=linetemp.get_station()[0]
                    if stationnum2==1:
                        if abs(stationnum1-1)>abs(len(linetemp.get_station())-stationnum1):
                            print("debug")                        
                            direction=linetemp.get_station()[-1]
                            stationnum2=len(linetemp.get_station())-1
                        else:
                            direction=linetemp.get_station()[0]

                timetable=stationstarted.give_timetable() 
                for i in timetable:
                    if i[0]==linetemp.get_numero() and i[1]==direction:
                        for m in i[-1]:
                            time_rest=m-timenow1
                            if time_rest>=0:
                                break
                if time_rest>=0 and time_rest<=120:
                    if stationnum1<=stationnum2:
                        for j in range(stationnum1,stationnum2+1):
                            for l in list_station:
                                if linetemp.get_station()[j]==l.get_name():
                                    stations.append(l.get_name())
                                    ticketflag.append(l.get_zone())
                    else:
                        for j in range(stationnum1,stationnum2-1,-1):
                            for l in list_station:
                                if linetemp.get_station()[j]==l.get_name():
                                    stations.append(l.get_name())                                   
                                    ticketflag.append(l.get_zone())
                    mintime=min(mintime,abs(stationnum1-stationnum2)*linetemp.get_time()+time_rest+timenow1)
                else:
                    print("车辆停止运营")
                    return 0
                return (startstation,endstation,timenow1,time_rest,timenow1+time_rest,stations,abs(stationnum1-stationnum2)*linetemp.get_time()+time_rest+timenow1,line,direction,ticketflag)
    return 0
            
def search1(stationstarted,stationended,route):
    goal=stationended.get_name()
    for i in stationstarted.get_neighbor():
        if i[0]==goal:
            poids=i[1]
            route.append((1,i[2],poids))
    return route
                

def search2(stationstarted,stationended,route):
    goal=stationended.get_name()
    for i in stationstarted.get_neighbor():
        for j in list_station:
            if i[0]==j.get_name():
                for k in j.get_neighbor():
                    if k[0]==goal:
                        poids=i[1]+k[1]+15
                        route.append((2,i[2],i[0],k[2],poids))
                        
    return route

def search3(stationstarted,stationended,route):
    goal=stationended.get_name()
    for i in stationstarted.get_neighbor():
        for j in list_station:
            if i[0]==j.get_name():
                for k in j.get_neighbor():
                    for l in list_station:
                        if k[0]==l.get_name():
                            for m in l.get_neighbor():
                                if m[0]==goal:
                                    poids=i[1]+k[1]+m[1]+30
                                    route.append((3,i[2],i[0],k[2],k[0],m[2],poids))
                        
    return route

def search4(stationstarted,stationended,route):
    goal=stationended.get_name()
    for i in stationstarted.get_neighbor():
        for j in list_station:
            if i[0]==j.get_name():
                for k in j.get_neighbor():
                    for l in list_station:
                        if k[0]==l.get_name():
                            for m in l.get_neighbor():
                                for n in list_station:
                                    if m[0]==n.get_name():
                                        for p in n.get_neighbor():
                                            if p[0]==goal:
                                                poids=i[1]+k[1]+m[1]+p[1]+45
                                                route.append((4,i[2],i[0],k[2],k[0],m[2],m[0],p[2],poids))
                                        
    return route
  

def achat():
    global charge
    try:
        zonenumber=int(input("请输入乘坐区号\n"))
    except ValueError:
        print("")    
    os.system("clear")    
    for i in prince_list:
        if i[0]==zonenumber:
            try:
                reducedtype=int(input("优惠类型？\n 1 市民\t 2 学生\t 3 老人\t 4 游客 5 无优惠\n"))
            except ValueError:
                print("")                
            reduced=1
            if reducedtype==1:
                reduced=0.8
            if reducedtype==2:
                reduced=0.3
            if reducedtype==3:
                reduced=0.5
            if reducedtype==4:
                reduced=0.9
            newprice=i[1]*reduced
            print("票价为",round(newprice,1),"元")
            try:
                ispayed=int(input("是否支付\n 1 确认\t 0 取消\n"))
            except ValueError:
                print("")
            os.system("clear")
            if ispayed and charge>=round(newprice,1):
                charge-=round(newprice,1)
                print("支付成功，以下为确认码")
                identi=rd.randint(1000000000000,10000000000000)                
                print(identi)
                identity.append(identi)
                return
            else:
                print("支付失败")
                return
    print("信息输入错误")
    return

def acount():
    global charge
    os.system("clear")
    print("账户信息")
    print("余额:",round(charge,1),"元")
    if len(identity)>0:
        print("已购买车票验证码")
        for i in identity:
            print(i)
    else:
        print("无车票验证码")
    return


def UIdisplay(results):
    for i in list_station:
        if results[0]==i.get_name() or results[0]==i.get_shortname():
            stationstarted=i
        if results[1]==i.get_name() or results[1]==i.get_shortname():
            stationended=i
    for k in list_line:
        if k.get_numero()==results[7]:
            linetemp=k
    print(stationstarted.get_name(),"---->",stationended.get_name())
    print(int(results[2]//60),":",int(results[2]%60),"+",int(results[3]//60),":",int(results[3]%60))
    print(int(results[4]//60),":",int(results[4]%60),"---->",int(results[6]//60),":",int(results[6]%60))
    print("")
    print(results[7],"\t",results[-2])
    print("")
    isconnected=0
    for j in results[5]:
        for m in list_station:
            if j==m.get_name():
                if isconnected==1:
                    #print("|")
                    #drawline(results[5][results[5].index(j)-1],j,k)
                    pass
                print("*",m.get_zone(),"",j)
                isconnected=1
            #drawpoint(j,k,0)
    print("")
    
def displayresults(route,startstation,endstation,ticketflag):
    if route[0]==1:
        results=searchroute(startstation,endstation,route[1],timenow,ticketflag)
        if results:
            UIdisplay(results)
        else:
            return 0
    if route[0]==2:
        results=searchroute(startstation,route[2],route[1],timenow,ticketflag)
        if results: UIdisplay(results)
        else:
            return 0
        results=searchroute(route[2],endstation,route[3],results[-4],results[-1])
        if results: UIdisplay(results)
        else:
            return 0        
    if route[0]==3:
        results=searchroute(startstation,route[2],route[1],timenow,ticketflag)
        if results: UIdisplay(results)
        else:
            return 0
        results=searchroute(route[2],route[4],route[3],results[-4],results[-1])
        if results: UIdisplay(results)
        else:
            return 0
        results=searchroute(route[4],endstation,route[5],results[-4],results[-1])
        if results:
            UIdisplay(results)
        else:
            return 0
    if route[0]==4:
        results=searchroute(startstation,route[2],route[1],timenow,ticketflag)
        if results: UIdisplay(results)
        else: return 0
        results=searchroute(route[2],route[4],route[3],results[-4],results[-1])
        if results: UIdisplay(results)
        else: return 0
        results=searchroute(route[4],route[6],route[5],results[-4],results[-1])
        if results: UIdisplay(results)
        else: return 0                      
        results=searchroute(route[6],endstation,route[7],results[-4],results[-1])
        if results: UIdisplay(results)
        else: return 0
    print("")
    ticketflag2 = list(set(results[-1]))
    print("经过区间")
    for i in ticketflag2:
        print(i,end="")
    print("\n")
    print("到达时间"," ",int(results[6]//60),":",int(results[6]%60))
    print("")    

        
def main():
    os.system("clear")
    print("小浪底公交服务系统v1.3")  
    global linemap
    isended=0
    global timenow
    global issunday
    global charge
    try: systemtime=int(input("系统时间？\n 1 是\t 0 否\n"))
    except ValueError:
        print("")
    if systemtime:
        hour=time.localtime().tm_hour
        minute=time.localtime().tm_min
        issunday=is_week_lastday()
    else:
        os.system("clear")
        try: hour=int(input("小时\n"))
        except ValueError:
            print("")
        os.system("clear")
        try: minute=int(input("分钟\n"))
        except ValueError:
            print("")
        os.system("clear")
        try: issunday=int(input("是星期天吗?\n 1 是\t 0 否\n"))
        except ValueError:
            print("")
    timenow=60*hour+minute
    for i in list_station:
        i.initialiser()
    charge=round(rd.randint(5,2000)/10,1)
    while(isended==0):
        os.system("clear")
        if systemtime:
            hour=time.localtime().tm_hour
            minute=time.localtime().tm_min
            issunday=is_week_lastday()
            timenow=60*hour+minute
        print(int(hour),":",int(minute),end=" ")
        if issunday:
            print("星期天",end=" ")
        else:
            print("工作日",end=" ")
        print("余额 ",round(charge,1),"元")
        print("0 退出系统",end="\n")
        print("1 路线查询",end="\t")
        print("2 购票系统",end="\t")        
        print("3 路号查询",end="\t")
        print("4 候车查询",end="\t")
        print("5 账户查询")
        option=-1
        while(option>10 or option<0):
            try:
                option=int(input(""))
            except ValueError:
                print("")
            os.system("clear")
        if option==3:
            searchline()
        if option==4:
            searchstation()
        if option==5:
            acount()
        if option==2:
            achat()
        if option==1:
            get_station=0
            while(get_station==0):
                startstation=input("出发地\n输入汉语全称或者拼音首字母\n")
                os.system("clear")                
                endstation=input("目的地\n输入汉语全称或者拼音首字母\n")
                os.system("clear")
                for i in list_station:
                    if startstation==i.get_name() or startstation==i.get_shortname():
                        stationstarted=i
                        get_station=1
                    if endstation==i.get_name() or endstation==i.get_shortname():
                        stationended=i
                        get_station=1
            route=[]
            route=search1(stationstarted,stationended,route)
            route=search2(stationstarted,stationended,route)
            if len(route)<1:
                route=search3(stationstarted,stationended,route)
                if len(route)<1:
                    route=search4(stationstarted,stationended,route)
            route_sorted=sorted(route, key=lambda s: s[-1])
            isendeded=0
            if len(route_sorted)<1:
                isendeded=1
            order=0
            while isendeded==0:
                ticketflag=[]
                displayresults(route_sorted[order],startstation,endstation,ticketflag)
                print(order+1,"/",len(route_sorted))
                try:
                    signal=int(input("\n 0 退出\t 1 下一结果\t 2 上一结果\n"))
                except ValueError:
                    print("")
                os.system("clear")                
                if signal==0:
                    isendeded=1
                else:
                    linemap=cv.imread("real.png")
                if signal==1:
                    order+=1
                if signal==2:
                    order-=1
                if order>=len(route_sorted):
                    order=len(route_sorted)-1
                if order<0:
                    order=0

                
                    
        if option==0:
            isended=1
        if isended==0:
            try:
                isended=int(input("\n\n 0 返回\n"))
            except ValueError:
                print("")


line6=busline(6,0,24,1,1.7,1,fast_normal_timetable,fast_sunday_timetable)
line6.add_station(["聚龙里（外环）","聚龙","西门口","三标东","大桥西","大桥东"
                   ,"食堂","三号楼东","一号楼东","一号楼","一号楼东","招待所","办公楼","红旗广场","小桥东"
                   ,"小桥西","聚龙"])
list_line.append(line6)

line8=busline(8,0,24,1,1.6,1,fast_normal_timetable,fast_sunday_timetable)
line8.add_station(["火车站里（外环）","火车站","食堂","大桥东","徐家汇","宾馆东","运动场东","办公楼"
                   ,"红旗广场","小桥东","小桥西","聚龙","三标东","大桥西","火车站"
                   ])
list_line.append(line8)

line11=busline(11,0,24,2,1.9,2,main_normal_timetable,middle_sunday_timetable)
line11.add_station(["火车站","食堂","大桥东","徐家汇","宾馆东","运动场东","办公楼"
                   "停车场东","小浪底大学","好又来","车队","车队桥西","加油站","景区北门","鑫苑名家"
                   ])
list_line.append(line11)

line12=busline(12,0,24,1,1.4,1,fast_normal_timetable,fast_sunday_timetable)
line12.add_station(["一号楼里（外环）","一号楼东","森林公园","办公楼","运动场东","宾馆东","徐家汇","大桥东","食堂","三号楼东","一号楼东"
                   ])
list_line.append(line12)


line4=busline(4,0,24,2,2.4,2,main_normal_timetable,middle_sunday_timetable)
line4.add_station(["桥沟","二标桥南","二标桥南","二标北门","二标宿舍","二标食堂","二标游泳池"
                   ,"一标河西","一标东","大桥西","三标东","西门口","聚龙"
                   ,"小桥西","建设银行","建设桥北","小浪底大学","好又来","车队"])
list_line.append(line4)

line1=busline(1,0,24,2,2.4,3,main_normal_timetable,middle_sunday_timetable)
line1.add_station(["火车站","大桥东","食堂","三号楼东","一号楼东","招待所"
                   ,"办公楼","红旗广场","小桥东","停车场西","小浪底大学"
                   ,"好又来","车队","坝后公园","富士康南","海洋馆","东门","松山村"
                   ,"国道口","电厂","高铁站"])
list_line.append(line1)

line16=busline(16,5,23,2,2.4,2)
line16.add_station(["车队","好又来","小浪底大学","停车场西","运动场西","宾馆大门","陈寨南","庙李南","老鸦陈南","大峪镇口","大峪镇经开中心","大峪镇十字街口","大峪镇人民路","大峪镇医院"])
list_line.append(line16)



line85=busline(85,5,23,2,2.4,3)
line85.add_station(["锅炉房","四标","森林公园","办公楼","停车场东","小浪底大学"
                   ,"好又来","车队","坝后公园","富士康北","驾校","东门","松山村","国道口","电厂","高铁站"])
list_line.append(line85)

line20=busline(20,5,23,3,2.7,2)
line20.add_station(["三角楼","桥沟中学","桥沟","一标游泳池","一标国际处","一标运动场","一标食堂","一标东","大桥西","大桥东","徐家汇","领导楼","洗衣房","宾馆西","宾馆"
                   ])
list_line.append(line20)

line30=busline(30,5,23,3,2.2,2)
line30.add_station(["桥沟","二标桥南","二标北门","二标宿舍","二标食堂","二标游泳池","一标河西","一标东","大桥西","大桥东","徐家汇","领导楼","运动场东","办公楼","一号楼西","三号楼西","三号楼"
                   ])
list_line.append(line30)

line54=busline(54,5,23,1,1.9)
line54.add_station(["一号楼","一号楼东","三号楼东","四号楼"               ,"食堂","大桥东","大桥西","一标东","一标食堂","一标运动场","一标国际处","一标游泳池","图书馆"])
list_line.append(line54)

line21=busline(21,5,23,3,2.2,2)
line21.add_station(["桥沟","二标桥南","二标北门","二标宿舍","二标食堂","二标游泳池","一标游泳池","一标国际处","一标运动场","一标食堂","一标东","大桥西","大桥东","火车站"
                   ])
list_line.append(line21)

line3=busline(3,0,24,3,2.1,2,main_normal_timetable,middle_sunday_timetable)
line3.add_station(["桥沟","桥沟中学","三角楼","石家街","辛家庙","大峪镇口","老鸦陈"
                   ,"庙李","陈寨","宾馆大门","运动场西","小桥东","红旗广场","办公楼",
                   "停车场东","小浪底大学","好又来","车队"
                   ])
list_line.append(line3)


line42=busline(42,5,23,3,2.6,2)
line42.add_station(["火车站","大桥东","徐家汇","宾馆东","宾馆","宾馆大门","陈寨南"
                   ,"庙李南","老鸦陈南","大峪镇口","辛家庙南","石家街南","三角楼","桥沟中学","桥沟"])
list_line.append(line42)




line95=busline(95,5,23,4,4.6,4)
line95.add_station(["九曲桥","新桥西","新桥东","保税区","高铁站","旅游局","北岸小学"
                   ,"景区停车场西","景区停车场东","黄河大桥北","黄河大桥南","东和清口","东和清","机场东","机场"])
list_line.append(line95)

line7=busline(7,5,23,1,1.4)
line7.add_station(["集装箱北","集装箱","集装箱南""三标东","菜市场","西门口","大桥西","大桥东","食堂","三号楼东","一号楼东","四标","锅炉房"
                   ])
list_line.append(line7)

line2=busline(2,5,23,1,1.9,1)
line2.add_station(["火车站","大桥东","食堂","徐家汇","领导楼","洗衣房","宾馆西"
                   ,"宾馆大门","运动场西","小桥东","小桥西","聚龙","菜市场"
                   ,"集装箱南","集装箱","集装箱西"])
list_line.append(line2)



line17=busline(17,5,23,1,1.7,1)
line17.add_station(["宾馆西","洗衣房","领导楼","徐家汇","大桥东","食堂","三号楼西","三号楼","三号楼东","一号楼东","招待所","办公楼","运动场东","宾馆东","宾馆","宾馆大门","宾馆西"])
list_line.append(line17)


line26=busline(26,5,23,1,1.7,1)
line26.add_station(["火车站里（外环）","火车站","食堂","三号楼西","一号楼西","一号楼","一号楼内""一号楼西","办公楼","红旗广场","东建材","运动场南","办公楼北","宾馆东","徐家汇","大桥东","火车站"
                   ])
list_line.append(line26)

line27=busline(27,5,23,1,1.5)
line27.add_station(["锅炉房","四标","一号楼东","森林公园","办公楼","红旗广场","小桥东"
                   ,"小桥西","聚龙","西门口","三标东","三标游泳池","三标内"])
list_line.append(line27)


line50=busline(50,5,23,4,2.4)
line50.add_station(["车队","思源学院","半坡","小浪底大学新区","东山宿舍楼","东山商城","白鹿原"
                   ])
list_line.append(line50)



line56=busline(56,5,23,1.6,1.3)
line56.add_station(["图书馆","一标游泳池","一标国际处","一标运动场","一标食堂","一标东","大桥西","三标东","西门口","聚龙"
                   ,"小桥西","小桥东","停车场西","小浪底大学","小浪底大学老区"])
list_line.append(line56)

line62=busline(62,5,23,3,2.3,2)
line62.add_station(["大峪镇中学","大峪镇体育场","大峪镇邮局","大峪镇十字街口","大峪镇北客站","大峪镇大排档","大峪镇口"
                   ,"老鸦陈","老鸦陈三街","庙李三街","庙李一街","陈寨一街","陈寨","陈寨南","宾馆大门","运动场西","小桥东","小桥西","建设银行","建设桥北","小浪底大学","小浪底大学老区"])
list_line.append(line62)

line63=busline(63,5,23,3,2.1,3)
line63.add_station(["大峪镇医院","大峪镇体育场","大峪镇邮局","大峪镇十字街口","大峪镇北客站","大峪镇大排档","大峪镇口"
        ,"辛家庙南","石家街南","三角楼","三角楼基地","桥沟北","桥沟新区中学","桥沟新区","二标桥南","二标北门","二标宿舍","二标食堂","二标游泳池","一标游泳池","图书馆"])
list_line.append(line63)

line64=busline(64,5,23,3,5.4,2)
line64.add_station(["桐树岭","桐树岭东","柳林西","柳林","柳林东","桑园西","桑园东"
                   ,"二标北门","二标桥南","桥沟"])
list_line.append(line64)

line77=busline(77,5,23,2,3.3,3)
line77.add_station(["加油站职工三区","加油站职工一区","加油站","车队桥西","车队","坝后公园","富士康北街"
                   ,"富士康中街","富士康南街","坝后公园南门","东岸观景台","转盘","东门","松山村","国道口","电厂","高铁站"])
list_line.append(line77)

line83=busline(83,5,23,2,1.6,1)
line83.add_station(["一号楼里（外环）","一号楼","一号楼西","办公楼","红旗广场","小桥东","运动场西"
                   ,"宾馆大门","宾馆","宾馆职工楼","徐家汇","大桥东","食堂","四号楼西","三号楼西","二号楼西","二号楼","一号楼东","一号楼"])
list_line.append(line83)



line91=busline(91,5,22,4,4.3,3,long_normal_timetable,long_sunday_timetable)
line91.add_station(["高铁站","电厂","国道口","西二旗","菜市口","一〇七基地","景区停车场东"
                   ,"黄河大桥北","黄河人家","河清口","泰山村西","泰山村"])
list_line.append(line91)

line18=busline(18,5,22,4,4.5,4,long_normal_timetable,long_sunday_timetable)
line18.add_station(["车队","车队桥西","加油站","景区北门","七号交通洞北","八号交通洞","七号交通洞南","微缩模型","西岸观景台","索桥西","索桥东","转盘","东门","松山村","国道口","电厂","高铁站"
                   ])
list_line.append(line18)

line19=busline(19,5,22,4,12.4,8,long_normal_timetable,long_sunday_timetable)
line19.add_station(["车队","车队桥西","加油站","景区北门","鑫苑名家","小坝","九号交通洞南","九号交通洞北","桐树岭","牛马潭","交叉口","小桥沟","桥沟新区","桥沟"
                   ])
list_line.append(line19)


###站点位置信息输入
Station_info=[["火车站",594,492,1],
["大桥东",580,505,1],
["食堂",597,519,1],
["三号楼东",605,567,1],
["一号楼东",588,607,1],
["招待所",561,627,1],
["办公楼",515,661,1],
["红旗广场",465,658,1],
["小桥东",441,654,1],
["停车场西",432,697,1],
["小浪底大学",406,751,2],
["好又来",382,822,2],
["车队",376,897,2],
["坝后公园",388,949,2],
["富士康南",404,1035,2],
["海洋馆",510,1167,3],
["东门",568,1219,3],
["松山村",604,1218,3],
["国道口",640,1216,3],
["电厂",636,1310,3],
["高铁站",634,1402,3],
["徐家汇",561,551,1],
["领导楼",533,551,1],
["洗衣房",502,547,1],
["宾馆西",491,563,1],
["宾馆大门",476,582,1],
["运动场西",466,608,1],
["小桥西",420,638,1],
["聚龙",429,619,1],
["菜市场",410,563,1],
["集装箱南",438,530,1],
["集装箱",406,468,1],
["集装箱西",318,434,1],
["桥沟",518,125,2],
["二标桥南",497,178,2],
["二标北门",439,172,2],
["二标宿舍",507,214,2],
["二标食堂",530,236,2],
["二标游泳池",558,270,2],
["一标河西",587,357,1],
["一标东",568,437,1],
["大桥西",553,474,1],
["三标东",495,514,1],
["西门口",449,578,1],
["建设银行",406,677,1],
["建设桥北",394,704,1],
["一号楼",572,607,1],
["内环",1,1,1],
["集装箱北",417,376,1],
["四标",608,592,1],
["锅炉房",623,544,1],
["宾馆东",535,610,1],
["运动场东",526,628,1],
["后勤部",596,504,1],
["桥沟中学",555,129,2],
["三角楼",604,142,2],
["石家街",609,210,2],
["辛家庙",618,279,2],
["大峪镇口",627,380,2],
["老鸦陈",616,447,1],
["庙李",588,465,1],
["陈寨",551,501,1],
["停车场东",454,695,1],
["车队桥西",338,899,2],
["加油站",269,900,2],
["景区北门",200,896,2],
["鑫苑名家",88,851,2],
["森林公园",563,633,1],
["陈寨南",499,538,1],
["庙李南",568,486,1],
["老鸦陈南",602,455,1],
["大峪镇经开中心",685,427,2],
["大峪镇十字街口",714,418,2],
["大峪镇人民路",713,456,2],
["大峪镇医院",712,503,2],
["三号楼西",564,541,1],
["三号楼",585,562,1],
["领导楼内",546,533,1],
["七号交通洞北",68,888,3],
["八号交通洞",22,748,3],
["七号交通洞南",10,1164,3],
["微缩模型",36,1268,4],
["西岸观景台",166,1272,4],
["索桥西",238,1328,4],
["索桥东",410,1286,4],
["转盘",436,1212,3],
["小坝",10,600,3],
["九号交通洞南",10,560,4],
["九号交通洞北",10,520,4],
["桐树岭",10,480,4],
["牛马潭",10,440,5],
["交叉口",10,400,5],
["小桥沟",262,26,3],
["桥沟新区",476,114,2],
["一标游泳池",556,288,1],
["一标国际处",556,317,1],
["一标运动场",548,368,1],
["一标食堂",542,402,1],
["宾馆",509,596,1],
["四号楼",590,542,1],
["一号楼西",552,602,1],
["东建材",472,625,1],
["办公楼北",496,628,1],
["三标游泳池",478,486],
["三标内",523,464,1],
["辛家庙南",620,323,2],
["石家街南",606,203,2],
["思源学院",426,784,2],
["半坡",408,887,2],
["小浪底大学新区",498,890,2],
["东山宿舍楼",527,852,2],
["东山商城",570,844,2],
["白鹿原",616,794,2],
["图书馆",513,291,1],
["小浪底大学老区",383,745,2],
["大峪镇中学",830,445,2],
["大峪镇体育场",780,440,2],
["大峪镇邮局",778,408,2],
["大峪镇北客站",712,345,2],
["大峪镇大排档",653,368,2],
["老鸦陈三街",637,448,1],
["庙李三街",618,458,1],
["庙李一街",581,492,1],
["陈寨一街",558,504,1],
["三角楼基地",566,69,2],
["桥沟北",505,33,2],
["桥沟新区中学",482,70,2],
["桐树岭东",20,270,4],
["柳林西",20,230,4],
["柳林",20,190,4],
["柳林东",20,150,4],
["桑园西",20,110,4],
["桑园东",159,197,3],
["加油站职工三区",300,645,2],
["加油站职工一区",278,792,2],
["富士康北街",430,993,2],
["富士康中街",434,1024,2],
["富士康南街",436,1060,2],
["坝后公园南门",396,1106,2],
["东岸观景台",402,1156,3],
["宾馆职工楼",544,578,1],
["二号楼",579,585,1],
["一号楼内",570,607,1],
["富士康北",396,989,2],
["驾校",432,1101,3],
["西二旗",700,1220,4],
["菜市口",740,1220,4],
["一〇七基地",780,1220,4],
["景区停车场东",832,1276,4],
["黄河大桥北",850,1234,5],
["黄河人家",836,1180,5],
["河清口",842,1324,5],
["泰山村西",836,1150,5],
["泰山村",836,1120,5],
["九曲桥",84,1452,4],
["新桥西",274,1436,4],
["新桥东",430,1366,4],
["保税区",478,1420,4],
["旅游局",744,1426,4],
["北岸小学",824,1390,4],
["景区停车场西",818,1322,4],
["黄河大桥南",848,1328,5],
["东和清口",848,1348,5],
["东和清",848,1376,5],
["机场东",848,1404,5],
["机场",848,1464,5]]


Station_short=[["火车站","hcz"],
["大桥东","dqd"],
["食堂","st"],
["三号楼东","shld"],
["一号楼东","yhld"],
["招待所","zds"],
["办公楼","bgl"],
["红旗广场","hqgc"],
["小桥东","xqd"],
["停车场西","tccx"],
["小浪底大学","xlddx"],
["好又来","hyl"],
["车队","cd"],
["坝后公园","bhgy"],
["富士康南","fskn"],
["海洋馆","hyg"],
["东门","dm"],
["松山村","ssc"],
["国道口","gdk"],
["电厂","dc"],
["高铁站","gtz"],
["外环","wh"],
["聚龙","jl"],
["西门口","xmk"],
["三标东","sbd"],
["大桥西","dqx"],
["一号楼","yhl"],
["小桥西","xqx"],
["内环","nh"],
["徐家汇","xjh"],
["宾馆东","bgd"],
["运动场东","ydcd"],
["后勤部","hqb"],
["桥沟","qg"],
["桥沟中学","qgzx"],
["三角楼","sjl"],
["石家街","sjj"],
["辛家庙","xjm"],
["大峪镇口","dyzk"],
["老鸦陈","lyc"],
["庙李","ml"],
["陈寨","cz"],
["宾馆大门","bgdm"],
["运动场西","ydcx"],
["停车场东","tccd"],
["二标桥南","ebqn"],
["二标北门","ebbm"],
["二标宿舍","ebss"],
["二标食堂","ebst"],
["二标游泳池","ebyyc"],
["一标河西","ybhx"],
["一标东","ybd"],
["建设银行","jsyh"],
["建设桥北","jsqb"],
["车队桥西","cdqx"],
["加油站","jyz"],
["景区北门","jqbm"],
["鑫苑名家","xymj"],
["陈寨南","czn"],
["庙李南","mln"],
["老鸦陈南","lycn"],
["大峪镇经开中心","dyzjkzx"],
["大峪镇十字街口","dyzszjk"],
["大峪镇人民路","dyzrml"],
["大峪镇医院","dyzyy"],
["森林公园","slgy"],
["锅炉房","glf"],
["四标","sb"],
["富士康北","fskb"],
["驾校","jx"],
["一标游泳池","ybyyc"],
["一标国际处","ybgjc"],
["一标运动场","ybydc"],
["一标食堂","ybst"],
["领导楼","ldl"],
["洗衣房","xyf"],
["宾馆西","bgx"],
["宾馆","bg"],
["一号楼西","yhlx"],
["三号楼西","shlx"],
["三号楼","shl"],
["辛家庙南","xjmn"],
["石家街南","sjjn"],
["九曲桥","jqq"],
["新桥西","xqx"],
["新桥东","xqd"],
["保税区","bsq"],
["旅游局","lyj"],
["北岸小学","baxx"],
["景区停车场西","jqtccx"],
["景区停车场东","jqtccd"],
["黄河大桥北","hhdqb"],
["黄河大桥南","hhdqn"],
["东和清口","dhqk"],
["东和清","dhq"],
["机场东","jcd"],
["机场","jc"],
["集装箱北","jzxb"],
["集装箱","jzx"],
["集装箱南三标东","jzxnsbd"],
["菜市场","csc"],
["集装箱南","jzxn"],
["集装箱西","jzxx"],
["领导楼内","ldln"],
["一号楼内一号楼西","yhlnyhlx"],
["东建材","djc"],
["运动场南","ydcn"],
["办公楼北","bglb"],
["三标游泳池","sbyyc"],
["三标内","sbn"],
["思源学院","syxy"],
["半坡","bp"],
["小浪底大学新区","xlddxxq"],
["东山宿舍楼","dsssl"],
["东山商城","dssc"],
["白鹿原","bly"],
["四号楼","shl"],
["图书馆","tsg"],
["小浪底大学老区","xlddxlq"],
["大峪镇中学","dyzzx"],
["大峪镇体育场","dyztyc"],
["大峪镇邮局","dyzyj"],
["大峪镇北客站","dyzbkz"],
["大峪镇大排档","dyzdpd"],
["老鸦陈三街","lycsj"],
["庙李三街","mlsj"],
["庙李一街","mlyj"],
["陈寨一街","czyj"],
["三角楼基地","sjljd"],
["桥沟北","qgb"],
["桥沟新区中学","qgxqzx"],
["桥沟新区","qgxq"],
["桐树岭","tsl"],
["桐树岭东","tsld"],
["柳林西","llx"],
["柳林","ll"],
["柳林东","lld"],
["桑园西","syx"],
["桑园东","syd"],
["加油站职工三区","jyzzgsq"],
["加油站职工一区","jyzzgyq"],
["富士康北街","fskbj"],
["富士康中街","fskzj"],
["富士康南街","fsknj"],
["坝后公园南门","bhgynm"],
["东岸观景台","dagjt"],
["转盘","zp"],
["宾馆职工楼","bgzgl"],
["二号楼","ehl"],
["一号楼内","yhln"],
["西二旗","xeq"],
["菜市口","csk"],
["一〇七基地","ylqjd"],
["黄河人家","hhrj"],
["河清口","hqk"],
["泰山村西","tscx"],
["泰山村","tsc"],
["七号交通洞北","qhjtdb"],
["八号交通洞","bhjtd"],
["七号交通洞南","qhjtdn"],
["微缩模型","wsmx"],
["西岸观景台","xagjt"],
["索桥西","sqx"],
["索桥东","sqd"],
["小坝","xb"],
["九号交通洞南","jhjtdn"],
["九号交通洞北","jhjtdb"],
["牛马潭","nmt"],
["交叉口","jck"],
["小桥沟","xqg"]]


for i in Station_info:
    for j in list_station:
        if i[0]==j.get_name():
            j.add_position(i,i[-1])

for i in Station_short:
    for j in list_station:
        if i[0]==j.get_name():
            j.add_shortname(i[-1])
        

colorbar=[[204, 51, 255],[255, 0, 102],[255, 153, 0],[0, 204, 0],[0, 51, 204]]

prince_list=[
    [1,1],
    [2,1],
    [3,2],
    [4,3],
    [5,4],
    [12,1.5],
    [23,2.5],
    [34,4.5],
    [45,6.5],
    [123,3],
    [234,5],
    [345,8],
    [1234,5.5],
    [2345,8.5],
    [12345,9]
]
            
linemap=cv.imread("real.png")

identity=[]
#print(len(list_line),len(list_station))
main()

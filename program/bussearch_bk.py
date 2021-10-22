# -*- coding: utf-8 -*-
"""
Created on Sun Jul 14 13:01:42 2019

@author: xuezh
"""
import math
import cv2 as cv
import matplotlib.pyplot as plt # plt 用于显示图片
import matplotlib.image as mpimg # mpimg 用于读取图片
import numpy as np
from PIL import Image, ImageDraw, ImageFont
###时刻表区###

fast_normal_timetable=[]
for i in range(5*60,24*60,6):
    fast_normal_timetable.append(i)
for i in range(7*60+3,9*60+3,6):
    fast_normal_timetable.append(i)
for i in range(17*60+3,19*60+3,6):
    fast_normal_timetable.append(i)
for i in range(0*60,5*60,30):
    fast_normal_timetable.append(i)
fast_normal_timetable.sort()

main_normal_timetable=[]
for i in range(5*60,24*60,10):
    main_normal_timetable.append(i)
for i in range(7*60+5,9*60+5,10):
    main_normal_timetable.append(i)
for i in range(17*60+5,19*60+5,10):
    main_normal_timetable.append(i)
for i in range(0*60,5*60,30):
    main_normal_timetable.append(i)
main_normal_timetable.sort()

slow_normal_timetable=[]
for i in range(5*60,22*60,20):
    slow_normal_timetable.append(i)
for i in range(7*60+10,9*60+10,20):
    slow_normal_timetable.append(i)
for i in range(17*60+10,19*60+10,20):
    slow_normal_timetable.append(i)
slow_normal_timetable.sort()

long_normal_timetable=[]
for i in range(7*60,21*60,40):
    long_normal_timetable.append(i)
for i in range(7*60+20,9*60+20,40):
    long_normal_timetable.append(i)
for i in range(17*60+20,19*60+20,40):
    long_normal_timetable.append(i)
long_normal_timetable.sort()

fast_sunday_timetable=[]
for i in range(7*60,21*60,12):
    fast_sunday_timetable.append(i)

middle_sunday_timetable=[]
for i in range(7*60,21*60,20):
    middle_sunday_timetable.append(i)

slow_sunday_timetable=[]
for i in range(8*60,20*60,40):
    slow_sunday_timetable.append(i)

long_sunday_timetable=[]
for i in range(8*60,19*60,80):
    long_sunday_timetable.append(i)

list_station=[]
list_line=[]

###类区###




class busline:
    def __init__(self,numero,starttime=5,endtime=22,proprity=2,time=1,price=1,timetable1=slow_normal_timetable,timetable2=slow_sunday_timetable):
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
        if self.__proprity==1:
            print("主线公交")
        elif self.__proprity==2:
            print("支线公交")
        else:
            print("长途公交")
        print(self.__numero,"路")
        print("票价",self.__price,"元")
        print("首班车",self.__starttime,"点")
        print("末班车",self.__endtime,"点")
        print("站点",self.__station)
        print("平均每站",self.__time,"分钟")
        self.affichage_timetable()
        print("线路图")
        img = mpimg.imread('{}-1.png'.format(str(self.__numero)))
        plt.imshow(img)
        plt.show()
    
    def get_starttime(self):
        return self.__starttime
    
    def get_endtime(self):
        return self.__endtime
    
    def affichage_timetable(self):
        print("始发站发车时间")
        if issunday==1:
            for i in self.__timetable2:
                print(i//60,"时",i%60,"分")
        else:
            for i in self.__timetable1:
                print(i//60,"时",i%60,"分")
    
    def get_timetable(self):
        if issunday==1:
            return self.__timetable2
        else:
            return self.__timetable1

class Station:
    def __init__(self,name,line):
        self.__name=name
        self.__line=[]
        self.__line.append(line)
        self.__neighborhood=[]
        self.__timetable=[]
        self.__position=[1,1,1]
    def get_name(self):
        return self.__name
        
    def add_line(self,line):
        self.__line.append(line)
    
    def get_line(self):
        return self.__line

    def get_position(self):
        return self.__position

    def add_position(self,position):
        self.__position=position
    
    def get_info(self):
        print(self.get_name(),"站：")
        print("停靠巴士：")
        print(self.get_line())
        self.get_timetable()
        print(self.get_position())
        
    def initialiser(self):
        for i in self.__line:
            for j in list_line:
                if i==j.get_numero():
                    liste_de_line=j.get_station()
                    for k in liste_de_line:
                        if k!=self.get_name():
                            self.__neighborhood.append((k,j.get_time()*abs(liste_de_line.index(k)-liste_de_line.index(self.get_name()))))
        self.__neighborhoodsorted=sorted(self.__neighborhood, key=lambda s: s[-1])
        for i in self.__line:
            for j in list_line:
                if i==j.get_numero():
                    direction=j.get_station()[-1]
                    delay=j.get_time()*abs(len(j.get_station())-j.get_station().index(self.get_name()))
                    timetableexact=[]
                    for i in j.get_timetable():
                        timetableexact.append(i+delay)
                    self.__timetable.append((j.get_numero(),direction,timetableexact))
                    direction=j.get_station()[0]
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
                print("开往",i[1],"方向的",i[0],"路车停止运营")
            else:
                print("开往",i[1],"方向的",i[0],"路车还有",int(time_rest),"分钟进站")
    def give_timetable(self):
        return self.__timetable
        
def searchline():
    line=int(input("请输入线路号："))
    for i in list_line:
        if line==i.get_numero():
            i.get_info()

def searchstation():
    station=input("请输入站点名：")
    for i in list_station:
        if station==i.get_name():
            i.get_info()

def drawline(station1,station2,line):
    global linemap
    for i in list_station:
        if station1==i.get_name():
            Station1=i
    for i in list_station:
        if station2==i.get_name():
            Station2=i
    n1,y1,x1=Station1.get_position()
    n2,y2,x2=Station2.get_position()
    cv.line(linemap, (y1, x1), (y2, x2), line.get_linecolor(), 5) #9

def drawpoint(station,line,isblackened):
    global linemap
    for i in list_station:
        if station==i.get_name():
            Station=i
    n1,y1,x1=Station.get_position()
    cv.circle(linemap, (y1,x1), 5, line.get_stationcolor(), 5) #33
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


def searchroute(startstation,endstation,timenow1):
    for i in list_station:
        if startstation==i.get_name():
            stationstarted=i
        if endstation==i.get_name():
            stationended=i
    for i in stationstarted.get_line():
        mintime=3000
        for j in list_line:
            if i==j.get_numero():
                linetemp=j
                found=0
                for k in linetemp.get_station():
                    if k==startstation:
                        stationnum1=linetemp.get_station().index(k)
                    if k==endstation:
                        stationnum2=linetemp.get_station().index(k)
                        found=1
                if found==1 and linetemp.get_numero()!=19 and linetemp.get_numero()!=91 and linetemp.get_numero()!=95 and linetemp.get_numero()!=64:
                    if stationnum1<=stationnum2:
                        for i in range(stationnum1,stationnum2):
                            drawline(j.get_station()[i],j.get_station()[i+1],linetemp)
                        for i in range(stationnum1,stationnum2+1):
                            if i == stationnum1 or i == stationnum2:
                                drawpoint(j.get_station()[i],linetemp,1)
                            else:
                                drawpoint(j.get_station()[i],linetemp,0)

                    else:
                        for i in range(stationnum2,stationnum1):
                            drawline(j.get_station()[i],j.get_station()[i+1],linetemp)
                        for i in range(stationnum2,stationnum1+1):
                            if i == stationnum1 or i == stationnum2:
                                drawpoint(j.get_station()[i],linetemp,1)
                            else:
                                drawpoint(j.get_station()[i],linetemp,0)

                if found==1 and (linetemp.get_numero()==19 or linetemp.get_numero()==91 or linetemp.get_numero()==95 or linetemp.get_numero()==64):
                    img2 = mpimg.imread('{}-1.png'.format(str(linetemp.get_numero())))
                    plt.imshow(img2)
                    plt.show()


                if found==1:
                    if stationnum1<=stationnum2:
                        direction=linetemp.get_station()[-1]
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
                        print("在",startstation,"站等候",int(time_rest),"分钟 乘坐开往",direction,"的",linetemp.get_numero(),"路车 到达",endstation,"站")
                        print("行程共",abs(stationnum1-stationnum2),"站")
                        print("到达时间：",int(abs(stationnum1-stationnum2)*linetemp.get_time()+time_rest+timenow1)//60,"时",int(abs(stationnum1-stationnum2)*linetemp.get_time()+time_rest+timenow1)%60,"分")
                        print("票价",linetemp.get_price(),"元")
                        mintime=min(mintime,abs(stationnum1-stationnum2)*linetemp.get_time()+time_rest+timenow1)
                    else :
                        print("糟糕！车辆停止运营了")

                    return mintime
                        
def searchcomplex(stationended,stationstarted,ordre,route):
    routetemp=route.copy()
    if ordre>4:
        return False
    if stationended==stationstarted:
        return route
    for i in stationended.get_neighbor():
        for j in list_station:
            if j.get_name()==i[0]:
                route=routetemp.copy()
                route.append(j.get_name())
                routereturn=searchcomplex(j,stationstarted,ordre+1,route)
                if routereturn!=False:
                    return routereturn
    return False
                    
def main():
    global linemap
    isended=0
    print("初始化中>>>>>>>>>>>")
    
    global timenow
    hour=float(input("出发于几点："))
    minute=float(input("出发于几分: "))
    timenow=60*hour+minute
    global issunday
    issunday=int(input("如果是星期天请打1："))
    print("初始化完成!")
    for i in list_station:
        i.initialiser()
    while(isended==0):
        print("功能选择")
        print("1=线路查询")
        print("2=站点查询")
        print("3=路线查询")
        print("4=更改时间")
        print("5=总线路图")
        print("6=退出")
        option=0
        while(option!=1 and option!=2 and option!=3 and option!=4 and option!=5 and option!=6):
            option=int(input("请输入数字以选择模式："))
        if option==1:
            searchline()
        if option==2:
            searchstation()
        if option==4:
            hour=float(input("出发于几点："))
            minute=float(input("出发于几分: "))
            timenow=60*hour+minute
            issunday=int(input("如果是星期天请打1："))
        if option==3:
            get_station=0
            while(get_station==0):
                startstation=input("请输入正确的出发站点：")
                endstation=input("输入正确的目标站点：")
                for i in list_station:
                    if startstation==i.get_name():
                        stationstarted=i
                        get_station=1
                    if endstation==i.get_name():
                        stationended=i
                        get_station=1

            print("**************************搜索结果***************************")


            
            result=searchcomplex(stationended,stationstarted,3,[])
            if result==False:
                result=searchcomplex(stationended,stationstarted,2,[])
                if result==False:
                    result=searchcomplex(stationended,stationstarted,1,[])
            result.reverse()
            result.append(endstation)
            timeensuite=timenow
            for i in range(len(result)-1):
                if i==(len(result)-2):
                    print("#############最后")
                elif i==0:
                    print("#############首先")
                else:
                    print("#############然后")
                print(result[i],result[i+1])
                timeensuite=searchroute(result[i],result[i+1],timeensuite)
            cv.imwrite('final.png', linemap)   
            plt.imshow(linemap)
            plt.show()

        if option != 4 and option != 5 and option !=6 :
            print("结果仅供参考，请结合小浪底大区交通图使用")
            print("查询结束，1键退出，0键继续")
            isended=int(input("请输入数字以选择模式："))
        
        if option == 5:
            img = mpimg.imread('plan2020.png')
            plt.imshow(img)
            plt.show()

        if option == 6:
            isended=1






line8=busline(8,0,24,1,1,1,fast_normal_timetable,fast_sunday_timetable)
line8.add_station(["外环","火车站","食堂","大桥东","徐家汇","宾馆东","运动场东","办公楼"
                   ,"红旗广场","小桥东","小桥西","聚龙","三标东","大桥西","火车站","后勤部","内环"
                   ])
list_line.append(line8)

line6=busline(6,0,24,1,1,1,fast_normal_timetable,fast_sunday_timetable)
line6.add_station(["外环","聚龙","西门口","三标东","大桥西","大桥东"
                   ,"食堂","四号楼东","三号楼东","二号楼东","一号楼东","一号楼","一号楼东","招待所","办公楼","红旗广场","小桥东"
                   ,"小桥西","聚龙","内环"])
list_line.append(line6)

line3=busline(3,0,24,1,1.8,2,main_normal_timetable,middle_sunday_timetable)
line3.add_station(["桥沟","桥沟中学","三角楼","石家街","辛家庙","大峪镇口","老鸦陈"
                   ,"庙李","陈寨","宾馆大门","运动场西","小桥东","红旗广场","办公楼",
                   "停车场东","小浪底大学","好又来","车队"
                   ])
list_line.append(line3)

line1=busline(1,0,24,1,1.6,3,main_normal_timetable,middle_sunday_timetable)
line1.add_station(["火车站","大桥东","食堂","三号楼东","一号楼东","招待所"
                   ,"办公楼","红旗广场","小桥东","停车场西","小浪底大学"
                   ,"好又来","车队","坝后公园","富士康南","海洋馆","东门","松山村"
                   ,"国道口","电厂","高铁站"])
list_line.append(line1)

line4=busline(4,0,24,1,2,2,main_normal_timetable,middle_sunday_timetable)
line4.add_station(["桥沟","二标桥南","二标桥南","二标北门","二标宿舍","二标食堂","二标游泳池"
                   ,"一标河西","一标东","大桥西","三标东","西门口","聚龙"
                   ,"小桥西","建设银行","建设桥北","小浪底大学","好又来","车队"])
list_line.append(line4)

line11=busline(11,0,24,1,1.3,2,main_normal_timetable,middle_sunday_timetable)
line11.add_station(["火车站","食堂","大桥东","徐家汇","宾馆东","运动场东",
                   "停车场东","小浪底大学","好又来","车队","车队桥西","加油站","景区北门","鑫苑名家"
                   ])
list_line.append(line11)

line12=busline(12,0,24,1,1,1,fast_normal_timetable,fast_sunday_timetable)
line12.add_station(["外环","一号楼东","森林公园","运动场东","宾馆东","徐家汇","大桥东","食堂","四号楼东","三号楼东","二号楼东","一号楼东","一号楼","内环"
                   ])
list_line.append(line12)

line7=busline(7,5,22,2,1.1)
line7.add_station(["集装箱北","集装箱","集装箱南""三标东","菜市场","西门口","大桥西","大桥东","食堂","四号楼东"
                   ,"三号楼东","二号楼东","一号楼东","四标","锅炉房"
                   ])
list_line.append(line7)

line2=busline(2,5,22,2,1.2,1)
line2.add_station(["火车站","大桥东","食堂","徐家汇","领导楼","洗衣房","宾馆西"
                   ,"宾馆大门","运动场西","小桥东","小桥西","聚龙","菜市场"
                   ,"集装箱南","集装箱","集装箱西"])
list_line.append(line2)



line16=busline(16,5,22,2,2.1,2)
line16.add_station(["车队","好又来","小浪底大学","停车场西","运动场西","宾馆大门","陈寨南","庙李南","老鸦陈南","大峪镇口","大峪镇经开中心","大峪镇十字街口","大峪镇人民路","大峪镇医院"])
list_line.append(line16)

line17=busline(17,5,22,2,1,1)
line17.add_station(["外环","领导楼","大桥东","食堂","四号楼西","三号楼西","三号楼","三号楼东","二号楼东","一号楼东","招待所","运动场东","宾馆东","徐家汇","领导楼","领导楼内","内环"])
list_line.append(line17)

line85=busline(85,5,22,2,1.9,3)
line85.add_station(["锅炉房","四标","森林公园","停车场东","小浪底大学"
                   ,"好又来","车队","坝后公园","富士康北","驾校","东门","松山村","国道口","电厂","高铁站"])
list_line.append(line85)

line20=busline(20,5,22,2,2.2,2)
line20.add_station(["三角楼","桥沟中学","桥沟","一标游泳池","一标国际处","一标运动场","一标食堂","一标东","大桥西","大桥东","徐家汇","领导楼","洗衣房","宾馆西","宾馆"
                   ])
list_line.append(line20)

line26=busline(26,5,22,2,1.2,1)
line26.add_station(["外环","四号楼","四号楼西","三号楼西","二号楼西","一号楼西","一号楼","一号楼内""一号楼西","办公楼","红旗广场","东建材","运动场南","运动场东","宾馆东","徐家汇","大桥东","食堂","四号楼东","四号楼","外环"
                   ])
list_line.append(line26)

line27=busline(27,5,22,2,1.3)
line27.add_station(["锅炉房","四标","一号楼东","森林公园","办公楼","红旗广场","小桥东"
                   ,"小桥西","聚龙","西门口","三标东","三标游泳池","三标内"])
list_line.append(line27)

line30=busline(30,5,22,2,2.2,2)
line30.add_station(["桥沟","二标桥南","二标北门","二标宿舍","二标食堂","二标游泳池","一标河西","一标东","大桥西","大桥东","徐家汇","领导楼","运动场东","一号楼西","二号楼西","三号楼西","三号楼"
                   ])
list_line.append(line30)

line42=busline(42,5,22,2,1.6,2)
line42.add_station(["火车站","大桥东","徐家汇","宾馆东","宾馆","宾馆大门","陈寨南"
                   ,"庙李南","老鸦陈南","大峪镇口","辛家庙南","石家街南","三角楼","桥沟中学","桥沟"])
list_line.append(line42)

line50=busline(50,5,22,2,2.4)
line50.add_station(["车队","思源学院","坡中","小浪底大学新区","东山宿舍楼","东山商城","白鹿原"
                   ])
list_line.append(line50)

line54=busline(54,5,22,2,1.7)
line54.add_station(["一号楼","一号楼东","二号楼东","三号楼东","四号楼东","四号楼","四号楼西"
                   ,"食堂","大桥东","大桥西","一标东","一标食堂","一标运动场","一标国际处","一标游泳池","图书馆"])
list_line.append(line54)

line56=busline(56,5,22,2,1.3)
line56.add_station(["图书馆","一标游泳池","一标国际处","一标运动场","一标食堂","一标东","大桥西","三标东","西门口","聚龙"
                   ,"小桥西","小桥东","停车场西","小浪底大学","小浪底大学老区"])
list_line.append(line56)

line62=busline(62,5,22,2,1.5,2)
line62.add_station(["大峪镇中学","大峪镇体育场","大峪镇邮局","大峪镇十字街口","大峪镇北客站","大峪镇大排档","大峪镇口"
                   ,"老鸦陈","老鸦陈三街","庙李三街","庙李一街","陈寨一街","陈寨","陈寨南","宾馆大门","运动场西","小桥东","小桥西","建设银行","建设桥北","小浪底大学","小浪底大学老区"])
list_line.append(line62)

line63=busline(63,5,22,2,1.5,3)
line63.add_station(["大峪镇医院","大峪镇体育场","大峪镇邮局","大峪镇十字街口","大峪镇北客站","大峪镇大排档","大峪镇口"
                   ,"辛家庙南","石家街南","三角楼","三角楼基地","桥沟北","桥沟新区中学","桥沟新区","二标桥南","二标北门","二标宿舍","二标食堂","二标游泳池","一标游泳池","图书馆"])
list_line.append(line63)

line64=busline(64,5,22,2,2.7,2)
line64.add_station(["桐树岭","桐树岭东","柳林西","柳林","柳林东","桑园西","桑园东"
                   ,"二标北门","二标桥南","桥沟"])
list_line.append(line64)

line77=busline(77,5,22,2,1.9,3)
line77.add_station(["加油站职工三区","加油站职工一区","加油站","车队桥西","车队","坝后公园","富士康北街"
                   ,"富士康中街","富士康南街","坝后公园南门","东岸观景台","转盘","东门","松山村","国道口","电厂","高铁站"])
list_line.append(line77)

line83=busline(83,5,22,2,1.3,1)
line83.add_station(["内环","一号楼","一号楼西","办公楼","红旗广场","小桥东","运动场西"
                   ,"宾馆大门","宾馆","宾馆职工楼","徐家汇","大桥东","食堂","四号楼西","三号楼西","二号楼西","二号楼","二号楼东","一号楼东","一号楼","一号楼内","外环"])
list_line.append(line83)



line91=busline(91,7,21,3,3.4,3,long_normal_timetable,long_sunday_timetable)
line91.add_station(["高铁站","电厂","国道口","西二旗","菜市口","一〇七基地","景区停车场东"
                   ,"黄河大桥北","黄河人家","河清口","泰山村西","泰山村"])
list_line.append(line91)

line95=busline(95,5,22,2,3.4,4)
line95.add_station(["九曲桥","新桥西","新桥东","保税区","高铁站","旅游局","北岸小学"
                   ,"景区停车场西","景区停车场东","黄河大桥北","黄河大桥南","东和清口","东和清","机场东","机场"])
list_line.append(line95)

line18=busline(18,7,21,3,3.5,4,long_normal_timetable,long_sunday_timetable)
line18.add_station(["车队","车队桥西","加油站","景区北门","七号交通洞北","八号交通洞","七号交通洞南","微缩模型","西岸观景台","索桥西","索桥东","转盘","东门","松山村","国道口","电厂","高铁站"
                   ])
list_line.append(line18)

line19=busline(19,7,21,3,8.4,8,long_normal_timetable,long_sunday_timetable)
line19.add_station(["车队","车队桥西","加油站","景区北门","鑫苑名家","小坝","九号交通洞南","九号交通洞北","桐树岭","牛马潭","交叉口","小桥沟","桥沟新区","桥沟"
                   ])
list_line.append(line19)


###站点位置信息输入

print("-------------小浪底大区公共交通查询系统--------------")
print("----------------当前版本V1.0 -----------------")
print("水利部小浪底水利枢纽建设管理局交通处小浪底大区车队集团信息科版权所有")




    
Station_info=[["火车站",594,492],
["大桥东",580,505],
["食堂",597,519],
["三号楼东",605,567],
["一号楼东",588,607],
["招待所",561,627],
["办公楼",494,651],
["红旗广场",465,658],
["小桥东",441,654],
["停车场西",432,697],
["小浪底大学",406,751],
["好又来",382,822],
["车队",376,897],
["坝后公园",388,949],
["富士康南",404,1035],
["海洋馆",510,1167],
["东门",568,1219],
["松山村",604,1218],
["国道口",640,1216],
["电厂",636,1310],
["高铁站",634,1402],
["徐家汇",561,551],
["领导楼",533,551],
["洗衣房",502,547],
["宾馆西",491,563],
["宾馆大门",476,582],
["运动场西",466,608],
["小桥西",420,638],
["聚龙",429,619],
["菜市场",410,563],
["集装箱南",438,530],
["集装箱",406,468],
["集装箱西",318,434],
["桥沟",518,125],
["二标桥南",497,178],
["二标北门",439,172],
["二标宿舍",507,214],
["二标食堂",530,236],
["二标游泳池",558,270],
["一标河西",587,357],
["一标东",568,437],
["大桥西",553,474],
["三标东",495,514],
["西门口",449,578],
["建设银行",406,677],
["建设桥北",394,704],
["外环",1,1],
["四号楼东",609,542],
["二号楼东",594,587],
["一号楼",572,607],
["内环",1,1],
["集装箱北",417,376],
["集装箱南三标东",439,534],
["四标",608,592],
["锅炉房",623,544],
["宾馆东",535,610],
["运动场东",526,628],
["后勤部",596,504],
["桥沟中学",555,129],
["三角楼",604,142],
["石家街",609,210],
["辛家庙",618,279],
["大峪镇口",627,380],
["老鸦陈",616,447],
["庙李",588,465],
["陈寨",551,501],
["停车场东",454,695],
["车队桥西",338,899],
["加油站",269,900],
["景区北门",200,896],
["鑫苑名家",88,851],
["森林公园",563,633],
["陈寨南",499,538],
["庙李南",568,486],
["老鸦陈南",602,455],
["大峪镇经开中心",685,427],
["大峪镇十字街口",714,418],
["大峪镇人民路",713,456],
["大峪镇医院",712,503],
["四号楼西",574,542],
["三号楼西",564,541],
["三号楼",585,562],
["领导楼内",546,533],
["七号交通洞北",68,888],
["八号交通洞",22,748],
["七号交通洞南",10,1164],
["微缩模型",36,1268],
["西岸观景台",166,1272],
["索桥西",238,1328],
["索桥东",410,1286],
["转盘",436,1212],
["小坝",1,1],
["九号交通洞南",1,1],
["九号交通洞北",1,1],
["桐树岭",1,1],
["牛马潭",1,1],
["交叉口",1,1],
["小桥沟",1,1],
["桥沟新区",476,114],
["一标游泳池",556,288],
["一标国际处",556,317],
["一标运动场",548,368],
["一标食堂",542,402],
["宾馆",509,596],
["四号楼",590,542],
["二号楼西",561,580],
["一号楼西",552,602],
["一号楼内一号楼西",555,606],
["东建材",472,625],
["运动场南",496,628],
["三标游泳池",478,486],
["三标内",523,464],
["辛家庙南",620,323],
["石家街南",606,203],
["思源学院",426,784],
["坡中",408,887],
["小浪底大学新区",498,890],
["东山宿舍楼",527,852],
["东山商城",570,844],
["白鹿原",616,794],
["图书馆",513,291],
["小浪底大学老区",383,745],
["大峪镇中学",830,445],
["大峪镇体育场",780,440],
["大峪镇邮局",778,408],
["大峪镇北客站",712,345],
["大峪镇大排档",653,368],
["老鸦陈三街",637,448],
["庙李三街",618,458],
["庙李一街",581,492],
["陈寨一街",558,504],
["三角楼基地",566,69],
["桥沟北",505,33],
["桥沟新区中学",482,70],
["桐树岭东",1,1],
["柳林西",1,1],
["柳林",1,1],
["柳林东",1,1],
["桑园西",1,1],
["桑园东",1,1],
["加油站职工三区",300,645],
["加油站职工一区",278,792],
["富士康北街",430,993],
["富士康中街",434,1024],
["富士康南街",436,1060],
["坝后公园南门",396,1106],
["东岸观景台",402,1156],
["宾馆职工楼",544,578],
["二号楼",579,585],
["一号楼内",570,607],
["富士康北",396,989],
["驾校",432,1101],
["西二旗",1,1],
["菜市口",1,1],
["一〇七基地",1,1],
["景区停车场东",1,1],
["黄河大桥北",1,1],
["黄河人家",1,1],
["河清口",1,1],
["泰山村西",1,1],
["泰山村",1,1],
["九曲桥",1,1],
["新桥西",1,1],
["新桥东",1,1],
["保税区",1,1],
["旅游局",1,1],
["北岸小学",1,1],
["景区停车场西",1,1],
["黄河大桥南",1,1],
["东和清口",1,1],
["东和清",1,1],
["机场东",1,1],
["机场",1,1]]

for i in Station_info:
    for j in list_station:
        if i[0]==j.get_name():
            j.add_position(i)

linemap=cv.imread("real.png")
print(len(list_line),len(list_station))
#main()
# coding: utf-8



# In[5]:


from pyswarm import pso
import numpy as np
import pandas as pd
import os
import math
import copy


np.set_printoptions(formatter={'float_kind':'{:f}'.format})


# In[91]:建立費用表單
rowNum = 6
columns = ['基本電費', '超約罰金', '線路補助費','總電費']
result = pd.DataFrame([[pd.NaT, pd.NaT, pd.NaT, pd.NaT] for n in range(rowNum)],columns=columns)

# In[91]:建立契約容量表單
rowNum = 28
columns = ['經常契約', '半尖峰契約', '週六半尖峰契約','離峰契約','更換對應契約週期(月)']
#contracts = pd.DataFrame([[pd.NaT, pd.NaT, pd.NaT, pd.NaT] for n in range(rowNum)],columns=columns)
contracts = pd.DataFrame(columns=columns)

# In[24]:前置作業(輸入檔案)
print("歡迎使用台電契約優化程式")
print("Welcome to the Taipower Contract Optimization Program")


print("1.請輸入讀檔路徑:")
print("1.Please enter the file path:")
path_position = input()
path = path_position
os.chdir(path)

print("2.請輸入資料(ex:Test):")
Data = input()
#B=pd.read_csv(Data + '.csv' )
B=pd.read_csv(Data + '.csv',encoding = 'Big5')

# In[24]:前置作業(輸入檔案)
print("3.請選擇起始月份")
print("a.1月")
print("b.2月")
print("c.3月")
print("d.4月")
print("e.5月")
print("f.6月")
print("g.7月")
print("h.8月")
print("i.9月")
print("j.10月")
print("k.11月")
print("l.12月")
begin_month = str(input())
begin_month_number = 0
if (begin_month == 'a'):
    begin_month_number = 0
elif (begin_month == 'b'):
    begin_month_number = 1
elif(begin_month == 'c'):
    begin_month_number = 2
elif(begin_month == 'd'):
    begin_month_number = 3   
elif(begin_month == 'e'):
    begin_month_number = 4
elif(begin_month == 'f'):
    begin_month_number = 5
elif(begin_month == 'g'):
    begin_month_number = 6
elif(begin_month == 'h'):
    begin_month_number = 7
elif(begin_month == 'i'):
    begin_month_number = 8
elif(begin_month == 'j'):
    begin_month_number = 9
elif(begin_month == 'k'):
    begin_month_number = 10
elif(begin_month == 'l'):
    begin_month_number = 11
else:
    print("System error. Please try it again")
# In[24]:前置作業(輸入檔案)

print("4.請選擇結束月份")
print("a.1月")
print("b.2月")
print("c.3月")
print("d.4月")
print("e.5月")
print("f.6月")
print("g.7月")
print("h.8月")
print("i.9月")
print("j.10月")
print("k.11月")
print("l.12月")
end_month = str(input())
end_month_number = 0
if (end_month == 'a'):
    end_month_number = 0
elif (end_month == 'b'):
    end_month_number = 1
elif(end_month == 'c'):
    end_month_number = 2
elif(end_month == 'd'):
    end_month_number = 3   
elif(end_month == 'e'):
    end_month_number = 4
elif(end_month == 'f'):
    end_month_number = 5
elif(end_month == 'g'):
    end_month_number = 6
elif(end_month == 'h'):
    end_month_number = 7
elif(end_month == 'i'):
    end_month_number = 8
elif(end_month == 'j'):
    end_month_number = 9
elif(end_month == 'k'):
    end_month_number = 10
elif(end_month == 'l'):
    end_month_number = 11
else:
    print("System error. Please try it again")
    
    
# In[24]:前置作業(輸入檔案)
#Z =B.iloc[13:39]
Contract_Distance = end_month_number-begin_month_number+1
Y = B.iloc[begin_month_number:end_month_number+1,1:5]

Y= Y.values
Z = B.iloc[:,6:10]
Z['z']=Z['經常契約']+Z['半尖峰契約']*0.75+(Z['週六半尖峰']+Z['離峰契約'])*0.2
# In[]
print("5.是使用何種用電?")
print("a.高壓電")
print("b.特高壓電")
Power_type = str(input())
if (Power_type == 'a'):
    price = np.array([[166.9,166.9,33.3,33.3],[166.9,166.9,33.3,33.3],[166.9,166.9,33.3,33.3],[166.9,166.9,33.3,33.3],[166.9,166.9,33.3,33.3],[223.6,166.9,44.7,44.7],[223.6,166.9,44.7,44.7],[223.6,166.9,44.7,44.7],[223.6,166.9,44.7,44.7],[166.9,166.9,33.3,33.3],[166.9,166.9,33.3,33.3],[166.9,166.9,33.3,33.3]])
elif (Power_type == 'b'):
    price = np.array([[160.6,160.6,32.1,32.1],[160.6,160.6,32.1,32.1],[160.6,160.6,32.1,32.1],[160.6,160.6,32.1,32.1],[160.6,160.6,32.1,32.1],[217.3,160.6,43.4,43.4],[217.3,160.6,43.4,43.4],[217.3,160.6,43.4,43.4],[217.3,160.6,43.4,43.4],[160.6,160.6,32.1,32.1],[160.6,160.6,32.1,32.1],[160.6,160.6,32.1,32.1]])
else:
    print("System error. Please try it again")

# In[]
print("6.是使用幾段式用電?")
print("a.二段式")
print("b.三段式")
Power_stage = str(input())
if (Power_stage == 'a' and Power_type == 'a'):
    price = np.array([[166.9,166.9,33.3,33.3],[166.9,166.9,33.3,33.3],[166.9,166.9,33.3,33.3],[166.9,166.9,33.3,33.3],[166.9,166.9,33.3,33.3],[223.6,0,44.7,44.7],[223.6,0,44.7,44.7],[223.6,0,44.7,44.7],[223.6,0,44.7,44.7],[166.9,166.9,33.3,33.3],[166.9,166.9,33.3,33.3],[166.9,166.9,33.3,33.3]])
elif (Power_stage == 'a' and Power_type == 'b' ):
    price = np.array([[160.6,160.6,32.1,32.1],[160.6,160.6,32.1,32.1],[160.6,160.6,32.1,32.1],[160.6,160.6,32.1,32.1],[160.6,160.6,32.1,32.1],[217.3,0,43.4,43.4],[217.3,0,43.4,43.4],[217.3,0,43.4,43.4],[217.3,0,43.4,43.4],[160.6,160.6,32.1,32.1],[160.6,160.6,32.1,32.1],[160.6,160.6,32.1,32.1]])
elif (Power_stage == 'b' and Power_type == 'a' ):
    price = np.array([[166.9,166.9,33.3,33.3],[166.9,166.9,33.3,33.3],[166.9,166.9,33.3,33.3],[166.9,166.9,33.3,33.3],[166.9,166.9,33.3,33.3],[223.6,166.9,44.7,44.7],[223.6,166.9,44.7,44.7],[223.6,166.9,44.7,44.7],[223.6,166.9,44.7,44.7],[166.9,166.9,33.3,33.3],[166.9,166.9,33.3,33.3],[166.9,166.9,33.3,33.3]])
elif (Power_stage == 'b' and Power_type == 'b' ):
    price = np.array([[160.6,160.6,32.1,32.1],[160.6,160.6,32.1,32.1],[160.6,160.6,32.1,32.1],[160.6,160.6,32.1,32.1],[160.6,160.6,32.1,32.1],[217.3,160.6,43.4,43.4],[217.3,160.6,43.4,43.4],[217.3,160.6,43.4,43.4],[217.3,160.6,43.4,43.4],[160.6,160.6,32.1,32.1],[160.6,160.6,32.1,32.1],[160.6,160.6,32.1,32.1]])
else:
    print("System error. Please try it again")
    
# In[]確認Price
    
price = price[begin_month_number:end_month_number+1,:]  
# In[]
sp = 1
print("7.是否有設定備用電力?")
print("a.Yes")
print("b.No")
Backup_power = str(input())

if (Backup_power == 'a'and Power_type =='b'):
    print('為自備多少伏特變電設備受電者?')
    print("a.自備161,000伏特變電設備受電者")
    print("b.自備345,000伏特變電設備受電者")
    print("c.以上皆非")
    Self_supportpower =  str(input())
    print('備用饋線是否使用地下管線?')
    print('a.Yes')
    print('b.No')
    Support_power_way =str(input())
    print('是否為用戶自備及維護?')
    print('a.Yes')
    print('b.No')
    Selfcare = str(input())
    if(Self_supportpower == 'a'):
        if (Support_power_way == 'b' and Selfcare =='a'):
            sp= 1.05*0.98
        elif(Support_power_way == 'a' and Selfcare =='a'):
            sp= 1.1*0.98
        else:
            sp = 1.15*0.98
    elif(Self_supportpower == 'b'):
        if (Support_power_way == 'b' and Selfcare =='a'):
            sp= 1.05*0.958
        elif(Support_power_way == 'a' and Selfcare =='a'):
            sp= 1.1*0.958
        else:
            sp = 1.15*0.958
    elif(Self_supportpower == 'c'):
        if (Support_power_way == 'b' and Selfcare =='a'):
            sp= 1.05
        elif(Support_power_way == 'a' and Selfcare =='a'):
            sp= 1.1
        else:
            sp = 1.15

elif(Backup_power == 'a' and Power_type =='a'):
    print('備用電力是否由同一二次變電所或配電變電所之另一饋線供應?')
    print('a.Yes')
    print('b.No')
    Support_power_place = str(input())
    print('備用饋線是否使用地下管線?')
    print('a.Yes')
    print('b.No')
    Support_power_way =str(input())
    print('是否為用戶自備及維護?')
    print('a.Yes')
    print('b.No')
    Selfcare = str(input())
    if(Support_power_place == 'a'):
        if (Support_power_way == 'b' and Selfcare =='a'):
            sp= 1
        elif(Support_power_way == 'a' and Selfcare =='a'):
            sp= 1.05
        else:
            sp = 1.1
    elif(Support_power_place == 'b'):
         if (Support_power_way == 'b' and Selfcare =='a'):
            sp= 1.05
         elif(Support_power_way == 'a' and Selfcare =='a'):
            sp= 1.1
         else:
            sp = 1.15


# In[]
print("8.選擇用電種類")
print("a.高壓用電")
print("b.69KV 特高壓用電")
print("c.161KV 特高壓用電")
print("d.345KV 特高壓用電")
Using_type = str(input())
if (Using_type =='a'):
    Maintenance_fee = float(185)
    Expansion_fee = float(1759)
elif(Using_type =='b'):
    Maintenance_fee = float(179)
    Expansion_fee = float(1600)
elif(Using_type =='c'):
    Maintenance_fee = float(176)
    Expansion_fee = float(1050)
elif(Using_type =='d'):
    Maintenance_fee = float(171)
    Expansion_fee = float(420)
else:
    print("System error. Please try it again")
# In[93]:
print("9.是否要手動輸入搜尋範圍?")
print("a.Yes" )
print("b.No")
enter_zone = str(input())

if (enter_zone == 'a') :
    print("lower_bound:")
    lower_bound = []
    for i in range(4):
         if(i+1==1):
             print("經常契約容量:")
             a = int(input())
             lower_bound.append(a)
             a = 0
         elif(i+1==2):
             print("半尖峰契約容量:")
             a = int(input())
             lower_bound.append(a)
             a = 0
         elif(i+1==3):
             print("週六半尖峰契約容量:")
             a = int(input())
             lower_bound.append(a)
             a = 0
         else:
             print("離峰契約榮量")
             a = int(input())
             lower_bound.append(a)
             a = 0

    print("uper_bound:")
    uper_bound =[]
    for i in range(4):
        if(i+1==1):
             print("經常契約容量:")
             a = int(input())
             uper_bound.append(a)
             a = 0
        elif(i+1==2):
             print("半尖峰契約容量:")
             a = int(input())
             uper_bound.append(a)
             a = 0
        elif(i+1==3):
             print("週六半尖峰契約容量:")
             a = int(input())
             uper_bound.append(a)
             a = 0
        else:
             print("離峰契約榮量")
             a = int(input())
             uper_bound.append(a)
             a = 0

        
elif (enter_zone == 'b') :
    lower_bound = []
    for i in range(4):
        if(i+1==1):
             lower_bound.append(min(Y[:,1]))
        elif(i+1==2):
             lower_bound.append(0)
        elif(i+1==3):
             lower_bound.append(0)
        else:
             lower_bound.append(0)
    uper_bound = []
    for i in range(4):
        if(i+1==1):
             uper_bound.append(max(max(Y[:,1]),max(Y[:,0])))
        elif(i+1==2):
             uper_bound.append(1)
        elif(i+1==3):
             uper_bound.append(3800-min(Y[:,1]))
        else:
             uper_bound.append(1)
    
   
else:
    print("System error. Please try it again")








# In[93]:

print('10.請輸入分析結果檔案名稱:')
Result_name  = str(input())
if (Result_name == ''):
    Result_name = Data + '_result'
    print("程式執行中...")
else:

    print("程式執行中...")
    
    
    
    
# In[5]:  
def findAllDivisors(targetNum):
   rslt = []
   i = 1
   while i<targetNum:
       if targetNum%i == 0:
           rslt.append(i)
       i = i + 1
   rslt.append(targetNum)
   return rslt

# In[5]:

stratages=findAllDivisors(Contract_Distance)
# In[28]:
def updateList(listObjA, listObjB, valToListObjB):
    processLog = {}
    for idx, n in enumerate(listObjA):
        deductQty = min(n, valToListObjB)
        if deductQty>0:
            valToListObjB -= deductQty
            listObjA[idx] -= deductQty
            processLog[12-idx] = deductQty
    listObjA.append(0)
    listObjB.append(valToListObjB)
    return processLog
# In[171]:

# Define the objective (to be minimize)
def weight(x, *args):
    Y, price, Z= args
    monthLen=int(len(Y))
    optLen = monthLen/int(len(x)/4)
#     e.g. 12個月份資料，以4組解求最佳化， 12/4 = 3， 
    Ebasic = 0
    Eover = 0
    Echange = 0
    EbasicChange=0
#    Etotal = 0
    zWhole =Z['z'].values
    descIdx=(np.array(range(24))+1)*-1
       # preProcess - put this part outside the month loop
    Acon = Z.iloc[Z.shape[0]-12:, 0].tolist()
    Ccon = (Z.iloc[Z.shape[0]-12:, 2]/5).tolist()
     
    AtoC = [0]
    CtoA = [0]
    for idx in range(11):
        curIdx = idx
        nxtIdx = idx+1
        diffA = Acon[nxtIdx]-Acon[curIdx]
        diffC = Ccon[nxtIdx]-Ccon[curIdx]
        if(diffA*diffC < 0):
            val = min(abs(diffA), abs(diffC))
            if(diffA<0):
                updateList(CtoA, AtoC, val)
            else:
                updateList(AtoC, CtoA, val)
        else:
            AtoC.append(0)
            CtoA.append(0)
    for monthIdx in range(monthLen):
        idicateIdx = int (monthIdx / optLen)
        x1, x2, x3, x4 = x[idicateIdx*4: (idicateIdx*4)+4]
        dsol1=x1
        dsol2=x2+x1
        dsol3=x1+x2+x3
        dsol4=x1+x2+x3+x4
        refPrice1, refPrice2, refPrice3, refPrice4 = price[monthIdx,:]
        Y1, Y2, Y3, Y4 = Y[monthIdx,:]
#        if (Power_type == 'a' and Backup_power == 'b'):
#            Ebasic+=(refPrice1*x1)+(refPrice2*x2)+(refPrice3*max(((x3+x4)-(0.5*(x1+x2))),0))
#        else:
        Ebasic+=(refPrice1*x1*sp)+(refPrice2*x2*sp)+(refPrice3*sp*max(((x3+x4)-(0.5*(x1+x2))),0))
#        elif(Power_type == 'b' and Backup_power == 'a' and Self_supportpower == 'a'):
#            Ebasic+=math.ceil((refPrice1*x1*1.15*0.98)+(refPrice2*x2*1.15*0.98)+(refPrice3*1.15*0.98*max(((x3+x4)-(0.5*(x1+x2))),0)))
#        elif(Power_type == 'b' and Backup_power == 'a' and Self_supportpower == 'b'):
#            Ebasic+=math.ceil((refPrice1*x1*1.15*0.958)+(refPrice2*x2*1.15*0.958)+(refPrice3*1.15*0.958*max(((x3+x4)-(0.5*(x1+x2))),0)))
#        elif(Power_type == 'b' and Backup_power == 'a' and Self_supportpower == 'c'):
#            Ebasic+=math.ceil((refPrice1*x1*1.15)+(refPrice2*x2*1.15)+(refPrice3*1.15*max(((x3+x4)-(0.5*(x1+x2))),0)))
#        elif(Power_type == 'a' and Backup_power == 'a'):
#            Ebasic+=math.ceil((refPrice1*x1*1.15*0.98)+(refPrice2*x2*1.1*0.98)+(refPrice3*1.1*0.98*max(((x3+x4)-(0.5*(x1+x2))),0)))
#        elif(Power_type == 'b' and Backup_power == 'b'):
#            Ebasic+=math.ceil((refPrice1*x1*1.15)+(refPrice2*x2*1.15)+(refPrice3*1.15*max(((x3+x4)-(0.5*(x1+x2))),0)))
        #over Rule1
        extremeHold=dsol1*1.1
        basicOver=max(min(extremeHold, Y1)-dsol1, 0)
        extremeOver=max(0, Y1-extremeHold)
        Eover+=2*refPrice1*basicOver
        Eover+=3*refPrice1*extremeOver
        #Over Rule2
        extremeHold=dsol2*1.1+max(Y1-dsol1, 0)
        basicOver = 0
        if ((Y2-dsol2)-max(Y1-dsol1, 0))<= 0.1*dsol2 and ((Y2-dsol2)-max(Y1-dsol1, 0))>0:
            basicOver = ((Y2-dsol2)-max(Y1-dsol1, 0))
            extremeOver=max(0, Y2-extremeHold)
        elif((Y2-dsol2)-max(Y1-dsol1, 0)) > 0.1*dsol2:
            basicOver = 0.1*dsol2
            extremeOver=max(0, Y2-extremeHold)
            extremeOver = max(extremeOver,0)
        else:
            basicOver = 0
            extremeOver = 0
        Eover+=2*refPrice2*basicOver
        Eover+=3*refPrice2*extremeOver
        #Over Rule3
        extremeHold = dsol3*1.1+max(Y1-dsol1, Y2-dsol2, 0)
        if((Y3-dsol3)-max(Y1-dsol1, Y2-dsol2, 0))<=0.1*dsol3 and ((Y3-dsol3)-max(Y1-dsol1, Y2-dsol2, 0))>0:
            basicOver = ((Y3-dsol3)-max(Y1-dsol1, Y2-dsol2, 0))
            extremeOver=max(0, Y3-extremeHold)
            basicOver = max(basicOver,0)
        elif((Y3-dsol3)-max(Y1-dsol1, Y2-dsol2, 0))>0.1*dsol3:
            basicOver = 0.1*dsol3
            extremeOver=max(0, Y3-extremeHold)
            extremeOver = max(extremeOver,0)
        else:
            basicOver = 0
            extremeOver =0
        Eover+=2*refPrice3*basicOver
        Eover+=3*refPrice3*extremeOver
        #Over Rule4
        extremeHold = dsol4*1.1+ max(Y1-dsol1, Y2-dsol2, Y3-dsol3, 0)
        if((Y4-dsol4)-max(Y1-dsol1, Y2-dsol2, Y3-dsol3, 0))<=0.1*dsol4 and ((Y4-dsol4)-max(Y1-dsol1, Y2-dsol2, Y3-dsol3, 0))>0:
            basicOver = ((Y4-dsol4)-max(Y1-dsol1, Y2-dsol2, Y3-dsol3, 0))
            extremeOver=max(0, Y4-extremeHold)
            basicOver = max(basicOver,0)
        elif((Y4-dsol4)-max(Y1-dsol1, Y2-dsol2, Y3-dsol3, 0))>0.1*dsol4:
            basicOver = 0.1*dsol4
            extremeOver=max(0, Y4-extremeHold)
            extremeOver = max(extremeOver,0)
        else:
            basicOver = 0
            extremeOver = 0
        Eover+=2*refPrice4*basicOver
        Eover+=3*refPrice4*extremeOver
#         Echange
        zStar=max(zWhole[len(zWhole)-24:len(zWhole)]) #找出錢24個月最大Z
        z= 1*x1+0.75*x2+0.2*x3+0.2*x4 #這一期的Z
        if(z>zWhole[-1] and z<=zStar): #判斷情況為case2 z(i-1)<z<z(*i)
            diff=z-zWhole[-1] #算出所需要的量
            curLevel=zWhole[-1] #用來比較的基準
            qtyList=[] #紀錄借用量的array
            idxList=[] #紀錄借用期數array
            for idxDiff, zIdx in enumerate(descIdx):
                subDiff=max(zWhole[zIdx]-curLevel, 0) #找可以借的量
                #判斷使否足夠借
                if (subDiff > diff): #足夠借
                    qtyList.append(diff) #紀錄借的量
                    diff-=diff #更新所需要借的量
                    idxList.append(idxDiff) #記錄間隔期數
                elif(subDiff> 0):
                    diff-=subDiff #更新可以借用的量
                    qtyList.append(subDiff) #紀錄借的量
                    idxList.append(idxDiff) #記錄間隔期數
                    curLevel=zWhole[zIdx] #更新比較基準
            Echange += min(Maintenance_fee*np.sum(np.array(idxList)*np.array(qtyList)),Expansion_fee*0.5*(z-zWhole[-1])) #計算線補費
        elif(z>zStar): #判斷情況case3 z>z*(i)
            diff=zStar-zWhole[-1]#算出所需要的量
            curLevel=zWhole[-1]#用來比較的基準
            qtyList=[] #紀錄借用量的array
            idxList=[] #紀錄借用期數array
            for idxDiff, zIdx in enumerate(descIdx):
                subDiff=max(zWhole[zIdx]-curLevel, 0) #找可以借的量
                #判斷使否足夠借
                if (subDiff > diff):#足夠借
                    qtyList.append(diff)#紀錄借的量
                    diff-=diff #更新所需要借的量
                    idxList.append(idxDiff) #記錄間隔期數
                elif(subDiff> 0):
                    diff-=subDiff #更新可以借用的量
                    qtyList.append(subDiff) #紀錄借的量
                    idxList.append(idxDiff)  #記錄間隔期數
                    curLevel=zWhole[zIdx] #更新比較基準
            Echange += min(Maintenance_fee*np.sum(np.array(idxList)*np.array(qtyList)),Expansion_fee*0.5*(zStar-zWhole[-1]))+Expansion_fee*(z-zStar)#計算線補費
        #update zWhole
        zWhole = np.concatenate([zWhole, [z]])
                 #        #Ebasicchange
        diffA = x1 - Acon[-1]
        diffC = (x3/5) - Ccon[-1]
        if(diffA*diffC < 0):
            val = min(abs(diffA), abs(diffC))
            if(diffA<0):
                updateList(CtoA, AtoC, val)
            else:
                processData = updateList(AtoC, CtoA, val)
                #計算費用
#                print (processData)
                for rsltKey,rsltVal in processData.items():
                    EbasicChange+=rsltKey*rsltVal*refPrice1
                
        else:
            AtoC.append(0)
            CtoA.append(0)
                #print (processData)
        AtoC.pop(0)
        CtoA.pop(0)
        Acon.pop(0)
        Ccon.pop(0)
        Acon.append(x1)
        Ccon.append(x3/5)
    Eover=int(Eover)
    Ebasic=int(Ebasic)
    Echange=int(Echange)
#    Etotal = Eover + Ebasic + Echange
#    print (Eover, Ebasic , Echange)
    return Ebasic+Eover+Echange+EbasicChange

# In[110]:run the result
    

#    
#    print("answer_length")
contract_length = stratages
for P, lenItem in enumerate(contract_length):
    lb = []
    ub = []
    for i in range(contract_length[P]):
        lb+=lower_bound
        ub+=uper_bound
    args=Y, price, Z
    xopt, fopt = pso(weight, lb, ub, args=args,maxiter=100)
    np.set_printoptions(formatter={'float_kind':'{:f}'.format})
    TS= np.around(xopt,decimals=0)
    b = []
    c = []
    reshapeSize = int(len(TS)/4)
    b = TS.reshape([reshapeSize, 4]).tolist()
    bTmp = copy.deepcopy(b)
    for n in bTmp:
        n.append(P)
    tmpDF= pd.DataFrame(bTmp, columns=contracts.columns.tolist())
    contracts = contracts.append(tmpDF, ignore_index=True)
    solSize = len(b)
    repTimes = int(Contract_Distance/solSize)
    for sol in b:
        c+=sol*repTimes
    print (b)
    def union(x):
         monthLen=int(len(x)/4)
         Ebasic = 0
         Eover = 0
         Echange = 0
         Etotal = 0
         EbasicChange=0
         zWhole =Z['z'].values
         descIdx=(np.array(range(24))+1)*-1
                  # preProcess - put this part outside the month loop
         Acon = Z.iloc[Z.shape[0]-12:, 0].tolist()
         Ccon = (Z.iloc[Z.shape[0]-12:, 2]/5).tolist()
         
         AtoC = [0]
         CtoA = [0]
         for idx in range(11):
             curIdx = idx
             nxtIdx = idx+1
             diffA = Acon[nxtIdx]-Acon[curIdx]
             diffC = Ccon[nxtIdx]-Ccon[curIdx]
             if(diffA*diffC < 0):
                 val = min(abs(diffA), abs(diffC))
                 if(diffA<0):
                     updateList(CtoA, AtoC, val)
                 else:
                     updateList(AtoC, CtoA, val)
             else:
                 AtoC.append(0)
                 CtoA.append(0)
         for monthIdx in range(monthLen):
             x1, x2, x3, x4 = x[monthIdx*4: (monthIdx*4)+4]
             dsol1=x1
             dsol2=x2+x1
             dsol3=x2+x1+x3
             dsol4=x2+x1+x3+x4
             refPrice1, refPrice2, refPrice3, refPrice4 = price[monthIdx,:]
             pastUsage1, pastUsage2, pastUsage3, pastUsage4 = Y[monthIdx,:]
             Ebasic+=(refPrice1*sp*x1)+(refPrice2*sp*x2)+(refPrice3*sp*max(((x3+x4)-(0.5*(x1+x2))),0))
#             if (Power_type == 'a' and Backup_power == 'b'):
#                 Ebasic+=(refPrice1*x1)+(refPrice2*x2)+(refPrice3*max(((x3+x4)-(0.5*(x1+x2))),0))
#             elif(Power_type == 'b' and Backup_power == 'a'):
#                 Ebasic+=math.ceil((refPrice1*x1*1.15*0.98)+(refPrice2*x2*1.15*0.98)+(refPrice3*1.15*0.98*max(((x3+x4)-(0.5*(x1+x2))),0)))
#             elif(Power_type == 'b' and Backup_power == 'b'):
#                 Ebasic+=math.ceil((refPrice1*x1*1.15)+(refPrice2*x2*1.15)+(refPrice3*1.15*max(((x3+x4)-(0.5*(x1+x2))),0)))
             #over Rule1
             extremeHold=dsol1*1.1
             basicOver=max(min(extremeHold, pastUsage1)-dsol1, 0)
             extremeOver=max(0, pastUsage1-extremeHold)
             Eover+=2*refPrice1*basicOver
             Eover+=3*refPrice1*extremeOver
             #Over Rule2
             extremeHold=dsol2*1.1+max(pastUsage1-dsol1, 0)
             basicOver = 0
             if ((pastUsage2-dsol2)-max(pastUsage1-dsol1, 0)) <= 0.1*dsol2 and ((pastUsage2-dsol2)-max(pastUsage1-dsol1, 0))>0:
                 basicOver = ((pastUsage2-dsol2)-max(pastUsage1-dsol1, 0))
                 extremeOver=max(0, pastUsage2-extremeHold)
                 basicOver = max(basicOver,0)
             elif((pastUsage2-dsol2)-max(pastUsage1-dsol1, 0)) > 0.1*dsol2:
                 basicOver = 0.1*dsol2
                 extremeOver=max(0, pastUsage2-extremeHold)
             else:
                 basicOver = 0
                 extremeOver = 0
             Eover+=2*refPrice2*basicOver
             Eover+=3*refPrice2*extremeOver
             #Over Rule3
             extremeHold = dsol3*1.1+max(pastUsage1-dsol1, pastUsage2-dsol2, 0)
             if((pastUsage3-dsol3)-max(pastUsage1-dsol1, pastUsage2-dsol2, 0))<=0.1*dsol3 and ((pastUsage3-dsol3)-max(pastUsage1-dsol1, pastUsage2-dsol2, 0))>0:
                 basicOver = ((pastUsage3-dsol3)-max(pastUsage1-dsol1, pastUsage2-dsol2, 0))
                 extremeOver=max(0, pastUsage3-extremeHold)
                 basicOver = max(basicOver,0)
             elif((pastUsage3-dsol3)-max(pastUsage1-dsol1, pastUsage2-dsol2, 0))>0.1*dsol3:
                 basicOver = 0.1*dsol3
                 extremeOver=max(0, pastUsage3-extremeHold)
             else:
                 basicOver = 0
                 extremeOver = 0
             Eover+=2*refPrice3*basicOver
             Eover+=3*refPrice3*extremeOver
             #Over Rule4
             extremeHold = dsol4*1.1+max(pastUsage1-dsol1, pastUsage2-dsol2, pastUsage3-dsol3, 0)
             if((pastUsage4-dsol4)-max(pastUsage1-dsol1, pastUsage2-dsol2, pastUsage3-dsol3, 0))<=0.1*dsol4 and ((pastUsage4-dsol4)-max(pastUsage1-dsol1, pastUsage2-dsol2, pastUsage3-dsol3, 0))>0:
                 basicOver = ((pastUsage4-dsol4)-max(pastUsage1-dsol1, pastUsage2-dsol2, pastUsage3-dsol3, 0))
                 extremeOver=max(0, pastUsage4-extremeHold)
                 basicOver = max(basicOver,0)
             elif((pastUsage4-dsol4)-max(pastUsage1-dsol1, pastUsage2-dsol2, pastUsage3-dsol3, 0))>0.1*dsol4:
                 basicOver = 0.1*dsol4
                 extremeOver=max(0, pastUsage4-extremeHold)
             else:
                 basicOver = 0
                 extremeOver = 0
             Eover+=2*refPrice4*basicOver
             Eover+=3*refPrice4*extremeOver
     #         Echange
             zStar=max(zWhole[len(zWhole)-24:len(zWhole)])
             z= 1*x1+0.75*x2+0.2*x3+0.2*x4
            
             if(z>zWhole[-1] and z<=zStar):
                 diff=z-zWhole[-1]
                 curLevel=zWhole[-1]
                 qtyList=[]
                 idxList=[]
                 for idxDiff, zIdx in enumerate(descIdx):
                     subDiff=max(zWhole[zIdx]-curLevel, 0)
                     if (subDiff > diff):
                         qtyList.append(diff)
                         diff-=diff
                         idxList.append(idxDiff)
                     elif(subDiff> 0):
                         diff-=subDiff
                         qtyList.append(subDiff)
                         idxList.append(idxDiff)
                         curLevel=zWhole[zIdx]
                 Echange += min(Maintenance_fee*np.sum(np.array(idxList)*np.array(qtyList)),Expansion_fee*0.5*(z-zWhole[-1]))                 
             elif(z>zStar):
                 diff=zStar-zWhole[-1]
                 curLevel=zWhole[-1]
                 qtyList=[]
                 idxList=[]
                 for idxDiff, zIdx in enumerate(descIdx):
                     subDiff=max(zWhole[zIdx]-curLevel, 0)
                     if (subDiff > diff):
                         diff-=diff
                         qtyList.append(diff)
                         idxList.append(idxDiff)
                     elif(subDiff> 0):
                         diff-=subDiff
                         qtyList.append(subDiff)
                         idxList.append(idxDiff)
                         curLevel=subDiff
                 Echange += min(Maintenance_fee*np.sum(np.array(idxList)*np.array(qtyList)),Expansion_fee*0.5*(zStar-zWhole[-1]))+Expansion_fee*(z-zStar)
             #update zWhole
             
             zWhole = np.concatenate([zWhole, [z]])
                      #        #Ebasicchange
             diffA = x1 - Acon[-1]
             diffC = (x3/5) - Ccon[-1]
             if(diffA*diffC < 0):
                 val = min(abs(diffA), abs(diffC))
                 if(diffA<0):
                     updateList(CtoA, AtoC, val)
                 else:
                     processData = updateList(AtoC, CtoA, val)
                     #計算費用
#                     print (processData)
                     for rsltKey,rsltVal in processData.items():
                         EbasicChange+=rsltKey*rsltVal*refPrice1
                     
             else:
                 AtoC.append(0)
                 CtoA.append(0)
             AtoC.pop(0)
             CtoA.pop(0)
             Acon.pop(0)
             Ccon.pop(0)
             Acon.append(x1)
             Ccon.append(x3/5)
         Eover=int(Eover)
         Ebasic=int(Ebasic)
         Echange=int(Echange)
         Etotal = Eover + Ebasic+ Echange + EbasicChange
    #     print (Ebasic , Eover, Echange)
         result['基本電費'][P] = Ebasic  
         result['超約罰金'][P] = Eover  
         result['線路補助費'][P] = Echange+ EbasicChange
         result['總電費'][P] = Etotal
         return Echange+Ebasic+Eover+ EbasicChange
    union(c)
#contracts['solIdx'] = contracts['solIdx']+1
print("輸出檔案中....")

# In[110]:輸出檔案

Corresponding_cycle = []
Contract_cycle = []
for idxx,value in enumerate(stratages):
    D = [int(Contract_Distance/value)]
    Contract_cycle += D
    Corresponding_cycle+=D*int(value)
    D=[]
# In[110]:輸出檔案
contracts['更換對應契約週期(月)']=Corresponding_cycle
# In[110]:輸出檔案
result=result.dropna(axis=0,how='all')  
result['更換契約週期(月)']=Contract_cycle

# In[110]:輸出檔案

res = pd.concat([result,contracts,B],axis=1)
res.to_csv(Result_name +'.csv',index = 0,encoding='utf_8_sig')
print("輸出完成")
input()


# In[110]:輸出檔案

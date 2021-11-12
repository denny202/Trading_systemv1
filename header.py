import ta
import talib
import numpy as np
RSI_PERIOD = 14
RSI_FIFTY = 50





def texty(file,*args):
    file.write(args)
    file.write(args)
    file.write(args)
    nl='/n'
    file.write(nl)
    print('Text saved')


#append arrays 
def array_closes(lenght_s,array_closes,kklines):
  for x in range (0,lenght_s):
    hourly_closes = kklines[x][4]
    array_closes.append(float(hourly_closes))
  return (array_closes)
#a numpy array
def numpyzzalo(arrayizalo):
    numpi=np.array(arrayizalo)
    return(numpi)



def mytime(millisec,array,candle):
    roi=False
    sec=millisec/1000
    currentsec= round(sec%60)
    tmin= sec/60
    currentmin=round(tmin%60)
    th=tmin/60
    currenthour=th%24
    print(currenthour," : ",currentmin,'still computing' )
    if currentmin==60 or currentmin==15 or currentmin==30 or currentmin==45:
       array.append(float(candle))
       array.pop(0)
       print("~~~~~~~i've appended a 15min~~~~~~~~~") 
    return(currentmin)         



def my_rsi (array):
    rsi_1 = talib.RSI(array,RSI_PERIOD)
    return rsi_1

def my_ema (array,ema):
    ema_1 = talib.EMA(array, timeperiod=ema)
    return ema_1


def price_minimum(price):
      percentage_min=price*0.0316
      min_earning = round (price + percentage_min,3)
      return  min_earning

def price_low(price):
      percentage_min=price*0.002
      min_earning = round (price - percentage_min,3)
      return  min_earning
  
  
'''
plt.subplot(3,1,1)
plt.plot(closes_min_1)
plt.subplot(3,1,2)
plt.plot(macd)
plt.plot(macdsignal)
plt.subplot(3,1,3)
plt.plot(rsi)

#plt.hist2d(macdhist)
plt.show()
'''
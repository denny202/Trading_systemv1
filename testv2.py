import websocket,json,requests,pprint
import math
from binance.client import Client
from binance.enums import *
import keyscopia
import numpy as np
import talib 
import pandas as pd
import matplotlib.pyplot as plt
import ta
import os
from datetime import datetime
#import defy 
from header import array_closes,mytime,numpyzzalo,my_ema,my_rsi,texty
#import botkey
from telegram.ext import *
import responses as rr
import time



RSI_PERIOD = 14
RSI_FIFTY = 50
trade_quantity = 7
trade_symbol = 'DOTUSDT'
SOCKET_1 ='wss://stream.binance.com:9443/ws/dotusdt@kline_1m'
#client 
b_client = Client(api_key=keyscopia.Akey
                , api_secret=keyscopia.Asec)


usdt_balance = b_client.get_asset_balance(asset='USDT')
balance_usd = round(float(usdt_balance['free']),1)



#array closes 
all_closes_1=[]
all_closes_15=[]
COUNT = 0
#historical data 
######################################################################
#position size
def order(symbol,side,order_type,quantity):
    try:
        ('print sending order')
        order=b_client.create_order(symbol=symbol,
                                    side=side,
                                    type=order_type,
                                    quantity=quantity,
                                    )
        print('order info : ',order)
    except Exception as e:
        print('Order 404 failed order - {}'.format(e))
        return False
    return (True,order)

def orderlimit(symbol,side,order_type,quantity,price_order):
    try:
        ('print sending order')
        orderlim=b_client.create_order(symbol=symbol,
                                    side=side,
                                    type=order_type,
                                    timeInForce=TIME_IN_FORCE_GTC,
                                    quantity=quantity,
                                    price=price_order)
        print('order info : ',orderlim)
        ory=str(orderlim)
    except Exception as e:
        print('Order 404 failed order - {}'.format(e))
        return False
    
    return (ory)

def OCO_order(symbol,side,order_type,quantity,stop_lossy,price_order):
    try:
        ('sending oco order')
        ocoorder = b_client.create_oco_order(
        symbol=symbol,
        side=side,
        stopLimitTimeInForce=TIME_IN_FORCE_GTC,
        quantity=quantity,
        stopPrice=stop_lossy,
        price=price_order)
        print('order info : ',ocoorder)
    except Exception as e:
        print('Order 404 failed order - {}'.format(e))
        return False
    
    return True


 
#def prices_candles():
############################################################################################################
klines = b_client.get_historical_klines('DOTUSDT', Client.KLINE_INTERVAL_1MINUTE, '4 hour ago UTC')
klines_15 = b_client.get_historical_klines('DOTUSDT', Client.KLINE_INTERVAL_15MINUTE, '3 days ago UTC')

#lenght closes
lenght1 = len(klines)
lenght15 =len(klines_15)

#check position
im_in_position = False
order_sold=False

#position sizing

#array not numpizzato    
closes_min_1 = array_closes(lenght1,all_closes_1,klines)
closes_min_15 = array_closes(lenght15,all_closes_15,klines_15)

last_bit=round(closes_min_1[-1])
trade_quantity=math.floor(balance_usd/last_bit)
print(trade_quantity," " , last_bit)

def on_open(ws):
        
    print('connection established')

def on_close(ws):
    
    print('closed connection')
     
     
def on_message(ws,message): 
    
     global all_closes_15
     global all_closes_1
     global im_in_position
     global order_sold
     global trade_quantity
     #global balance
     global closes_min_1
     global closes_min_15
     global RSI_PERIOD
     kline_stream =[]
     position = False
     last=' last close is \n '
     sell_text = ' i sold at  '
     buy_text = ' i bought at  '
     newline = ' \n ' 
     
    
     
     
     json_msg = json.loads(message)
    
     #GET CANDLE
     candle = json_msg['k']
     is_candle_closed = candle['x'] 
     close = candle['c']
     high = candle['h']
     low = candle['l']
     timy = candle['T']
     
     #BALANCES
   
     coin_balance = b_client.get_asset_balance(asset='DOT')
     balance_coin = float(coin_balance['free'])
     
     
     all_orders=b_client.get_all_orders(symbol=trade_symbol,limit=20)
     lenn=len(all_orders)
     
     
     #take stream candle close and append it to all
     if balance_coin > 2 :
         im_in_position=True
         
     if is_candle_closed:
        ipiu=mytime(timy,closes_min_15,close)
        ipiu;
        
        
        print('********START*********')
        print('candle closed at {} {} Time : {}'.format(close,ipiu,timy))
       # print (' local : ', localtime)
        print('_______________________________')
        #take stream candle close and append it to all
        closes_min_1.append(float(close))
        closes_min_1.pop(0)
    
        #trasform it to numpy   
        npi_1=numpyzzalo(closes_min_1) 
        npi_15=numpyzzalo(closes_min_15)
        #count 15 min chart 
 
#INDICATORS 1 min        
        macd_1, macdsignal_1, macdhist_1=talib.MACD(npi_1,12,26,9)
             # slowk, slowd = talib.STOCH(high, low, close, fastk_period=5, slowk_period=3, slowk_matype=0, slowd_period=3, slowd_matype=0)
        rsi_1m=my_rsi(npi_1)
        ema_1m_50=my_ema(npi_1,50)
        ema_1m_200=my_ema(npi_1,200)

#INDICATORS 15 min
        macd_15, macdsignal_15, macdhist_15=talib.MACD(npi_15,12,26,9)
        rsi_15m=my_rsi(npi_15)
        ema_15m_34=my_ema(npi_15,34)
        ema_15m_200=my_ema(npi_15,200)
        
        
          
#at 15min append close candle 

    #take the last indicator from the array -1  either numpy or float
    #normal float cuz logic order does not work with np
        last_rsi_1 = np.around(rsi_1m[-1],4)
        normal_rsi_1=float(last_rsi_1) 
    #1   
        last_shortema_1 = np.around(ema_1m_50[-1],4)
        normal_sema_1=float(last_shortema_1)
        
        last_longema_1 = np.around(ema_1m_200[-1],4)
        normal_lema_1=float(last_longema_1)
        
        last_macd_1=np.around(macd_1[-1],4)
        normal_macd_1=float(last_macd_1)
        
        last_signal_1=np.around(macdsignal_1[-1],4) 
        normal_macd_1=float(last_macd_1)
    #15 RSI
        last_rsi_15 = np.around(rsi_15m[-1] ,4)
        normal_rsi_15=float(last_rsi_15)
        ######
        l2_rsi_15 = np.around(rsi_15m[-3],4)
        l2_rsi_15=float(l2_rsi_15)
        
    #15 SHORT EXPONENTIAL MOVING AVERAGE  34  
        last_shortema_15 = np.around(ema_15m_34[-1],4)
        normal_sema_15=float(last_shortema_15)
        ######
        l2_shortema_15 = np.around(ema_15m_34[-3],4)
        l2_sema_15=float(l2_shortema_15)
        
    #15 LAST EXPONENTIAL MOVING AVERAGE  200    
        last_longema_15 = np.around(ema_15m_200[-1],4)
        normal_lema_15=float(last_longema_15)
        ######
        l2_longema_15 = np.around(ema_15m_200[-3],4)
        l2_lema_15=float(l2_longema_15)  
        
    #15 MACD      
        last_macd_15=np.around(macd_15[-1],4)
        last_signal_15=np.around(macdsignal_15[-1],4)
    
        normal_macd_15=float(last_macd_15)
        normal_signal_15=float(last_signal_15)



        
        
        open_orders = b_client.get_open_orders(symbol=trade_symbol)
      
        print('=======================================')
        print('          TIMEFRAMES          15 | 01        Balance : {} coin {} '.format(balance_usd,balance_coin))
        print('---------------------------------------')
        print('|||||the current  rsi is {} | {}'.format(last_rsi_15,last_rsi_1))
        print('|||||the current SEMA is {} | {}'.format(last_shortema_15,last_shortema_1))
        print('|||||the current LEMA is {} | {}'.format(last_longema_15,last_longema_1))
        print('|||||the current Macd is {} | {}'.format(last_macd_15,last_macd_1))
        print('||||the current signal is {} | {}'.format(last_signal_15,last_signal_1))
        print('---------------------------------------- My position :', im_in_position)
        print(' ')
        print('total order executed {}'.format(len(all_orders)),'| last 15M close {}'.format(closes_min_15[-1]))
        print('***************************END*************************************')
        print(' ')
        
     
#OPEN FILE 
        file = open('pricev1.txt','a')
    
    
    
    

#FULL LOGIC

        if normal_sema_15 > normal_lema_15 and l2_sema_15 < l2_lema_15: 
            
            #if balance_usd < 20: 
            print('Short ema just crossed over ')
            buy_order_ema =orderlimit(trade_symbol,SIDE_BUY,ORDER_TYPE_LIMIT,trade_quantity,close)
            im_in_position=True
            first_text='order 1st condition buy '
            file.write(first_text)
            file.write(buy_order_ema)
            file.write(newline)
            
           
            '''if stochastic goes above 91 sell orders 
            im in position false after sell '''
            
            if normal_rsi_15 > 69:
                #guadagno=price_minimum(close)
                sell_order_ema=orderlimit(trade_symbol,SIDE_SELL,ORDER_TYPE_LIMIT,trade_quantity,close)
                im_in_position=False 
                firsts_text='order 1st condition sell '
                file.write(firsts_text)
                file.write(sell_order_ema)
                file.write(newline)

#2nd PART         
        if normal_sema_15 > normal_lema_15 and normal_rsi_15 < 55  and l2_rsi_15 < normal_rsi_15:
            print('condition for uptrend are met')
    
            
            if im_in_position:
                print(' but im already in! ',im_in_position)
                        
            else:
                print('i m buying YOLO at = {}'.format(close))
                all_condition_buy=orderlimit(trade_symbol,SIDE_BUY,ORDER_TYPE_LIMIT,trade_quantity,close) 
                sec_text_buy='second condition buy '
                file.write(sec_text_buy)
                file.write(all_condition_buy)
                file.write(newline)
                im_in_position=True         
                print('---------------')
                print('i bought my position: ',im_in_position)
                
                
                ###selling order
                if normal_rsi_15 > 69:
                    #guadagno=price_minimum(close)
                    print('1st normal rsi above ')
                    sell_order=orderlimit(trade_symbol,SIDE_SELL,ORDER_TYPE_LIMIT,trade_quantity,close)
                    rsi_text='selling rsi above high '
                    file.write(rsi_text)
                    file.write(sell_order)
                    file.write(newline)
 #                  
                    #check open orders
                   
                    im_in_position=False     
                        
                    print('i sold Actual position: ',im_in_position)
        if normal_sema_15 < normal_lema_15:
            
            if balance_coin == 0:
                print('NOT ENOUGH COINS')
            else:
                print('sema < lema are above ')
               # lowp=price_low(close)
                sell_order=orderlimit(trade_symbol,SIDE_SELL,ORDER_TYPE_LIMIT,trade_quantity,close)
                #print(sell_order)
                downtrend_text="downtrend selling "
                file.write(downtrend_text)
                file.write(sell_order)
                file.write(newline)
               
                im_in_position=False
            #             
        if normal_rsi_15 > 69:
                #guadagno=price_minimum(close)
                rss= '2nd normal rsi above '
                print(rss)
                sell_order_ema=orderlimit(trade_symbol,SIDE_SELL,ORDER_TYPE_LIMIT,trade_quantity,close)
                file.write(rss)
                file.write(sell_order_ema)
                file.write(newline)
                im_in_position=False               
       
          ################################TELEGRAM BOT ##################################     
     file.close()
##################################################################################  
ws = websocket.WebSocketApp(SOCKET_1,on_open=on_open,on_close=on_close,on_message=on_message)
ws.run_forever()
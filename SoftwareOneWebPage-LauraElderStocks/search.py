import cbpro
print('cbpro imported')
import time
print('time imported')
import os
print('os imported')
import numpy as np
print('numpy imported')
import sys, select, os
print('sys, select, os imported')
import matplotlib.pyplot as plt
print('matplotlib.pyplot as plt imported')
import matplotlib.animation as animation
print('matplotlib.pyplot as animation imported') 
import pandas as pd
print('Pandas as PD imported')

plt.ion()

public_client = cbpro.PublicClient() #pulls data from CBpro

print('')
print(public_client.get_time())

#pulls data from Coinbase API database
btc_data = public_client.get_product_24hr_stats('BTC-USD')
eth_data = public_client.get_product_24hr_stats('ETH-USD')
ada_data = public_client.get_product_24hr_stats('ADA-USD')

count = 0 #establish variables for infinite while loop 
index = 0 #index variable created to calculate time of program run
time_delay = 60 #in seconds, determines looping speed 
mva = 13; # add +1 for appropriate indexing

#create first set of lists for data collection
btc_last_list = [float(btc_data['last'])]
eth_last_list = [float(eth_data['last'])]
ada_last_list = [float(ada_data['last'])]
time_array = [0]

print('Bitcoin: ' + str(btc_data['last']))
print('Ether: ' + str(eth_data['last']))
print('ADA: ' + str(ada_data['last']))
print('')

load_timer = 1

while load_timer <= time_delay:
    
     time.sleep(1)
     percent_loaded = load_timer / time_delay * 100
     print(str(int(percent_loaded)) + "% ", end = "")
     load_timer = load_timer + 1

while count == 0: 

    print('') 
    #pulls new round of data for while loop collection 
    iso_time = public_client.get_time()
    btc_data = public_client.get_product_24hr_stats('BTC-USD')
    eth_data = public_client.get_product_24hr_stats('ETH-USD')
    ada_data = public_client.get_product_24hr_stats('ADA-USD')
    time_run = (index * time_delay + time_delay) / 60

    btc_data_last = float(btc_data['last'])
    eth_data_last = float(eth_data['last'])
    ada_data_last = float(ada_data['last'])
    time_array.append(time_run) 

    #Calculate change in price from based on time delay setting
    btc_last_list.append(btc_data_last)
    btc_change = (btc_last_list[index + 1] - btc_last_list[index]) / btc_last_list[index] * 100
    
    btc_mvadata = np.array(btc_last_list) #this sequence calculates moving average using numpy and pandas functions
    d = pd.Series(btc_mvadata)
    btc_mva = d.rolling(mva).mean() #reference MVA variable to determine count

    eth_last_list.append(eth_data_last)
    eth_change = (eth_last_list[index + 1] - eth_last_list[index]) / eth_last_list[index] * 100
    
    eth_mvadata = np.array(eth_last_list)
    d = pd.Series(eth_mvadata)
    eth_mva = d.rolling(mva).mean()

    ada_last_list.append(ada_data_last)
    ada_change = (ada_last_list[index + 1] - ada_last_list[index]) / ada_last_list[index] * 100
    
    ada_mvadata = np.array(ada_last_list)
    d = pd.Series(ada_mvadata)
    ada_mva = d.rolling(mva).mean()

    #display outputs of data collected and calculated
    print(iso_time['iso'])
    print('Bitcoin: ' + str(btc_data['last']) + ' Price %: ' + str(btc_change))
    print('Ether: ' + str(eth_data['last']) + ' Price %: ' + str(eth_change))
    print('ADA: ' + str(ada_data['last']) + ' Price %: ' + str(ada_change))
    print('')
    print('Total time run: ' + str(time_run) + ' minutes')
    print('')

    plt.close('all')
    
   
    fig = plt.figure()
    gs = fig.add_gridspec(3, hspace=0)
    axs = gs.subplots(sharex=True)
    fig.suptitle('Select Crypto Values: ' + str(time_run) + ' mins')
    
    axs[0].plot(time_array, btc_last_list, time_array, btc_mva)
    axs[0].set_title('BTC')
    axs[0].set_xlabel('time')
    
    axs[1].plot(time_array, eth_last_list, time_array, eth_mva)
    axs[1].set_title('ETH')
    axs[1].set_xlabel('time')
    
    axs[2].plot(time_array, ada_last_list, time_array, ada_mva)
    axs[2].set_title('ADA')
    axs[2].set_xlabel('time')
    
    plt.show() #updates plot in console while looping
     
    index = index + 1
    
    load_timer = 1
    print('')
    
    while load_timer <= time_delay:
        
        time.sleep(1)
        percent_loaded = load_timer / time_delay * 100
        print(str(int(percent_loaded)) + "% ", end = "")
        load_timer = load_timer + 1

    print('')
  

from flask import Flask, request, render_template, session, redirect
import numpy as np
import pandas as pd


from web3 import Web3
import json

import plotly
import plotly.express as px


import time
from processblock import process_block





#connects to external node
w3 = Web3(Web3.HTTPProvider('https://eth.llamarpc.com'))
w3.is_connected()

#it is preffered to be connected to a local node, in that case,  ignore line 19 and 20, and use the two lines below with the path to node running on your computer)
#w3 = Web3(Web3.IPCProvider('your_pathway_to_the_node'))
#w3.is_connected()




def toDict(dictToParse):
    # convert any 'AttributeDict' type found to 'dict'
    parsedDict = dict(dictToParse)
    for key, val in parsedDict.items():
        # check for nested dict structures to iterate through
        if  'dict' in str(type(val)).lower():
            parsedDict[key] = toDict(val)
        # convert 'HexBytes' type to 'str'
        elif 'HexBytes' in str(type(val)):
            parsedDict[key] = val.hex()
    return parsedDict


#a function that takes as an input the number of blocks that you want the analysis to be done backwards from the current/latest block and saves all needed/useful values into a dataframe.

def block_to_DF(number_of_blocks):
    latest_block = w3.eth.get_block('latest')
    latest_block_number = latest_block["number"]
    first_block_number = latest_block_number - number_of_blocks
    blocks_to_json = []
    for i in range(first_block_number,latest_block_number+1):
        block_to_json = toDict(w3.eth.get_block(i))
        blocks_to_json.append(block_to_json)
    my_frame = pd.DataFrame(blocks_to_json)
    my_frame['tx_number'] = my_frame.transactions.apply(lambda x: len(x))
    my_frame = my_frame[['number',"hash", 'tx_number',"gasUsed","miner"]]
    return(my_frame)







app = Flask(__name__)


@app.route('/')
def mainHTML():
    return render_template("index_main.html")

@app.route('/aave')
def table():
    df = pd.read_csv('receipts_downloaded.csv',sep = ",") #we may change for receipts.csv but it take time to fill the file with new data, the absolute path is neccecary to be changed to the path where the file is located on your computer
    return render_template('index.html',  tables=[df.to_html(classes='data')], titles=df.columns.values)



@app.route("/plot") 
def plot_html():
    df = block_to_DF(5)
    #df = pd.read_csv('/Users/pavelrezabek/Desktop/last_5_tx.csv',sep = ";")
    df=df.applymap(str)



     
    # Create Bar chart
    fig = px.bar(df, x='miner', y='gasUsed', color='number') #, , barmode='group'
     
    # Create graphJSON
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
     
    # Use render_template to pass graphJSON to html
    return render_template('bar.html', graphJSON=graphJSON)



@app.route("/plot_aave") 
def plot_aave():
    df = pd.read_csv('receipts_downloaded.csv',sep = ",") #we may change for receipts.csv but it take time to fill the file with new data, the absolute path is neccecary to be changed to the path where the file is located on your computer
    #df = pd.read_csv('/Users/pavelrezabek/Desktop/last_5_tx.csv',sep = ";")
    df["time"] = df["time"]-1680037880
    df1 = df[(df["currency"] == "USDC") | (df["currency"] == "USDT")| (df["currency"] == "DAI")| (df["currency"] == "WBTC")]


     
    # Create Bar chart
    fig = px.line(df1, x='time', y='borrowRate',color='currency') 
     
    # Create graphJSON
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
     
    # Use render_template to pass graphJSON to html
    return render_template('bar.html', graphJSON=graphJSON)










@app.route("/download_new_tx") 
def start_the_download():
    #connects to external node
    w3_provider = Web3(Web3.HTTPProvider('https://eth.llamarpc.com'))
    w3_provider.is_connected()
    last_block_num = w3_provider.eth.block_number
                    
    while True:

        start_time = time.time()
        #try and except - to avoid getting error when +1 block is not yet confirmed
        try:   
            latest_block = w3_provider.eth.get_block(last_block_num, full_transactions=True)
            
            process_block(latest_block, w3_provider)

            process_time = time.time() - start_time
            print()
            print("BLOCK", last_block_num)
            print(str(len(latest_block["transactions"])) + " transactions")
            print(str(round(process_time))+ "sec processing time")

            last_block_num += 1
            #sleep time set to minimize calls to external node and to still be able to process block under 10s
            time.sleep(2)

        except:
            print()
            print("BLOCK",last_block_num)
            print("Error API failed")
            print()
            time.sleep(3)






@app.route("/<usr>") # this is just for fun when I load anything different than above specified
def user(usr):
    block_number = int(usr)
    df = block_to_DF(block_number)


    return render_template('index.html',  tables=[df.to_html(classes='data')], titles=df.columns.values)






if __name__ == '__main__':
    app.run()



from flask import Flask, request, render_template, session, redirect
import numpy as np
import pandas as pd

import web3
from web3 import Web3
import json

#connects to external node
w3 = Web3(Web3.HTTPProvider('https://eth.llamarpc.com'))
w3.isConnected()
#w3.eth.get_block(12345)

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



def block_to_DF(number_of_blocks):
    latest_block = w3.eth.get_block("latest")
    latest_block_number = latest_block["number"]
    first_block_number = latest_block_number - number_of_blocks
    blocks_to_json = []
    for i in range(first_block_number,latest_block_number+1):
        block_to_json = toDict(w3.eth.get_block(i))
        blocks_to_json.append(block_to_json)
    my_frame = pd.DataFrame(blocks_to_json)
    my_frame['tx_number'] = my_frame.transactions.apply(lambda x: len(x))
    return(my_frame)
my_frame = block_to_DF(4)







app = Flask(__name__)

df = my_frame


@app.route('/', methods=("POST", "GET"))
def html_table():

    return render_template('index.html',  tables=[df.to_html(classes='data')], titles=df.columns.values)



if __name__ == '__main__':
    app.run()
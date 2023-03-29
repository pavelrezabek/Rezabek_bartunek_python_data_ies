from flask import Flask, request, render_template, session, redirect
import numpy as np
import pandas as pd


from web3 import Web3
import json



import json
import plotly
import plotly.express as px




#connects to external node
w3 = Web3(Web3.HTTPProvider('https://eth.llamarpc.com'))
print(w3.is_connected())






tx_receipt = w3.eth.get_transaction_receipt("0x89fea8c44c56126186182985179d323310fb4df2a0a20454607ee94c9b079968")

data = tx_receipt['logs'][5]['address']

currency = "USDT"
print("Borrowed currency:", currency)
print(data)
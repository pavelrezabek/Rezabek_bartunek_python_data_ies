import time
from web3 import Web3
from hexbytes import HexBytes

def process_block(block_dict, w3_provider):

    for tx_object in block_dict['transactions']:
        # line 9 identifies whether the transactions interacts with AAVE V2 contract
        if tx_object['to'] == '0x7d2768dE32b0b80b7a3454c06BdAc94A69DDc7A9':
            print('AAVE transaction detected in txn index', tx_object['transactionIndex'])
            #below handles when API doesn't want to send transactions
            try:
                tx_receipt = w3_provider.eth.get_transaction_receipt(tx_object['hash'])
            
            except:
                try:
                    tx_receipt = w3_provider.eth.get_transaction_receipt(tx_object['hash'])
                except:
                    try:
                        tx_receipt = w3_provider.eth.get_transaction_receipt(tx_object['hash'])
                    except:
                        print("AGGGGHHHH")
            
            if len(tx_receipt['logs']) < 7:
                print('Not formatted for this type of transaction')
            #identifies the data where all information about aave is (borrow rate, value etc.)
            elif tx_receipt['logs'] != [] and tx_receipt['logs'][6]["topics"][0] == HexBytes('0xc6a898309e823ee50bac64e45ca8adba6690e99e7841c45d754e2a38e9019d9b'):
                data = tx_receipt['logs'][6]['data']

                data_hex = data.hex()
                data_hex_string = str(data_hex)[2:]

                data_list = []
                for index in range(0, int(len(data_hex_string)/64)):
                    hex_num = int(data_hex_string[(0 + index * 64):(64 + index * 64)], 16)
                    data_list.append(hex_num)
                
                print("    Borrow transaction comfirmed")
                borrow_rate = data_list[3] / (10**27)
                borrow_rate_percent = round(borrow_rate * 100, 3)
                print("    BORROW RATE:", borrow_rate)
                print("    BORROW RATE PERCENT:", str(borrow_rate_percent) + "%")

                borrow_rate_mode = data_list[2]
                print("    BORROW RATE MODE:", borrow_rate_mode)

                value = data_list[1]
                
                currency = tx_receipt['logs'][5]['address']
                #hash of currencies to readable names
                if currency == "0x6B175474E89094C44Da98b954EedeAC495271d0F":
                    currency = "DAI"
                if currency == "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48":
                    currency = "USDC"
                    value = value/1000000
                if currency == "0xdAC17F958D2ee523a2206206994597C13D831ec7":
                    currency = "USDT"
                    value = value/1000000
                if currency == "0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599":
                    currency = "WBTC"
                    value = value/100000000
                print("    Borrowed funds:", value)
                print("    Borrowed currency:", currency)
                #saves what we need in csv
                with open("receipt.csv", "a") as f:
                    line = str(round(time.time()/10)*10) + "," + str(tx_receipt['blockNumber']) + "," + str(tx_object['transactionIndex']) + "," + str(tx_object['hash'].hex()) + "," + str(borrow_rate) + "," + str(borrow_rate_mode) + "," + str(value) + "," + str(currency) + "\n"
                    f.write(line)
            elif len(tx_receipt['logs']) < 8:
                print('Not formatted for this type of transaction')
            #handles problem if there is 8 logs in AAVE transactions (happens rarely but happens -> happens when same address already borrowed in the past and the loan is still active)
            elif tx_receipt['logs'] != [] and tx_receipt['logs'][7]["topics"][0] == HexBytes('0xc6a898309e823ee50bac64e45ca8adba6690e99e7841c45d754e2a38e9019d9b'):
                data = tx_receipt['logs'][7]['data']

                data_hex = data.hex()
                data_hex_string = str(data_hex)[2:]

                data_list = []
                for index in range(0, int(len(data_hex_string)/64)):
                    hex_num = int(data_hex_string[(0 + index * 64):(64 + index * 64)], 16)
                    data_list.append(hex_num)
                
                print("    Borrow transaction comfirmed")
                borrow_rate = data_list[3] / (10**27)
                borrow_rate_percent = round(borrow_rate * 100, 3)
                print("    BORROW RATE:", borrow_rate)
                print("    BORROW RATE PERCENT:", str(borrow_rate_percent) + "%")

                borrow_rate_mode = data_list[2]
                print("    BORROW RATE MODE:", borrow_rate_mode)

                value = data_list[1]
                
                currency = tx_receipt['logs'][6]['address']

                if currency == "0x6B175474E89094C44Da98b954EedeAC495271d0F":
                    currency = "DAI"
                if currency == "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48":
                    currency = "USDC"
                    value = value/1000000
                if currency == "0xdAC17F958D2ee523a2206206994597C13D831ec7":
                    currency = "USDT"
                    value = value/1000000
                if currency == "0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599":
                    currency = "WBTC"
                    value = value/100000000
                print("    Borrowed funds:", value)
                print("    Borrowed currency:", currency)

                with open("receipt.csv", "a") as f:
                    line = str(round(time.time()/10)*10) + "," + str(tx_receipt['blockNumber']) + "," + str(tx_object['transactionIndex']) + "," + str(tx_object['hash'].hex()) + "," + str(borrow_rate) + "," + str(borrow_rate_mode) + "," + str(value) + "," + str(currency) + "\n"
                    f.write(line)


                   
            print()

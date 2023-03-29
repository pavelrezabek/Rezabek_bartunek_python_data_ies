import time
from web3 import Web3
from processblock import process_block

#connects to external node
w3_provider = Web3(Web3.HTTPProvider('https://eth.llamarpc.com'))
w3_provider.is_connected()
last_block_num = w3_provider.eth.block_number
                
while True:

    start_time = time.time()

    try:   
        latest_block = w3_provider.eth.get_block(last_block_num, full_transactions=True)
        
        process_block(latest_block, w3_provider)

        process_time = time.time() - start_time
        print()
        print("BLOCK", last_block_num)
        print(str(len(latest_block["transactions"])) + " transactions")
        print(str(round(process_time))+ "sec processing time")

        last_block_num += 1
        time.sleep(1)

    except:
        print()
        print("BLOCK",last_block_num)
        print("Error API failed")
        print()
        time.sleep(3)

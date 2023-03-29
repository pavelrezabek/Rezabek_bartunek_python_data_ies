# Rezabek_bartunek_python_data_ies: AAVE explorer

This program functions as an Ethereum and AAVE explorer on the Ethereum network. To begin, open the terminal in the working directory and start the local flask server, loading the address http://127.0.0.1:5000. The program will connect to a public RPC provider by default, though you can secure a faster connection by connecting to your own node with the instructions found at https://ethereum.org/en/developers/docs/nodes-and-clients/run-a-node/.

At the homepage ("/nothing"), enter the number of blocks you wish to view and submit to see the details. Going to "/aave" will show you the table with AAVE transactions and data from pre-downloaded transactions. If you wish to download the AAVE transactions yourself, go to "/download_new_tx".

Navigate to "/plot" to see a plot of the last 5 blocks and "/plot_aave" to view a plot of interest rates on different tokens from AAVE. To make the program show AAVE data loaded locally, change “receipts_downloaded.csv” to “receipts.csv”; however, this can be time-consuming as AAVE transactions occur approximately every half-hour.
import requests
from solcx import compile_standard, install_solc
import json
from web3 import Web3
import os
from dotenv import load_dotenv

load_dotenv()


install_solc()


with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

# compile our solidity

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
    solc_version="0.6.0",
)

with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

# get the bytecode
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

# get Abi
# abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]
abi = json.loads(
    compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["metadata"]
)["output"]["abi"]

# for connecting to ganache

w3 = Web3(
    Web3.HTTPProvider("https://rinkeby.infura.io/v3/3e108db8d01346af890f4671871fe9b0")
)

chain_id = 4
my_address = "0x9478e1aaf1f41235757cedD6D859AF373d1Fc522"
private_key = os.getenv("PRIVATE_KEY")
# requests.adapters.DEFAULT_RETRIES = 7  # increase retries number
# s = requests.session()
# s.keep_alive = False  # disable keep alive
# s.get(w3)


# create a contract in pyhton
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)


# Get the latest transaction
nonce = w3.eth.getTransactionCount(my_address)
# 1. Build a transaction
# 2. Sign a transaction
# 3. Send a transaction


transaction = SimpleStorage.constructor().buildTransaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": my_address,
        "nonce": nonce,
    }
)


signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)

# Send this signed transaction
print("Deploying Contract")
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print("Deployed!")

# Working with contract, you need
# contract address and contract abi
simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)

# call => simulate making the call and getting a return value, no state change is made
# Transact => Actually makes a state change
print(simple_storage.functions.retrieve().call())
print("updating contract...")
store_transaction = simple_storage.functions.store(15).buildTransaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": my_address,
        "nonce": nonce + 1,
    }
)
signed_store_txn = w3.eth.account.sign_transaction(
    store_transaction, private_key=private_key
)
send_store_tx = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(send_store_tx)
print("Updated!!")
print(simple_storage.functions.retrieve().call())

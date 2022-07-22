from block import Blockchain
from flask import jsonify
from fastapi import FastAPI
import json

app = FastAPI()

blockchain = Blockchain()


@app.get('/mine_block/{data}/{user}/{workT}/{run}')
def mine_block(data,user,workT,run):
   # get the data we need to create a block
   previous_block = blockchain.get_previous_block()
   previous_proof = previous_block['proof']
   proof = blockchain.proof_of_work(previous_proof)
   previous_hash = blockchain.hash(previous_block)


   block = blockchain.create_blockchain(proof, previous_hash,data,user,workT,run)
   response = {'message': 'Block mined!',
               'index': block['index'],
               'timestamp': block['timestamp'],
               'Username':block['Username'],
               'type':block['type'],
               'data':block['data'],
               'workTime':block['workTime'],
               'proof': block['proof'],
               'previous_hash': block['previous_hash']}
   return json.dumps(response)


@app.get('/get_chain')
def get_chain():
   response = {'chain': blockchain.chain,
               'length': len(blockchain.chain)}
   return json.dumps(response)

@app.get('/find_user/{usrname}')
def get_user(usrname):
    response = []
    for data in blockchain.chain:
        if data["Username"]==usrname:
            response.append(data)
    return json.dumps(response)
    
@app.get('/find_type/{type2}')
def get_type(type2):
    response = []
    for data in blockchain.chain:
        if data['type']==type2:
            response.append(data)
    return json.dumps(response)

@app.get('/validate')
def validate():
    return blockchain.is_chain_valid(blockchain.chain)


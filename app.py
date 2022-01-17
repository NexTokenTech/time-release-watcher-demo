import json
from flask import Flask

import requests

from apscheduler.schedulers.background import BackgroundScheduler
from flask_cors import CORS  # comment this on deployment


from dbmodel import *
from model_tools import generate_block, generate_transaction_block
from decrypt_tools import decrypt_msg_solution

import sys
sys.path.append("../Time-Capsule-Watcher/Time-Release-Blockchain")
from crypto.tx_sign import *
from crypto.elgamal import PublicKey, PrivateKey
from crypto.elgamal_util import *
import crypto.elgamal as elgamal

app = Flask(__name__)
CORS(app)  # comment this on deployment


@app.route('/blocks')
def blocks():
    try:
        result = session.query(Block).order_by(Block.height.desc()).all()
        # session.commit()
        tmp_list = []
        for item in result:
            tmp_list.append(item.to_dict())
        return {
            'resultStatus': 'SUCCESS',
            'message': tmp_list
        }
    except exc.SQLAlchemyError as e:
        print('{}'.format(str(e)), 'blocks api')
        return {
            'resultStatus': 'FAIL',
            'message': []
        }


@app.route('/lastBlock', methods=['GET', 'POST'])
def last_block():
    try:
        result = session.query(Block).order_by(Block.height.desc()).first()
        # session.commit()
        if result is not None:
            return {
                'resultStatus': 'SUCCESS',
                'message': result.to_dict()
            }
        else:
            return {
                'resultStatus': 'FAIL',
                'message': {}
            }
    except exc.SQLAlchemyError as e:
        print('{}'.format(str(e)), 'last blocks api')
        return {
            'resultStatus': 'FAIL',
            'message': {}
        }


@app.route('/lastBlocks/<int:block_height>', methods=['GET', 'POST'])
def last_blocks(block_height: int):
    try:
        result = session.query(Block).filter(Block.height > block_height).order_by(Block.height).all()
        # session.commit()
        tmp_list = []
        for item in result:
            tmp_list.append(item.to_dict())
        return {
            'resultStatus': 'SUCCESS',
            'message': tmp_list
        }
    except exc.SQLAlchemyError as e:
        print('{}'.format(str(e)), 'last blocks api')
        return {
            'resultStatus': 'FAIL',
            'message': []
        }


@app.route('/transactions', methods=['GET', 'POST'])
def transactions_predict():
    try:
        result = session.query(Transaction).filter(Transaction.from_address != 'network').order_by(Transaction.release_block_idx.desc()).all()
        # session.commit()
        tmp_list = []
        for item in result:
            tmp_list.append(item.to_dict())
        return {
            'resultStatus': 'SUCCESS',
            'message': tmp_list
        }
    except exc.SQLAlchemyError as e:
        print('{}'.format(str(e)), 'transactions api')
        return {
            'resultStatus': 'FAIL',
            'message': []
        }


@app.route('/lastTransactions/<int:release_block_idx>', methods=['GET', 'POST'])
def last_transactions(release_block_idx: str):
    try:
        result = session.query(Transaction).filter(Transaction.release_block_idx == release_block_idx).all()
        # session.commit()
        if result is not None and len(result) > 0:
            tmp_list = []
            for item in result:
                tmp_list.append(item.to_dict())
            return {
                'resultStatus': 'SUCCESS',
                'message': tmp_list
            }
        else:
            return {
                'resultStatus': 'SUCCESS',
                'message': []
            }
    except exc.SQLAlchemyError as e:
        print('{}'.format(str(e)), 'transactions api')
        return {
            'resultStatus': 'FAIL',
            'message': []
        }


@app.route('/transactions/<string:block_id>', methods=['GET', 'POST'])
def transactions(block_id: str):
    try:
        result = session.query(Transaction).filter(Transaction.relation_block_id == block_id).all()
        # session.commit()
        tmp_list = []
        for item in result:
            tmp_list.append(item.to_dict())
        return {
            'resultStatus': 'SUCCESS',
            'message': tmp_list
        }
    except exc.SQLAlchemyError as e:
        print('{}'.format(str(e)), 'transactions api')
        return {
            'resultStatus': 'FAIL',
            'message': []
        }


@app.route('/sendPredict/content=<string:predict_content>&lock_time=<int:lock_time>', methods=['POST'])
def send_predict(predict_content: str, lock_time: int):
    addr_from = "uWiVRoaGGKjH/WUcDyumsv05g0Y/o2qa1so9vcBMhm1cKwVJlefQ5O45SBEjykJSjwv1NV/qB6I0dnHR+ciF2Q=="
    addr_to = "uWiVRoaGGKjH/WUcDyumsv05g0Y/o2qa1so9vcBMhm1cKwVJlefQ5O45SBEjykJSjwv1NV/qB6I0dnHR+ciF2Q=="
    tx_private_key = "54aa2dbfed1ccf4d8377501a0b26e23b703300397a3f13f4895fc08311fefc73"
    message = predict_content
    lock_time = lock_time
    result = send_transaction(addr_from, tx_private_key, addr_to, 1, message, lock_time)
    return  result


def send_transaction(addr_from, private_key, addr_to, amount, msg=None, lock_time=0):
    """
    Sends your transaction to different nodes. Once any of the nodes manage
    to mine a block, your transaction will be added to the blockchain. Despite
    that, there is a low chance your transaction gets canceled due to other nodes
    having a longer chain. So make sure your transaction is deep into the chain
    before claiming it as approved!

    Args:
        addr_from: send tx from address
        private_key: private key to sign the tx
        addr_to: send tx to address
        amount: amount of token to be sent
        msg: message to be release in the future
        lock_time: time for locking the message before its release

    Returns:

    """
    if len(private_key) == 64:
        # tx ID is omitted instead of using address to query tx data from database
        # for simplification of implementation
        # prepare tx info and signature
        data = {"addr_from": addr_from,
                "addr_to": addr_to,
                "amount": amount,
        }
        signature = sign_ecdsa_data(private_key, data)
        url = 'http://localhost:8080' + '/txion'
        # decode signature bytes into utf-8 string
        data["signature"] = signature.decode()
        headers = {"Content-Type": "application/json"}
        if msg and lock_time > 0:
            # prepare time release encryption
            last_block = session.query(Block).order_by(Block.height.desc()).first()
            # after a number of block, the encrypted message will be released
            block_interval = lock_time // 30

            pubkey_str_list = last_block.public_key.split(", ")
            # print(strlist)
            p = int(pubkey_str_list[2], 16)
            g = int(pubkey_str_list[0], 16)
            h = int(pubkey_str_list[1], 16)
            bit_length = int(pubkey_str_list[3])
            pub_key = PublicKey(p, g, h, bit_length)

            future_pub_key = pub_key
            # derive future public key
            for _ in range(block_interval):
                future_pub_key = elgamal.generate_pub_key(
                    seed=int(future_pub_key.p + future_pub_key.g + future_pub_key.h),
                    bit_length=future_pub_key.bit_length)
            # encrypt time release message
            cipher = elgamal.encrypt(future_pub_key, msg)
            data['release_block_idx'] = last_block.height + block_interval
            data['cipher'] = cipher
        print("~~~~~~~~~~~~~~~~{} {}".format(url, data))
        res = requests.post(url, json=data, headers=headers)
        print(res.text)
        return {
            'resultStatus': 'SUCCESS',
            'message': res.text
        }
    else:
        print("Wrong address or key length! Verify and try again.")
        return {
            'resultStatus': 'SUCCESS',
            'message': "Wrong address or key length! Verify and try again."
        }


@app.route('/')
def hello_world():  # put application's code here
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    cycle_request()
    return 'Hello World!'


def cycle_request():
    # BlockingScheduler
    scheduler = BackgroundScheduler(timezone='Asia/Shanghai')
    scheduler.add_job(job, 'interval', seconds=3)  # Run once every 3S
    scheduler.start()


def job():
    # The scheduled task makes a request every 30s to obtain the latest block
    try:
        results = session.query(func.count(Block.block_id)).scalar()
        # session.commit()
        if results == 0:
            url = "http://localhost:8080/blocks"
            response = requests.get(url).content
            block_list = json.loads(response)
            last_block = block_list[len(block_list) - 1]
            # last_timestamp = last_block["timestamp"]
            add_blocks(block_list=block_list)
        else:
            url = "http://localhost:8080/last"
            response = requests.get(url).content
            block = json.loads(response)
            # last_timestamp = block["timestamp"]
            add_block(block)
    except exc.SQLAlchemyError as e:
        print('{}'.format(str(e)), 'job function')


def add_blocks(block_list: [dict]):
    transaction_list_tmp = []
    for block in block_list:
        block_id = block["id"]
        result = session.query(Block).filter(Block.block_id == block_id).all()
        # session.commit()

        transactions_list = block["transactions"]
        if len(result) > 0:
            print("has same block,will not insert to db again")
        else:
            print("has no same block")
            if transactions_list is not None:
                tx_count = len(transactions_list)
                block_item = generate_block(block, tx_count)
                session.add(block_item)
                session.commit()
                for idx in range(0, len(transactions_list)):
                    tx = transactions_list[idx]
                    if tx["addr_from"] == "network":
                        tx_model = generate_transaction_block(
                            block_id=block_item.block_id,
                            transaction=tx,
                            release_msg=""
                        )
                        session.add(tx_model)
                        session.commit()
                    else:
                        tx["block_id"] = block_item.block_id
                        transaction_list_tmp.append(tx)
            else:
                block_item = generate_block(block, 0)
                session.add(block_item)
                session.commit()
    for transaction in transaction_list_tmp:
        result = session.query(Block).filter(transaction["release_block_idx"] == Block.height).all()
        # session.commit()
        if len(result) > 0:
            block_result = result[0]
            # print("{}~~~~~~~~~~~~~~~~{}".format(block.public_key, transaction["cipher"]))
            plain_text = decrypt_msg_solution(
                pubkey=block_result.public_key,
                solution_str=block_result.solution,
                chiper=transaction["cipher"])
            tx_model = generate_transaction_block(
                block_id=block_result.block_id,
                transaction=transaction,
                release_msg=plain_text
            )
            session.add(tx_model)
            session.commit()
            # print("~~~~~~~~~~~~~~~~{}".format(plain_text))
        else:
            tx_model = generate_transaction_block(
                block_id=transaction["block_id"],
                transaction=transaction,
                release_msg=""
            )
            session.add(tx_model)
            session.commit()


def add_block(block: dict):
    if block["transactions"] is not None:
        transactions_list = block["transactions"]
        tx_count = len(transactions_list)

        block_id = block["id"]
        result = session.query(Block).filter(Block.block_id == block_id).all()
        # session.commit()
        if len(result) > 0:
            print("has same block,will not insert to db again")
        else:
            # print("has no same block")
            # insert new block and transactions to db
            block_item = generate_block(block, tx_count)
            session.add(block_item)
            session.commit()

            for idx in range(0, len(transactions_list)):
                tx = transactions_list[idx]
                print("~~~~~~~~~~~~~~~~~~~~~~{}    {}".format(block_id,tx))
                tx_model = generate_transaction_block(
                    block_id=block_id,
                    transaction=tx,
                    release_msg=""
                )
                # TODO when one transaction has a timerelease range,need another table to restore Array<release_block_idx>
                # tmp_str = "txid_{}_block_height_{}".format(idx, block["height"]).encode("utf8")
                # s = hashlib.sha256()  # Get the hash algorithm.
                # s.update(tmp_str)  # Hash the data.
                # b = s.hexdigest()
                # if tx_model.from_address != "network":
                #     block_height_model = TxBlockHeight(
                #         tx_block_height_id=b,
                #         tx_id=tx_model.tx_id,
                #         block_height=tx["release_block_idx"]
                #     )
                #     session.add(block_height_model)
                session.add(tx_model)
                session.commit()

            # puzzle traverser time release
            transactions_list_need_to_release = session.query(Transaction).filter(
                Transaction.release_block_idx == block["height"]).all()
            # session.commit()
            print("has no same block {}".format(transactions_list_need_to_release))
            if len(transactions_list_need_to_release) > 0:
                for transactions_need_to_release in transactions_list_need_to_release:
                    print("{}~~~~~~~~~~~~~~~~{}".format(block["public_key"], transactions_need_to_release.chiper))
                    plain_text = decrypt_msg_solution(
                        pubkey=block["public_key"],
                        solution_str=block["solution"],
                        chiper=transactions_need_to_release.chiper)
                    print("~~~~~~~~~~~~~~~~{}".format(plain_text))
                    res = session.query(Transaction).filter(
                        Transaction.tx_id == transactions_need_to_release.tx_id).update({"decrypted_msg": plain_text})
                    session.commit()
                    print("result~~~~~~~~~~~~{}".format(res))
            session.commit()


def startup():
    print("-------------------start up---------------------")


if __name__ == '__main__':
    app.run()
    # production env
    # time.sleep(5)
    # startup()


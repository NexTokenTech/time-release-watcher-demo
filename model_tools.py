from dbmodel import Transaction, Block


# generate transaction source data with block_id
def generate_transaction_block(block_id: str, transaction: dict, release_msg: str):
    if block_id == "":
        return Transaction(
            tx_id=transaction["id"],
            relation_block_id=block_id,
            relation_block_height=transaction["block_height"],
            from_address=transaction["addr_from"],
            to_address=transaction["addr_to"],
            version=transaction["version"],
            chiper=transaction["cipher"],
            amount=transaction["amount"],
            release_block_idx=transaction["release_block_idx"],
        )
    else:
        return Transaction(
            tx_id=transaction["id"],
            relation_block_id=block_id,
            relation_block_height=transaction["block_height"],
            from_address=transaction["addr_from"],
            to_address=transaction["addr_to"],
            version=transaction["version"],
            chiper=transaction["cipher"],
            amount=transaction["amount"],
            release_block_idx=transaction["release_block_idx"],
            decrypted_msg=release_msg
        )


# generate block with block dictionary and tx_count
def generate_block(block: dict, tx_count: int):
    return Block(block_id=block["id"],
                 height=block["height"],
                 header_hash=block["header_hash"],
                 pre_block_hash=block["prev_block_hash"],
                 difficulty=block["difficulty"],
                 public_key=block["public_key"],
                 recieve_at=block["timestamp"],
                 tx_count=tx_count,
                 nonce=block["nonce"],
                 solution=block["solution"])

from sqlalchemy import create_engine, func, exc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, BigInteger, String, Float, Text
from client_config import CLIENT_DB_URL

Base = declarative_base()

engine = create_engine(CLIENT_DB_URL, echo=False)
Session = sessionmaker(bind=engine)
session = Session()


class Block(Base):
    __tablename__ = "block"
    block_id = Column(Integer, autoincrement=True, primary_key=True)
    pre_block_hash = Column(String(64))
    header_hash = Column(String(64))
    size = Column(Integer)
    height = Column(BigInteger)
    recieve_at = Column(Float)
    tx_count = Column(Integer)
    nonce = Column(Text)
    difficulty = Column(BigInteger)
    public_key = Column(Text)
    solution = Column(Text)

    def save(self):
        session.add(self)
        session.commit()

    def __str__(self):
        return self.blockid

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Transaction(Base):
    __tablename__ = 'transaction'
    tx_id = Column(String(64), primary_key=True, autoincrement=False)
    relation_block_id = Column(Text)
    relation_block_height = Column(BigInteger)
    create_time = Column(Float)
    chiper = Column(Text)
    decrypted_msg = Column(Text)
    predictor_field = Column(Text)
    relation_predictor_id = Column(Integer)
    from_address = Column(Text)
    to_address = Column(Text)
    amount = Column(BigInteger)
    version = Column(Integer)
    release_block_idx = Column(Integer)

    def save(self):
        session.add(self)
        session.commit()

    def __str__(self):
        return self.txid

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class TxBlockHeight(Base):
    __tablename__ = 'txblockheight'
    tx_block_height_id = Column(Text, primary_key=True, autoincrement=False)
    tx_id = Column(String(64))
    block_height = Column(BigInteger)

    def save(self):
        session.add(self)
        session.commit()

    def __str__(self):
        return self.blockheight

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

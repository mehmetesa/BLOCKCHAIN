import hashlib
import json
import time
from typing import List, Dict, Optional
from datetime import datetime


class Transaction:
    """Transaction sınıfı - Blockchain'deki işlemleri temsil eder"""
    
    def __init__(self, sender: str, receiver: str, amount: float, timestamp: float = None):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.timestamp = timestamp or time.time()
    
    def to_dict(self) -> Dict:
        """Transaction'ı dictionary'ye çevirir"""
        return {
            'sender': self.sender,
            'receiver': self.receiver,
            'amount': self.amount,
            'timestamp': self.timestamp
        }
    
    def __repr__(self):
        return f"Transaction({self.sender} -> {self.receiver}: {self.amount})"


class Block:
    """Block sınıfı - Blockchain'deki blokları temsil eder"""
    
    def __init__(self, index: int, transactions: List[Transaction], previous_hash: str, 
                 timestamp: float = None, nonce: int = 0):
        self.index = index
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.timestamp = timestamp or time.time()
        self.nonce = nonce
        self.hash = self.calculate_hash()
    
    def calculate_hash(self) -> str:
        """Block'un hash değerini hesaplar"""
        block_string = json.dumps({
            'index': self.index,
            'transactions': [tx.to_dict() for tx in self.transactions],
            'previous_hash': self.previous_hash,
            'timestamp': self.timestamp,
            'nonce': self.nonce
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def mine_block(self, difficulty: int):
        """Proof of Work - Block'u mine eder"""
        target = "0" * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
        return self.hash
    
    def to_dict(self) -> Dict:
        """Block'u dictionary'ye çevirir"""
        return {
            'index': self.index,
            'transactions': [tx.to_dict() for tx in self.transactions],
            'previous_hash': self.previous_hash,
            'timestamp': self.timestamp,
            'nonce': self.nonce,
            'hash': self.hash
        }
    
    def __repr__(self):
        return f"Block(Index: {self.index}, Hash: {self.hash[:16]}...)"


class Blockchain:
    """Blockchain sınıfı - Ana blockchain yapısı"""
    
    def __init__(self, difficulty: int = 4):
        self.chain: List[Block] = [self.create_genesis_block()]
        self.pending_transactions: List[Transaction] = []
        self.difficulty = difficulty
        self.mining_reward = 50.0
    
    def create_genesis_block(self) -> Block:
        """Genesis block (ilk blok) oluşturur"""
        genesis_transaction = Transaction("System", "Genesis", 0)
        return Block(0, [genesis_transaction], "0")
    
    def get_latest_block(self) -> Block:
        """Son bloğu döndürür"""
        return self.chain[-1]
    
    def add_transaction(self, transaction: Transaction) -> bool:
        """Bekleyen transaction'lara ekler"""
        if not self.is_valid_transaction(transaction):
            return False
        self.pending_transactions.append(transaction)
        return True
    
    def is_valid_transaction(self, transaction: Transaction) -> bool:
        """Transaction'ın geçerliliğini kontrol eder"""
        if transaction.amount <= 0:
            return False
        if transaction.sender == transaction.receiver:
            return False
        return True
    
    def get_balance(self, address: str) -> float:
        """Bir adresin bakiyesini hesaplar"""
        balance = 0.0
        for block in self.chain:
            for tx in block.transactions:
                if tx.sender == address:
                    balance -= tx.amount
                if tx.receiver == address:
                    balance += tx.amount
        return balance
    
    def mine_pending_transactions(self, mining_reward_address: str) -> Block:
        """Bekleyen transaction'ları mine eder ve yeni blok oluşturur"""
        # Mining reward transaction'ı ekle
        reward_tx = Transaction("System", mining_reward_address, self.mining_reward)
        self.pending_transactions.append(reward_tx)
        
        # Yeni blok oluştur
        new_block = Block(
            len(self.chain),
            self.pending_transactions.copy(),
            self.get_latest_block().hash
        )
        
        # Proof of Work ile mine et
        print(f"Mining block {new_block.index}...")
        start_time = time.time()
        new_block.mine_block(self.difficulty)
        mining_time = time.time() - start_time
        
        print(f"Block mined! Hash: {new_block.hash}")
        print(f"Mining time: {mining_time:.2f} seconds")
        print(f"Nonce: {new_block.nonce}")
        
        # Bloğu chain'e ekle
        self.chain.append(new_block)
        
        # Bekleyen transaction'ları temizle
        self.pending_transactions = []
        
        return new_block
    
    def is_chain_valid(self) -> bool:
        """Blockchain'in geçerliliğini kontrol eder"""
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            
            # Hash kontrolü
            if current_block.hash != current_block.calculate_hash():
                print(f"Block {i} hash is invalid!")
                return False
            
            # Previous hash kontrolü
            if current_block.previous_hash != previous_block.hash:
                print(f"Block {i} previous hash is invalid!")
                return False
            
            # Proof of Work kontrolü
            if current_block.hash[:self.difficulty] != "0" * self.difficulty:
                print(f"Block {i} doesn't have valid proof of work!")
                return False
        
        return True
    
    def to_dict(self) -> Dict:
        """Blockchain'i dictionary'ye çevirir"""
        return {
            'chain': [block.to_dict() for block in self.chain],
            'pending_transactions': [tx.to_dict() for tx in self.pending_transactions],
            'difficulty': self.difficulty,
            'mining_reward': self.mining_reward
        }
    
    def __repr__(self):
        return f"Blockchain(Blocks: {len(self.chain)}, Pending: {len(self.pending_transactions)})"


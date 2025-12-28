#!/usr/bin/env python3
"""
Blockchain CLI Tool
Educational blockchain implementation from scratch.
"""

import json
import sys
from blockchain import Blockchain, Transaction


class BlockchainCLI:
    """Blockchain için komut satırı arayüzü"""
    
    def __init__(self):
        self.blockchain = Blockchain(difficulty=4)
        self.miner_address = "Miner1"
    
    def print_menu(self):
        """Ana menüyü yazdırır"""
        print("\n" + "="*50)
        print("🔗 BLOCKCHAIN CLI TOOL")
        print("="*50)
        print("1. Yeni Transaction Oluştur")
        print("2. Bekleyen Transaction'ları Görüntüle")
        print("3. Block Mine Et")
        print("4. Blockchain'i Görüntüle")
        print("5. Blockchain Geçerliliğini Kontrol Et")
        print("6. Adres Bakiyesi Sorgula")
        print("7. Blockchain İstatistikleri")
        print("8. Blockchain'i JSON'a Aktar")
        print("0. Çıkış")
        print("="*50)
    
    def create_transaction(self):
        """Yeni transaction oluşturur"""
        print("\n--- Yeni Transaction Oluştur ---")
        sender = input("Gönderen adres: ").strip()
        receiver = input("Alıcı adres: ").strip()
        
        try:
            amount = float(input("Miktar: ").strip())
            if amount <= 0:
                print("❌ Miktar 0'dan büyük olmalıdır!")
                return
            
            transaction = Transaction(sender, receiver, amount)
            
            if self.blockchain.add_transaction(transaction):
                print(f"✅ Transaction başarıyla eklendi!")
                print(f"   {sender} -> {receiver}: {amount}")
            else:
                print("❌ Geçersiz transaction!")
        except ValueError:
            print("❌ Geçersiz miktar!")
    
    def view_pending_transactions(self):
        """Bekleyen transaction'ları gösterir"""
        print("\n--- Bekleyen Transaction'lar ---")
        if not self.blockchain.pending_transactions:
            print("Bekleyen transaction yok.")
        else:
            for i, tx in enumerate(self.blockchain.pending_transactions, 1):
                print(f"{i}. {tx.sender} -> {tx.receiver}: {tx.amount}")
    
    def mine_block(self):
        """Yeni blok mine eder"""
        print("\n--- Block Mine Etme ---")
        if not self.blockchain.pending_transactions:
            print("⚠️  Mine edilecek transaction yok!")
            return
        
        print(f"Bekleyen {len(self.blockchain.pending_transactions)} transaction var.")
        confirm = input("Mine etmek istiyor musunuz? (e/h): ").strip().lower()
        
        if confirm == 'e':
            self.blockchain.mine_pending_transactions(self.miner_address)
            print("✅ Block başarıyla mine edildi!")
        else:
            print("Mine işlemi iptal edildi.")
    
    def view_blockchain(self):
        """Blockchain'i görüntüler"""
        print("\n--- Blockchain ---")
        print(f"Toplam Blok Sayısı: {len(self.blockchain.chain)}\n")
        
        for block in self.blockchain.chain:
            print(f"📦 Block #{block.index}")
            print(f"   Hash: {block.hash}")
            print(f"   Previous Hash: {block.previous_hash}")
            print(f"   Nonce: {block.nonce}")
            print(f"   Timestamp: {block.timestamp}")
            print(f"   Transaction Sayısı: {len(block.transactions)}")
            
            if block.transactions:
                print("   Transactions:")
                for tx in block.transactions:
                    print(f"      • {tx.sender} -> {tx.receiver}: {tx.amount}")
            print()
    
    def validate_blockchain(self):
        """Blockchain geçerliliğini kontrol eder"""
        print("\n--- Blockchain Geçerlilik Kontrolü ---")
        if self.blockchain.is_chain_valid():
            print("✅ Blockchain geçerli!")
        else:
            print("❌ Blockchain geçersiz!")
    
    def check_balance(self):
        """Adres bakiyesini sorgular"""
        print("\n--- Bakiye Sorgula ---")
        address = input("Adres: ").strip()
        balance = self.blockchain.get_balance(address)
        print(f"💰 {address} bakiyesi: {balance}")
    
    def show_statistics(self):
        """Blockchain istatistiklerini gösterir"""
        print("\n--- Blockchain İstatistikleri ---")
        print(f"Toplam Blok Sayısı: {len(self.blockchain.chain)}")
        print(f"Bekleyen Transaction: {len(self.blockchain.pending_transactions)}")
        print(f"Mining Zorluğu: {self.blockchain.difficulty}")
        print(f"Mining Ödülü: {self.blockchain.mining_reward}")
        
        total_transactions = sum(len(block.transactions) for block in self.blockchain.chain)
        print(f"Toplam Transaction: {total_transactions}")
        
        if self.blockchain.is_chain_valid():
            print("Durum: ✅ Geçerli")
        else:
            print("Durum: ❌ Geçersiz")
    
    def export_to_json(self):
        """Blockchain'i JSON dosyasına aktarır"""
        print("\n--- Blockchain JSON'a Aktar ---")
        filename = input("Dosya adı (örn: blockchain.json): ").strip()
        if not filename:
            filename = "blockchain.json"
        
        try:
            blockchain_dict = self.blockchain.to_dict()
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(blockchain_dict, f, indent=2, ensure_ascii=False)
            print(f"✅ Blockchain {filename} dosyasına aktarıldı!")
        except Exception as e:
            print(f"❌ Hata: {e}")
    
    def run(self):
        """CLI'yi çalıştırır"""
        print("🚀 Blockchain CLI Tool başlatıldı!")
        print("Educational blockchain implementation from scratch.")
        
        while True:
            self.print_menu()
            choice = input("\nSeçiminiz: ").strip()
            
            if choice == '1':
                self.create_transaction()
            elif choice == '2':
                self.view_pending_transactions()
            elif choice == '3':
                self.mine_block()
            elif choice == '4':
                self.view_blockchain()
            elif choice == '5':
                self.validate_blockchain()
            elif choice == '6':
                self.check_balance()
            elif choice == '7':
                self.show_statistics()
            elif choice == '8':
                self.export_to_json()
            elif choice == '0':
                print("\n👋 Çıkılıyor...")
                break
            else:
                print("❌ Geçersiz seçim!")
            
            input("\nDevam etmek için Enter'a basın...")


if __name__ == "__main__":
    cli = BlockchainCLI()
    try:
        cli.run()
    except KeyboardInterrupt:
        print("\n\n👋 Çıkılıyor...")
        sys.exit(0)


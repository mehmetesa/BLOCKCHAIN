// Blockchain Web Interface
// Educational blockchain implementation from scratch

class BlockchainWebInterface {
    constructor() {
        this.blockchain = {
            chain: [this.createGenesisBlock()],
            pending_transactions: [],
            difficulty: 4,
            mining_reward: 50.0
        };
        this.isMining = false;
        this.init();
    }

    createGenesisBlock() {
        const genesisData = {
            index: 0,
            transactions: [{
                sender: "System",
                receiver: "Genesis",
                amount: 0,
                timestamp: Date.now()
            }],
            previous_hash: "0",
            timestamp: Date.now(),
            nonce: 0
        };
        return {
            ...genesisData,
            hash: this.calculateHashSync(genesisData)
        };
    }

    calculateHashSync(block) {
        const blockString = JSON.stringify(block);
        return this.simpleHash(blockString);
    }

    async calculateHash(block) {
        const blockString = JSON.stringify(block);
        return await this.sha256(blockString);
    }

    simpleHash(message) {
        // Basit hash fonksiyonu (genesis block için)
        let hash = 0;
        for (let i = 0; i < message.length; i++) {
            const char = message.charCodeAt(i);
            hash = ((hash << 5) - hash) + char;
            hash = hash & hash;
        }
        return Math.abs(hash).toString(16).padStart(64, '0');
    }

    async sha256(message) {
        // Web Crypto API kullanarak SHA-256 hash hesaplama
        const msgBuffer = new TextEncoder().encode(message);
        const hashBuffer = await crypto.subtle.digest('SHA-256', msgBuffer);
        const hashArray = Array.from(new Uint8Array(hashBuffer));
        return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
    }

    async init() {
        await this.updateUI();
        this.setupEventListeners();
    }

    setupEventListeners() {
        document.getElementById('transaction-form').addEventListener('submit', (e) => {
            e.preventDefault();
            this.addTransaction();
        });

        document.getElementById('mine-btn').addEventListener('click', () => {
            this.mineBlock();
        });

        document.getElementById('check-balance-btn').addEventListener('click', () => {
            this.checkBalance();
        });
    }

    addTransaction() {
        const sender = document.getElementById('sender').value.trim();
        const receiver = document.getElementById('receiver').value.trim();
        const amount = parseFloat(document.getElementById('amount').value);

        if (!sender || !receiver || !amount || amount <= 0) {
            alert('Lütfen geçerli bilgiler girin!');
            return;
        }

        if (sender === receiver) {
            alert('Gönderen ve alıcı aynı olamaz!');
            return;
        }

        const transaction = {
            sender,
            receiver,
            amount,
            timestamp: Date.now()
        };

        this.blockchain.pending_transactions.push(transaction);
        this.updateUI();
        
        document.getElementById('transaction-form').reset();
        this.showNotification('Transaction başarıyla eklendi!', 'success');
    }

    async mineBlock() {
        if (this.isMining || this.blockchain.pending_transactions.length === 0) {
            return;
        }

        this.isMining = true;
        this.showMiningSimulation();

        // Mining reward transaction ekle
        const rewardTx = {
            sender: "System",
            receiver: "Miner1",
            amount: this.blockchain.mining_reward,
            timestamp: Date.now()
        };
        this.blockchain.pending_transactions.push(rewardTx);

        // Yeni blok oluştur
        const newBlock = {
            index: this.blockchain.chain.length,
            transactions: [...this.blockchain.pending_transactions],
            previous_hash: this.blockchain.chain[this.blockchain.chain.length - 1].hash,
            timestamp: Date.now(),
            nonce: 0
        };

        // Proof of Work
        const target = "0".repeat(this.blockchain.difficulty);
        let attempts = 0;
        const maxAttempts = 10000; // Simülasyon için limit

        while (attempts < maxAttempts) {
            newBlock.nonce++;
            newBlock.hash = await this.calculateHash(newBlock);
            
            if (newBlock.hash.substring(0, this.blockchain.difficulty) === target) {
                break;
            }
            
            attempts++;

            // Progress güncelle
            if (attempts % 100 === 0) {
                const progress = Math.min((attempts / maxAttempts) * 100, 99);
                this.updateMiningProgress(progress, newBlock.nonce);
                await this.sleep(10); // UI'ı güncellemek için
            }
        }

        if (newBlock.hash?.substring(0, this.blockchain.difficulty) === target) {
            this.blockchain.chain.push(newBlock);
            this.blockchain.pending_transactions = [];
            this.hideMiningSimulation();
            this.updateUI();
            this.showNotification('Block başarıyla mine edildi!', 'success');
        } else {
            this.hideMiningSimulation();
            this.showNotification('Mining başarısız oldu. Tekrar deneyin.', 'error');
        }

        this.isMining = false;
    }

    checkBalance() {
        const address = document.getElementById('balance-address').value.trim();
        if (!address) {
            alert('Lütfen bir adres girin!');
            return;
        }

        let balance = 0;
        for (const block of this.blockchain.chain) {
            for (const tx of block.transactions) {
                if (tx.sender === address) {
                    balance -= tx.amount;
                }
                if (tx.receiver === address) {
                    balance += tx.amount;
                }
            }
        }

        const resultDiv = document.getElementById('balance-result');
        resultDiv.innerHTML = `<strong>${address}</strong> bakiyesi: <span style="color: var(--success-color);">${balance.toFixed(2)}</span>`;
    }

    async updateUI() {
        await this.updateStats();
        this.updatePendingTransactions();
        this.updateBlockchain();
    }

    async updateStats() {
        document.getElementById('total-blocks').textContent = this.blockchain.chain.length;
        document.getElementById('pending-txs').textContent = this.blockchain.pending_transactions.length;
        document.getElementById('difficulty').textContent = this.blockchain.difficulty;
        
        const isValid = await this.isChainValid();
        document.getElementById('status').textContent = isValid ? '✅ Geçerli' : '❌ Geçersiz';
        
        const mineBtn = document.getElementById('mine-btn');
        mineBtn.disabled = this.blockchain.pending_transactions.length === 0 || this.isMining;
    }

    updatePendingTransactions() {
        const container = document.getElementById('pending-transactions');
        
        if (this.blockchain.pending_transactions.length === 0) {
            container.innerHTML = '<p class="empty-message">Bekleyen transaction yok</p>';
            return;
        }

        container.innerHTML = this.blockchain.pending_transactions.map((tx, index) => `
            <div class="transaction-item">
                <div class="tx-header">
                    <span><strong>${tx.sender}</strong> → <strong>${tx.receiver}</strong></span>
                    <span class="tx-amount">${tx.amount.toFixed(2)}</span>
                </div>
                <div class="tx-details">Transaction #${index + 1}</div>
            </div>
        `).join('');
    }

    updateBlockchain() {
        const container = document.getElementById('blockchain-view');
        
        if (this.blockchain.chain.length === 0) {
            container.innerHTML = '<p class="empty-message">Blockchain boş</p>';
            return;
        }

        container.innerHTML = this.blockchain.chain.map(block => `
            <div class="block">
                <div class="block-header">
                    <span class="block-index">Block #${block.index}</span>
                    <span class="block-hash">${block.hash?.substring(0, 16)}...</span>
                </div>
                <div class="block-info">
                    <div class="block-info-item">
                        <strong>Previous Hash:</strong><br>
                        <span style="font-family: monospace; font-size: 0.8rem;">${block.previous_hash.substring(0, 16)}...</span>
                    </div>
                    <div class="block-info-item">
                        <strong>Nonce:</strong> ${block.nonce}<br>
                        <strong>Transactions:</strong> ${block.transactions.length}
                    </div>
                </div>
                ${block.transactions.length > 0 ? `
                    <div class="block-transactions">
                        <h4>Transactions:</h4>
                        ${block.transactions.map(tx => `
                            <div class="block-tx-item">
                                ${tx.sender} → ${tx.receiver}: ${tx.amount.toFixed(2)}
                            </div>
                        `).join('')}
                    </div>
                ` : ''}
            </div>
        `).reverse().join(''); // En yeni bloklar üstte
    }

    async isChainValid() {
        for (let i = 1; i < this.blockchain.chain.length; i++) {
            const currentBlock = this.blockchain.chain[i];
            const previousBlock = this.blockchain.chain[i - 1];

            const calculatedHash = await this.calculateHash(currentBlock);
            if (currentBlock.hash !== calculatedHash) {
                return false;
            }

            if (currentBlock.previous_hash !== previousBlock.hash) {
                return false;
            }
        }
        return true;
    }

    showMiningSimulation() {
        document.getElementById('mining-simulation').style.display = 'flex';
        this.updateMiningProgress(0, 0);
    }

    hideMiningSimulation() {
        document.getElementById('mining-simulation').style.display = 'none';
    }

    updateMiningProgress(progress, nonce) {
        document.getElementById('progress-fill').style.width = progress + '%';
        document.getElementById('progress-fill').textContent = Math.round(progress) + '%';
        document.getElementById('mining-status').textContent = `Mining devam ediyor... (${Math.round(progress)}%)`;
        document.getElementById('mining-nonce').textContent = `Nonce: ${nonce}`;
    }

    showNotification(message, type) {
        // Basit bildirim sistemi
        const notification = document.createElement('div');
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 15px 20px;
            background: ${type === 'success' ? '#10b981' : '#ef4444'};
            color: white;
            border-radius: 5px;
            z-index: 2000;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        `;
        notification.textContent = message;
        document.body.appendChild(notification);

        setTimeout(() => {
            notification.remove();
        }, 3000);
    }

    sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
}

// Sayfa yüklendiğinde başlat
document.addEventListener('DOMContentLoaded', () => {
    new BlockchainWebInterface();
});


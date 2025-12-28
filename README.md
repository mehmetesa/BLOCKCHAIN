# 🔗 Blockchain - Educational Implementation

**Educational blockchain implementation from scratch.**

Sıfırdan yazılmış, eğitim amaçlı bir blockchain implementasyonu. Bu proje blockchain teknolojisinin temel kavramlarını öğrenmek için tasarlanmıştır.

## 📋 İçerik

- ✅ **Block** - Blockchain'deki blok yapısı
- ✅ **Hash** - SHA-256 hash algoritması
- ✅ **Proof of Work** - Mining algoritması
- ✅ **Transaction Doğrulama** - Transaction geçerlilik kontrolü
- ✅ **CLI Tool** - Komut satırı arayüzü
- ✅ **Web Arayüzü** - Tarayıcı tabanlı görsel arayüz
- ✅ **Mining Simülasyonu** - Gerçek zamanlı mining simülasyonu

## 🚀 Kurulum

### Gereksinimler

- Python 3.7 veya üzeri
- Modern web tarayıcısı (Chrome, Firefox, Edge)

### Kurulum Adımları

1. Projeyi klonlayın veya indirin:
```bash
git clone <repository-url>
cd blockchain-project
```

2. Python bağımlılıkları (opsiyonel):
```bash
pip install -r requirements.txt
```

## 💻 Kullanım

### CLI Tool

Komut satırı arayüzünü başlatmak için:

```bash
python cli.py
```

**CLI Özellikleri:**
- Yeni transaction oluşturma
- Bekleyen transaction'ları görüntüleme
- Block mine etme
- Blockchain'i görüntüleme
- Blockchain geçerlilik kontrolü
- Adres bakiyesi sorgulama
- Blockchain istatistikleri
- JSON'a aktarma

### Web Arayüzü

Web arayüzünü kullanmak için:

1. `web_interface.html` dosyasını tarayıcınızda açın
2. Transaction oluşturun
3. Block mine edin
4. Blockchain'i görüntüleyin

**Web Arayüzü Özellikleri:**
- Görsel blockchain görüntüleme
- Gerçek zamanlı mining simülasyonu
- Transaction yönetimi
- Bakiye sorgulama
- İstatistikler

## 📚 Blockchain Yapısı

### Block Yapısı

```python
{
    "index": 0,
    "transactions": [...],
    "previous_hash": "0",
    "timestamp": 1234567890,
    "nonce": 0,
    "hash": "abc123..."
}
```

### Transaction Yapısı

```python
{
    "sender": "Alice",
    "receiver": "Bob",
    "amount": 10.5,
    "timestamp": 1234567890
}
```

## 🔐 Güvenlik Notları

Bu proje **eğitim amaçlıdır** ve production ortamında kullanılmamalıdır. Gerçek bir blockchain için:

- Daha güçlü hash algoritmaları (SHA-256)
- Daha gelişmiş konsensüs mekanizmaları
- Ağ protokolleri
- Güvenlik önlemleri
- Performans optimizasyonları

gerekir.

## 🎓 Öğrenilen Kavramlar

- Blockchain mimarisi
- Hash fonksiyonları
- Proof of Work algoritması
- Transaction doğrulama
- Merkezi olmayan sistemler
- Kriptografi temelleri

## 📝 Lisans

Bu proje eğitim amaçlıdır ve açık kaynak kodludur.

## 🔗 Kaynaklar

- [Bitcoin Whitepaper](https://bitcoin.org/bitcoin.pdf)
- [Blockchain Basics](https://en.wikipedia.org/wiki/Blockchain)

---

**Not:** Bu proje eğitim amaçlıdır. Gerçek kripto para birimleri veya finansal işlemler için kullanılmamalıdır.

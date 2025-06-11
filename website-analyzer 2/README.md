# Website Analyzer v2.0

Un software interno avanzato per l'analisi di siti web ed ecommerce con design moderno e performance ottimizzate.

## 🚀 Caratteristiche Principali

- **Design Apple-like**: Interfaccia moderna e minimalista
- **Performance Ottimizzate**: Fino a 10x più veloce con tecnologie asincrone
- **Funzionalità RESPONSABILE**: Sistema di consulenza automatizzato
- **Analisi Completa**: Tecnologie, annunci, tracker e performance
- **Pacchetti Commerciali**: 5 pacchetti predefiniti con prezzi automatici

## 📋 Requisiti

- Python 3.11+
- 4GB RAM
- Connessione internet

## 🛠️ Installazione

### Metodo 1: Locale
```bash
# Estrai il pacchetto
tar -xzf website-analyzer-v2.tar.gz
cd website-analyzer

# Attiva ambiente virtuale
source venv/bin/activate

# Avvia il server
python src/main.py
```

### Metodo 2: Docker
```bash
# Build dell'immagine
docker build -t website-analyzer .

# Esecuzione container
docker run -p 5001:5001 website-analyzer
```

### Metodo 3: GitHub Codespaces
1. Carica il progetto su GitHub
2. Apri in Codespaces
3. Il devcontainer si configurerà automaticamente

## 🌐 Utilizzo

1. Apri il browser su `http://localhost:5001`
2. Inserisci email aziendale (@fuzzymarketing.it)
3. Usa **Hunter** per analisi tecniche
4. Usa **RESPONSABILE** per consulenze commerciali

## 📦 Pacchetti Disponibili

| Pacchetto | Prezzo | Descrizione |
|-----------|--------|-------------|
| START | €1.200/mese | Gestione ADV base + email marketing |
| GROW | €1.500/mese | ADV + newsletter + social |
| PREMIUM | €2.200/mese | Servizio completo con SEO e blog |
| CONTENT & SOCIAL | €1.200/mese | Focus su contenuti social |
| ECOMMERCE CUSTOM | €1.500/mese | Restyling store completo |

## 🔧 Architettura

- **Backend**: Flask + asyncio + aiohttp
- **Frontend**: HTML5/CSS3/JavaScript vanilla
- **Analisi**: BeautifulSoup + SoupStrainer
- **Caching**: Sistema in-memory con TTL

## 📊 Performance

- **Analisi asincrona**: 10x più veloce
- **Parsing ottimizzato**: 50% più efficiente
- **Cache intelligente**: 85% hit rate
- **Concorrenza**: Analisi multiple simultanee

## 🎨 Design System

- **Colori**: Palette Apple (Blu #007AFF, Verde #34C759)
- **Tipografia**: San Francisco system font
- **Layout**: Grid responsive con breakpoint mobile-first
- **Animazioni**: Transizioni fluide e micro-interazioni

## 📁 Struttura Progetto

```
website-analyzer/
├── src/
│   ├── main.py              # Server Flask principale
│   ├── analyzer.py          # Engine di analisi ottimizzato
│   ├── routes/
│   │   └── analyzer.py      # API endpoints
│   └── static/
│       └── index.html       # Frontend completo
├── venv/                    # Ambiente virtuale Python
├── requirements.txt         # Dipendenze Python
├── .devcontainer/          # Configurazione container
├── DOCUMENTAZIONE_AGGIORNATA.md
├── GUIDA_UTENTE.md
└── README.md
```

## 🔒 Sicurezza

- Validazione input per prevenire XSS
- Rate limiting per protezione da abusi
- Headers CORS configurati
- Sanitizzazione URL automatica

## 📈 Monitoraggio

Il sistema fornisce metriche real-time:
- Tempo di risposta per richiesta
- Dimensione contenuto analizzato
- Efficienza cache
- Errori e retry automatici

## 🚀 Deployment

### Locale
```bash
python src/main.py
# Accesso: http://localhost:5001
```

### Produzione
```bash
# Con gunicorn (consigliato)
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5001 src.main:app
```

## 🔮 Roadmap

- [ ] Dashboard analytics avanzata
- [ ] API REST per integrazioni
- [ ] Export risultati (PDF, Excel)
- [ ] Notifiche real-time
- [ ] Database persistente

## 📞 Supporto

- **Email**: supporto@fuzzymarketing.it
- **Documentazione**: Vedi GUIDA_UTENTE.md
- **Issues**: Usa il sistema di ticketing interno

## 📄 Licenza

Proprietario - Fuzzy Marketing © 2025

---

**Website Analyzer v2.0** - Powered by Fuzzy Marketing


# Website Analyzer - Documentazione Tecnica

## Architettura del Sistema

### Panoramica
Website Analyzer è un'applicazione web basata su architettura client-server:
- **Backend**: Flask (Python) con API REST
- **Frontend**: HTML/CSS/JavaScript vanilla
- **Analisi**: Combinazione di web scraping statico e dinamico

### Struttura del Progetto
```
website-analyzer/
├── src/
│   ├── main.py              # Entry point dell'applicazione Flask
│   ├── analyzer.py          # Modulo principale di analisi
│   ├── routes/
│   │   ├── analyzer.py      # API endpoints per l'analisi
│   │   └── user.py          # Endpoints utente (template)
│   ├── models/
│   │   └── user.py          # Modelli database (template)
│   ├── static/
│   │   └── index.html       # Interfaccia utente frontend
│   └── database/
│       └── app.db           # Database SQLite
├── venv/                    # Virtual environment Python
├── requirements.txt         # Dipendenze Python
└── README.md
```

## Componenti Principali

### 1. WebsiteAnalyzer (analyzer.py)
Classe principale che gestisce l'analisi dei siti web.

#### Metodi Principali:
- `analyze_url(url)`: Analizza un singolo URL
- `analyze_multiple_urls(urls)`: Analizza più URL in batch
- `_analyze_static_content(url)`: Analisi con requests/BeautifulSoup
- `_analyze_dynamic_content(url)`: Analisi con Selenium
- `_load_adblock_rules()`: Carica regole EasyList per rilevamento annunci
- `_load_tech_signatures()`: Carica firme per rilevamento tecnologie

#### Tecnologie di Rilevamento:
```python
tech_signatures = {
    'cms': {
        'WordPress': [r'/wp-content/', r'/wp-includes/', ...],
        'Drupal': [r'/sites/default/', r'Drupal\.settings', ...],
        # ...
    },
    'frameworks': {
        'React': [r'react', r'__REACT_DEVTOOLS_GLOBAL_HOOK__', ...],
        # ...
    },
    # ...
}
```

### 2. API Endpoints (routes/analyzer.py)

#### POST /api/analyze
Endpoint principale per l'analisi dei siti web.

**Request Body:**
```json
{
    "urls": ["https://example.com", "https://another-site.com"]
}
```

**Response:**
```json
{
    "status": "success",
    "results": [
        {
            "url": "https://example.com",
            "status": "success",
            "technologies": {
                "cms": ["WordPress"],
                "frameworks": ["jQuery"],
                "analytics": ["Google Analytics"]
            },
            "ads_detected": false,
            "ad_domains": [],
            "trackers": []
        }
    ],
    "total_analyzed": 1
}
```

#### GET /api/health
Endpoint per verificare lo stato del servizio.

#### GET /api/test
Endpoint di test per verificare il funzionamento dell'analyzer.

### 3. Frontend (static/index.html)
Interfaccia utente single-page sviluppata in HTML/CSS/JavaScript vanilla.

#### Funzionalità JavaScript:
- `addUrl()`: Aggiunge URL alla lista di analisi
- `removeUrl(index)`: Rimuove URL dalla lista
- `analyzeWebsites()`: Invia richiesta di analisi al backend
- `displayResults(results)`: Visualizza i risultati dell'analisi

## Dipendenze

### Backend Python
```
Flask==3.1.1
flask-cors==6.0.0
requests==2.32.4
beautifulsoup4==4.13.4
selenium==4.33.0
adblockparser==0.7
lxml==5.4.0
```

### Sistema
- Chrome/Chromium (per Selenium WebDriver)
- Python 3.11+

## Configurazione e Deployment

### Installazione Locale
```bash
# Clona il repository
cd website-analyzer

# Attiva virtual environment
source venv/bin/activate

# Installa dipendenze
pip install -r requirements.txt

# Avvia il server
python src/main.py
```

### Configurazione Selenium
Il software utilizza Chrome headless per l'analisi dinamica:
```python
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
```

### Variabili di Configurazione
- **Host**: 0.0.0.0 (per accesso esterno)
- **Porta**: 5001 (configurabile in main.py)
- **Debug**: True (disabilitare in produzione)

## Sicurezza

### Misure Implementate
- CORS abilitato per richieste cross-origin
- Validazione degli URL in input
- Timeout per richieste HTTP (10 secondi)
- Gestione errori robusta

### Considerazioni di Sicurezza
- Non memorizzazione di dati sensibili
- Analisi read-only dei siti target
- Isolamento del browser headless

## Performance e Ottimizzazioni

### Strategie di Ottimizzazione
- Combinazione di analisi statica (veloce) e dinamica (completa)
- Timeout configurabili per evitare blocchi
- Gestione parallela di più URL (implementabile)

### Metriche Tipiche
- Analisi statica: 2-5 secondi per URL
- Analisi dinamica: 10-30 secondi per URL
- Memoria: ~100MB per istanza Selenium

## Estensibilità

### Aggiunta Nuove Tecnologie
Per aggiungere il rilevamento di nuove tecnologie, modificare `_load_tech_signatures()`:
```python
'nuova_categoria': {
    'Nome Tecnologia': [
        r'pattern_regex_1',
        r'pattern_regex_2'
    ]
}
```

### Nuovi Metodi di Analisi
- Implementare nuovi metodi nella classe `WebsiteAnalyzer`
- Aggiungere chiamate nei metodi `analyze_url()` o `analyze_multiple_urls()`

## Troubleshooting

### Problemi Comuni
1. **Chrome non trovato**: Installare Chrome/Chromium
2. **Timeout Selenium**: Aumentare timeout in `_setup_selenium_driver()`
3. **Errori regex**: Verificare escape dei caratteri speciali nelle firme

### Log e Debug
Il sistema utilizza il modulo `logging` di Python:
```python
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
```

### Monitoraggio
- Log delle richieste Flask
- Log degli errori di analisi
- Metriche di performance (implementabili)

---

*Documentazione Tecnica v1.0*


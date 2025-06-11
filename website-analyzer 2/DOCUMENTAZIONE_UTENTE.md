# Website Analyzer - Documentazione Utente

## Panoramica

Website Analyzer è un software interno progettato per analizzare siti web tramite URL e identificare:
- Tecnologie e applicazioni installate (CMS, framework, librerie JavaScript, server web, strumenti di analytics)
- Presenza di annunci pubblicitari e tracker

## Caratteristiche Principali

### Analisi Tecnologie
Il software è in grado di rilevare:
- **CMS**: WordPress, Drupal, Joomla, Shopify
- **Framework JavaScript**: React, Vue.js, Angular, jQuery
- **Strumenti di Analytics**: Google Analytics, Google Tag Manager, Facebook Pixel
- **Server Web**: Apache, Nginx, Microsoft IIS

### Rilevamento Annunci e Tracker
- Utilizza le regole EasyList per il rilevamento degli annunci
- Identifica domini noti per pubblicità e tracciamento
- Analizza script e iframe sospetti

## Come Utilizzare il Software

### 1. Accesso all'Interfaccia
- Aprire il browser e navigare all'URL del software
- L'interfaccia presenta un design moderno e intuitivo

### 2. Inserimento URL
- Inserire l'URL da analizzare nel campo di input
- Cliccare su "Aggiungi URL" per aggiungerlo alla lista
- È possibile aggiungere più URL per un'analisi batch

### 3. Avvio Analisi
- Cliccare su "🚀 Avvia Analisi" per iniziare il processo
- L'analisi può richiedere alcuni minuti per completarsi
- Un indicatore di caricamento mostra il progresso

### 4. Visualizzazione Risultati
I risultati vengono presentati in schede organizzate per ogni URL analizzato:

#### Stato Analisi
- ✅ **Successo**: Analisi completata con successo
- ❌ **Errore**: Problemi durante l'analisi (con dettagli dell'errore)

#### Tecnologie Rilevate
Le tecnologie sono organizzate per categoria:
- 📄 **CMS**: Content Management System
- ⚛️ **Framework**: Framework JavaScript
- 📈 **Analytics**: Strumenti di analisi
- 🖥️ **Server Web**: Server web utilizzato

#### Annunci e Tracker
- 🚨 **Annunci Rilevati**: Indica la presenza di pubblicità
- ✅ **Nessun Annuncio**: Nessuna pubblicità rilevata
- Lista dei domini pubblicitari e tracker identificati

## Limitazioni e Considerazioni

### Limitazioni Tecniche
- L'analisi si basa su firme e pattern noti, potrebbero sfuggire tecnologie personalizzate
- Alcuni siti con misure anti-scraping potrebbero non essere analizzabili completamente
- Il rilevamento degli annunci dipende dalle regole EasyList aggiornate

### Performance
- L'analisi di siti complessi può richiedere diversi minuti
- Il software utilizza sia analisi statica che dinamica (con browser headless)
- Le performance dipendono dalla velocità di risposta del sito target

### Sicurezza
- Il software non memorizza i dati analizzati
- Tutte le analisi sono effettuate in tempo reale
- Non vengono raccolte informazioni personali dai siti analizzati

## Risoluzione Problemi

### Errori Comuni
1. **URL non valido**: Assicurarsi che l'URL inizi con http:// o https://
2. **Timeout**: Il sito potrebbe essere lento o non raggiungibile
3. **Errore di rete**: Verificare la connessione internet

### Suggerimenti per Migliori Risultati
- Utilizzare URL completi e corretti
- Testare con siti pubblicamente accessibili
- Evitare siti con protezioni anti-bot eccessive

## Supporto Tecnico

Per assistenza tecnica o segnalazione di bug, contattare il team di sviluppo interno.

---

*Versione 1.0 - Sviluppato internamente*


from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from src.analyzer import WebsiteAnalyzer
import logging

# Configurazione logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

analyzer_bp = Blueprint('analyzer', __name__)

@analyzer_bp.route('/analyze', methods=['POST'])
@cross_origin()
def analyze_website():
    """Endpoint per analizzare uno o più siti web"""
    try:
        data = request.get_json()
        
        if not data or 'urls' not in data:
            return jsonify({
                'error': 'È necessario fornire una lista di URL da analizzare',
                'status': 'error'
            }), 400
        
        urls = data['urls']
        
        if not isinstance(urls, list) or len(urls) == 0:
            return jsonify({
                'error': 'La lista degli URL deve contenere almeno un elemento',
                'status': 'error'
            }), 400
        
        # Valida gli URL
        valid_urls = []
        for url in urls:
            if isinstance(url, str) and (url.startswith('http://') or url.startswith('https://')):
                valid_urls.append(url)
            else:
                logger.warning(f"URL non valido ignorato: {url}")
        
        if len(valid_urls) == 0:
            return jsonify({
                'error': 'Nessun URL valido fornito',
                'status': 'error'
            }), 400
        
        # Inizializza l'analyzer
        analyzer = WebsiteAnalyzer()
        
        # Analizza gli URL
        results = analyzer.analyze_multiple_urls(valid_urls)
        
        return jsonify({
            'status': 'success',
            'results': results,
            'total_analyzed': len(results)
        })
        
    except Exception as e:
        logger.error(f"Errore nell'analisi: {e}")
        return jsonify({
            'error': f'Errore interno del server: {str(e)}',
            'status': 'error'
        }), 500

@analyzer_bp.route('/health', methods=['GET'])
@cross_origin()
def health_check():
    """Endpoint per verificare lo stato del servizio"""
    return jsonify({
        'status': 'healthy',
        'service': 'Website Analyzer API'
    })

@analyzer_bp.route('/test', methods=['GET'])
@cross_origin()
def test_analyzer():
    """Endpoint di test per verificare il funzionamento dell'analyzer"""
    try:
        analyzer = WebsiteAnalyzer()
        test_url = 'https://example.com'
        result = analyzer.analyze_url(test_url)
        
        return jsonify({
            'status': 'success',
            'test_result': result,
            'message': 'Test completato con successo'
        })
        
    except Exception as e:
        logger.error(f"Errore nel test: {e}")
        return jsonify({
            'error': f'Errore nel test: {str(e)}',
            'status': 'error'
        }), 500


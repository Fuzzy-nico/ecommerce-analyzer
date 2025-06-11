import asyncio
import aiohttp
import requests
from bs4 import BeautifulSoup, SoupStrainer
import re
import time
import logging
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urljoin, urlparse
import json
from typing import Dict, List, Optional, Tuple
import hashlib
from datetime import datetime, timedelta

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PerformanceOptimizedAnalyzer:
    """
    Analyzer ottimizzato per performance con tecniche avanzate:
    - Programmazione asincrona
    - Connection pooling
    - Caching intelligente
    - Parsing selettivo
    """
    
    def __init__(self):
        self.session = None
        self.cache = {}
        self.cache_ttl = timedelta(hours=1)  # Cache TTL di 1 ora
        self.tech_signatures = self._load_tech_signatures()
        self.adblock_rules = self._load_adblock_rules()
        
    async def __aenter__(self):
        """Context manager per gestione sessione asincrona"""
        connector = aiohttp.TCPConnector(
            limit=100,  # Pool di 100 connessioni
            limit_per_host=10,  # Max 10 connessioni per host
            ttl_dns_cache=300,  # Cache DNS per 5 minuti
            use_dns_cache=True,
        )
        
        timeout = aiohttp.ClientTimeout(total=30, connect=10)
        
        self.session = aiohttp.ClientSession(
            connector=connector,
            timeout=timeout,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
        )
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Chiusura sessione asincrona"""
        if self.session:
            await self.session.close()
    
    def _get_cache_key(self, url: str) -> str:
        """Genera chiave cache per URL"""
        return hashlib.md5(url.encode()).hexdigest()
    
    def _is_cache_valid(self, cache_entry: dict) -> bool:
        """Verifica se entry cache è ancora valida"""
        if 'timestamp' not in cache_entry:
            return False
        
        cache_time = datetime.fromisoformat(cache_entry['timestamp'])
        return datetime.now() - cache_time < self.cache_ttl
    
    def _cache_result(self, url: str, result: dict):
        """Salva risultato in cache"""
        cache_key = self._get_cache_key(url)
        self.cache[cache_key] = {
            'result': result,
            'timestamp': datetime.now().isoformat()
        }
    
    def _get_cached_result(self, url: str) -> Optional[dict]:
        """Recupera risultato da cache se valido"""
        cache_key = self._get_cache_key(url)
        
        if cache_key in self.cache:
            cache_entry = self.cache[cache_key]
            if self._is_cache_valid(cache_entry):
                logger.info(f"Cache hit per {url}")
                return cache_entry['result']
            else:
                # Rimuovi entry scaduta
                del self.cache[cache_key]
        
        return None
    
    async def analyze_url(self, url: str) -> dict:
        """Analizza singolo URL con ottimizzazioni performance"""
        start_time = time.time()
        
        # Controlla cache
        cached_result = self._get_cached_result(url)
        if cached_result:
            return cached_result
        
        try:
            # Analisi asincrona
            static_analysis = await self._analyze_static_async(url)
            
            # Combina risultati
            result = {
                'url': url,
                'status': 'success',
                'analysis_time': time.time() - start_time,
                'technologies': static_analysis.get('technologies', {}),
                'ads_detected': static_analysis.get('ads_detected', False),
                'ad_domains': static_analysis.get('ad_domains', []),
                'trackers': static_analysis.get('trackers', []),
                'performance_metrics': {
                    'response_time': static_analysis.get('response_time', 0),
                    'content_size': static_analysis.get('content_size', 0),
                    'parsing_time': static_analysis.get('parsing_time', 0)
                }
            }
            
            # Salva in cache
            self._cache_result(url, result)
            
            logger.info(f"Analisi completata per {url} in {result['analysis_time']:.2f}s")
            return result
            
        except Exception as e:
            logger.error(f"Errore nell'analisi di {url}: {str(e)}")
            return {
                'url': url,
                'status': 'error',
                'error': str(e),
                'analysis_time': time.time() - start_time
            }
    
    async def analyze_multiple_urls(self, urls: List[str], max_concurrent: int = 10) -> List[dict]:
        """Analizza più URL contemporaneamente con controllo concorrenza"""
        semaphore = asyncio.Semaphore(max_concurrent)
        
        async def analyze_with_semaphore(url):
            async with semaphore:
                return await self.analyze_url(url)
        
        # Esegui analisi concorrenti
        tasks = [analyze_with_semaphore(url) for url in urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Gestisci eccezioni
        processed_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                processed_results.append({
                    'url': urls[i],
                    'status': 'error',
                    'error': str(result)
                })
            else:
                processed_results.append(result)
        
        return processed_results
    
    async def _analyze_static_async(self, url: str) -> dict:
        """Analisi statica asincrona ottimizzata"""
        request_start = time.time()
        
        try:
            async with self.session.get(url) as response:
                response_time = time.time() - request_start
                
                if response.status != 200:
                    raise Exception(f"HTTP {response.status}")
                
                content = await response.text()
                content_size = len(content)
                
                # Parsing ottimizzato con SoupStrainer
                parsing_start = time.time()
                result = await self._parse_content_optimized(content, url)
                parsing_time = time.time() - parsing_start
                
                result.update({
                    'response_time': response_time,
                    'content_size': content_size,
                    'parsing_time': parsing_time
                })
                
                return result
                
        except Exception as e:
            raise Exception(f"Errore nella richiesta: {str(e)}")
    
    async def _parse_content_optimized(self, content: str, url: str) -> dict:
        """Parsing ottimizzato del contenuto HTML"""
        
        # Parsing selettivo per performance
        head_strainer = SoupStrainer(['head', 'title', 'meta', 'script', 'link'])
        body_strainer = SoupStrainer(['body', 'script', 'iframe', 'div'])
        
        # Parse head per metadati e tecnologie
        head_soup = BeautifulSoup(content, 'html.parser', parse_only=head_strainer)
        
        # Parse body per contenuto e annunci
        body_soup = BeautifulSoup(content, 'html.parser', parse_only=body_strainer)
        
        # Analisi parallela con ThreadPoolExecutor
        with ThreadPoolExecutor(max_workers=3) as executor:
            # Esegui analisi in parallelo
            tech_future = executor.submit(self._detect_technologies, head_soup, body_soup)
            ads_future = executor.submit(self._detect_ads, body_soup, url)
            
            # Raccogli risultati
            technologies = tech_future.result()
            ads_result = ads_future.result()
        
        return {
            'technologies': technologies,
            'ads_detected': ads_result['detected'],
            'ad_domains': ads_result['domains'],
            'trackers': ads_result['trackers']
        }
    
    def _detect_technologies(self, head_soup: BeautifulSoup, body_soup: BeautifulSoup) -> dict:
        """Rilevamento tecnologie ottimizzato"""
        technologies = {
            'cms': [],
            'frameworks': [],
            'analytics': [],
            'server': []
        }
        
        # Combina contenuto per analisi
        combined_content = str(head_soup) + str(body_soup)
        
        # Analisi pattern ottimizzata
        for category, tech_patterns in self.tech_signatures.items():
            for tech_name, patterns in tech_patterns.items():
                for pattern in patterns:
                    try:
                        if re.search(pattern, combined_content, re.IGNORECASE):
                            if tech_name not in technologies[category]:
                                technologies[category].append(tech_name)
                            break  # Esci al primo match per performance
                    except re.error:
                        continue
        
        return technologies
    
    def _detect_ads(self, soup: BeautifulSoup, url: str) -> dict:
        """Rilevamento annunci ottimizzato"""
        ad_domains = set()
        trackers = set()
        
        # Analizza script e iframe
        elements = soup.find_all(['script', 'iframe', 'img', 'link'])
        
        for element in elements:
            src = element.get('src') or element.get('href')
            if src:
                # Estrai dominio
                try:
                    parsed_url = urlparse(src if src.startswith('http') else urljoin(url, src))
                    domain = parsed_url.netloc.lower()
                    
                    # Controlla contro regole adblock
                    if self._is_ad_domain(domain):
                        ad_domains.add(domain)
                    
                    if self._is_tracker_domain(domain):
                        trackers.add(domain)
                        
                except Exception:
                    continue
        
        return {
            'detected': len(ad_domains) > 0,
            'domains': list(ad_domains),
            'trackers': list(trackers)
        }
    
    def _is_ad_domain(self, domain: str) -> bool:
        """Verifica se dominio è pubblicitario"""
        ad_keywords = [
            'doubleclick', 'googlesyndication', 'googleadservices',
            'facebook.com/tr', 'google-analytics', 'googletagmanager',
            'adsystem', 'advertising', 'ads', 'adnxs'
        ]
        
        return any(keyword in domain for keyword in ad_keywords)
    
    def _is_tracker_domain(self, domain: str) -> bool:
        """Verifica se dominio è tracker"""
        tracker_keywords = [
            'analytics', 'tracking', 'metrics', 'stats',
            'hotjar', 'mixpanel', 'segment', 'amplitude'
        ]
        
        return any(keyword in domain for keyword in tracker_keywords)
    
    def _load_tech_signatures(self) -> dict:
        """Carica firme tecnologie ottimizzate"""
        return {
            'cms': {
                'WordPress': [
                    r'/wp-content/',
                    r'/wp-includes/',
                    r'wp-json',
                    r'wordpress'
                ],
                'Drupal': [
                    r'/sites/default/',
                    r'Drupal\.settings',
                    r'/modules/',
                    r'drupal'
                ],
                'Joomla': [
                    r'/components/',
                    r'joomla',
                    r'/templates/'
                ],
                'Shopify': [
                    r'shopify',
                    r'cdn\.shopify\.com',
                    r'myshopify\.com'
                ]
            },
            'frameworks': {
                'React': [
                    r'react',
                    r'__REACT_DEVTOOLS_GLOBAL_HOOK__',
                    r'ReactDOM'
                ],
                'Vue.js': [
                    r'vue\.js',
                    r'Vue\.config',
                    r'__VUE__'
                ],
                'Angular': [
                    r'angular',
                    r'ng-app',
                    r'@angular'
                ],
                'jQuery': [
                    r'jquery',
                    r'\$\.fn\.jquery',
                    r'jQuery'
                ]
            },
            'analytics': {
                'Google Analytics': [
                    r'google-analytics\.com',
                    r'gtag\(',
                    r'ga\('
                ],
                'Google Tag Manager': [
                    r'googletagmanager\.com',
                    r'gtm\.js'
                ],
                'Facebook Pixel': [
                    r'facebook\.com/tr',
                    r'fbq\('
                ]
            },
            'server': {
                'Apache': [
                    r'Apache',
                    r'Server: Apache'
                ],
                'Nginx': [
                    r'nginx',
                    r'Server: nginx'
                ],
                'Microsoft IIS': [
                    r'Microsoft-IIS',
                    r'Server: Microsoft-IIS'
                ]
            }
        }
    
    def _load_adblock_rules(self) -> list:
        """Carica regole adblock semplificate"""
        return [
            r'doubleclick\.net',
            r'googlesyndication\.com',
            r'googleadservices\.com',
            r'facebook\.com/tr',
            r'adsystem\.com'
        ]

# Classe wrapper per compatibilità con il codice esistente
class WebsiteAnalyzer:
    """Wrapper per mantenere compatibilità con l'interfaccia esistente"""
    
    def __init__(self):
        self.performance_analyzer = None
    
    def analyze_url(self, url: str) -> dict:
        """Analizza singolo URL (versione sincrona)"""
        return asyncio.run(self._analyze_url_async(url))
    
    def analyze_multiple_urls(self, urls: list) -> dict:
        """Analizza più URL (versione sincrona)"""
        return asyncio.run(self._analyze_multiple_urls_async(urls))
    
    async def _analyze_url_async(self, url: str) -> dict:
        """Analisi asincrona singolo URL"""
        async with PerformanceOptimizedAnalyzer() as analyzer:
            return await analyzer.analyze_url(url)
    
    async def _analyze_multiple_urls_async(self, urls: list) -> dict:
        """Analisi asincrona multipla"""
        async with PerformanceOptimizedAnalyzer() as analyzer:
            results = await analyzer.analyze_multiple_urls(urls)
            
            return {
                'status': 'success',
                'results': results,
                'total_analyzed': len(results),
                'successful': len([r for r in results if r.get('status') == 'success']),
                'failed': len([r for r in results if r.get('status') == 'error'])
            }


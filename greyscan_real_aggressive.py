"""
GreyScan REAL Aggressive Engine
==============================

This version targets REAL endpoints for actual platforms like DexScreener,
CoinGecko, etc. It will find the actual working APIs and data sources.

The goal: 100% success by finding the REAL data endpoints that actually exist.
"""

import asyncio
import aiohttp
import json
import time
import random
import re
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple
from urllib.parse import urljoin, urlparse, quote
import ssl
from dataclasses import dataclass

@dataclass
class RealAttempt:
    """Track real attempts against real endpoints"""
    target: str
    method: str
    url: str
    success: bool
    status_code: Optional[int]
    content_size: int
    data_found: List[str]
    failure_reason: Optional[str]
    response_time: float
    timestamp: float

class GreyScanRealAggressive:
    """
    Aggressive engine that targets REAL endpoints for REAL platforms
    """
    
    def __init__(self, target_symbols: List[str] = None):
        print("🔥 INITIALIZING REAL AGGRESSIVE ENGINE")
        print("🎯 Targeting REAL endpoints for REAL platforms")
        print("💪 Will find actual working data sources")
        print("🧠 LEARNING MODE: Will remember what works and apply to future targets")
        
        self.session = None
        self.target_symbols = target_symbols or ["price", "data", "api", "token", "volume", "market"]
        self.all_attempts: List[RealAttempt] = []
        
        # LEARNING SYSTEM
        self.successful_patterns: Dict[str, List[str]] = {}  # platform -> working URL patterns
        self.failed_patterns: Dict[str, Set[str]] = {}       # platform -> failed URL patterns
        self.pattern_success_rates: Dict[str, float] = {}    # pattern -> success rate
        self.learned_headers: Dict[str, Dict[str, str]] = {} # platform -> working headers
        
        # REAL platform endpoint patterns
        self.real_platforms = {
            'dexscreener': {
                'base_domain': 'dexscreener.com',
                'patterns': [
                    'https://dexscreener.com/ethereum/{target}',
                    'https://dexscreener.com/bsc/{target}',
                    'https://dexscreener.com/polygon/{target}',
                    'https://api.dexscreener.com/latest/dex/tokens/{target}',
                    'https://api.dexscreener.com/latest/dex/search/?q={target}',
                    'https://dexscreener.com/api/token/{target}',
                    'https://dexscreener.com/_next/data/build-id/ethereum/{target}.json',
                    'https://dexscreener.com/api/search?q={target}',
                ]
            },
            'coingecko': {
                'base_domain': 'coingecko.com',
                'patterns': [
                    'https://api.coingecko.com/api/v3/coins/{target}',
                    'https://api.coingecko.com/api/v3/search?query={target}',
                    'https://www.coingecko.com/en/coins/{target}',
                    'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids={target}',
                    'https://www.coingecko.com/price_charts/{target}/usd/24_hours.json',
                    'https://api.coingecko.com/api/v3/simple/price?ids={target}&vs_currencies=usd',
                ]
            },
            'coinmarketcap': {
                'base_domain': 'coinmarketcap.com',
                'patterns': [
                    'https://coinmarketcap.com/currencies/{target}/',
                    'https://api.coinmarketcap.com/v1/ticker/{target}/',
                    'https://coinmarketcap.com/api/v1/cryptocurrency/quotes/latest?symbol={target}',
                    'https://web-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?symbol={target}',
                    'https://coinmarketcap.com/_next/data/build-id/currencies/{target}.json',
                ]
            },
            'defillama': {
                'base_domain': 'defillama.com',
                'patterns': [
                    'https://api.llama.fi/protocol/{target}',
                    'https://defillama.com/protocol/{target}',
                    'https://api.llama.fi/protocols',
                    'https://defillama.com/api/protocol/{target}',
                    'https://yields.llama.fi/pools',
                ]
            },
            'etherscan': {
                'base_domain': 'etherscan.io',
                'patterns': [
                    'https://etherscan.io/token/{target}',
                    'https://api.etherscan.io/api?module=token&action=tokeninfo&contractaddress={target}',
                    'https://etherscan.io/address/{target}',
                    'https://api.etherscan.io/api?module=account&action=balance&address={target}',
                    'https://etherscan.io/api/token/{target}',
                ]
            },
            'uniswap': {
                'base_domain': 'uniswap.org',
                'patterns': [
                    'https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v3',
                    'https://info.uniswap.org/token/{target}',
                    'https://api.uniswap.org/v1/tokens/{target}',
                ]
            },
            'pancakeswap': {
                'base_domain': 'pancakeswap.finance',
                'patterns': [
                    'https://api.pancakeswap.info/api/v2/tokens/{target}',
                    'https://pancakeswap.finance/info/token/{target}',
                ]
            }
        }
        
        print("✨ Real aggressive engine ready - targeting actual endpoints!")
    
    async def initialize_session(self):
        """Initialize session for real requests"""
        connector = aiohttp.TCPConnector(ssl=ssl.create_default_context())
        timeout = aiohttp.ClientTimeout(total=30)
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/html, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Cache-Control': 'no-cache',
            'DNT': '1'
        }
        
        self.session = aiohttp.ClientSession(
            connector=connector,
            timeout=timeout,
            headers=headers
        )
    
    async def real_aggressive_collect(self, targets: List[Tuple[str, str]]) -> List[Dict[str, Any]]:
        """
        Aggressively collect from REAL platforms with REAL endpoints
        """
        
        if not self.session:
            await self.initialize_session()
        
        print(f"🚀 REAL AGGRESSIVE COLLECTION: {len(targets)} targets")
        
        all_results = []
        
        for target_name, platform in targets:
            print(f"\n🎯 ATTACKING {platform.upper()}: {target_name}")
            
            if platform not in self.real_platforms:
                print(f"❌ Unknown platform: {platform}")
                continue
            
            result = await self._attack_real_platform(target_name, platform)
            
            if result:
                all_results.append(result)
                print(f"✅ SUCCESS: {target_name} on {platform} - {result['data_size']} bytes")
            else:
                print(f"❌ FAILED: {target_name} on {platform}")
        
        # Results
        success_rate = len(all_results) / len(targets) if targets else 0
        print(f"\n📊 REAL RESULTS:")
        print(f"Success rate: {success_rate:.1%} ({len(all_results)}/{len(targets)})")
        print(f"Total attempts: {len(self.all_attempts)}")
        
        return all_results
    
    async def _attack_real_platform(self, target: str, platform: str) -> Optional[Dict[str, Any]]:
        """Attack a real platform with LEARNING - try successful patterns first"""
        
        print(f"🧠 LEARNING ATTACK: {platform}")
        
        # STEP 1: Try previously successful patterns first
        if platform in self.successful_patterns:
            print(f"🎯 Trying {len(self.successful_patterns[platform])} LEARNED successful patterns first...")
            
            for pattern in self.successful_patterns[platform]:
                result = await self._try_learned_pattern(target, platform, pattern)
                if result:
                    print(f"🎉 LEARNED PATTERN SUCCESS: {pattern}")
                    return result
        
        # STEP 2: Try base patterns, but skip known failures
        platform_info = self.real_platforms[platform]
        base_patterns = platform_info['patterns']
        
        # Filter out known failures
        if platform in self.failed_patterns:
            base_patterns = [p for p in base_patterns if p not in self.failed_patterns[platform]]
        
        print(f"🔄 Trying {len(base_patterns)} base patterns (filtered by learning)...")
        
        for i, pattern in enumerate(base_patterns):
            result = await self._try_pattern_with_variations(target, platform, pattern, f"base_{i}")
            
            if result:
                # LEARN from success
                self._learn_from_success(platform, pattern, result['url'])
                print(f"🎉 BASE PATTERN SUCCESS: {pattern}")
                return result
            else:
                # LEARN from failure
                self._learn_from_failure(platform, pattern)
        
        # STEP 3: Generate new patterns based on what we learned
        print(f"🧠 Generating NEW patterns based on learning...")
        new_patterns = self._generate_learned_patterns(platform)
        
        for i, pattern in enumerate(new_patterns):
            result = await self._try_pattern_with_variations(target, platform, pattern, f"learned_{i}")
            
            if result:
                self._learn_from_success(platform, pattern, result['url'])
                print(f"🎉 LEARNED GENERATION SUCCESS: {pattern}")
                return result
            else:
                self._learn_from_failure(platform, pattern)
        
        return None
    
    async def _try_real_endpoint(self, target: str, platform: str, url: str, method: str) -> Dict[str, Any]:
        """Try a real endpoint and analyze the response"""
        
        start_time = time.time()
        
        attempt = RealAttempt(
            target=target,
            method=method,
            url=url,
            success=False,
            status_code=None,
            content_size=0,
            data_found=[],
            failure_reason=None,
            response_time=0.0,
            timestamp=time.time()
        )
        
        try:
            # Try different headers for different endpoint types
            headers = self._get_headers_for_url(url)
            
            async with self.session.get(url, headers=headers) as response:
                attempt.status_code = response.status
                attempt.response_time = time.time() - start_time
                
                if response.status == 200:
                    content = await response.text()
                    attempt.content_size = len(content)
                    
                    if len(content) > 50:  # Has some content
                        # Analyze content for useful data
                        data_found = self._analyze_real_content(content, platform)
                        
                        if data_found:
                            attempt.success = True
                            attempt.data_found = data_found
                            
                            return {
                                'success': True,
                                'content': content,
                                'content_size': len(content),
                                'data_found': data_found,
                                'status_code': response.status
                            }
                        else:
                            attempt.failure_reason = "no_useful_data"
                    else:
                        attempt.failure_reason = "minimal_content"
                        
                elif response.status == 404:
                    attempt.failure_reason = "not_found"
                elif response.status == 403:
                    attempt.failure_reason = "forbidden"
                elif response.status == 429:
                    attempt.failure_reason = "rate_limited"
                    # Wait a bit if rate limited
                    await asyncio.sleep(2)
                else:
                    attempt.failure_reason = f"http_{response.status}"
                    
        except asyncio.TimeoutError:
            attempt.failure_reason = "timeout"
            attempt.response_time = time.time() - start_time
        except Exception as e:
            attempt.failure_reason = f"exception_{type(e).__name__}"
            attempt.response_time = time.time() - start_time
        
        self.all_attempts.append(attempt)
        return {'success': False, 'reason': attempt.failure_reason}
    
    def _get_headers_for_url(self, url: str) -> Dict[str, str]:
        """Get appropriate headers based on URL type"""
        
        base_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Cache-Control': 'no-cache',
            'DNT': '1'
        }
        
        # API endpoints
        if '/api/' in url or url.startswith('https://api.'):
            base_headers['Accept'] = 'application/json'
            base_headers['Content-Type'] = 'application/json'
        # Web pages
        else:
            base_headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
        
        # Platform-specific headers
        if 'coingecko' in url:
            base_headers['Referer'] = 'https://www.coingecko.com/'
        elif 'dexscreener' in url:
            base_headers['Referer'] = 'https://dexscreener.com/'
        elif 'coinmarketcap' in url:
            base_headers['Referer'] = 'https://coinmarketcap.com/'
        
        return base_headers
    
    def _analyze_real_content(self, content: str, platform: str) -> List[str]:
        """Analyze real content to determine if it contains useful data"""
        
        data_found = []
        content_lower = content.lower()
        
        # Look for target symbols
        for symbol in self.target_symbols:
            if symbol in content_lower:
                data_found.append(symbol)
        
        # Platform-specific analysis
        if platform == 'dexscreener':
            if any(keyword in content_lower for keyword in ['pair', 'liquidity', 'volume', 'price']):
                data_found.append('dex_data')
        elif platform == 'coingecko':
            if any(keyword in content_lower for keyword in ['market_cap', 'rank', 'supply']):
                data_found.append('coin_data')
        elif platform == 'coinmarketcap':
            if any(keyword in content_lower for keyword in ['market cap', 'circulating supply']):
                data_found.append('market_data')
        elif platform == 'defillama':
            if any(keyword in content_lower for keyword in ['tvl', 'protocol', 'defi']):
                data_found.append('defi_data')
        elif platform == 'etherscan':
            if any(keyword in content_lower for keyword in ['contract', 'transaction', 'balance']):
                data_found.append('blockchain_data')
        
        # General indicators of useful data
        if any(indicator in content_lower for indicator in ['{', 'json', 'api', 'data']):
            data_found.append('structured_data')
        
        # Large content is usually useful
        if len(content) > 10000:
            data_found.append('substantial_content')
        
        return list(set(data_found))  # Remove duplicates
    
    async def _try_learned_pattern(self, target: str, platform: str, pattern: str) -> Optional[Dict[str, Any]]:
        """Try a previously successful pattern"""
        
        target_variations = [target.lower(), target.upper(), target]
        
        for target_var in target_variations:
            url = pattern.format(target=target_var)
            result = await self._try_real_endpoint(target, platform, url, "learned")
            
            if result and result['success']:
                return {
                    'target': target,
                    'platform': platform,
                    'method': 'learned_pattern',
                    'url': url,
                    'data_size': result['content_size'],
                    'symbols': result['data_found'],
                    'timestamp': datetime.now().isoformat(),
                    'content': result['content'][:1000]
                }
        
        return None
    
    async def _try_pattern_with_variations(self, target: str, platform: str, pattern: str, method: str) -> Optional[Dict[str, Any]]:
        """Try a pattern with target variations"""
        
        target_variations = [
            target.lower(), target.upper(), target,
            target.replace(' ', '-'), target.replace(' ', '_'),
            target.replace('-', '_'), target.replace('_', '-')
        ]
        
        for target_var in target_variations:
            url = pattern.format(target=target_var)
            result = await self._try_real_endpoint(target, platform, url, method)
            
            if result and result['success']:
                return {
                    'target': target,
                    'platform': platform,
                    'method': method,
                    'url': url,
                    'data_size': result['content_size'],
                    'symbols': result['data_found'],
                    'timestamp': datetime.now().isoformat(),
                    'content': result['content'][:1000]
                }
        
        return None
    
    def _learn_from_success(self, platform: str, pattern: str, successful_url: str):
        """Learn from successful attempts"""
        
        # Add to successful patterns
        if platform not in self.successful_patterns:
            self.successful_patterns[platform] = []
        
        if pattern not in self.successful_patterns[platform]:
            self.successful_patterns[platform].append(pattern)
            print(f"📚 LEARNED SUCCESS: {platform} -> {pattern}")
        
        # Update success rate
        pattern_key = f"{platform}_{pattern}"
        current_rate = self.pattern_success_rates.get(pattern_key, 0.5)
        self.pattern_success_rates[pattern_key] = min(current_rate + 0.2, 1.0)
        
        # Extract and learn URL structure
        self._extract_url_patterns(platform, successful_url)
    
    def _learn_from_failure(self, platform: str, pattern: str):
        """Learn from failed attempts"""
        
        # Add to failed patterns
        if platform not in self.failed_patterns:
            self.failed_patterns[platform] = set()
        
        self.failed_patterns[platform].add(pattern)
        
        # Decrease success rate
        pattern_key = f"{platform}_{pattern}"
        current_rate = self.pattern_success_rates.get(pattern_key, 0.5)
        self.pattern_success_rates[pattern_key] = max(current_rate - 0.1, 0.0)
    
    def _extract_url_patterns(self, platform: str, successful_url: str):
        """Extract patterns from successful URLs to generate new ones"""
        
        # Extract domain patterns
        if 'api.' in successful_url:
            new_pattern = successful_url.replace('api.', 'api2.').replace('{target}', '{target}')
            self._add_generated_pattern(platform, new_pattern)
        
        # Extract path patterns
        if '/v3/' in successful_url:
            new_pattern = successful_url.replace('/v3/', '/v2/').replace('{target}', '{target}')
            self._add_generated_pattern(platform, new_pattern)
            new_pattern = successful_url.replace('/v3/', '/v1/').replace('{target}', '{target}')
            self._add_generated_pattern(platform, new_pattern)
    
    def _add_generated_pattern(self, platform: str, pattern: str):
        """Add a generated pattern to the platform's patterns"""
        
        if platform not in self.real_platforms:
            return
        
        # Convert back to template format
        pattern_template = pattern.replace(platform, '{target}')
        
        if pattern_template not in self.real_platforms[platform]['patterns']:
            self.real_platforms[platform]['patterns'].append(pattern_template)
            print(f"🧠 GENERATED NEW PATTERN: {platform} -> {pattern_template}")
    
    def _generate_learned_patterns(self, platform: str) -> List[str]:
        """Generate new patterns based on what we learned from other platforms"""
        
        new_patterns = []
        
        # Learn from successful patterns of other platforms
        for other_platform, patterns in self.successful_patterns.items():
            if other_platform == platform:
                continue
            
            for pattern in patterns:
                # Adapt successful patterns from other platforms
                adapted = pattern.replace(other_platform, platform)
                if adapted != pattern and adapted not in new_patterns:
                    new_patterns.append(adapted)
        
        # Generate variations based on common API patterns
        common_variations = [
            f"https://api.{platform}.com/v1/{{target}}",
            f"https://api.{platform}.com/v2/{{target}}",
            f"https://api.{platform}.io/{{target}}",
            f"https://{platform}.com/api/{{target}}",
            f"https://{platform}.com/api/v1/{{target}}",
            f"https://data.{platform}.com/{{target}}",
            f"https://public.{platform}.com/{{target}}"
        ]
        
        new_patterns.extend(common_variations)
        
        return new_patterns[:10]  # Limit to prevent explosion
    
    def display_learning_stats(self):
        """Display what the system has learned"""
        
        print(f"\n🧠 LEARNING STATISTICS:")
        print(f"Successful patterns learned: {sum(len(patterns) for patterns in self.successful_patterns.values())}")
        print(f"Failed patterns recorded: {sum(len(patterns) for patterns in self.failed_patterns.values())}")
        
        if self.successful_patterns:
            print(f"\n✅ SUCCESSFUL PATTERNS BY PLATFORM:")
            for platform, patterns in self.successful_patterns.items():
                print(f"  {platform}: {len(patterns)} working patterns")
                for pattern in patterns[:3]:  # Show first 3
                    print(f"    - {pattern}")
        
        if self.pattern_success_rates:
            print(f"\n📊 TOP PATTERN SUCCESS RATES:")
            sorted_patterns = sorted(self.pattern_success_rates.items(), key=lambda x: x[1], reverse=True)
            for pattern, rate in sorted_patterns[:5]:
                print(f"  {pattern}: {rate:.1%}")
    
    async def close(self):
        """Clean up resources and display learning stats"""
        self.display_learning_stats()
        
        if self.session:
            await self.session.close()

# Test with REAL targets
async def test_real_aggressive():
    """Test with real crypto targets on real platforms"""
    
    print("🔥 TESTING REAL AGGRESSIVE ENGINE")
    print("=" * 60)
    print("Targeting REAL crypto data from REAL platforms")
    
    # REAL crypto targets
    real_targets = [
        # DexScreener targets (token addresses)
        ("0xa0b86a33e6441e6c7b7b6b6b6b6b6b6b6b6b6b6b", "dexscreener"),  # Example token
        ("ethereum", "dexscreener"),  # Search term
        
        # CoinGecko targets
        ("bitcoin", "coingecko"),
        ("ethereum", "coingecko"),
        
        # CoinMarketCap targets  
        ("BTC", "coinmarketcap"),
        ("ETH", "coinmarketcap"),
        
        # DeFiLlama targets
        ("uniswap", "defillama"),
        ("aave", "defillama"),
        
        # Etherscan targets (addresses)
        ("0xA0b86a33E6441e6C7b7b6b6b6b6b6b6b6b6b6b6b", "etherscan"),
    ]
    
    engine = GreyScanRealAggressive(target_symbols=[
        "price", "volume", "market", "token", "data", "api", "json", 
        "liquidity", "tvl", "supply", "cap", "rank"
    ])
    
    try:
        results = await engine.real_aggressive_collect(real_targets)
        
        print(f"\n🎉 REAL RESULTS:")
        print(f"Targets attempted: {len(real_targets)}")
        print(f"Successful collections: {len(results)}")
        print(f"Success rate: {len(results)/len(real_targets):.1%}")
        
        if results:
            print(f"\n💎 SUCCESSFUL REAL DATA COLLECTIONS:")
            for result in results:
                print(f"  ✅ {result['target']} on {result['platform']}")
                print(f"     Data size: {result['data_size']} bytes")
                print(f"     Data types: {result['symbols']}")
                print(f"     URL: {result['url']}")
                print(f"     Sample: {result['content'][:200]}...")
                print()
        
        # Show failure analysis
        failed_attempts = [a for a in engine.all_attempts if not a.success]
        if failed_attempts:
            failure_reasons = {}
            for attempt in failed_attempts:
                reason = attempt.failure_reason or 'unknown'
                failure_reasons[reason] = failure_reasons.get(reason, 0) + 1
            
            print(f"🔍 FAILURE ANALYSIS:")
            for reason, count in sorted(failure_reasons.items(), key=lambda x: x[1], reverse=True):
                print(f"  {reason}: {count} times")
        
        return results
        
    finally:
        await engine.close()

if __name__ == "__main__":
    asyncio.run(test_real_aggressive())
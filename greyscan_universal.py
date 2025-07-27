#!/usr/bin/env python3
"""
GreyScan Universal - Global Widget Crawler
If it worked on Twitter, it'll work everywhere else
"""

import asyncio
import aiohttp
import json
import re
from typing import List, Dict, Any, Tuple
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import time
from dataclasses import dataclass

@dataclass
class UniversalTarget:
    name: str
    platform: str
    custom_url: str = None

class GreyScanUniversal:
    def __init__(self):
        self.session = None
        self.learned_patterns = {}
        self.failed_patterns = set()
        self.success_stats = {}
        
        # Universal widget patterns that work across platforms
        self.universal_patterns = {
            # Embed patterns (most common)
            "embed": [
                "https://{platform}/embed/{target}",
                "https://www.{platform}/embed/{target}",
                "https://{platform}/widgets/{target}",
                "https://platform.{platform}/widgets/{target}",
                "https://embed.{platform}/{target}",
                "https://widget.{platform}/{target}",
            ],
            
            # API patterns (public endpoints)
            "api": [
                "https://api.{platform}/v1/{target}",
                "https://api.{platform}/v2/{target}",
                "https://api.{platform}/public/{target}",
                "https://{platform}/api/{target}",
                "https://www.{platform}/api/v1/{target}",
            ],
            
            # Preview/share patterns
            "preview": [
                "https://{platform}/preview/{target}",
                "https://www.{platform}/share/{target}",
                "https://{platform}/p/{target}",
                "https://{platform}/post/{target}",
                "https://{platform}/content/{target}",
            ],
            
            # RSS/Feed patterns
            "feed": [
                "https://{platform}/rss/{target}",
                "https://{platform}/feed/{target}",
                "https://www.{platform}/feeds/{target}",
                "https://{platform}/{target}/rss",
                "https://{platform}/{target}/feed",
            ],
            
            # Mobile/lite versions (often less protected)
            "mobile": [
                "https://m.{platform}/{target}",
                "https://mobile.{platform}/{target}",
                "https://lite.{platform}/{target}",
                "https://{platform}/m/{target}",
            ],
            
            # Archive/cache patterns
            "archive": [
                "https://webcache.googleusercontent.com/search?q=cache:{platform}/{target}",
                "https://archive.org/wayback/available?url={platform}/{target}",
                "https://web.archive.org/web/*/{platform}/{target}",
            ]
        }
        
        # Platform-specific intelligence
        self.platform_intelligence = {
            "youtube": {
                "patterns": ["https://www.youtube.com/embed/{target}", "https://www.youtube.com/oembed?url=https://youtube.com/watch?v={target}"],
                "data_selectors": ["title", "view-count", "like-button", "channel-name"],
                "success_indicators": ["videoDetails", "title", "viewCount"]
            },
            "instagram": {
                "patterns": ["https://www.instagram.com/p/{target}/embed/", "https://instagram.com/{target}/?__a=1"],
                "data_selectors": ["caption", "likes", "timestamp", "media"],
                "success_indicators": ["graphql", "edge_media", "caption"]
            },
            "reddit": {
                "patterns": ["https://www.reddit.com/r/{target}.json", "https://www.reddit.com/embed?url=https://reddit.com/r/{target}"],
                "data_selectors": ["title", "score", "num_comments", "author"],
                "success_indicators": ["data", "children", "title"]
            },
            "tiktok": {
                "patterns": ["https://www.tiktok.com/embed/{target}", "https://www.tiktok.com/oembed?url=https://tiktok.com/@user/video/{target}"],
                "data_selectors": ["video-meta", "like-count", "share-count"],
                "success_indicators": ["videoData", "stats", "playCount"]
            },
            "medium": {
                "patterns": ["https://medium.com/{target}?format=json", "https://medium.com/p/{target}"],
                "data_selectors": ["title", "subtitle", "author", "claps"],
                "success_indicators": ["payload", "value", "title"]
            },
            "telegram": {
                "patterns": ["https://t.me/s/{target}", "https://t.me/{target}"],
                "data_selectors": ["message", "views", "timestamp"],
                "success_indicators": ["tgme_widget_message", "text"]
            },
            "substack": {
                "patterns": ["https://{target}.substack.com/api/v1/posts", "https://{target}.substack.com/feed"],
                "data_selectors": ["title", "subtitle", "author"],
                "success_indicators": ["posts", "title", "subtitle"]
            },
            "coinmarketcap": {
                "patterns": ["https://api.coinmarketcap.com/v1/ticker/{target}/", "https://coinmarketcap.com/currencies/{target}/"],
                "data_selectors": ["price", "volume", "market_cap"],
                "success_indicators": ["price_usd", "market_cap_usd"]
            },
            "coingecko": {
                "patterns": ["https://api.coingecko.com/api/v3/coins/{target}", "https://www.coingecko.com/en/coins/{target}"],
                "data_selectors": ["current_price", "market_cap", "volume"],
                "success_indicators": ["market_data", "current_price"]
            }
        }
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=10),
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
            }
        )
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
            
    async def universal_scan(self, targets: List[UniversalTarget]) -> List[Dict[str, Any]]:
        """Universal scanning across all platforms"""
        print(f"🌍 UNIVERSAL SCAN: {len(targets)} targets across platforms")
        print("🔓 If it worked on Twitter, it'll work everywhere!")
        
        all_results = []
        
        for target in targets:
            print(f"\n🎯 ATTACKING {target.platform.upper()}: {target.name}")
            
            result = await self._attack_universal_target(target)
            if result:
                all_results.append(result)
                print(f"✅ SUCCESS: {target.name} on {target.platform} - {result['data_size']} bytes")
            else:
                print(f"❌ FAILED: {target.name} on {target.platform}")
                
        success_rate = len(all_results) / len(targets) * 100
        print(f"\n🌍 UNIVERSAL RESULTS:")
        print(f"Success rate: {success_rate:.1f}% ({len(all_results)}/{len(targets)})")
        
        return all_results
        
    async def _attack_universal_target(self, target: UniversalTarget) -> Dict[str, Any]:
        """Attack a single target using universal patterns"""
        
        # Try custom URL first if provided
        if target.custom_url:
            url = target.custom_url.replace("{target}", target.name)
            result = await self._try_url(url, target, "custom")
            if result:
                return result
                
        # Try learned patterns first
        platform_key = target.platform.lower()
        if platform_key in self.learned_patterns:
            for pattern in self.learned_patterns[platform_key]:
                url = pattern.replace("{target}", target.name).replace("{platform}", target.platform)
                result = await self._try_url(url, target, "learned")
                if result:
                    return result
                    
        # Try platform-specific intelligence
        if platform_key in self.platform_intelligence:
            patterns = self.platform_intelligence[platform_key]["patterns"]
            for pattern in patterns:
                url = pattern.replace("{target}", target.name)
                result = await self._try_url(url, target, "intelligence")
                if result:
                    # Learn this pattern
                    if platform_key not in self.learned_patterns:
                        self.learned_patterns[platform_key] = []
                    if pattern not in self.learned_patterns[platform_key]:
                        self.learned_patterns[platform_key].append(pattern)
                    return result
                    
        # Try universal patterns
        for pattern_type, patterns in self.universal_patterns.items():
            for pattern in patterns:
                if pattern in self.failed_patterns:
                    continue
                    
                url = pattern.replace("{target}", target.name).replace("{platform}", target.platform)
                result = await self._try_url(url, target, f"universal_{pattern_type}")
                if result:
                    # Learn this pattern
                    if platform_key not in self.learned_patterns:
                        self.learned_patterns[platform_key] = []
                    if pattern not in self.learned_patterns[platform_key]:
                        self.learned_patterns[platform_key].append(pattern)
                    return result
                else:
                    self.failed_patterns.add(pattern)
                    
        return None
        
    async def _try_url(self, url: str, target: UniversalTarget, method: str) -> Dict[str, Any]:
        """Try to fetch data from a URL"""
        try:
            async with self.session.get(url) as response:
                if response.status == 200:
                    content = await response.text()
                    
                    # Check if this looks like real data
                    if self._is_valid_data(content, target.platform):
                        data_size = len(content.encode('utf-8'))
                        
                        # Extract structured data
                        extracted_data = self._extract_data(content, target.platform)
                        
                        return {
                            'target': target.name,
                            'platform': target.platform,
                            'url': url,
                            'method': method,
                            'data_size': data_size,
                            'content': content[:1000],  # First 1000 chars
                            'extracted_data': extracted_data,
                            'timestamp': time.time()
                        }
                        
        except Exception as e:
            pass  # Silent fail, try next pattern
            
        return None
        
    def _is_valid_data(self, content: str, platform: str) -> bool:
        """Check if content contains valid data"""
        if len(content) < 100:  # Too short
            return False
            
        # Platform-specific success indicators
        if platform.lower() in self.platform_intelligence:
            indicators = self.platform_intelligence[platform.lower()]["success_indicators"]
            return any(indicator in content for indicator in indicators)
            
        # Universal success indicators
        success_patterns = [
            r'"title":', r'"name":', r'"content":', r'"text":', r'"data":',
            r'<title>', r'<meta', r'<script', r'<div', r'<span',
            r'api', r'json', r'xml', r'rss', r'feed'
        ]
        
        return any(re.search(pattern, content, re.IGNORECASE) for pattern in success_patterns)
        
    def _extract_data(self, content: str, platform: str) -> Dict[str, Any]:
        """Extract structured data from content"""
        extracted = {}
        
        try:
            # Try JSON first
            if content.strip().startswith('{') or content.strip().startswith('['):
                json_data = json.loads(content)
                extracted['json'] = json_data
                
                # Extract common fields
                if isinstance(json_data, dict):
                    for key in ['title', 'name', 'text', 'content', 'description', 'price', 'value']:
                        if key in json_data:
                            extracted[key] = json_data[key]
                            
        except json.JSONDecodeError:
            pass
            
        # Try HTML parsing
        try:
            soup = BeautifulSoup(content, 'html.parser')
            
            # Extract title
            if soup.title:
                extracted['title'] = soup.title.get_text().strip()
                
            # Extract meta tags
            meta_tags = {}
            for meta in soup.find_all('meta'):
                if meta.get('property'):
                    meta_tags[meta.get('property')] = meta.get('content')
                elif meta.get('name'):
                    meta_tags[meta.get('name')] = meta.get('content')
            extracted['meta'] = meta_tags
            
            # Extract text content
            text_content = soup.get_text()
            if text_content:
                extracted['text_preview'] = text_content[:500].strip()
                
        except Exception:
            pass
            
        return extracted

# Test the universal scanner
async def test_universal_scanner():
    """Test universal scanning across multiple platforms"""
    
    print("🌍 TESTING UNIVERSAL SCANNER")
    print("=" * 60)
    print("If it worked on Twitter, it'll work everywhere!")
    
    # Universal targets across platforms
    targets = [
        # Video platforms
        UniversalTarget("dQw4w9WgXcQ", "youtube"),  # Rick Roll video ID
        UniversalTarget("pewdiepie", "youtube"),    # Channel
        
        # Social platforms  
        UniversalTarget("elonmusk", "twitter"),
        UniversalTarget("BzKGsw7Lzkg", "instagram"),  # Post ID
        
        # Content platforms
        UniversalTarget("programming", "reddit"),
        UniversalTarget("python", "medium"),
        
        # Crypto platforms
        UniversalTarget("bitcoin", "coingecko"),
        UniversalTarget("BTC", "coinmarketcap"),
        
        # News/messaging
        UniversalTarget("durov", "telegram"),
        
        # Custom URL test
        UniversalTarget("test", "custom", "https://httpbin.org/json"),
    ]
    
    async with GreyScanUniversal() as scanner:
        results = await scanner.universal_scan(targets)
        
        print(f"\n🎉 UNIVERSAL RESULTS:")
        print(f"Targets attempted: {len(targets)}")
        print(f"Successful scans: {len(results)}")
        print(f"Success rate: {len(results)/len(targets):.1%}")
        
        if results:
            print(f"\n💎 SUCCESSFUL UNIVERSAL SCANS:")
            for result in results:
                print(f"  ✅ {result['target']} on {result['platform']}")
                print(f"     Method: {result['method']}")
                print(f"     Data size: {result['data_size']} bytes")
                print(f"     URL: {result['url']}")
                if result['extracted_data']:
                    print(f"     Extracted: {list(result['extracted_data'].keys())}")
                print()
                
        # Show learned patterns
        if scanner.learned_patterns:
            print(f"🧠 LEARNED UNIVERSAL PATTERNS:")
            for platform, patterns in scanner.learned_patterns.items():
                print(f"  {platform}: {len(patterns)} patterns")
                for pattern in patterns:
                    print(f"    - {pattern}")
                    
        return results

if __name__ == "__main__":
    asyncio.run(test_universal_scanner())
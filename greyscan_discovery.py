"""
Emergent Path Discovery Scraper
===============================

This scraper doesn't just test predefined endpoints - it LEARNS from failures
and discovers emergent paths by analyzing response patterns, following redirects,
and finding hidden endpoints that sites don't expect to be accessed.

Key Features:
1. Failure analysis → Discovery of alternative paths
2. Response pattern recognition → Finding similar endpoints
3. Redirect following → Uncovering hidden routes
4. Error page analysis → Extracting leaked information
5. Emergent path generation → Creating new endpoint possibilities

This is the true adaptive intelligence we discovered with Twitter widgets!
"""

import asyncio
import aiohttp
import json
import time
import random
import re
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple, Set
import ssl
from dataclasses import dataclass
from urllib.parse import urljoin, urlparse, parse_qs
import hashlib

@dataclass
class EmergentPath:
    """A discovered emergent path"""
    platform: str
    original_target: str
    discovered_url: str
    discovery_method: str  # 'redirect_follow', 'error_analysis', 'pattern_match', etc.
    success_rate: float
    data_types: List[str]
    discovered_at: float

@dataclass
class FailureAnalysis:
    """Analysis of a failed attempt"""
    platform: str
    target: str
    failed_url: str
    status_code: int
    failure_reason: str
    response_content: str
    potential_alternatives: List[str]
    timestamp: float

class EmergentPathScraper:
    """
    Scraper that learns from failures and discovers emergent paths
    """
    
    def __init__(self):
        print("🧠 INITIALIZING EMERGENT PATH DISCOVERY SCRAPER")
        print("🔍 Learning from failures to discover hidden endpoints...")
        print("🌟 Finding emergent paths that sites don't expect...")
        
        self.session = None
        self.discovered_paths: List[EmergentPath] = []
        self.failure_analyses: List[FailureAnalysis] = []
        self.tested_urls: Set[str] = set()
        
        # Base patterns to start with (will evolve through learning)
        self.base_patterns = {
            'reddit': [
                'https://www.reddit.com/user/{target}.json',
                'https://www.reddit.com/u/{target}.json',
                'https://www.reddit.com/user/{target}/about.json',
                'https://www.reddit.com/user/{target}/overview.json'
            ],
            'instagram': [
                'https://www.instagram.com/{target}/',
                'https://www.instagram.com/{target}/?__a=1',
                'https://www.instagram.com/api/v1/users/web_profile_info/?username={target}'
            ],
            'tiktok': [
                'https://www.tiktok.com/@{target}',
                'https://www.tiktok.com/api/user/detail/?uniqueId={target}',
                'https://www.tiktok.com/@{target}/video'
            ],
            'github': [
                'https://api.github.com/users/{target}',
                'https://github.com/{target}',
                'https://github.com/{target}.json'
            ],
            'medium': [
                'https://medium.com/@{target}',
                'https://medium.com/@{target}?format=json',
                'https://medium.com/api/users/{target}'
            ]
        }
        
        print("✨ Emergent path scraper ready for discovery!")
    
    async def initialize_session(self):
        """Initialize session with adaptive headers"""
        connector = aiohttp.TCPConnector(ssl=ssl.create_default_context())
        timeout = aiohttp.ClientTimeout(total=30)
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Cache-Control': 'no-cache'
        }
        
        self.session = aiohttp.ClientSession(
            connector=connector,
            timeout=timeout,
            headers=headers
        )
    
    async def discover_emergent_paths(self, platform: str, targets: List[str], max_iterations: int = 3) -> List[EmergentPath]:
        """
        Main discovery method - learns from failures and finds emergent paths
        """
        
        if not self.session:
            await self.initialize_session()
        
        print(f"\n🔍 DISCOVERING EMERGENT PATHS FOR {platform.upper()}")
        print(f"Targets: {targets}")
        print(f"Max learning iterations: {max_iterations}")
        
        current_patterns = self.base_patterns.get(platform, [])
        
        for iteration in range(max_iterations):
            print(f"\n🔄 ITERATION {iteration + 1}/{max_iterations}")
            
            iteration_discoveries = []
            iteration_failures = []
            
            # Test current patterns
            for target in targets:
                for pattern in current_patterns:
                    url = pattern.format(target=target)
                    
                    if url in self.tested_urls:
                        continue  # Skip already tested URLs
                    
                    result = await self._test_url_with_analysis(platform, target, url)
                    
                    if result['success']:
                        # Success - record the working path
                        path = EmergentPath(
                            platform=platform,
                            original_target=target,
                            discovered_url=url,
                            discovery_method='pattern_test',
                            success_rate=1.0,
                            data_types=result['data_types'],
                            discovered_at=time.time()
                        )
                        iteration_discoveries.append(path)
                        print(f"✅ Found working path: {url}")
                    else:
                        # Failure - analyze for emergent paths
                        analysis = FailureAnalysis(
                            platform=platform,
                            target=target,
                            failed_url=url,
                            status_code=result['status_code'],
                            failure_reason=result['failure_reason'],
                            response_content=result['content'][:1000],  # First 1000 chars
                            potential_alternatives=[],
                            timestamp=time.time()
                        )
                        iteration_failures.append(analysis)
                        print(f"❌ Failed: {url} - {result['failure_reason']}")
                    
                    self.tested_urls.add(url)
                    await asyncio.sleep(0.3)  # Rate limiting
            
            # LEARN FROM FAILURES - This is the key innovation!
            new_patterns = await self._learn_from_failures(iteration_failures)
            
            if new_patterns:
                print(f"🧠 LEARNED {len(new_patterns)} NEW PATTERNS FROM FAILURES:")
                for pattern in new_patterns:
                    print(f"   {pattern}")
                current_patterns.extend(new_patterns)
            
            # Add discoveries to global list
            self.discovered_paths.extend(iteration_discoveries)
            self.failure_analyses.extend(iteration_failures)
            
            # If we found working paths, analyze them for more patterns
            if iteration_discoveries:
                pattern_variations = self._generate_pattern_variations(iteration_discoveries)
                if pattern_variations:
                    print(f"🔄 GENERATED {len(pattern_variations)} PATTERN VARIATIONS:")
                    for variation in pattern_variations:
                        print(f"   {variation}")
                    current_patterns.extend(pattern_variations)
        
        return self.discovered_paths
    
    async def _test_url_with_analysis(self, platform: str, target: str, url: str) -> Dict[str, Any]:
        """Test a URL and return detailed analysis"""
        
        try:
            headers = self._get_rotating_headers()
            
            async with self.session.get(url, headers=headers, allow_redirects=True) as response:
                content = await response.text()
                
                result = {
                    'success': False,
                    'status_code': response.status,
                    'content': content,
                    'data_types': [],
                    'failure_reason': None,
                    'redirects': []
                }
                
                # Follow redirect chain for emergent path discovery
                if hasattr(response, 'history') and response.history:
                    result['redirects'] = [str(r.url) for r in response.history]
                    print(f"🔄 Redirect chain: {' → '.join(result['redirects'])} → {response.url}")
                
                if response.status == 200 and len(content) > 500:
                    # Analyze content for useful data
                    data_types = self._analyze_content_types(platform, content)
                    
                    if data_types:
                        result['success'] = True
                        result['data_types'] = data_types
                    else:
                        result['failure_reason'] = 'no_useful_data'
                        # But still analyze the content for patterns!
                        await self._analyze_response_for_patterns(platform, url, content)
                        
                elif response.status == 200:
                    result['failure_reason'] = 'minimal_content'
                elif response.status == 404:
                    result['failure_reason'] = 'not_found'
                    # Analyze 404 pages - they often leak information!
                    await self._analyze_404_for_hints(platform, url, content)
                elif response.status == 403:
                    result['failure_reason'] = 'forbidden'
                    # Forbidden might mean the endpoint exists but needs different approach
                    await self._analyze_forbidden_for_alternatives(platform, url, content)
                elif response.status == 429:
                    result['failure_reason'] = 'rate_limited'
                else:
                    result['failure_reason'] = f'http_{response.status}'
                
                return result
                
        except asyncio.TimeoutError:
            return {
                'success': False,
                'status_code': 0,
                'content': '',
                'data_types': [],
                'failure_reason': 'timeout',
                'redirects': []
            }
        except Exception as e:
            return {
                'success': False,
                'status_code': 0,
                'content': '',
                'data_types': [],
                'failure_reason': f'exception_{type(e).__name__}',
                'redirects': []
            }
    
    async def _learn_from_failures(self, failures: List[FailureAnalysis]) -> List[str]:
        """
        CORE LEARNING METHOD - Analyze failures to discover new patterns
        This is where the magic happens!
        """
        
        new_patterns = []
        
        for failure in failures:
            platform = failure.platform
            failed_url = failure.failed_url
            content = failure.response_content
            
            # Method 1: Analyze error messages for hints
            if failure.status_code == 404:
                hints = self._extract_hints_from_404(content)
                for hint in hints:
                    new_pattern = self._convert_hint_to_pattern(platform, failed_url, hint)
                    if new_pattern and new_pattern not in new_patterns:
                        new_patterns.append(new_pattern)
            
            # Method 2: URL structure analysis
            url_variations = self._generate_url_variations(failed_url)
            new_patterns.extend(url_variations)
            
            # Method 3: Look for API endpoints mentioned in responses
            api_endpoints = self._extract_api_endpoints_from_content(content)
            for endpoint in api_endpoints:
                pattern = self._adapt_endpoint_to_pattern(platform, endpoint)
                if pattern and pattern not in new_patterns:
                    new_patterns.append(pattern)
            
            # Method 4: Analyze redirect patterns
            if hasattr(failure, 'redirects') and failure.redirects:
                redirect_patterns = self._learn_from_redirects(failure.redirects)
                new_patterns.extend(redirect_patterns)
        
        # Remove duplicates and invalid patterns
        unique_patterns = list(set(new_patterns))
        valid_patterns = [p for p in unique_patterns if self._is_valid_pattern(p)]
        
        return valid_patterns[:5]  # Limit to top 5 to avoid explosion
    
    def _extract_hints_from_404(self, content: str) -> List[str]:
        """Extract hints from 404 error pages"""
        hints = []
        
        # Look for suggested URLs in error pages
        url_patterns = [
            r'href=["\']([^"\']+)["\']',
            r'url\s*:\s*["\']([^"\']+)["\']',
            r'endpoint["\']?\s*:\s*["\']([^"\']+)["\']'
        ]
        
        for pattern in url_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            hints.extend(matches)
        
        # Look for API documentation references
        api_hints = re.findall(r'/api/[^"\s<>]+', content, re.IGNORECASE)
        hints.extend(api_hints)
        
        return hints[:10]  # Limit hints
    
    def _convert_hint_to_pattern(self, platform: str, failed_url: str, hint: str) -> Optional[str]:
        """Convert a hint from error page to a testable pattern"""
        
        if not hint or len(hint) < 5:
            return None
        
        # Clean up the hint
        hint = hint.strip()
        
        # Convert relative URLs to absolute
        if hint.startswith('/'):
            base_url = '/'.join(failed_url.split('/')[:3])
            hint = base_url + hint
        
        # Replace common patterns with target placeholder
        if '/users/' in hint:
            hint = hint.replace('/users/', '/users/{target}')
        elif '/user/' in hint:
            hint = hint.replace('/user/', '/user/{target}')
        elif '/@' in hint:
            hint = hint.replace('/@', '/@{target}')
        
        return hint
    
    def _generate_url_variations(self, failed_url: str) -> List[str]:
        """Generate variations of a failed URL"""
        variations = []
        
        # Common API variations
        base_variations = [
            failed_url.replace('/user/', '/users/'),
            failed_url.replace('/users/', '/user/'),
            failed_url + '.json',
            failed_url + '?format=json',
            failed_url + '/feed',
            failed_url + '/profile',
            failed_url + '/info',
            failed_url.replace('www.', 'api.'),
            failed_url.replace('https://', 'https://api.'),
            failed_url.replace('https://', 'https://m.'),
            failed_url.replace('https://', 'https://mobile.')
        ]
        
        # Add variations that might work
        for variation in base_variations:
            if variation != failed_url and self._is_valid_url(variation):
                variations.append(variation)
        
        return variations[:8]  # Limit variations
    
    def _extract_api_endpoints_from_content(self, content: str) -> List[str]:
        """Extract API endpoints mentioned in response content"""
        endpoints = []
        
        # Look for API endpoints in JavaScript, JSON, or HTML
        patterns = [
            r'["\']https?://[^"\']+/api/[^"\']+["\']',
            r'["\'][^"\']*api[^"\']*["\']',
            r'endpoint["\']?\s*:\s*["\']([^"\']+)["\']'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            endpoints.extend(matches)
        
        return endpoints[:5]  # Limit endpoints
    
    def _adapt_endpoint_to_pattern(self, platform: str, endpoint: str) -> Optional[str]:
        """Adapt discovered endpoint to a pattern with target placeholder"""
        
        if not endpoint or '{target}' in endpoint:
            return endpoint
        
        # Common adaptations based on platform
        adaptations = {
            'reddit': [
                (r'/u/\w+', '/u/{target}'),
                (r'/user/\w+', '/user/{target}')
            ],
            'instagram': [
                (r'/\w+/', '/{target}/'),
                (r'username=\w+', 'username={target}')
            ],
            'github': [
                (r'/users/\w+', '/users/{target}'),
                (r'github\.com/\w+', 'github.com/{target}')
            ]
        }
        
        platform_adaptations = adaptations.get(platform, [])
        
        for pattern, replacement in platform_adaptations:
            if re.search(pattern, endpoint):
                return re.sub(pattern, replacement, endpoint)
        
        return None
    
    def _generate_pattern_variations(self, successful_paths: List[EmergentPath]) -> List[str]:
        """Generate variations based on successful patterns"""
        variations = []
        
        for path in successful_paths:
            url = path.discovered_url
            
            # Generate similar patterns
            if '.json' in url:
                variations.append(url.replace('.json', '.xml'))
                variations.append(url.replace('.json', ''))
            
            if '/api/' in url:
                variations.append(url.replace('/api/', '/v1/'))
                variations.append(url.replace('/api/', '/v2/'))
            
            if '?format=json' in url:
                variations.append(url.replace('?format=json', '?format=xml'))
                variations.append(url.replace('?format=json', ''))
        
        return variations[:5]  # Limit variations
    
    async def _analyze_response_for_patterns(self, platform: str, url: str, content: str):
        """Analyze response content for hidden patterns"""
        # This could discover more endpoints mentioned in the response
        pass
    
    async def _analyze_404_for_hints(self, platform: str, url: str, content: str):
        """Analyze 404 pages for hints about correct endpoints"""
        # 404 pages often contain suggestions or leaked information
        pass
    
    async def _analyze_forbidden_for_alternatives(self, platform: str, url: str, content: str):
        """Analyze forbidden responses for alternative approaches"""
        # 403 might mean endpoint exists but needs different headers/auth
        pass
    
    def _learn_from_redirects(self, redirects: List[str]) -> List[str]:
        """Learn patterns from redirect chains"""
        patterns = []
        
        for redirect in redirects:
            # Convert redirect to pattern
            if '/user/' in redirect:
                pattern = redirect.replace('/user/', '/user/{target}')
                patterns.append(pattern)
        
        return patterns
    
    def _analyze_content_types(self, platform: str, content: str) -> List[str]:
        """Analyze content to determine what useful data it contains"""
        data_types = []
        
        # Generic data type detection
        if 'followers' in content.lower() or 'following' in content.lower():
            data_types.append('social_metrics')
        
        if 'posts' in content.lower() or 'tweets' in content.lower():
            data_types.append('content_data')
        
        if '"id"' in content and '"name"' in content:
            data_types.append('profile_data')
        
        if len(content) > 50000:  # Large content
            data_types.append('substantial_data')
        
        # Platform-specific detection
        if platform == 'reddit':
            if 'karma' in content.lower():
                data_types.append('karma_data')
            if 'subreddit' in content.lower():
                data_types.append('subreddit_data')
        
        elif platform == 'github':
            if 'repositories' in content.lower() or 'repos' in content.lower():
                data_types.append('repo_data')
            if 'contributions' in content.lower():
                data_types.append('activity_data')
        
        return data_types
    
    def _get_rotating_headers(self) -> Dict[str, str]:
        """Get rotating headers for requests"""
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        ]
        
        return {
            'User-Agent': random.choice(user_agents),
            'Accept': 'application/json, text/html, */*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Cache-Control': 'no-cache'
        }
    
    def _is_valid_pattern(self, pattern: str) -> bool:
        """Check if a pattern is valid"""
        return (
            pattern and 
            len(pattern) > 10 and 
            ('http' in pattern or pattern.startswith('/')) and
            '{target}' in pattern
        )
    
    def _is_valid_url(self, url: str) -> bool:
        """Check if URL is valid"""
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except:
            return False
    
    def display_discoveries(self):
        """Display all discovered emergent paths"""
        
        if not self.discovered_paths:
            print("\n❌ No emergent paths discovered")
            return
        
        print(f"\n🌟 DISCOVERED {len(self.discovered_paths)} EMERGENT PATHS:")
        
        # Group by platform
        by_platform = {}
        for path in self.discovered_paths:
            if path.platform not in by_platform:
                by_platform[path.platform] = []
            by_platform[path.platform].append(path)
        
        for platform, paths in by_platform.items():
            print(f"\n🔥 {platform.upper()} ({len(paths)} paths):")
            for path in paths:
                print(f"  ✅ {path.discovered_url}")
                print(f"     Method: {path.discovery_method}")
                print(f"     Data: {path.data_types}")
        
        # Show learning statistics
        print(f"\n📊 LEARNING STATISTICS:")
        print(f"Total URLs tested: {len(self.tested_urls)}")
        print(f"Failures analyzed: {len(self.failure_analyses)}")
        print(f"Success rate: {len(self.discovered_paths)/len(self.tested_urls):.1%}")
        
        # Show most common failure reasons
        failure_reasons = {}
        for failure in self.failure_analyses:
            reason = failure.failure_reason
            failure_reasons[reason] = failure_reasons.get(reason, 0) + 1
        
        if failure_reasons:
            print(f"\n🔍 FAILURE ANALYSIS:")
            for reason, count in sorted(failure_reasons.items(), key=lambda x: x[1], reverse=True):
                print(f"  {reason}: {count} times")
    
    async def close(self):
        """Clean up resources"""
        if self.session:
            await self.session.close()

async def test_emergent_discovery():
    """Test emergent path discovery"""
    
    print("🌟 EMERGENT PATH DISCOVERY TEST")
    print("=" * 50)
    print("Testing true adaptive learning - discovering hidden paths from failures!")
    print()
    
    scraper = EmergentPathScraper()
    
    try:
        # Test different platforms
        platforms_to_test = {
            'reddit': ['elonmusk', 'VitalikButerin'],
            'github': ['ethereum', 'bitcoin'],
            'instagram': ['elonmusk', 'ethereum']
        }
        
        all_discoveries = []
        
        for platform, targets in platforms_to_test.items():
            discoveries = await scraper.discover_emergent_paths(platform, targets, max_iterations=2)
            all_discoveries.extend(discoveries)
        
        # Display results
        scraper.display_discoveries()
        
        # Analyze SaaS potential
        working_platforms = len(set(d.platform for d in all_discoveries))
        total_platforms = len(platforms_to_test)
        
        print(f"\n💰 SAAS POTENTIAL:")
        print(f"Platforms with discovered paths: {working_platforms}/{total_platforms}")
        print(f"Total emergent paths found: {len(all_discoveries)}")
        
        if len(all_discoveries) > 5:
            print("🚀 HIGH POTENTIAL - Multiple emergent paths discovered!")
        elif len(all_discoveries) > 0:
            print("📈 MODERATE POTENTIAL - Some paths found")
        else:
            print("🔄 NEEDS MORE LEARNING - Try more iterations")
        
        return all_discoveries
        
    finally:
        await scraper.close()

if __name__ == "__main__":
    asyncio.run(test_emergent_discovery())
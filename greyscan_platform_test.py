"""
Multi-Platform Adaptive Scraper Test
====================================

Testing our adaptive learning approach on multiple platforms to discover
new bypasses and data sources. This could be the foundation of a major SaaS tool!

Platforms to test:
- Reddit (various endpoints)
- LinkedIn (public profiles)
- Instagram (public data)
- TikTok (public profiles)
- YouTube (channel data)
- GitHub (public repos)
- Medium (public articles)
"""

import asyncio
import aiohttp
import json
import time
import random
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple
import ssl
from dataclasses import dataclass
import re

@dataclass
class PlatformAttempt:
    """Track attempts across different platforms"""
    platform: str
    target: str
    method: str
    success: bool
    status_code: Optional[int]
    data_size: int
    response_time: float
    failure_reason: Optional[str]
    data_found: List[str]
    timestamp: float

class MultiPlatformScraper:
    """
    Adaptive scraper that learns optimal methods for each platform
    """
    
    def __init__(self):
        print("🌐 INITIALIZING MULTI-PLATFORM ADAPTIVE SCRAPER")
        print("🧠 Testing adaptive learning across platforms...")
        print("💰 Exploring SaaS potential...")
        
        self.session = None
        self.attempt_history: List[PlatformAttempt] = []
        
        # Platform configurations discovered through learning
        self.platform_methods = {
            'reddit': {
                'json_api': 'https://www.reddit.com/user/{target}.json',
                'rss_feed': 'https://www.reddit.com/user/{target}.rss',
                'about_page': 'https://www.reddit.com/user/{target}/about.json'
            },
            'linkedin': {
                'public_profile': 'https://www.linkedin.com/in/{target}',
                'company_page': 'https://www.linkedin.com/company/{target}',
                'posts_feed': 'https://www.linkedin.com/in/{target}/recent-activity'
            },
            'instagram': {
                'public_profile': 'https://www.instagram.com/{target}/',
                'embed_api': 'https://www.instagram.com/p/{target}/embed/',
                'media_info': 'https://www.instagram.com/{target}/?__a=1'
            },
            'tiktok': {
                'public_profile': 'https://www.tiktok.com/@{target}',
                'embed_api': 'https://www.tiktok.com/oembed?url=https://www.tiktok.com/@{target}',
                'rss_alternative': 'https://www.tiktok.com/@{target}/rss'
            },
            'youtube': {
                'channel_page': 'https://www.youtube.com/c/{target}',
                'channel_id': 'https://www.youtube.com/channel/{target}',
                'rss_feed': 'https://www.youtube.com/feeds/videos.xml?channel_id={target}',
                'about_page': 'https://www.youtube.com/c/{target}/about'
            },
            'github': {
                'user_api': 'https://api.github.com/users/{target}',
                'repos_api': 'https://api.github.com/users/{target}/repos',
                'profile_page': 'https://github.com/{target}',
                'contributions': 'https://github.com/{target}/contributions'
            },
            'medium': {
                'user_profile': 'https://medium.com/@{target}',
                'user_feed': 'https://medium.com/feed/@{target}',
                'user_api': 'https://medium.com/@{target}?format=json'
            }
        }
        
        print("✨ Multi-platform scraper ready for discovery!")
    
    async def initialize_session(self):
        """Initialize session with rotating headers"""
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
    
    async def test_all_platforms(self) -> Dict[str, Any]:
        """Test adaptive scraping across all platforms"""
        
        if not self.session:
            await self.initialize_session()
        
        # Test targets for each platform
        test_targets = {
            'reddit': ['elonmusk', 'VitalikButerin', 'bitcoin', 'ethereum'],
            'linkedin': ['elonmusk', 'vitalik-buterin', 'microsoft', 'google'],
            'instagram': ['elonmusk', 'ethereum', 'bitcoin', 'crypto'],
            'tiktok': ['elonmusk', 'crypto', 'bitcoin', 'ethereum'],
            'youtube': ['elonmusk', 'ethereum', 'bitcoin', 'coindesk'],
            'github': ['ethereum', 'bitcoin', 'microsoft', 'google'],
            'medium': ['vitalikbuterin', 'ethereum', 'bitcoin', 'crypto']
        }
        
        results = {}
        
        for platform, targets in test_targets.items():
            print(f"\n🔍 TESTING {platform.upper()}...")
            platform_results = await self._test_platform(platform, targets)
            results[platform] = platform_results
            
            # Short delay between platforms
            await asyncio.sleep(1)
        
        # Analyze cross-platform patterns
        self._analyze_cross_platform_patterns()
        
        return results
    
    async def _test_platform(self, platform: str, targets: List[str]) -> Dict[str, Any]:
        """Test all methods for a specific platform"""
        
        platform_results = {
            'total_attempts': 0,
            'successful_attempts': 0,
            'working_methods': [],
            'failed_methods': [],
            'discovered_data': []
        }
        
        methods = self.platform_methods.get(platform, {})
        
        for target in targets[:2]:  # Test first 2 targets to avoid rate limits
            for method_name, url_template in methods.items():
                
                attempt = await self._test_method(platform, target, method_name, url_template)
                self.attempt_history.append(attempt)
                platform_results['total_attempts'] += 1
                
                if attempt.success:
                    platform_results['successful_attempts'] += 1
                    if method_name not in platform_results['working_methods']:
                        platform_results['working_methods'].append(method_name)
                    
                    platform_results['discovered_data'].append({
                        'target': target,
                        'method': method_name,
                        'data_size': attempt.data_size,
                        'data_found': attempt.data_found
                    })
                    
                    print(f"✅ {platform}/{method_name}: {target} - {attempt.data_size} bytes")
                else:
                    if method_name not in platform_results['failed_methods']:
                        platform_results['failed_methods'].append(method_name)
                    print(f"❌ {platform}/{method_name}: {target} - {attempt.failure_reason}")
                
                # Small delay between requests
                await asyncio.sleep(0.5)
        
        success_rate = platform_results['successful_attempts'] / platform_results['total_attempts'] if platform_results['total_attempts'] > 0 else 0
        platform_results['success_rate'] = success_rate
        
        print(f"📊 {platform.upper()} Results: {success_rate:.1%} success rate ({platform_results['successful_attempts']}/{platform_results['total_attempts']})")
        
        return platform_results
    
    async def _test_method(self, platform: str, target: str, method_name: str, url_template: str) -> PlatformAttempt:
        """Test a specific method on a platform"""
        
        start_time = time.time()
        url = url_template.format(target=target)
        
        attempt = PlatformAttempt(
            platform=platform,
            target=target,
            method=method_name,
            success=False,
            status_code=None,
            data_size=0,
            response_time=0.0,
            failure_reason=None,
            data_found=[],
            timestamp=time.time()
        )
        
        try:
            # Rotate headers for each request
            headers = self._get_rotating_headers()
            
            async with self.session.get(url, headers=headers) as response:
                attempt.status_code = response.status
                attempt.response_time = time.time() - start_time
                
                if response.status == 200:
                    content = await response.text()
                    attempt.data_size = len(content)
                    
                    if len(content) > 500:  # Has substantial content
                        # Extract useful data based on platform
                        data_found = self._extract_platform_data(platform, content)
                        
                        if data_found:
                            attempt.success = True
                            attempt.data_found = data_found
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
                else:
                    attempt.failure_reason = f"http_{response.status}"
                    
        except asyncio.TimeoutError:
            attempt.failure_reason = "timeout"
            attempt.response_time = time.time() - start_time
        except Exception as e:
            attempt.failure_reason = f"exception_{type(e).__name__}"
            attempt.response_time = time.time() - start_time
        
        return attempt
    
    def _get_rotating_headers(self) -> Dict[str, str]:
        """Get rotating headers for each request"""
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        ]
        
        return {
            'User-Agent': random.choice(user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Cache-Control': 'no-cache'
        }
    
    def _extract_platform_data(self, platform: str, content: str) -> List[str]:
        """Extract useful data based on platform type"""
        
        data_found = []
        
        if platform == 'reddit':
            # Look for karma, posts, comments
            if '"comment_karma"' in content or '"link_karma"' in content:
                data_found.append('karma_data')
            if '"subreddit"' in content:
                data_found.append('subreddit_data')
                
        elif platform == 'linkedin':
            # Look for profile info, connections
            if 'connections' in content.lower() or 'followers' in content.lower():
                data_found.append('connection_data')
            if 'experience' in content.lower() or 'education' in content.lower():
                data_found.append('profile_data')
                
        elif platform == 'instagram':
            # Look for followers, posts
            if 'followers' in content.lower() or 'following' in content.lower():
                data_found.append('follower_data')
            if 'posts' in content.lower() or 'media' in content.lower():
                data_found.append('media_data')
                
        elif platform == 'tiktok':
            # Look for followers, videos
            if 'followers' in content.lower() or 'likes' in content.lower():
                data_found.append('engagement_data')
            if 'video' in content.lower():
                data_found.append('video_data')
                
        elif platform == 'youtube':
            # Look for subscribers, videos
            if 'subscribers' in content.lower() or 'views' in content.lower():
                data_found.append('channel_stats')
            if 'video' in content.lower() or 'playlist' in content.lower():
                data_found.append('content_data')
                
        elif platform == 'github':
            # Look for repos, contributions
            if '"public_repos"' in content or '"followers"' in content:
                data_found.append('profile_stats')
            if '"name"' in content and '"description"' in content:
                data_found.append('repo_data')
                
        elif platform == 'medium':
            # Look for articles, followers
            if 'followers' in content.lower() or 'following' in content.lower():
                data_found.append('social_data')
            if 'article' in content.lower() or 'story' in content.lower():
                data_found.append('content_data')
        
        # Generic data indicators
        if len(content) > 10000:  # Large content = likely useful
            data_found.append('substantial_content')
        
        if any(keyword in content.lower() for keyword in ['api', 'json', 'data']):
            data_found.append('structured_data')
        
        return data_found
    
    def _analyze_cross_platform_patterns(self):
        """Analyze patterns across all platforms"""
        
        print(f"\n🧠 CROSS-PLATFORM ANALYSIS:")
        print(f"Total attempts across all platforms: {len(self.attempt_history)}")
        
        # Success rates by platform
        platform_stats = {}
        for attempt in self.attempt_history:
            platform = attempt.platform
            if platform not in platform_stats:
                platform_stats[platform] = {'total': 0, 'success': 0}
            platform_stats[platform]['total'] += 1
            if attempt.success:
                platform_stats[platform]['success'] += 1
        
        print(f"\n📊 SUCCESS RATES BY PLATFORM:")
        for platform, stats in platform_stats.items():
            rate = stats['success'] / stats['total'] if stats['total'] > 0 else 0
            print(f"  {platform}: {rate:.1%} ({stats['success']}/{stats['total']})")
        
        # Most successful methods
        method_stats = {}
        for attempt in self.attempt_history:
            if attempt.success:
                key = f"{attempt.platform}_{attempt.method}"
                method_stats[key] = method_stats.get(key, 0) + 1
        
        if method_stats:
            print(f"\n🔥 MOST SUCCESSFUL METHODS:")
            for method, count in sorted(method_stats.items(), key=lambda x: x[1], reverse=True)[:5]:
                print(f"  {method}: {count} successes")
        
        # Common failure reasons
        failure_stats = {}
        for attempt in self.attempt_history:
            if not attempt.success and attempt.failure_reason:
                failure_stats[attempt.failure_reason] = failure_stats.get(attempt.failure_reason, 0) + 1
        
        if failure_stats:
            print(f"\n❌ COMMON FAILURE REASONS:")
            for reason, count in sorted(failure_stats.items(), key=lambda x: x[1], reverse=True)[:5]:
                print(f"  {reason}: {count} times")
    
    async def close(self):
        """Clean up resources"""
        if self.session:
            await self.session.close()

async def test_multi_platform():
    """Test the multi-platform adaptive scraper"""
    
    print("🌐 MULTI-PLATFORM ADAPTIVE SCRAPER TEST")
    print("=" * 60)
    print("Testing if our adaptive learning approach works on other platforms...")
    print("This could be the foundation of a major SaaS tool! 💰")
    print()
    
    scraper = MultiPlatformScraper()
    
    try:
        results = await scraper.test_all_platforms()
        
        print(f"\n🎯 OVERALL RESULTS:")
        
        total_platforms = len(results)
        working_platforms = sum(1 for r in results.values() if r['success_rate'] > 0)
        
        print(f"Platforms tested: {total_platforms}")
        print(f"Platforms with working methods: {working_platforms}")
        print(f"Overall platform success rate: {working_platforms/total_platforms:.1%}")
        
        # Show best performing platforms
        print(f"\n🏆 BEST PERFORMING PLATFORMS:")
        sorted_platforms = sorted(results.items(), key=lambda x: x[1]['success_rate'], reverse=True)
        
        for platform, data in sorted_platforms[:3]:
            if data['success_rate'] > 0:
                print(f"\n{platform.upper()}:")
                print(f"  Success rate: {data['success_rate']:.1%}")
                print(f"  Working methods: {data['working_methods']}")
                print(f"  Data discovered: {len(data['discovered_data'])} items")
        
        # SaaS potential analysis
        viable_platforms = [p for p, d in results.items() if d['success_rate'] > 0.3]
        
        print(f"\n💰 SAAS POTENTIAL ANALYSIS:")
        print(f"Viable platforms for SaaS: {len(viable_platforms)}")
        print(f"Platforms: {viable_platforms}")
        
        if len(viable_platforms) >= 3:
            print("🚀 HIGH SaaS POTENTIAL - Multiple platforms working!")
        elif len(viable_platforms) >= 1:
            print("📈 MODERATE SaaS POTENTIAL - Some platforms working")
        else:
            print("🔄 LEARNING PHASE - Need more adaptation")
        
        return results
        
    finally:
        await scraper.close()

if __name__ == "__main__":
    asyncio.run(test_multi_platform())
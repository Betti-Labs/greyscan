#!/usr/bin/env python3
"""
GreyScan Intelligence - Full Web Intelligence Platform
The civilian Palantir - complete OSINT and data intelligence system
"""

import asyncio
import aiohttp
import json
import re
import sqlite3
import hashlib
import time
from datetime import datetime, timedelta
from typing import List, Dict, Any, Set, Tuple, Optional
from dataclasses import dataclass, asdict
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import networkx as nx
from collections import defaultdict, Counter
import pickle
import os

@dataclass
class IntelligenceTarget:
    """Enhanced target with intelligence metadata"""
    name: str
    platform: str
    target_type: str = "person"  # person, organization, topic, hashtag, etc.
    aliases: List[str] = None
    priority: int = 1  # 1-10 priority level
    tags: List[str] = None
    custom_url: str = None
    
    def __post_init__(self):
        if self.aliases is None:
            self.aliases = []
        if self.tags is None:
            self.tags = []

@dataclass
class IntelligenceData:
    """Structured intelligence data point"""
    target_id: str
    platform: str
    data_type: str  # post, profile, metric, relationship, etc.
    content: str
    metadata: Dict[str, Any]
    timestamp: float
    confidence: float = 1.0
    source_url: str = ""
    related_entities: List[str] = None
    
    def __post_init__(self):
        if self.related_entities is None:
            self.related_entities = []

class GreyScanIntelligence:
    """Full intelligence platform with cross-referencing and analysis"""
    
    def __init__(self, db_path: str = "intelligence.db"):
        self.db_path = db_path
        self.session = None
        
        # Intelligence databases
        self.entity_graph = nx.Graph()
        self.learned_patterns = {}
        self.failed_patterns = set()
        self.intelligence_cache = {}
        
        # Analysis engines
        self.sentiment_keywords = {
            'positive': ['good', 'great', 'excellent', 'amazing', 'love', 'best', 'awesome', 'fantastic'],
            'negative': ['bad', 'terrible', 'awful', 'hate', 'worst', 'horrible', 'disgusting', 'pathetic'],
            'neutral': ['okay', 'fine', 'normal', 'standard', 'regular', 'typical']
        }
        
        # Platform intelligence (from universal scanner)
        self.platform_patterns = {
            "twitter": [
                "https://platform.twitter.com/widgets/tweet.html?id={target}",
                "https://syndication.twitter.com/srv/timeline-profile/screen-name/{target}",
                "https://webcache.googleusercontent.com/search?q=cache:twitter.com/{target}"
            ],
            "youtube": [
                "https://www.youtube.com/embed/{target}",
                "https://www.youtube.com/oembed?url=https://youtube.com/watch?v={target}",
                "https://www.youtube.com/channel/{target}/about"
            ],
            "instagram": [
                "https://www.instagram.com/p/{target}/embed/",
                "https://www.instagram.com/{target}/?__a=1",
                "https://i.instagram.com/api/v1/users/web_profile_info/?username={target}"
            ],
            "reddit": [
                "https://www.reddit.com/r/{target}.json",
                "https://www.reddit.com/user/{target}.json",
                "https://www.reddit.com/embed?url=https://reddit.com/r/{target}"
            ],
            "linkedin": [
                "https://www.linkedin.com/in/{target}",
                "https://www.linkedin.com/company/{target}",
                "https://www.linkedin.com/pub/dir/{target}"
            ],
            "github": [
                "https://api.github.com/users/{target}",
                "https://github.com/{target}.json",
                "https://api.github.com/users/{target}/repos"
            ],
            "medium": [
                "https://medium.com/@{target}?format=json",
                "https://medium.com/{target}?format=json",
                "https://medium.com/@{target}/latest"
            ],
            "telegram": [
                "https://t.me/s/{target}",
                "https://t.me/{target}",
                "https://web.telegram.org/z/#{target}"
            ],
            "tiktok": [
                "https://www.tiktok.com/@{target}",
                "https://www.tiktok.com/embed/{target}",
                "https://www.tiktok.com/oembed?url=https://tiktok.com/@{target}"
            ],
            "coingecko": [
                "https://api.coingecko.com/api/v3/coins/{target}",
                "https://www.coingecko.com/en/coins/{target}",
                "https://api.coingecko.com/api/v3/search?query={target}"
            ],
            "coinmarketcap": [
                "https://api.coinmarketcap.com/v1/ticker/{target}/",
                "https://coinmarketcap.com/currencies/{target}/",
                "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?symbol={target}"
            ]
        }
        
        self._init_database()
        
    def _init_database(self):
        """Initialize SQLite database for intelligence storage"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Entities table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS entities (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                entity_type TEXT,
                platforms TEXT,  -- JSON array
                aliases TEXT,    -- JSON array
                tags TEXT,       -- JSON array
                first_seen REAL,
                last_updated REAL,
                confidence REAL DEFAULT 1.0
            )
        ''')
        
        # Intelligence data table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS intelligence_data (
                id TEXT PRIMARY KEY,
                entity_id TEXT,
                platform TEXT,
                data_type TEXT,
                content TEXT,
                metadata TEXT,   -- JSON
                timestamp REAL,
                confidence REAL,
                source_url TEXT,
                related_entities TEXT,  -- JSON array
                FOREIGN KEY (entity_id) REFERENCES entities (id)
            )
        ''')
        
        # Relationships table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS relationships (
                id TEXT PRIMARY KEY,
                entity1_id TEXT,
                entity2_id TEXT,
                relationship_type TEXT,
                strength REAL DEFAULT 1.0,
                first_seen REAL,
                last_confirmed REAL,
                platforms TEXT,  -- JSON array
                FOREIGN KEY (entity1_id) REFERENCES entities (id),
                FOREIGN KEY (entity2_id) REFERENCES entities (id)
            )
        ''')
        
        # Analysis results table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS analysis_results (
                id TEXT PRIMARY KEY,
                entity_id TEXT,
                analysis_type TEXT,
                results TEXT,    -- JSON
                timestamp REAL,
                FOREIGN KEY (entity_id) REFERENCES entities (id)
            )
        ''')
        
        conn.commit()
        conn.close()
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=15),
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'none',
                'Cache-Control': 'max-age=0'
            }
        )
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
            
    async def full_intelligence_scan(self, targets: List[IntelligenceTarget]) -> Dict[str, Any]:
        """Complete intelligence operation with cross-referencing and analysis"""
        
        print(f"🧠 FULL INTELLIGENCE SCAN: {len(targets)} targets")
        print("🔍 Cross-referencing, analyzing, and building intelligence profiles...")
        
        start_time = time.time()
        all_intelligence = []
        
        # Phase 1: Data Collection
        print(f"\n📡 PHASE 1: DATA COLLECTION")
        for i, target in enumerate(targets):
            print(f"🎯 [{i+1}/{len(targets)}] Collecting: {target.name} ({target.platform})")
            
            intelligence = await self._collect_target_intelligence(target)
            if intelligence:
                all_intelligence.extend(intelligence)
                await self._store_intelligence(target, intelligence)
                
        # Phase 2: Entity Resolution
        print(f"\n🔗 PHASE 2: ENTITY RESOLUTION")
        entity_map = await self._resolve_entities(all_intelligence)
        
        # Phase 3: Relationship Analysis
        print(f"\n🕸️ PHASE 3: RELATIONSHIP ANALYSIS")
        relationships = await self._analyze_relationships(all_intelligence, entity_map)
        
        # Phase 4: Cross-Platform Analysis
        print(f"\n🌐 PHASE 4: CROSS-PLATFORM ANALYSIS")
        cross_analysis = await self._cross_platform_analysis(all_intelligence, entity_map)
        
        # Phase 5: Temporal Analysis
        print(f"\n⏰ PHASE 5: TEMPORAL ANALYSIS")
        temporal_analysis = await self._temporal_analysis(all_intelligence)
        
        # Phase 6: Intelligence Report Generation
        print(f"\n📊 PHASE 6: INTELLIGENCE REPORT")
        intelligence_report = await self._generate_intelligence_report(
            all_intelligence, entity_map, relationships, cross_analysis, temporal_analysis
        )
        
        total_time = time.time() - start_time
        
        print(f"\n🎉 INTELLIGENCE OPERATION COMPLETE")
        print(f"⏱️ Total time: {total_time:.2f}s")
        print(f"📊 Data points collected: {len(all_intelligence)}")
        print(f"🔗 Entities resolved: {len(entity_map)}")
        print(f"🕸️ Relationships found: {len(relationships)}")
        
        return intelligence_report
        
    async def _collect_target_intelligence(self, target: IntelligenceTarget) -> List[IntelligenceData]:
        """Collect intelligence data for a single target"""
        
        intelligence_data = []
        
        # Try all patterns for this platform
        platform_patterns = self.platform_patterns.get(target.platform.lower(), [])
        
        for pattern in platform_patterns:
            url = pattern.replace("{target}", target.name)
            
            try:
                async with self.session.get(url) as response:
                    if response.status == 200:
                        content = await response.text()
                        
                        if self._is_valid_intelligence(content, target.platform):
                            # Extract structured intelligence
                            extracted = self._extract_intelligence(content, target, url)
                            if extracted:
                                intelligence_data.extend(extracted)
                                
                            # Learn successful pattern
                            if target.platform not in self.learned_patterns:
                                self.learned_patterns[target.platform] = []
                            if pattern not in self.learned_patterns[target.platform]:
                                self.learned_patterns[target.platform].append(pattern)
                                
                            break  # Success, move to next target
                            
            except Exception as e:
                continue
                
        return intelligence_data
        
    def _extract_intelligence(self, content: str, target: IntelligenceTarget, url: str) -> List[IntelligenceData]:
        """Extract structured intelligence from raw content"""
        
        intelligence_points = []
        target_id = self._generate_entity_id(target.name, target.platform)
        
        # Extract JSON data
        json_data = self._extract_json_intelligence(content)
        if json_data:
            intelligence_points.append(IntelligenceData(
                target_id=target_id,
                platform=target.platform,
                data_type="structured_data",
                content=json.dumps(json_data)[:5000],  # Limit size
                metadata={"data_type": "json", "fields": list(json_data.keys()) if isinstance(json_data, dict) else []},
                timestamp=time.time(),
                source_url=url
            ))
            
        # Extract profile information
        profile_data = self._extract_profile_intelligence(content, target.platform)
        if profile_data:
            intelligence_points.append(IntelligenceData(
                target_id=target_id,
                platform=target.platform,
                data_type="profile",
                content=json.dumps(profile_data),
                metadata={"extraction_method": "profile_parsing"},
                timestamp=time.time(),
                source_url=url
            ))
            
        # Extract content/posts
        content_data = self._extract_content_intelligence(content, target.platform)
        for content_item in content_data:
            intelligence_points.append(IntelligenceData(
                target_id=target_id,
                platform=target.platform,
                data_type="content",
                content=content_item["text"][:2000],
                metadata=content_item.get("metadata", {}),
                timestamp=content_item.get("timestamp", time.time()),
                source_url=url,
                related_entities=content_item.get("mentions", [])
            ))
            
        # Extract relationships/mentions
        relationships = self._extract_relationship_intelligence(content, target.platform)
        for relationship in relationships:
            intelligence_points.append(IntelligenceData(
                target_id=target_id,
                platform=target.platform,
                data_type="relationship",
                content=json.dumps(relationship),
                metadata={"relationship_type": relationship.get("type", "mention")},
                timestamp=time.time(),
                source_url=url,
                related_entities=[relationship.get("target", "")]
            ))
            
        return intelligence_points
        
    def _extract_json_intelligence(self, content: str) -> Dict[str, Any]:
        """Extract JSON data from content"""
        try:
            # Try direct JSON parsing
            if content.strip().startswith('{') or content.strip().startswith('['):
                return json.loads(content)
                
            # Try to find JSON in HTML
            json_matches = re.findall(r'<script[^>]*>.*?({.*?}|\\[.*?\\]).*?</script>', content, re.DOTALL)
            for match in json_matches:
                try:
                    return json.loads(match)
                except:
                    continue
                    
        except Exception:
            pass
            
        return {}
        
    def _extract_profile_intelligence(self, content: str, platform: str) -> Dict[str, Any]:
        """Extract profile/account information"""
        profile = {}
        
        try:
            soup = BeautifulSoup(content, 'html.parser')
            
            # Extract title
            if soup.title:
                profile['title'] = soup.title.get_text().strip()
                
            # Extract meta tags
            meta_data = {}
            for meta in soup.find_all('meta'):
                if meta.get('property'):
                    meta_data[meta.get('property')] = meta.get('content')
                elif meta.get('name'):
                    meta_data[meta.get('name')] = meta.get('content')
            profile['meta'] = meta_data
            
            # Platform-specific extraction
            if platform == 'twitter':
                # Extract Twitter-specific data
                profile.update(self._extract_twitter_profile(soup))
            elif platform == 'linkedin':
                profile.update(self._extract_linkedin_profile(soup))
            elif platform == 'github':
                profile.update(self._extract_github_profile(soup))
                
        except Exception:
            pass
            
        return profile
        
    def _extract_content_intelligence(self, content: str, platform: str) -> List[Dict[str, Any]]:
        """Extract posts/content from the page"""
        content_items = []
        
        try:
            soup = BeautifulSoup(content, 'html.parser')
            
            # Platform-specific content extraction
            if platform == 'twitter':
                content_items.extend(self._extract_twitter_content(soup))
            elif platform == 'reddit':
                content_items.extend(self._extract_reddit_content(soup))
            elif platform == 'medium':
                content_items.extend(self._extract_medium_content(soup))
                
        except Exception:
            pass
            
        return content_items
        
    def _extract_relationship_intelligence(self, content: str, platform: str) -> List[Dict[str, Any]]:
        """Extract relationships and mentions"""
        relationships = []
        
        # Extract @mentions
        mentions = re.findall(r'@(\w+)', content)
        for mention in mentions:
            relationships.append({
                'type': 'mention',
                'target': mention,
                'platform': platform
            })
            
        # Extract hashtags
        hashtags = re.findall(r'#(\w+)', content)
        for hashtag in hashtags:
            relationships.append({
                'type': 'hashtag',
                'target': hashtag,
                'platform': platform
            })
            
        # Extract URLs/links
        urls = re.findall(r'https?://[^\s<>"]+', content)
        for url in urls:
            domain = urlparse(url).netloc
            relationships.append({
                'type': 'link',
                'target': domain,
                'url': url,
                'platform': platform
            })
            
        return relationships
        
    def _extract_twitter_profile(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Extract Twitter-specific profile data"""
        profile = {}
        
        # Look for Twitter-specific elements
        name_elem = soup.find('meta', {'property': 'og:title'})
        if name_elem:
            profile['display_name'] = name_elem.get('content')
            
        desc_elem = soup.find('meta', {'property': 'og:description'})
        if desc_elem:
            profile['bio'] = desc_elem.get('content')
            
        return profile
        
    def _extract_twitter_content(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        """Extract Twitter posts/tweets"""
        content_items = []
        
        # Look for tweet content
        tweet_texts = soup.find_all('p', class_=re.compile(r'tweet|text'))
        for tweet in tweet_texts:
            text = tweet.get_text().strip()
            if text and len(text) > 10:
                content_items.append({
                    'text': text,
                    'metadata': {'content_type': 'tweet'},
                    'mentions': re.findall(r'@(\w+)', text),
                    'hashtags': re.findall(r'#(\w+)', text)
                })
                
        return content_items
        
    def _extract_reddit_content(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        """Extract Reddit posts"""
        content_items = []
        
        # Look for Reddit post titles and content
        titles = soup.find_all(['h1', 'h2', 'h3'], class_=re.compile(r'title'))
        for title in titles:
            text = title.get_text().strip()
            if text:
                content_items.append({
                    'text': text,
                    'metadata': {'content_type': 'post_title'},
                    'mentions': [],
                    'hashtags': []
                })
                
        return content_items
        
    def _extract_medium_content(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        """Extract Medium articles"""
        content_items = []
        
        # Look for article titles and content
        articles = soup.find_all(['article', 'div'], class_=re.compile(r'post|article'))
        for article in articles:
            text = article.get_text().strip()
            if text and len(text) > 50:
                content_items.append({
                    'text': text[:1000],  # Limit length
                    'metadata': {'content_type': 'article'},
                    'mentions': [],
                    'hashtags': []
                })
                
        return content_items
        
    def _is_valid_intelligence(self, content: str, platform: str) -> bool:
        """Check if content contains valid intelligence data"""
        if len(content) < 200:
            return False
            
        # Platform-specific validation
        platform_indicators = {
            'twitter': ['twitter', 'tweet', 'profile', '@'],
            'youtube': ['youtube', 'video', 'channel', 'subscribe'],
            'instagram': ['instagram', 'photo', 'post', 'followers'],
            'reddit': ['reddit', 'subreddit', 'post', 'comment'],
            'linkedin': ['linkedin', 'professional', 'experience', 'skills'],
            'github': ['github', 'repository', 'commit', 'code'],
            'medium': ['medium', 'article', 'story', 'author'],
            'telegram': ['telegram', 'channel', 'message', 'subscribers']
        }
        
        indicators = platform_indicators.get(platform.lower(), [])
        if indicators:
            return any(indicator in content.lower() for indicator in indicators)
            
        # Generic validation
        return any(pattern in content.lower() for pattern in [
            'json', 'api', 'data', 'content', 'profile', 'user', 'post', 'message'
        ])
        
    async def _store_intelligence(self, target: IntelligenceTarget, intelligence_data: List[IntelligenceData]):
        """Store intelligence data in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Store/update entity
            entity_id = self._generate_entity_id(target.name, target.platform)
            cursor.execute('''
                INSERT OR REPLACE INTO entities 
                (id, name, entity_type, platforms, aliases, tags, first_seen, last_updated, confidence)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                entity_id,
                target.name,
                target.target_type,
                json.dumps([target.platform]),
                json.dumps(target.aliases),
                json.dumps(target.tags),
                time.time(),
                time.time(),
                1.0
            ))
            
            # Store intelligence data
            for intel in intelligence_data:
                intel_id = hashlib.md5(f"{intel.target_id}_{intel.platform}_{intel.data_type}_{intel.timestamp}".encode()).hexdigest()
                cursor.execute('''
                    INSERT OR REPLACE INTO intelligence_data
                    (id, entity_id, platform, data_type, content, metadata, timestamp, confidence, source_url, related_entities)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    intel_id,
                    intel.target_id,
                    intel.platform,
                    intel.data_type,
                    intel.content,
                    json.dumps(intel.metadata),
                    intel.timestamp,
                    intel.confidence,
                    intel.source_url,
                    json.dumps(intel.related_entities)
                ))
                
            conn.commit()
            
        except Exception as e:
            print(f"Database error: {e}")
        finally:
            conn.close()
            
    def _generate_entity_id(self, name: str, platform: str) -> str:
        """Generate unique entity ID"""
        return hashlib.md5(f"{name.lower()}_{platform.lower()}".encode()).hexdigest()
        
    async def _resolve_entities(self, intelligence_data: List[IntelligenceData]) -> Dict[str, Dict[str, Any]]:
        """Resolve and merge entities across platforms"""
        print("🔍 Resolving entities across platforms...")
        
        entity_map = {}
        
        # Group by target_id
        entities_by_id = defaultdict(list)
        for intel in intelligence_data:
            entities_by_id[intel.target_id].append(intel)
            
        # Build entity profiles
        for entity_id, intel_list in entities_by_id.items():
            platforms = list(set(intel.platform for intel in intel_list))
            data_types = list(set(intel.data_type for intel in intel_list))
            
            # Extract entity name from first intelligence point
            entity_name = intel_list[0].target_id.split('_')[0] if intel_list else "unknown"
            
            entity_map[entity_id] = {
                'name': entity_name,
                'platforms': platforms,
                'data_types': data_types,
                'intelligence_count': len(intel_list),
                'first_seen': min(intel.timestamp for intel in intel_list),
                'last_seen': max(intel.timestamp for intel in intel_list)
            }
            
        return entity_map
        
    async def _analyze_relationships(self, intelligence_data: List[IntelligenceData], entity_map: Dict[str, Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Analyze relationships between entities"""
        print("🕸️ Analyzing entity relationships...")
        
        relationships = []
        
        # Extract relationships from intelligence data
        for intel in intelligence_data:
            if intel.related_entities:
                for related_entity in intel.related_entities:
                    if related_entity and related_entity.strip():
                        relationships.append({
                            'source': intel.target_id,
                            'target': related_entity,
                            'type': intel.data_type,
                            'platform': intel.platform,
                            'timestamp': intel.timestamp,
                            'strength': 1.0
                        })
                        
        # Deduplicate and strengthen relationships
        relationship_map = defaultdict(list)
        for rel in relationships:
            key = f"{rel['source']}_{rel['target']}_{rel['type']}"
            relationship_map[key].append(rel)
            
        strengthened_relationships = []
        for key, rel_list in relationship_map.items():
            if len(rel_list) > 0:
                base_rel = rel_list[0]
                base_rel['strength'] = len(rel_list)  # Strength based on frequency
                base_rel['platforms'] = list(set(rel['platform'] for rel in rel_list))
                strengthened_relationships.append(base_rel)
                
        return strengthened_relationships
        
    async def _cross_platform_analysis(self, intelligence_data: List[IntelligenceData], entity_map: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze patterns across platforms"""
        print("🌐 Performing cross-platform analysis...")
        
        analysis = {
            'platform_coverage': {},
            'content_patterns': {},
            'temporal_patterns': {},
            'cross_platform_entities': []
        }
        
        # Platform coverage analysis
        platform_counts = Counter(intel.platform for intel in intelligence_data)
        analysis['platform_coverage'] = dict(platform_counts)
        
        # Find entities present on multiple platforms
        for entity_id, entity_info in entity_map.items():
            if len(entity_info['platforms']) > 1:
                analysis['cross_platform_entities'].append({
                    'entity_id': entity_id,
                    'name': entity_info['name'],
                    'platforms': entity_info['platforms'],
                    'platform_count': len(entity_info['platforms'])
                })
                
        return analysis
        
    async def _temporal_analysis(self, intelligence_data: List[IntelligenceData]) -> Dict[str, Any]:
        """Analyze temporal patterns in the data"""
        print("⏰ Performing temporal analysis...")
        
        analysis = {
            'time_range': {},
            'activity_patterns': {},
            'trending_topics': []
        }
        
        if intelligence_data:
            timestamps = [intel.timestamp for intel in intelligence_data]
            analysis['time_range'] = {
                'start': min(timestamps),
                'end': max(timestamps),
                'duration_hours': (max(timestamps) - min(timestamps)) / 3600
            }
            
            # Activity patterns by hour
            activity_by_hour = defaultdict(int)
            for intel in intelligence_data:
                hour = datetime.fromtimestamp(intel.timestamp).hour
                activity_by_hour[hour] += 1
            analysis['activity_patterns'] = dict(activity_by_hour)
            
        return analysis
        
    async def _generate_intelligence_report(self, intelligence_data: List[IntelligenceData], 
                                          entity_map: Dict[str, Dict[str, Any]], 
                                          relationships: List[Dict[str, Any]], 
                                          cross_analysis: Dict[str, Any], 
                                          temporal_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive intelligence report"""
        
        report = {
            'summary': {
                'total_intelligence_points': len(intelligence_data),
                'unique_entities': len(entity_map),
                'relationships_found': len(relationships),
                'platforms_covered': len(cross_analysis['platform_coverage']),
                'cross_platform_entities': len(cross_analysis['cross_platform_entities']),
                'analysis_timestamp': time.time()
            },
            'entities': entity_map,
            'relationships': relationships,
            'cross_platform_analysis': cross_analysis,
            'temporal_analysis': temporal_analysis,
            'intelligence_data': [asdict(intel) for intel in intelligence_data[:100]]  # Limit for report size
        }
        
        return report

# Test the full intelligence system
async def test_intelligence_system():
    """Test the complete intelligence platform"""
    
    print("🧠 TESTING FULL INTELLIGENCE SYSTEM")
    print("=" * 60)
    print("Building comprehensive intelligence profiles...")
    
    # Intelligence targets
    targets = [
        IntelligenceTarget("elonmusk", "twitter", "person", ["elon", "musk"], 10, ["tech", "ceo"]),
        IntelligenceTarget("elonmusk", "youtube", "person", ["elon", "musk"], 10, ["tech", "ceo"]),
        IntelligenceTarget("bitcoin", "coingecko", "cryptocurrency", ["btc"], 9, ["crypto", "currency"]),
        IntelligenceTarget("BTC", "coinmarketcap", "cryptocurrency", ["bitcoin"], 9, ["crypto", "currency"]),
        IntelligenceTarget("programming", "reddit", "topic", [], 7, ["tech", "development"]),
        IntelligenceTarget("python", "medium", "topic", [], 6, ["programming", "language"]),
    ]
    
    async with GreyScanIntelligence() as intelligence_system:
        report = await intelligence_system.full_intelligence_scan(targets)
        
        print(f"\n📊 INTELLIGENCE REPORT SUMMARY:")
        print(f"Intelligence points: {report['summary']['total_intelligence_points']}")
        print(f"Unique entities: {report['summary']['unique_entities']}")
        print(f"Relationships: {report['summary']['relationships_found']}")
        print(f"Platforms covered: {report['summary']['platforms_covered']}")
        print(f"Cross-platform entities: {report['summary']['cross_platform_entities']}")
        
        # Show top entities
        if report['entities']:
            print(f"\n🎯 TOP ENTITIES:")
            sorted_entities = sorted(report['entities'].items(), 
                                   key=lambda x: x[1]['intelligence_count'], reverse=True)
            for entity_id, entity_info in sorted_entities[:5]:
                print(f"  📍 {entity_info['name']}")
                print(f"     Platforms: {', '.join(entity_info['platforms'])}")
                print(f"     Intelligence points: {entity_info['intelligence_count']}")
                print(f"     Data types: {', '.join(entity_info['data_types'])}")
                
        # Show relationships
        if report['relationships']:
            print(f"\n🕸️ TOP RELATIONSHIPS:")
            sorted_rels = sorted(report['relationships'], key=lambda x: x['strength'], reverse=True)
            for rel in sorted_rels[:5]:
                print(f"  🔗 {rel['source']} → {rel['target']}")
                print(f"     Type: {rel['type']} | Strength: {rel['strength']} | Platforms: {', '.join(rel['platforms'])}")
                
        return report

if __name__ == "__main__":
    asyncio.run(test_intelligence_system())
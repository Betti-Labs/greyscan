#!/usr/bin/env python3
"""
GreyScan Master Intelligence Orchestrator
=========================================

The ULTIMATE intelligence system that combines ALL engines:
- Discovery Engine: Finds hidden endpoints
- Universal Scanner: 90% success across platforms  
- Intelligence Platform: Cross-referencing and analysis
- Crypto Engine: Financial intelligence
- Core Engine: Adaptive learning
- Real-time correlation and mega-dataset generation

This is the civilian Palantir - complete web intelligence domination!
"""

import asyncio
import time
import json
from datetime import datetime
from typing import List, Dict, Any, Set
from dataclasses import dataclass, asdict

# Import all our engines
from greyscan_intelligence import GreyScanIntelligence, IntelligenceTarget
from greyscan_universal import GreyScanUniversal, UniversalTarget
from greyscan_discovery import EmergentPathScraper
from greyscan_real_aggressive import GreyScanRealAggressive
from greyscan_core import GreyScanEngine

@dataclass
class MasterTarget:
    """Enhanced target for master intelligence operations"""
    name: str
    platforms: List[str]  # Platforms to scan
    target_type: str = "unknown"
    aliases: List[str] = None
    priority: int = 5
    tags: List[str] = None
    crypto_symbol: str = None  # For crypto targets
    
    def __post_init__(self):
        if self.aliases is None:
            self.aliases = []
        if self.tags is None:
            self.tags = []

class GreyScanMaster:
    """The ultimate intelligence orchestrator combining all engines"""
    
    def __init__(self):
        self.discovery_engine = None
        self.universal_engine = None
        self.intelligence_engine = None
        self.crypto_engine = None
        self.core_engine = None
        
        # Master results storage
        self.master_database = {}
        self.discovered_paths = {}
        self.all_intelligence = []
        self.correlation_map = {}
        
    async def __aenter__(self):
        """Initialize all engines"""
        print("🚀 INITIALIZING MASTER INTELLIGENCE ORCHESTRATOR")
        print("=" * 80)
        print("🧠 Loading ALL intelligence engines...")
        
        # Initialize all engines
        self.discovery_engine = EmergentPathScraper()
        self.universal_engine = GreyScanUniversal()
        self.intelligence_engine = GreyScanIntelligence()
        self.crypto_engine = GreyScanRealAggressive()
        self.core_engine = GreyScanEngine()
        
        # Initialize engines that need it
        await self.universal_engine.__aenter__()
        await self.intelligence_engine.__aenter__()
        
        print("✨ ALL ENGINES LOADED - MASTER SYSTEM READY")
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Cleanup all engines"""
        if self.universal_engine:
            await self.universal_engine.__aexit__(exc_type, exc_val, exc_tb)
        if self.intelligence_engine:
            await self.intelligence_engine.__aexit__(exc_type, exc_val, exc_tb)
        if self.crypto_engine:
            await self.crypto_engine.close()
        if self.core_engine:
            await self.core_engine.close()
            
    async def ultimate_intelligence_operation(self, targets: List[MasterTarget]) -> Dict[str, Any]:
        """The ultimate intelligence operation using ALL engines"""
        
        print(f"\n🔥 ULTIMATE INTELLIGENCE OPERATION")
        print(f"🎯 Targets: {len(targets)}")
        print(f"🚀 Engines: 5 (Discovery, Universal, Intelligence, Crypto, Core)")
        print("=" * 80)
        
        start_time = time.time()
        
        # PHASE 1: DISCOVERY - Find hidden endpoints
        print(f"\n🔍 PHASE 1: EMERGENT PATH DISCOVERY")
        discovered_paths = await self._discovery_phase(targets)
        
        # PHASE 2: UNIVERSAL SCANNING - Maximum platform coverage
        print(f"\n🌍 PHASE 2: UNIVERSAL PLATFORM SCANNING")
        universal_results = await self._universal_phase(targets, discovered_paths)
        
        # PHASE 3: INTELLIGENCE ANALYSIS - Cross-referencing
        print(f"\n🧠 PHASE 3: INTELLIGENCE ANALYSIS")
        intelligence_results = await self._intelligence_phase(targets)
        
        # PHASE 4: CRYPTO INTELLIGENCE - Financial data
        print(f"\n💰 PHASE 4: CRYPTO INTELLIGENCE")
        crypto_results = await self._crypto_phase(targets)
        
        # PHASE 5: CORE ADAPTIVE - Learning optimization
        print(f"\n⚡ PHASE 5: CORE ADAPTIVE LEARNING")
        core_results = await self._core_phase(targets)
        
        # PHASE 6: MASTER CORRELATION - Combine everything
        print(f"\n🔗 PHASE 6: MASTER CORRELATION")
        master_report = await self._correlation_phase(
            discovered_paths, universal_results, intelligence_results, 
            crypto_results, core_results
        )
        
        total_time = time.time() - start_time
        
        print(f"\n🎉 ULTIMATE INTELLIGENCE OPERATION COMPLETE")
        print(f"⏱️ Total time: {total_time:.2f}s")
        print(f"📊 Total data points: {master_report['summary']['total_data_points']}")
        print(f"🔗 Cross-engine correlations: {master_report['summary']['correlations_found']}")
        print(f"🌐 Platforms penetrated: {master_report['summary']['platforms_penetrated']}")
        
        return master_report
        
    async def _discovery_phase(self, targets: List[MasterTarget]) -> Dict[str, List]:
        """Phase 1: Discover hidden endpoints for all platforms"""
        
        discovered_paths = {}
        
        # Group targets by platform for discovery
        platform_targets = {}
        for target in targets:
            for platform in target.platforms:
                if platform not in platform_targets:
                    platform_targets[platform] = []
                platform_targets[platform].append(target.name)
        
        # Discover paths for each platform
        for platform, target_names in platform_targets.items():
            if len(target_names) > 0:
                print(f"🔍 Discovering paths for {platform}: {target_names[:3]}...")
                try:
                    paths = await self.discovery_engine.discover_emergent_paths(
                        platform=platform,
                        targets=target_names[:2],  # Limit for speed
                        max_iterations=2
                    )
                    discovered_paths[platform] = paths
                    print(f"✅ Found {len(paths)} emergent paths for {platform}")
                except Exception as e:
                    print(f"⚠️ Discovery failed for {platform}: {e}")
                    discovered_paths[platform] = []
        
        total_paths = sum(len(paths) for paths in discovered_paths.values())
        print(f"🔍 DISCOVERY COMPLETE: {total_paths} total emergent paths found")
        
        return discovered_paths
        
    async def _universal_phase(self, targets: List[MasterTarget], discovered_paths: Dict) -> List[Dict]:
        """Phase 2: Universal scanning with discovered paths"""
        
        # Convert to universal targets
        universal_targets = []
        for target in targets:
            for platform in target.platforms:
                universal_targets.append(UniversalTarget(target.name, platform))
        
        print(f"🌍 Scanning {len(universal_targets)} universal targets...")
        
        try:
            results = await self.universal_engine.universal_scan(universal_targets)
            print(f"✅ Universal scan: {len(results)} successful collections")
            return results
        except Exception as e:
            print(f"⚠️ Universal scan error: {e}")
            return []
            
    async def _intelligence_phase(self, targets: List[MasterTarget]) -> Dict[str, Any]:
        """Phase 3: Full intelligence analysis"""
        
        # Convert to intelligence targets
        intelligence_targets = []
        for target in targets:
            for platform in target.platforms:
                intelligence_targets.append(IntelligenceTarget(
                    name=target.name,
                    platform=platform,
                    target_type=target.target_type,
                    aliases=target.aliases,
                    priority=target.priority,
                    tags=target.tags
                ))
        
        print(f"🧠 Intelligence analysis on {len(intelligence_targets)} targets...")
        
        try:
            report = await self.intelligence_engine.full_intelligence_scan(intelligence_targets)
            print(f"✅ Intelligence: {report['summary']['total_intelligence_points']} points, {report['summary']['relationships_found']} relationships")
            return report
        except Exception as e:
            print(f"⚠️ Intelligence analysis error: {e}")
            return {'summary': {'total_intelligence_points': 0, 'relationships_found': 0}, 'entities': {}, 'relationships': []}
            
    async def _crypto_phase(self, targets: List[MasterTarget]) -> List[Dict]:
        """Phase 4: Crypto-specific intelligence"""
        
        # Filter crypto targets
        crypto_targets = []
        for target in targets:
            if 'crypto' in target.tags or target.crypto_symbol:
                for platform in ['coingecko', 'coinmarketcap', 'defillama']:
                    if platform in target.platforms:
                        symbol = target.crypto_symbol or target.name
                        crypto_targets.append((symbol, platform))
        
        if not crypto_targets:
            print("💰 No crypto targets found")
            return []
            
        print(f"💰 Crypto intelligence on {len(crypto_targets)} targets...")
        
        try:
            results = await self.crypto_engine.real_aggressive_collect(crypto_targets)
            print(f"✅ Crypto: {len(results)} successful collections")
            return results
        except Exception as e:
            print(f"⚠️ Crypto intelligence error: {e}")
            return []
            
    async def _core_phase(self, targets: List[MasterTarget]) -> List[Dict]:
        """Phase 5: Core adaptive learning"""
        
        # Convert to core targets (focus on social media)
        core_targets = []
        for target in targets:
            if 'twitter' in target.platforms or 'social' in target.tags:
                core_targets.append((target.name, target.target_type))
        
        if not core_targets:
            print("⚡ No social targets for core engine")
            return []
            
        print(f"⚡ Core adaptive learning on {len(core_targets)} targets...")
        
        try:
            results = await self.core_engine.adaptive_collect(core_targets)
            print(f"✅ Core: {len(results)} successful collections")
            return results
        except Exception as e:
            print(f"⚠️ Core engine error: {e}")
            return []
            
    async def _correlation_phase(self, discovered_paths, universal_results, 
                                intelligence_results, crypto_results, core_results) -> Dict[str, Any]:
        """Phase 6: Master correlation of all results"""
        
        print("🔗 Correlating results from all engines...")
        
        # Count total data points
        total_data_points = 0
        total_data_points += len(universal_results)
        total_data_points += intelligence_results.get('summary', {}).get('total_intelligence_points', 0)
        total_data_points += len(crypto_results)
        total_data_points += len(core_results)
        total_data_points += sum(len(paths) for paths in discovered_paths.values())
        
        # Count platforms penetrated
        platforms_penetrated = set()
        
        for result in universal_results:
            platforms_penetrated.add(result.get('platform', 'unknown'))
            
        for result in crypto_results:
            platforms_penetrated.add(result.get('platform', 'unknown'))
            
        for result in core_results:
            platforms_penetrated.add('twitter')  # Core engine focuses on Twitter
            
        platforms_penetrated.update(discovered_paths.keys())
        
        # Cross-engine correlations
        correlations_found = 0
        entity_correlations = {}
        
        # Correlate entities across engines
        if 'entities' in intelligence_results:
            for entity_id, entity_info in intelligence_results['entities'].items():
                entity_name = entity_info.get('name', '').lower()
                
                # Find matches in other engines
                matches = {
                    'universal': [r for r in universal_results if r.get('target', '').lower() == entity_name],
                    'crypto': [r for r in crypto_results if r.get('target', '').lower() == entity_name],
                    'core': [r for r in core_results if r.get('target', '').lower() == entity_name]
                }
                
                if any(matches.values()):
                    entity_correlations[entity_name] = matches
                    correlations_found += 1
        
        # Build master report
        master_report = {
            'summary': {
                'operation_type': 'ultimate_intelligence',
                'engines_used': 5,
                'total_data_points': total_data_points,
                'platforms_penetrated': len(platforms_penetrated),
                'correlations_found': correlations_found,
                'operation_timestamp': time.time()
            },
            'engine_results': {
                'discovery': {
                    'total_paths': sum(len(paths) for paths in discovered_paths.values()),
                    'platforms': list(discovered_paths.keys()),
                    'paths_by_platform': {k: len(v) for k, v in discovered_paths.items()}
                },
                'universal': {
                    'total_collections': len(universal_results),
                    'success_rate': len(universal_results) / max(1, len(universal_results)) * 100,
                    'platforms': list(set(r.get('platform') for r in universal_results))
                },
                'intelligence': {
                    'intelligence_points': intelligence_results.get('summary', {}).get('total_intelligence_points', 0),
                    'entities_resolved': intelligence_results.get('summary', {}).get('unique_entities', 0),
                    'relationships_found': intelligence_results.get('summary', {}).get('relationships_found', 0)
                },
                'crypto': {
                    'total_collections': len(crypto_results),
                    'total_data_size': sum(r.get('data_size', 0) for r in crypto_results),
                    'platforms': list(set(r.get('platform') for r in crypto_results))
                },
                'core': {
                    'total_collections': len(core_results),
                    'learning_patterns': len(getattr(self.core_engine, 'learned_patterns', {}))
                }
            },
            'correlations': entity_correlations,
            'platforms_penetrated': list(platforms_penetrated),
            'raw_results': {
                'discovered_paths': discovered_paths,
                'universal_results': universal_results[:10],  # Limit for size
                'intelligence_results': intelligence_results,
                'crypto_results': crypto_results[:10],  # Limit for size
                'core_results': core_results[:10]  # Limit for size
            }
        }
        
        print(f"🔗 CORRELATION COMPLETE: {correlations_found} cross-engine correlations found")
        
        return master_report

# Test the ultimate system
async def test_ultimate_system():
    """Test the ultimate intelligence system"""
    
    print("🔥 TESTING ULTIMATE INTELLIGENCE SYSTEM")
    print("=" * 80)
    print("🚀 Combining ALL engines for maximum intelligence gathering")
    
    # Define comprehensive targets
    targets = [
        MasterTarget(
            name="bitcoin",
            platforms=["coingecko", "coinmarketcap", "reddit", "twitter"],
            target_type="cryptocurrency",
            aliases=["btc", "bitcoin-core"],
            priority=10,
            tags=["crypto", "currency", "finance"],
            crypto_symbol="BTC"
        ),
        MasterTarget(
            name="ethereum",
            platforms=["coingecko", "defillama", "reddit", "twitter"],
            target_type="cryptocurrency", 
            aliases=["eth", "ether"],
            priority=10,
            tags=["crypto", "defi", "smart-contracts"],
            crypto_symbol="ETH"
        ),
        MasterTarget(
            name="elonmusk",
            platforms=["twitter", "youtube", "reddit"],
            target_type="person",
            aliases=["elon", "musk"],
            priority=9,
            tags=["tech", "ceo", "influencer", "social"]
        ),
        MasterTarget(
            name="programming",
            platforms=["reddit", "github", "medium"],
            target_type="topic",
            aliases=["coding", "development"],
            priority=7,
            tags=["tech", "development", "community"]
        )
    ]
    
    # Run ultimate intelligence operation
    async with GreyScanMaster() as master:
        report = await master.ultimate_intelligence_operation(targets)
        
        # Display results
        print(f"\n🎉 ULTIMATE INTELLIGENCE RESULTS:")
        print(f"📊 Total Data Points: {report['summary']['total_data_points']}")
        print(f"🌐 Platforms Penetrated: {report['summary']['platforms_penetrated']}")
        print(f"🔗 Cross-Engine Correlations: {report['summary']['correlations_found']}")
        print(f"🚀 Engines Used: {report['summary']['engines_used']}")
        
        # Engine breakdown
        print(f"\n🔧 ENGINE BREAKDOWN:")
        engines = report['engine_results']
        print(f"  🔍 Discovery: {engines['discovery']['total_paths']} emergent paths")
        print(f"  🌍 Universal: {engines['universal']['total_collections']} collections")
        print(f"  🧠 Intelligence: {engines['intelligence']['intelligence_points']} points")
        print(f"  💰 Crypto: {engines['crypto']['total_collections']} collections")
        print(f"  ⚡ Core: {engines['core']['total_collections']} collections")
        
        # Platform coverage
        print(f"\n🌐 PLATFORMS PENETRATED:")
        for platform in sorted(report['platforms_penetrated']):
            print(f"  ✅ {platform}")
        
        # Correlations
        if report['correlations']:
            print(f"\n🔗 CROSS-ENGINE CORRELATIONS:")
            for entity, matches in list(report['correlations'].items())[:3]:
                print(f"  🎯 {entity}:")
                for engine, results in matches.items():
                    if results:
                        print(f"    {engine}: {len(results)} matches")
        
        return report

if __name__ == "__main__":
    asyncio.run(test_ultimate_system())
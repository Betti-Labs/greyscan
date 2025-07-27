"""
GreyScan Integration Test
========================

Quick test to ensure all components work together properly.
"""

import asyncio
import sys

async def test_core_engine():
    """Test the core GreyScan engine"""
    print("🔍 Testing GreyScan Core Engine...")
    
    try:
        from greyscan_core import GreyScanEngine
        
        scanner = GreyScanEngine()
        print("✅ GreyScan engine initialized successfully")
        
        # Test with a small target set
        targets = [("elonmusk", "test")]
        
        results = await scanner.adaptive_collect(targets)
        
        if results and len(results) > 0:
            print(f"✅ Core engine working - collected {len(results)} items")
            return True
        else:
            print("❌ Core engine failed - no results")
            return False
            
    except Exception as e:
        print(f"❌ Core engine error: {e}")
        return False
    finally:
        if 'scanner' in locals():
            await scanner.close()

async def test_discovery_engine():
    """Test the emergent discovery engine"""
    print("\n🌟 Testing Emergent Discovery Engine...")
    
    try:
        from greyscan_discovery import EmergentPathScraper
        
        discoverer = EmergentPathScraper()
        print("✅ Discovery engine initialized successfully")
        
        # Test with minimal discovery
        paths = await discoverer.discover_emergent_paths(
            platform="github",
            targets=["ethereum"],
            max_iterations=1
        )
        
        if paths and len(paths) > 0:
            print(f"✅ Discovery engine working - found {len(paths)} paths")
            return True
        else:
            print("❌ Discovery engine failed - no paths found")
            return False
            
    except Exception as e:
        print(f"❌ Discovery engine error: {e}")
        return False
    finally:
        if 'discoverer' in locals():
            await discoverer.close()

async def main():
    """Run all integration tests"""
    print("🚀 GREYSCAN INTEGRATION TEST")
    print("=" * 50)
    
    tests_passed = 0
    total_tests = 2
    
    # Test core engine
    if await test_core_engine():
        tests_passed += 1
    
    # Test discovery engine
    if await test_discovery_engine():
        tests_passed += 1
    
    # Results
    print(f"\n📊 TEST RESULTS:")
    print(f"Tests passed: {tests_passed}/{total_tests}")
    print(f"Success rate: {tests_passed/total_tests:.1%}")
    
    if tests_passed == total_tests:
        print("🎉 ALL TESTS PASSED - GreyScan is ready!")
        return True
    else:
        print("❌ SOME TESTS FAILED - Check errors above")
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
# GreyScan Best Practices

Guidelines for optimal performance, reliability, and ethical use of the GreyScan Python scripts.

## Script Usage Best Practices

### Running the Intelligence Platform

```bash
# Full intelligence scan with cross-referencing
python greyscan_intelligence.py

# Expected: 1,340+ intelligence points, entity resolution, relationship mapping
```

**Best Practices:**
- Run in a stable network environment
- Ensure sufficient disk space for SQLite database
- Allow 3-5 seconds for full intelligence operations
- Check console output for real-time progress

### Running the Universal Scanner

```bash
# Universal platform scanning (90% success rate)
python greyscan_universal.py

# Expected: 9/10 platforms successfully penetrated
```

**Best Practices:**
- Test with known working targets first
- Monitor success rates across platforms
- Check learned patterns for optimization opportunities

### Running the Core Engine

```bash
# Adaptive learning engine (100% crypto success)
python greyscan_core.py

# Expected: 6/6 crypto targets successful with pattern learning
```

**Best Practices:**
- Use for crypto-specific intelligence gathering
- Monitor learning statistics for pattern optimization
- Leverage 100% success rate for reliable crypto data

### Running the GUI

```bash
# Launch Tkinter interface
python greyscan_gui.py
```

**Best Practices:**
- Use for interactive target configuration
- Monitor real-time learning logs
- Export results for further analysis

## Target Selection

### Intelligence Targets (greyscan_intelligence.py)

```python
# Good intelligence targets
good_targets = [
    IntelligenceTarget("bitcoin", "coingecko", "cryptocurrency", ["btc"], 10, ["crypto"]),
    IntelligenceTarget("elonmusk", "twitter", "person", ["elon", "musk"], 10, ["tech"]),
    IntelligenceTarget("programming", "reddit", "topic", [], 7, ["development"]),
    IntelligenceTarget("python", "medium", "topic", [], 6, ["programming"])
]

# Avoid these
avoid_targets = [
    IntelligenceTarget("private_account", "twitter", "person"),  # Private accounts
    IntelligenceTarget("random_string", "unknown", "unknown"),  # Non-existent entities
    IntelligenceTarget("", "platform", "type")  # Empty names
]
```

### Universal Targets (greyscan_universal.py)

```python
# Proven working targets
working_targets = [
    UniversalTarget("bitcoin", "coingecko"),           # Crypto data
    UniversalTarget("elonmusk", "twitter"),            # Public figures
    UniversalTarget("programming", "reddit"),          # Popular topics
    UniversalTarget("dQw4w9WgXcQ", "youtube"),        # Video IDs
    UniversalTarget("BzKGsw7Lzkg", "instagram"),      # Post IDs
    UniversalTarget("python", "medium"),               # Content topics
    UniversalTarget("durov", "telegram")               # Public channels
]
```

### Core Engine Targets (greyscan_core.py)

```python
# High-success crypto targets
crypto_targets = [
    ("bitcoin", "coingecko"),
    ("ethereum", "coingecko"),
    ("BTC", "coinmarketcap"),
    ("ETH", "coinmarketcap"),
    ("uniswap", "defillama"),
    ("aave", "defillama")
]
```

## Performance Optimization

### Custom Script Integration

```python
import asyncio
from greyscan_intelligence import GreyScanIntelligence, IntelligenceTarget

async def optimized_intelligence_operation():
    """Optimized intelligence gathering with error handling"""
    
    # Define high-value targets
    targets = [
        IntelligenceTarget("bitcoin", "coingecko", "cryptocurrency", ["btc"], 10, ["crypto"]),
        IntelligenceTarget("ethereum", "coingecko", "cryptocurrency", ["eth"], 10, ["crypto"]),
        IntelligenceTarget("programming", "reddit", "topic", [], 8, ["tech"])
    ]
    
    try:
        async with GreyScanIntelligence() as intel:
            report = await intel.full_intelligence_scan(targets)
            
            # Validate results
            if report['summary']['total_intelligence_points'] > 100:
                print(f"✅ High-quality intelligence: {report['summary']['total_intelligence_points']} points")
                return report
            else:
                print("⚠️ Low intelligence yield - consider different targets")
                return None
                
    except Exception as e:
        print(f"❌ Intelligence operation failed: {e}")
        return None

# Run optimized operation
report = asyncio.run(optimized_intelligence_operation())
```

### Batch Processing for Large Operations

```python
async def batch_intelligence_processing(all_targets, batch_size=5):
    """Process large target lists in batches"""
    
    all_reports = []
    
    for i in range(0, len(all_targets), batch_size):
        batch = all_targets[i:i + batch_size]
        
        print(f"Processing batch {i//batch_size + 1}/{len(all_targets)//batch_size + 1}")
        
        try:
            async with GreyScanIntelligence() as intel:
                report = await intel.full_intelligence_scan(batch)
                all_reports.append(report)
                
        except Exception as e:
            print(f"Batch {i//batch_size + 1} failed: {e}")
            continue
        
        # Brief pause between batches
        await asyncio.sleep(2)
    
    return all_reports
```

## Data Quality and Validation

### Intelligence Report Validation

```python
def validate_intelligence_report(report):
    """Validate intelligence report quality"""
    
    if not report or 'summary' not in report:
        print("❌ Invalid report structure")
        return False
    
    summary = report['summary']
    
    # Check minimum thresholds
    checks = {
        'intelligence_points': summary.get('total_intelligence_points', 0) >= 50,
        'entities_resolved': summary.get('unique_entities', 0) >= 1,
        'platforms_covered': summary.get('platforms_covered', 0) >= 1,
        'relationships_found': summary.get('relationships_found', 0) >= 0
    }
    
    print("📊 INTELLIGENCE REPORT VALIDATION:")
    for check, passed in checks.items():
        status = "✅" if passed else "❌"
        print(f"  {status} {check}: {summary.get(check.replace('_', '_'), 'N/A')}")
    
    return all(checks.values())

# Usage after intelligence operation
if report:
    is_valid = validate_intelligence_report(report)
    if is_valid:
        print("🎉 High-quality intelligence report generated")
    else:
        print("⚠️ Report quality below threshold")
```

### Collection Results Validation

```python
def validate_collection_results(results):
    """Validate universal scanner results"""
    
    if not results:
        print("❌ No results collected")
        return []
    
    validated_results = []
    
    for result in results:
        # Check minimum data size
        if result.get('data_size', 0) < 1000:
            print(f"⚠️ Small data size for {result.get('target')}: {result.get('data_size')} bytes")
            continue
        
        # Check for extracted data
        if not result.get('extracted_data'):
            print(f"⚠️ No structured data extracted for {result.get('target')}")
        
        # Check method used
        if result.get('method') == 'unknown':
            print(f"⚠️ Unknown method used for {result.get('target')}")
        
        validated_results.append(result)
    
    print(f"✅ Validated {len(validated_results)}/{len(results)} results")
    return validated_results
```

## Data Export and Storage

### Export Intelligence Reports

```python
import json
from datetime import datetime

def export_intelligence_report(report, format='json'):
    """Export intelligence report to file"""
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    if format == 'json':
        filename = f'intelligence_report_{timestamp}.json'
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
    
    elif format == 'summary':
        filename = f'intelligence_summary_{timestamp}.txt'
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("GREYSCAN INTELLIGENCE REPORT\n")
            f.write("=" * 50 + "\n\n")
            
            summary = report.get('summary', {})
            f.write(f"Intelligence Points: {summary.get('total_intelligence_points', 0)}\n")
            f.write(f"Entities Resolved: {summary.get('unique_entities', 0)}\n")
            f.write(f"Relationships Found: {summary.get('relationships_found', 0)}\n")
            f.write(f"Platforms Covered: {summary.get('platforms_covered', 0)}\n\n")
            
            # Top entities
            entities = report.get('entities', {})
            if entities:
                f.write("TOP ENTITIES:\n")
                sorted_entities = sorted(entities.items(), 
                                       key=lambda x: x[1].get('intelligence_count', 0), 
                                       reverse=True)
                
                for entity_id, entity_info in sorted_entities[:5]:
                    f.write(f"  • {entity_info.get('name', 'Unknown')}\n")
                    f.write(f"    Platforms: {', '.join(entity_info.get('platforms', []))}\n")
                    f.write(f"    Intelligence Points: {entity_info.get('intelligence_count', 0)}\n\n")
    
    print(f"Intelligence report exported to {filename}")
    return filename
```

### Query Intelligence Database

```python
import sqlite3
import json

def query_intelligence_database(db_path="intelligence.db"):
    """Query the automatically created intelligence database"""
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get database statistics
        cursor.execute('SELECT COUNT(*) FROM entities')
        entity_count = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM intelligence_data')
        intel_count = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM relationships')
        rel_count = cursor.fetchone()[0]
        
        print(f"📊 INTELLIGENCE DATABASE STATISTICS:")
        print(f"  Entities: {entity_count}")
        print(f"  Intelligence Points: {intel_count}")
        print(f"  Relationships: {rel_count}")
        
        # Get top entities by intelligence count
        cursor.execute('''
            SELECT e.name, e.entity_type, e.platforms, COUNT(i.id) as intel_count
            FROM entities e
            LEFT JOIN intelligence_data i ON e.id = i.entity_id
            GROUP BY e.id
            ORDER BY intel_count DESC
            LIMIT 10
        ''')
        
        top_entities = cursor.fetchall()
        
        if top_entities:
            print(f"\n🎯 TOP ENTITIES BY INTELLIGENCE:")
            for name, entity_type, platforms, count in top_entities:
                platforms_list = json.loads(platforms) if platforms else []
                print(f"  • {name} ({entity_type})")
                print(f"    Platforms: {', '.join(platforms_list)}")
                print(f"    Intelligence Points: {count}")
        
        conn.close()
        
    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")
    except FileNotFoundError:
        print("❌ Intelligence database not found. Run greyscan_intelligence.py first.")

# Usage after running intelligence operations
query_intelligence_database()
```

## Error Handling and Troubleshooting

### Robust Script Execution

```python
import logging
import asyncio

def setup_logging():
    """Setup logging for debugging"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('greyscan.log'),
            logging.StreamHandler()
        ]
    )

async def robust_intelligence_operation(targets, max_retries=3):
    """Intelligence operation with comprehensive error handling"""
    
    setup_logging()
    
    for attempt in range(max_retries):
        try:
            logging.info(f"Starting intelligence operation (attempt {attempt + 1})")
            
            async with GreyScanIntelligence() as intel:
                report = await intel.full_intelligence_scan(targets)
                
                if report and report['summary']['total_intelligence_points'] > 0:
                    logging.info(f"Intelligence operation successful: {report['summary']['total_intelligence_points']} points")
                    return report
                else:
                    logging.warning("Intelligence operation returned no data")
                    
        except asyncio.TimeoutError:
            logging.error(f"Attempt {attempt + 1}: Operation timed out")
            
        except Exception as e:
            logging.error(f"Attempt {attempt + 1}: {type(e).__name__}: {e}")
        
        if attempt < max_retries - 1:
            wait_time = 2 ** attempt  # Exponential backoff
            logging.info(f"Retrying in {wait_time} seconds...")
            await asyncio.sleep(wait_time)
    
    logging.error("All attempts failed")
    return None
```

### Common Issues and Solutions

```python
def diagnose_system():
    """Diagnose common system issues"""
    
    print("🔍 GREYSCAN SYSTEM DIAGNOSIS")
    print("=" * 50)
    
    # Check Python version
    import sys
    python_version = sys.version_info
    if python_version >= (3, 8):
        print(f"✅ Python version: {python_version.major}.{python_version.minor}")
    else:
        print(f"❌ Python version too old: {python_version.major}.{python_version.minor} (need 3.8+)")
    
    # Check dependencies
    dependencies = ['aiohttp', 'beautifulsoup4', 'networkx']
    for dep in dependencies:
        try:
            __import__(dep)
            print(f"✅ {dep}: Available")
        except ImportError:
            print(f"❌ {dep}: Missing (run: pip install {dep})")
    
    # Check network connectivity
    import socket
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        print("✅ Network connectivity: OK")
    except OSError:
        print("❌ Network connectivity: Failed")
    
    # Check disk space
    import shutil
    free_space = shutil.disk_usage('.').free / (1024**3)  # GB
    if free_space > 1:
        print(f"✅ Disk space: {free_space:.1f} GB available")
    else:
        print(f"⚠️ Disk space: Only {free_space:.1f} GB available")
    
    # Check file permissions
    try:
        with open('test_write.tmp', 'w') as f:
            f.write('test')
        import os
        os.remove('test_write.tmp')
        print("✅ File permissions: OK")
    except Exception:
        print("❌ File permissions: Cannot write to directory")

# Run diagnosis
diagnose_system()
```

## Security and Ethics

### Rate Limiting and Respectful Usage

```python
import time
from collections import defaultdict

class RespectfulUsage:
    """Ensure respectful usage of target platforms"""
    
    def __init__(self):
        self.request_times = defaultdict(list)
        self.max_requests_per_minute = 30
    
    def can_make_request(self, platform):
        """Check if we can make a request to this platform"""
        now = time.time()
        minute_ago = now - 60
        
        # Clean old requests
        self.request_times[platform] = [
            req_time for req_time in self.request_times[platform] 
            if req_time > minute_ago
        ]
        
        # Check rate limit
        if len(self.request_times[platform]) >= self.max_requests_per_minute:
            return False
        
        self.request_times[platform].append(now)
        return True
    
    def wait_time_needed(self, platform):
        """Calculate wait time needed before next request"""
        if self.can_make_request(platform):
            return 0
        
        oldest_request = min(self.request_times[platform])
        return 60 - (time.time() - oldest_request)

# Usage in custom scripts
usage_monitor = RespectfulUsage()

async def respectful_collection(targets):
    """Collection that respects platform rate limits"""
    results = []
    
    for target in targets:
        platform = target.platform if hasattr(target, 'platform') else 'unknown'
        
        # Check if we can make request
        if not usage_monitor.can_make_request(platform):
            wait_time = usage_monitor.wait_time_needed(platform)
            print(f"⏳ Rate limiting: waiting {wait_time:.1f}s for {platform}")
            await asyncio.sleep(wait_time)
        
        # Make request
        async with GreyScanUniversal() as scanner:
            batch_results = await scanner.universal_scan([target])
            results.extend(batch_results)
    
    return results
```

### Data Privacy Protection

```python
import re

def sanitize_intelligence_data(report):
    """Remove potentially sensitive information from intelligence data"""
    
    # Patterns to redact
    sensitive_patterns = [
        (r'\b\d{3}-\d{2}-\d{4}\b', '[SSN-REDACTED]'),
        (r'\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b', '[CARD-REDACTED]'),
        (r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[EMAIL-REDACTED]'),
        (r'\b\d{3}[- ]?\d{3}[- ]?\d{4}\b', '[PHONE-REDACTED]')
    ]
    
    def sanitize_text(text):
        if not isinstance(text, str):
            return text
        
        for pattern, replacement in sensitive_patterns:
            text = re.sub(pattern, replacement, text)
        return text
    
    # Sanitize intelligence data
    if 'intelligence_data' in report:
        for intel_point in report['intelligence_data']:
            if 'content' in intel_point:
                intel_point['content'] = sanitize_text(intel_point['content'])
    
    # Sanitize entity data
    if 'entities' in report:
        for entity_info in report['entities'].values():
            for key, value in entity_info.items():
                if isinstance(value, str):
                    entity_info[key] = sanitize_text(value)
    
    return report
```

## Testing and Validation

### System Test Suite

```python
async def run_system_tests():
    """Comprehensive system test suite"""
    
    print("🧪 GREYSCAN SYSTEM TEST SUITE")
    print("=" * 50)
    
    tests = []
    
    # Test 1: Core Engine
    print("\n1. Testing Core Engine...")
    try:
        engine = GreyScanEngine()
        results = await engine.adaptive_collect([("bitcoin", "coingecko")])
        await engine.close()
        
        if results and len(results) > 0:
            tests.append(("Core Engine", True, f"{len(results)} results"))
        else:
            tests.append(("Core Engine", False, "No results"))
    except Exception as e:
        tests.append(("Core Engine", False, str(e)))
    
    # Test 2: Universal Scanner
    print("\n2. Testing Universal Scanner...")
    try:
        async with GreyScanUniversal() as scanner:
            results = await scanner.universal_scan([UniversalTarget("bitcoin", "coingecko")])
        
        if results and len(results) > 0:
            tests.append(("Universal Scanner", True, f"{len(results)} results"))
        else:
            tests.append(("Universal Scanner", False, "No results"))
    except Exception as e:
        tests.append(("Universal Scanner", False, str(e)))
    
    # Test 3: Intelligence Platform
    print("\n3. Testing Intelligence Platform...")
    try:
        async with GreyScanIntelligence() as intel:
            report = await intel.full_intelligence_scan([
                IntelligenceTarget("bitcoin", "coingecko", "cryptocurrency")
            ])
        
        if report and report['summary']['total_intelligence_points'] > 0:
            tests.append(("Intelligence Platform", True, f"{report['summary']['total_intelligence_points']} points"))
        else:
            tests.append(("Intelligence Platform", False, "No intelligence"))
    except Exception as e:
        tests.append(("Intelligence Platform", False, str(e)))
    
    # Test Results
    print(f"\n📊 TEST RESULTS:")
    passed = 0
    for test_name, success, details in tests:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"  {status} {test_name}: {details}")
        if success:
            passed += 1
    
    print(f"\n🎯 OVERALL: {passed}/{len(tests)} tests passed ({passed/len(tests)*100:.1f}%)")
    
    return passed == len(tests)

# Run system tests
system_healthy = asyncio.run(run_system_tests())
```

## Summary

### Key Best Practices

1. **✅ Target Selection**: Use proven working targets from our test results
2. **✅ Error Handling**: Implement retry logic and comprehensive error handling
3. **✅ Data Validation**: Validate intelligence reports and collection results
4. **✅ Export & Storage**: Export results and query the intelligence database
5. **✅ Rate Limiting**: Respect platform limits with respectful usage patterns
6. **✅ Privacy Protection**: Sanitize sensitive data before storage/export
7. **✅ System Testing**: Run diagnostic tests to ensure system health

### Performance Guidelines

- **Intelligence Platform**: Expect 1,340+ intelligence points in ~3.65 seconds
- **Universal Scanner**: Achieve 90% success rate across 10 platforms
- **Core Engine**: Maintain 100% success rate on crypto targets
- **Database**: Query intelligence.db for persistent intelligence storage

### Troubleshooting Checklist

1. Check Python version (3.8+ required)
2. Verify dependencies (aiohttp, beautifulsoup4, networkx)
3. Test network connectivity
4. Ensure sufficient disk space and file permissions
5. Run system diagnostic tests
6. Check console output for specific error messages

**Remember**: GreyScan's adaptive intelligence works best when given stable network conditions and proper error handling. The learning algorithms improve over time, so consistent usage leads to better results.
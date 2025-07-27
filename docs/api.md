# GreyScan Python Library Documentation

Documentation for the GreyScan intelligence platform Python scripts and classes.

## Available Scripts

### Core Intelligence Scripts

- `greyscan_intelligence.py` - Full intelligence platform with cross-referencing
- `greyscan_universal.py` - Universal platform scanner (90% success rate)  
- `greyscan_core.py` - Adaptive learning engine (100% crypto success)
- `greyscan_gui.py` - Tkinter GUI interface
- `demo.py` - Basic usage demonstration

## Python Classes

### GreyScanIntelligence

Full intelligence platform with cross-platform correlation and analysis.

#### Usage

```python
import asyncio
from greyscan_intelligence import GreyScanIntelligence, IntelligenceTarget

async def main():
    # Define intelligence targets
    targets = [
        IntelligenceTarget("bitcoin", "coingecko", "cryptocurrency", ["btc"], 10, ["crypto"]),
        IntelligenceTarget("elonmusk", "twitter", "person", ["elon", "musk"], 10, ["tech"])
    ]
    
    # Run intelligence scan
    async with GreyScanIntelligence() as intel:
        report = await intel.full_intelligence_scan(targets)
        
        print(f"Intelligence Points: {report['summary']['total_intelligence_points']}")
        print(f"Entities Resolved: {report['summary']['unique_entities']}")
        print(f"Relationships Found: {report['summary']['relationships_found']}")

asyncio.run(main())
```

#### IntelligenceTarget Parameters

```python
IntelligenceTarget(
    name: str,              # Target identifier (e.g., "bitcoin", "elonmusk")
    platform: str,          # Platform to search (e.g., "coingecko", "twitter")
    target_type: str,       # Type: "person", "cryptocurrency", "topic", etc.
    aliases: List[str],     # Alternative names (e.g., ["btc", "bitcoin-core"])
    priority: int,          # Priority 1-10 (10 = highest)
    tags: List[str]         # Classification tags (e.g., ["crypto", "currency"])
)
```

### GreyScanUniversal

Universal platform scanner with 90% success rate across all major platforms.

#### Usage

```python
import asyncio
from greyscan_universal import GreyScanUniversal, UniversalTarget

async def main():
    targets = [
        UniversalTarget("bitcoin", "coingecko"),
        UniversalTarget("elonmusk", "twitter"),
        UniversalTarget("programming", "reddit")
    ]
    
    async with GreyScanUniversal() as scanner:
        results = await scanner.universal_scan(targets)
        
        print(f"Success Rate: {len(results)/len(targets):.1%}")
        for result in results:
            print(f"✅ {result['target']} on {result['platform']} - {result['data_size']} bytes")

asyncio.run(main())
```

### GreyScanEngine

Adaptive learning engine with pattern recognition.

#### Usage

```python
import asyncio
from greyscan_core import GreyScanEngine

async def main():
    engine = GreyScanEngine(target_symbols=["price", "volume", "market", "data"])
    
    targets = [
        ("bitcoin", "coingecko"),
        ("ethereum", "coingecko")
    ]
    
    try:
        results = await engine.adaptive_collect(targets)
        
        for result in results:
            print(f"Target: {result['target']}")
            print(f"Data Size: {result['data_size']} bytes")
            print(f"Method: {result['method']}")
            print(f"URL: {result['url']}")
    finally:
        await engine.close()

asyncio.run(main())
```

## Running the Scripts

### Intelligence Platform Test

```bash
python greyscan_intelligence.py
```

**Expected Output:**
```
🧠 TESTING FULL INTELLIGENCE SYSTEM
============================================================
📡 PHASE 1: DATA COLLECTION
🎯 [1/6] Collecting: elonmusk (twitter)
🎯 [2/6] Collecting: bitcoin (coingecko)
...
🎉 INTELLIGENCE OPERATION COMPLETE
📊 Data points collected: 1340
🔗 Entities resolved: 5
🕸️ Relationships found: 129
```

### Universal Scanner Test

```bash
python greyscan_universal.py
```

**Expected Output:**
```
🌍 TESTING UNIVERSAL SCANNER
============================================================
🎯 ATTACKING YOUTUBE: dQw4w9WgXcQ
✅ SUCCESS: dQw4w9WgXcQ on youtube - 107521 bytes
...
Success rate: 90.0% (9/10)
```

### Core Engine Test

```bash
python greyscan_core.py
```

**Expected Output:**
```
🔥 TESTING ADAPTIVE LEARNING ENGINE
============================================================
🚀 ADAPTIVE COLLECTION: 6 targets
✅ SUCCESS: bitcoin on coingecko - 94170 bytes
...
Success rate: 100.0% (6/6)
```

### GUI Interface

```bash
python greyscan_gui.py
```

**Launches:** Tkinter GUI with forms for target input and real-time results display.

## Data Structures

### Intelligence Report

```python
{
    "summary": {
        "total_intelligence_points": int,
        "unique_entities": int,
        "relationships_found": int,
        "platforms_covered": int,
        "cross_platform_entities": int
    },
    "entities": {
        "entity_id": {
            "name": str,
            "platforms": List[str],
            "intelligence_count": int,
            "data_types": List[str]
        }
    },
    "relationships": [
        {
            "source": str,
            "target": str,
            "type": str,
            "strength": float,
            "platforms": List[str]
        }
    ]
}
```

### Collection Result

```python
{
    "target": str,
    "platform": str,
    "url": str,
    "method": str,
    "data_size": int,
    "content": str,
    "extracted_data": dict,
    "timestamp": float
}
```

## Platform Support

### Confirmed Working Platforms

| Platform | Success Rate | Script | Method |
|----------|-------------|---------|---------|
| YouTube | 100% | universal | Embed endpoints |
| Instagram | 100% | universal | Embed widgets |
| Reddit | 100% | universal | JSON APIs |
| Twitter | 100% | universal | Google Cache |
| Medium | 100% | universal | Format parameters |
| CoinGecko | 100% | core/intelligence | Public APIs |
| Telegram | 100% | universal | Public channels |

### Platform-Specific Examples

#### Crypto Intelligence
```python
crypto_targets = [
    IntelligenceTarget("bitcoin", "coingecko", "cryptocurrency"),
    IntelligenceTarget("ethereum", "coingecko", "cryptocurrency"),
    IntelligenceTarget("BTC", "coinmarketcap", "cryptocurrency")
]
```

#### Social Media Intelligence
```python
social_targets = [
    UniversalTarget("elonmusk", "twitter"),
    UniversalTarget("programming", "reddit"),
    UniversalTarget("python", "medium")
]
```

#### Video Platform Intelligence
```python
video_targets = [
    UniversalTarget("dQw4w9WgXcQ", "youtube"),  # Video ID
    UniversalTarget("pewdiepie", "youtube")     # Channel
]
```

## Database Storage

The intelligence platform automatically creates an SQLite database (`intelligence.db`) with:

- **Entities table**: Unique entities with cross-platform links
- **Intelligence data table**: All collected data points
- **Relationships table**: Mapped connections between entities
- **Analysis results table**: Processed intelligence insights

## Error Handling

All scripts include comprehensive error handling:

```python
try:
    async with GreyScanIntelligence() as intel:
        report = await intel.full_intelligence_scan(targets)
except Exception as e:
    print(f"Error: {e}")
    # Script continues with partial results
```

## Performance Notes

- **Intelligence Platform**: ~3.65 seconds for 6 targets
- **Universal Scanner**: ~90% success rate across platforms
- **Core Engine**: 100% success rate on crypto targets
- **Memory Usage**: Minimal, results are streamed
- **Rate Limiting**: Automatic delays to prevent blocking

## Integration Examples

### Custom Script Integration

```python
# Your custom script
import asyncio
from greyscan_intelligence import GreyScanIntelligence, IntelligenceTarget

async def my_intelligence_operation():
    targets = [
        # Your targets here
    ]
    
    async with GreyScanIntelligence() as intel:
        report = await intel.full_intelligence_scan(targets)
        
        # Process results
        return report

# Run your operation
results = asyncio.run(my_intelligence_operation())
```

### Data Export

```python
import json

# Export intelligence report
with open('intelligence_report.json', 'w') as f:
    json.dump(report, f, indent=2)

# Export collection results
with open('collection_results.json', 'w') as f:
    json.dump(results, f, indent=2)
```

## Requirements

```
Python 3.8+
aiohttp
beautifulsoup4
networkx
sqlite3 (built-in)
tkinter (built-in, for GUI)
```

## Installation

```bash
# Clone repository
git clone https://github.com/Betti-Labs/greyscan.git
cd greyscan

# Install dependencies
pip install aiohttp beautifulsoup4 networkx

# Test the system
python greyscan_intelligence.py
```

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all dependencies are installed
2. **Network Timeouts**: Check internet connection
3. **Low Success Rates**: Verify target names are correct
4. **Database Errors**: Ensure write permissions in directory

### Debug Mode

Enable debug output by modifying the scripts:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Contributing

This is a research project. See `CONTRIBUTING.md` for guidelines.
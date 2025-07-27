# GreyScan API Reference

Complete API documentation for GreyScan adaptive data intelligence platform.

## Core Classes

### GreyScanEngine

The main adaptive intelligence engine for data collection.

#### Constructor

```python
from greyscan_core import GreyScanEngine

scanner = GreyScanEngine(target_symbols=None)
```

**Parameters:**
- `target_symbols` (List[str], optional): Keywords to search for in collected data. Defaults to crypto symbols.

**Example:**
```python
# For marketing research
scanner = GreyScanEngine(target_symbols=[
    "marketing", "brand", "campaign", "ROI", "conversion"
])

# For competitor analysis  
scanner = GreyScanEngine(target_symbols=[
    "product", "launch", "revenue", "growth", "partnership"
])
```

#### Methods

##### `async adaptive_collect(targets: List[Tuple[str, str]]) -> List[Dict[str, Any]]`

Collect data from targets using adaptive intelligence.

**Parameters:**
- `targets`: List of (target_name, target_type) tuples

**Returns:**
- List of dictionaries containing collected data

**Example:**
```python
targets = [
    ("microsoft", "tech_company"),
    ("google", "tech_company"),
    ("apple", "tech_company")
]

results = await scanner.adaptive_collect(targets)

for result in results:
    print(f"Target: {result['target']}")
    print(f"Data size: {result['data_size']} bytes")
    print(f"Keywords found: {result['symbols']}")
    print(f"Method used: {result['method']}")
```

**Response Format:**
```python
{
    "target": "microsoft",
    "target_type": "tech_company", 
    "method": "twitter_widgets",
    "url": "https://platform.twitter.com/widgets/follow_button.html?screen_name=microsoft",
    "content": "...",  # First 2000 chars
    "data_size": 60859,
    "symbols": ["AI", "cloud", "product"],
    "timestamp": "2025-01-27T12:00:00",
    "status": "success"
}
```

##### `async close()`

Clean up resources and close connections.

**Example:**
```python
try:
    results = await scanner.adaptive_collect(targets)
finally:
    await scanner.close()
```

### EmergentPathScraper

Advanced discovery engine for finding hidden data sources.

#### Constructor

```python
from greyscan_discovery import EmergentPathScraper

discoverer = EmergentPathScraper()
```

#### Methods

##### `async discover_emergent_paths(platform: str, targets: List[str], max_iterations: int = 3) -> List[EmergentPath]`

Discover hidden data pathways through adaptive learning.

**Parameters:**
- `platform`: Platform to analyze ("reddit", "github", "instagram", etc.)
- `targets`: List of target identifiers
- `max_iterations`: Maximum learning iterations (default: 3)

**Returns:**
- List of EmergentPath objects

**Example:**
```python
paths = await discoverer.discover_emergent_paths(
    platform="reddit",
    targets=["elonmusk", "VitalikButerin"],
    max_iterations=2
)

print(f"Discovered {len(paths)} emergent paths")
```

##### `display_discoveries()`

Display all discovered paths in formatted output.

**Example:**
```python
discoverer.display_discoveries()
```

## Data Structures

### EmergentPath

```python
@dataclass
class EmergentPath:
    platform: str              # Platform name
    original_target: str        # Target that led to discovery
    discovered_url: str         # Working URL found
    discovery_method: str       # How it was discovered
    success_rate: float         # Success probability
    data_types: List[str]       # Types of data available
    discovered_at: float        # Timestamp of discovery
```

### CollectionAttempt

```python
@dataclass
class CollectionAttempt:
    target: str                 # Target identifier
    target_type: str           # Type of target
    success: bool              # Whether attempt succeeded
    status_code: Optional[int] # HTTP status code
    data_size: int             # Size of collected data
    response_time: float       # Request response time
    method_used: str           # Collection method used
    failure_reason: Optional[str] # Reason for failure
    symbols_found: List[str]   # Keywords found in data
    timestamp: float           # Attempt timestamp
```

## Configuration

### Target Symbols

Customize keywords based on your use case:

```python
# Marketing & Advertising
marketing_symbols = [
    "marketing", "brand", "campaign", "engagement", "ROI", 
    "conversion", "audience", "content", "strategy", "social"
]

# Competitor Analysis
competitor_symbols = [
    "product", "launch", "revenue", "growth", "customers",
    "partnership", "acquisition", "funding", "expansion"
]

# Brand Monitoring
brand_symbols = [
    "review", "customer", "service", "quality", "price",
    "experience", "recommend", "love", "hate", "disappointed"
]

# Lead Generation
lead_symbols = [
    "CEO", "founder", "hiring", "team", "job", "career",
    "opportunity", "partnership", "contact", "demo"
]
```

### Platform Support

Currently supported platforms:

| Platform | Success Rate | Methods Available |
|----------|-------------|-------------------|
| Twitter/X | 100% | widget_bypass |
| Reddit | 67% | json_api, rss_feed, about_page |
| Instagram | 67% | public_profile, embed_api |
| TikTok | 83% | public_profile, rss_alternative |
| GitHub | 75% | user_api, repos_api, profile_page |
| Medium | 100% | user_profile, user_feed, user_api |
| LinkedIn | 0% | Rate limited (working on bypass) |

## Error Handling

### Common Exceptions

```python
try:
    results = await scanner.adaptive_collect(targets)
except asyncio.TimeoutError:
    print("Request timed out")
except aiohttp.ClientError as e:
    print(f"Network error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

### Failure Analysis

GreyScan automatically analyzes failures and learns from them:

```python
# Access failure analysis
for attempt in scanner.attempt_history:
    if not attempt.success:
        print(f"Failed: {attempt.target}")
        print(f"Reason: {attempt.failure_reason}")
        print(f"Status: {attempt.status_code}")
```

## Performance Optimization

### Batch Processing

```python
# Optimal batch sizes based on platform
batch_sizes = {
    "twitter": 8,    # High success rate
    "reddit": 4,     # Moderate rate limiting
    "instagram": 6,  # Good performance
    "github": 8,     # API + web hybrid
}
```

### Rate Limiting

GreyScan automatically handles rate limiting:

```python
# Adaptive delays based on success rate
# High success (>80%): 0.5s delay
# Medium success (50-80%): 1.0s delay  
# Low success (<50%): 2.0s+ delay
```

### Memory Management

```python
# Always close connections
async with GreyScanEngine() as scanner:
    results = await scanner.adaptive_collect(targets)
    # Automatically closed
```

## Advanced Usage

### Custom Learning

```python
# Access learned patterns
for pattern in scanner.learned_patterns:
    print(f"Pattern: {pattern.pattern_type}")
    print(f"Data: {pattern.pattern_data}")
    print(f"Confidence: {pattern.confidence}")
```

### Multi-Platform Collection

```python
async def collect_from_multiple_platforms():
    platforms = ["twitter", "reddit", "github"]
    all_results = []
    
    for platform in platforms:
        scanner = GreyScanEngine()
        try:
            results = await scanner.adaptive_collect(targets)
            all_results.extend(results)
        finally:
            await scanner.close()
    
    return all_results
```

### Real-Time Monitoring

```python
import asyncio

async def continuous_monitoring(targets, interval=300):
    """Monitor targets every 5 minutes"""
    scanner = GreyScanEngine()
    
    try:
        while True:
            results = await scanner.adaptive_collect(targets)
            
            # Process results
            for result in results:
                if result['symbols']:  # Found keywords
                    print(f"Alert: {result['target']} mentioned {result['symbols']}")
            
            await asyncio.sleep(interval)
    finally:
        await scanner.close()
```

## Integration Examples

### Flask Web App

```python
from flask import Flask, jsonify
from greyscan_core import GreyScanEngine

app = Flask(__name__)

@app.route('/scan/<target>')
async def scan_target(target):
    scanner = GreyScanEngine()
    try:
        results = await scanner.adaptive_collect([(target, "unknown")])
        return jsonify(results)
    finally:
        await scanner.close()
```

### Database Storage

```python
import sqlite3
import json

async def store_results(results):
    conn = sqlite3.connect('greyscan.db')
    
    for result in results:
        conn.execute("""
            INSERT INTO scans (target, data_size, symbols, timestamp)
            VALUES (?, ?, ?, ?)
        """, (
            result['target'],
            result['data_size'], 
            json.dumps(result['symbols']),
            result['timestamp']
        ))
    
    conn.commit()
    conn.close()
```

## Troubleshooting

See [Troubleshooting Guide](troubleshooting.md) for common issues and solutions.

## Contributing

See [Contributing Guide](../CONTRIBUTING.md) for development guidelines.
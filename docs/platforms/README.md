# Platform Guides

Comprehensive guides for each supported platform in GreyScan.

## Supported Platforms

| Platform | Success Rate | Guide | Status |
|----------|-------------|-------|---------|
| [Twitter/X](twitter.md) | 100% | ✅ Complete | Production Ready |
| [Reddit](reddit.md) | 67% | ✅ Complete | Production Ready |
| [Instagram](instagram.md) | 67% | ✅ Complete | Production Ready |
| [TikTok](tiktok.md) | 83% | ✅ Complete | Production Ready |
| [GitHub](github.md) | 75% | ✅ Complete | Production Ready |
| [Medium](medium.md) | 100% | ✅ Complete | Production Ready |
| [LinkedIn](linkedin.md) | 0% | ⚠️ Limited | Rate Limited |

## Quick Start by Platform

### Twitter/X - 100% Success Rate
```python
# Twitter breakthrough method
targets = [("elonmusk", "influencer"), ("microsoft", "company")]
results = await scanner.adaptive_collect(targets)
```

### Reddit - Multiple Methods
```python
# Reddit JSON API access
scanner = GreyScanEngine(target_symbols=["crypto", "bitcoin", "ethereum"])
targets = [("elonmusk", "user"), ("VitalikButerin", "user")]
results = await scanner.adaptive_collect(targets)
```

### GitHub - API + Web Hybrid
```python
# GitHub dual approach
targets = [("ethereum", "organization"), ("bitcoin", "organization")]
results = await scanner.adaptive_collect(targets)
```

## Platform-Specific Features

### Data Types by Platform

**Twitter/X:**
- Profile information
- Follower counts
- Tweet content (via widgets)
- Engagement metrics

**Reddit:**
- User karma scores
- Subreddit activity
- Post history
- Comment patterns

**Instagram:**
- Profile data
- Follower/following counts
- Post metadata
- Story highlights

**GitHub:**
- Repository information
- Contribution activity
- Organization membership
- Code statistics

## Best Practices by Platform

### Rate Limiting
- **Twitter**: No limits via widget method
- **Reddit**: 1 request per second recommended
- **Instagram**: 2-3 second delays between requests
- **GitHub**: API limits apply, use hybrid approach

### Data Quality
- **High Quality**: Twitter, Medium, GitHub
- **Medium Quality**: Reddit, TikTok
- **Variable Quality**: Instagram, LinkedIn

### Reliability
- **Most Reliable**: Twitter (100%), Medium (100%)
- **Very Reliable**: TikTok (83%), GitHub (75%)
- **Moderately Reliable**: Reddit (67%), Instagram (67%)
- **Unreliable**: LinkedIn (0% - rate limited)

## Adding New Platforms

See [Contributing Guide](../../CONTRIBUTING.md) for guidelines on adding new platform support.

## Troubleshooting

For platform-specific issues, see individual platform guides or the main [Troubleshooting Guide](../troubleshooting.md).
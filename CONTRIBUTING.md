# Contributing to GreyScan

Thank you for your interest in contributing to GreyScan! This document provides guidelines for contributing to the project.

## Code of Conduct

By participating in this project, you agree to abide by our Code of Conduct. Please treat all contributors with respect and create a welcoming environment for everyone.

## Getting Started

### Prerequisites
- Python 3.8 or higher
- Git
- Basic understanding of async/await programming

### Development Setup
1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/your-username/greyscan.git
   cd greyscan
   ```
3. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Development Guidelines

### Code Style
- Follow PEP 8 style guidelines
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Keep functions focused and small

### Testing
- Write tests for new features
- Ensure all tests pass before submitting
- Test with multiple platforms when possible

### Documentation
- Update README.md for new features
- Add inline comments for complex logic
- Update docstrings when changing function behavior

## Submitting Changes

### Pull Request Process
1. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```
2. Make your changes
3. Test thoroughly
4. Commit with clear messages:
   ```bash
   git commit -m "Add: Brief description of changes"
   ```
5. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```
6. Create a Pull Request

### Pull Request Guidelines
- Provide a clear description of changes
- Reference any related issues
- Include test results
- Ensure code follows style guidelines

## Types of Contributions

### Bug Reports
- Use the issue template
- Provide detailed reproduction steps
- Include system information
- Add relevant logs or error messages

### Feature Requests
- Describe the problem you're solving
- Explain your proposed solution
- Consider backward compatibility
- Discuss potential alternatives

### Code Contributions
- Platform adapters for new sites
- Learning algorithm improvements
- Performance optimizations
- Bug fixes

## Platform Adapter Guidelines

When adding support for new platforms:

1. **Research thoroughly**: Understand the platform's structure
2. **Start simple**: Begin with basic public data access
3. **Follow patterns**: Use existing adapters as templates
4. **Test extensively**: Verify with multiple accounts/targets
5. **Document findings**: Explain discovered patterns

### Adapter Structure
```python
async def collect_platform_data(self, target: str) -> Optional[Dict[str, Any]]:
    """
    Collect data from platform
    
    Args:
        target: Target identifier (username, etc.)
        
    Returns:
        Dictionary with collected data or None if failed
    """
    # Implementation here
```

## Learning Algorithm Contributions

When improving learning algorithms:

1. **Preserve existing functionality**
2. **Add comprehensive tests**
3. **Document algorithm changes**
4. **Consider performance impact**
5. **Validate with real data**

## Security Considerations

- Never commit credentials or API keys
- Respect rate limits and terms of service
- Consider privacy implications
- Use secure coding practices
- Report security issues privately

## Questions?

- Open an issue for general questions
- Use discussions for broader topics
- Contact maintainers for sensitive issues

Thank you for contributing to GreyScan!
# Contributing to Tetris Ultimate Edition

First off, thank you for considering contributing to Tetris Ultimate Edition! It's people like you that make this game better for everyone.

## Code of Conduct

This project and everyone participating in it is governed by our commitment to providing a welcoming and inspiring community for all. Please be respectful and constructive in all interactions.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the existing issues to avoid duplicates. When you create a bug report, include as many details as possible:

**Bug Report Template:**
- **Title**: Clear and descriptive title
- **Description**: Detailed description of the problem
- **Steps to Reproduce**:
  1. Step 1
  2. Step 2
  3. ...
- **Expected Behavior**: What you expected to happen
- **Actual Behavior**: What actually happened
- **Screenshots**: If applicable
- **Environment**:
  - OS: [e.g., Windows 11, macOS 13, Ubuntu 22.04]
  - Python Version: [e.g., 3.10.5]
  - Pygame Version: [e.g., 2.6.1]
- **Additional Context**: Any other relevant information

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, include:

- **Clear title** describing the enhancement
- **Detailed description** of the proposed functionality
- **Use case**: Why this enhancement would be useful
- **Possible implementation**: If you have ideas on how to implement it
- **Alternatives considered**: Other solutions you've thought about

### Pull Requests

1. **Fork the repository** and create your branch from `main`
2. **Make your changes** following our coding standards
3. **Add tests** if you've added code that should be tested
4. **Ensure the test suite passes**
5. **Update documentation** as needed
6. **Write a clear commit message**
7. **Submit your pull request**

## Development Process

### Setting Up Development Environment

```bash
# Clone your fork
git clone https://github.com/yourusername/tetris-ultimate.git
cd tetris-ultimate

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install pytest pytest-cov black pylint mypy

# Install package in editable mode
pip install -e .
```

### Running Tests

```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=tetris --cov-report=html

# Run specific test file
pytest tests/test_tetris.py -v

# Run tests with headless display (for CI)
export SDL_VIDEODRIVER=dummy
export SDL_AUDIODRIVER=dummy
pytest
```

### Code Style

We follow PEP 8 Python style guide with some modifications:

- **Line length**: Maximum 100 characters
- **Quotes**: Use double quotes for strings
- **Imports**: Group imports (standard library, third-party, local)
- **Docstrings**: Use triple double quotes with clear descriptions

**Formatting Tools:**
```bash
# Format code with black
black tetris.py tests/

# Check with flake8
flake8 tetris.py tests/ --max-line-length=100

# Lint with pylint
pylint tetris.py

# Type checking with mypy
mypy tetris.py
```

### Commit Messages

Follow conventional commit format:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples:**
```
feat(gameplay): add power-up system

Implemented a power-up system that spawns randomly during gameplay.
Power-ups include speed boost, clear line, and bomb.

Closes #123
```

```
fix(rotation): correct wall-kick behavior for I-piece

Fixed an issue where the I-piece would not rotate correctly
near the walls. Updated rotation logic to follow SRS guidelines.

Fixes #456
```

### Branch Naming

- `feature/description` - For new features
- `fix/description` - For bug fixes
- `docs/description` - For documentation
- `refactor/description` - For refactoring

## Testing Guidelines

### Writing Tests

- Write tests for all new functionality
- Maintain or improve code coverage
- Use descriptive test names
- Follow AAA pattern (Arrange, Act, Assert)
- Mock external dependencies when appropriate

**Example Test:**
```python
def test_piece_rotation(self, game):
    """Test that pieces rotate correctly"""
    # Arrange
    original_shape = game.current_piece.shape
    
    # Act
    game.rotate_piece()
    
    # Assert
    assert game.current_piece.shape != original_shape
```

### Test Coverage

- Aim for >80% code coverage
- All new features must have tests
- Critical paths should have comprehensive tests

## Documentation

### Code Documentation

- Add docstrings to all classes and functions
- Use clear, descriptive variable names
- Comment complex logic
- Keep README up to date

### README Updates

When adding features, update:
- Features list
- Controls (if applicable)
- Installation instructions (if needed)
- Usage examples

## Pull Request Process

1. **Update Documentation**: Ensure all docs reflect your changes
2. **Add Tests**: Include tests for new functionality
3. **Run Tests**: Ensure all tests pass locally
4. **Update CHANGELOG**: Add entry describing your changes
5. **Create PR**: Use the PR template and fill it out completely
6. **Code Review**: Address any feedback from reviewers
7. **Merge**: Once approved, your PR will be merged

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
How has this been tested?

## Checklist
- [ ] My code follows the style guidelines
- [ ] I have performed a self-review
- [ ] I have commented my code
- [ ] I have updated the documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests
- [ ] New and existing tests pass
- [ ] I have updated CHANGELOG.md
```

## Recognition

Contributors will be recognized in:
- CONTRIBUTORS.md file
- Release notes
- GitHub contributors page

## Questions?

Feel free to:
- Open an issue for questions
- Reach out to maintainers
- Check existing documentation

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to Tetris Ultimate Edition! 🎮

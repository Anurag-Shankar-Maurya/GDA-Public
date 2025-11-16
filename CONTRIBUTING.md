# Contributing to GDA - Global Development Alliance

Thank you for your interest in contributing to the Global Development Alliance platform! We welcome contributions from developers, designers, and community members who share our vision of empowering volunteer organizations worldwide.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Documentation](#documentation)
- [Pull Request Process](#pull-request-process)
- [Issue Reporting](#issue-reporting)
- [Community](#community)

## 🤝 Code of Conduct

This project adheres to a code of conduct to ensure a welcoming environment for all contributors. By participating, you agree to:

- **Be Respectful**: Treat all individuals with respect and kindness
- **Be Inclusive**: Welcome contributors from all backgrounds and skill levels
- **Be Collaborative**: Work together constructively toward shared goals
- **Be Professional**: Maintain professional communication and behavior

## 🚀 Getting Started

### Prerequisites
- Python 3.10 or higher
- Git
- Virtual environment manager
- Code editor (VS Code recommended)

### Setup Development Environment

1. **Fork and Clone**
   ```bash
   git clone https://github.com/YOUR_USERNAME/GDA2.git
   cd GDA2
   ```

2. **Create Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Environment Setup**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

4. **Database Setup**
   ```bash
   cd gda
   python manage.py migrate
   python manage.py createsuperuser
   ```

5. **Run Development Server**
   ```bash
   python manage.py runserver
   ```

## 🔄 Development Workflow

### Branch Naming Convention
```
feature/description-of-feature
bugfix/description-of-bug
hotfix/critical-fix
docs/update-documentation
refactor/code-improvement
```

### Commit Message Format
```
type(scope): description

[optional body]

[optional footer]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance tasks

**Examples:**
```
feat(auth): add OAuth2 social login
fix(user-profile): resolve avatar upload issue
docs(readme): update installation instructions
```

## 📝 Coding Standards

### Python Standards
- Follow [PEP 8](https://pep8.org/) style guide
- Use [Black](https://black.readthedocs.io/) for code formatting
- Maximum line length: 88 characters
- Use meaningful variable and function names

### Django Best Practices
- Follow [Django coding style](https://docs.djangoproject.com/en/stable/internals/contributing/writing-code/coding-style/)
- Use Django's built-in authentication and authorization
- Implement proper error handling and logging
- Write comprehensive docstrings for models and views

### JavaScript Standards
- Use ES6+ features
- Follow [Airbnb JavaScript Style Guide](https://github.com/airbnb/javascript)
- Use meaningful variable names
- Add comments for complex logic

### HTML/CSS Standards
- Use semantic HTML5 elements
- Follow BEM methodology for CSS classes
- Ensure responsive design principles
- Maintain accessibility standards (WCAG 2.1)

## 🧪 Testing Guidelines

### Test Coverage Requirements
- **Minimum Coverage**: 80% code coverage
- **Critical Paths**: 95% coverage for authentication and payment flows
- **New Features**: 100% coverage for new code

### Test Categories
```python
# Unit Tests
def test_user_creation():
    """Test user model creation and validation"""

# Integration Tests
def test_project_enrollment_flow():
    """Test complete project enrollment workflow"""

# End-to-End Tests
def test_admin_dashboard_access():
    """Test admin dashboard functionality"""
```

### Running Tests
```bash
# Run all tests
python manage.py test

# Run with coverage
coverage run manage.py test
coverage report --fail-under=80

# Run specific test file
python manage.py test apps.users.tests.test_models

# Run tests for specific app
python manage.py test users
```

## 📚 Documentation

### Code Documentation
- **Docstrings**: Use Google-style docstrings for all functions and classes
- **Comments**: Add inline comments for complex logic
- **README**: Keep module-level README files updated

### API Documentation
- **OpenAPI/Swagger**: Document all API endpoints
- **Postman Collections**: Maintain up-to-date API collections
- **Usage Examples**: Provide code samples for common use cases

## 🔄 Pull Request Process

### Before Submitting
1. **Update Branch**: Ensure your branch is up-to-date with main
2. **Run Tests**: All tests must pass locally
3. **Code Quality**: Run linting and formatting checks
4. **Documentation**: Update relevant documentation

### PR Template
```markdown
## Description
Brief description of the changes made

## Type of Change
- [ ] Bug fix (non-breaking change)
- [ ] New feature (non-breaking change)
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] Manual testing completed

## Screenshots (if applicable)
Add screenshots of UI changes

## Checklist
- [ ] Code follows project standards
- [ ] Tests pass locally
- [ ] Documentation updated
- [ ] No breaking changes
```

### Review Process
1. **Automated Checks**: CI/CD pipeline runs tests and linting
2. **Peer Review**: At least one maintainer reviews the code
3. **Approval**: PR approved by maintainer
4. **Merge**: Squash merge with descriptive commit message

## 🐛 Issue Reporting

### Bug Reports
**Template:**
```
**Title:** [BUG] Brief description of the issue

**Environment:**
- OS: [e.g., Windows 10]
- Browser: [e.g., Chrome 91]
- Python Version: [e.g., 3.10.0]

**Steps to Reproduce:**
1. Go to '...'
2. Click on '...'
3. See error

**Expected Behavior:**
What should happen

**Actual Behavior:**
What actually happens

**Screenshots:**
If applicable, add screenshots

**Additional Context:**
Any other context about the problem
```

### Feature Requests
**Template:**
```
**Title:** [FEATURE] Brief description of requested feature

**Problem Statement:**
Describe the problem this feature would solve

**Proposed Solution:**
Describe your proposed solution

**Alternatives Considered:**
Describe alternative solutions you've considered

**Additional Context:**
Any other context or screenshots
```

## 🌐 Community

### Communication Channels
- **GitHub Discussions**: General discussions and Q&A
- **Discord**: Real-time community chat
- **Newsletter**: Monthly updates and announcements

### Getting Help
1. **Check Documentation**: Review README and docs first
2. **Search Issues**: Look for existing issues and solutions
3. **Create Discussion**: Ask questions in GitHub Discussions
4. **Contact Maintainers**: Reach out to core team members

### Recognition
Contributors are recognized through:
- **GitHub Contributors List**: Automatic recognition
- **Release Notes**: Feature credits in changelogs
- **Community Spotlight**: Featured contributor spotlights

## 🎯 Contribution Areas

### High Priority
- **Security**: Security vulnerability fixes
- **Performance**: Performance optimizations
- **Accessibility**: WCAG compliance improvements

### Medium Priority
- **New Features**: Core functionality enhancements
- **UI/UX**: User interface improvements
- **Documentation**: Documentation improvements

### Low Priority
- **Code Quality**: Refactoring and cleanup
- **Testing**: Additional test coverage
- **Tools**: Development tool improvements

## 📄 License

By contributing to this project, you agree that your contributions will be licensed under the same license as the project (MIT License).

## 🙏 Thank You

Your contributions help make the Global Development Alliance platform better for volunteer organizations worldwide. We appreciate your time and effort in making this project successful!

---

*For questions or support, please create a GitHub Discussion or contact the maintainers.*
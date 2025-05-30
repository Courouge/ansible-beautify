# 🤝 Contributing to Ansible Beautify

First off, thank you for considering contributing to Ansible Beautify! It's people like you that make this tool better for the entire Ansible community.

## 🎯 Ways to Contribute

### 🐛 Reporting Bugs
- Use the GitHub issue tracker
- Describe the bug clearly with steps to reproduce
- Include your environment details (OS, browser, etc.)
- Add screenshots if applicable

### 💡 Suggesting Features
- Open a feature request on GitHub
- Describe the use case and expected behavior
- Explain why this would be useful for other users

### 🔧 Code Contributions
- Fix bugs or implement new features
- Improve documentation
- Add tests
- Optimize performance

### 📚 Documentation
- Improve README or other docs
- Add examples and use cases
- Fix typos or unclear instructions

## 🚀 Getting Started

### Prerequisites
- Node.js 14+ and npm
- Python 3.7+
- Docker and Docker Compose (recommended)

### Development Setup

1. **Fork and clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/ansible-beautify.git
   cd ansible-beautify
   ```

2. **Start with Docker (Recommended)**
   ```bash
   docker-compose up -d --build
   ```

3. **Or run manually:**
   
   **Backend:**
   ```bash
   cd backend
   pip install -r requirements.txt
   python api.py
   ```
   
   **Frontend:**
   ```bash
   cd react-api
   npm install
   npm start
   ```

4. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:5000

## 📝 Pull Request Process

### Before You Start
1. Create an issue to discuss major changes
2. Fork the repository
3. Create a feature branch: `git checkout -b feature/amazing-feature`

### Making Changes
1. **Follow coding standards:**
   - Use meaningful commit messages
   - Follow existing code style
   - Add comments for complex logic
   - Keep functions small and focused

2. **For Frontend (React):**
   - Use functional components when possible
   - Follow React best practices
   - Ensure responsive design
   - Test on multiple browsers

3. **For Backend (Python):**
   - Follow PEP 8 style guide
   - Add proper error handling
   - Document functions with docstrings
   - Ensure Python 3.7+ compatibility

### Testing Your Changes
1. **Manual Testing:**
   - Test the basic functionality
   - Try edge cases and error scenarios
   - Test on different screen sizes
   - Verify all Ansible modules work

2. **Code Quality:**
   - Run linting tools
   - Check for console errors
   - Ensure no broken functionality

### Submitting
1. **Commit your changes:**
   ```bash
   git add .
   git commit -m "feat: add amazing new feature"
   ```

2. **Push to your fork:**
   ```bash
   git push origin feature/amazing-feature
   ```

3. **Create a Pull Request:**
   - Use a clear, descriptive title
   - Describe what changes you made and why
   - Reference any related issues
   - Add screenshots for UI changes

## 📋 Commit Message Convention

We use conventional commits for clear history:

- `feat:` new feature
- `fix:` bug fix
- `docs:` documentation changes
- `style:` formatting, missing semicolons, etc.
- `refactor:` code refactoring
- `test:` adding tests
- `chore:` updating build tasks, etc.

Examples:
```bash
feat: add copy to clipboard functionality
fix: resolve parsing error for complex modules
docs: update installation instructions
style: improve responsive design for mobile
```

## 🎨 Adding New Ansible Modules

To add support for new Ansible modules:

1. **Add to modules list:**
   ```bash
   echo "your_module_name" >> backend/modules.txt
   ```

2. **Test the module:**
   - Create test cases with your module
   - Ensure proper parsing and formatting
   - Test edge cases

3. **Submit PR:**
   - Include example usage in PR description
   - Add module documentation link if available

## 🐛 Bug Report Template

When reporting bugs, please include:

```markdown
## Bug Description
A clear description of what the bug is.

## Steps to Reproduce
1. Go to '...'
2. Click on '....'
3. Enter text '....'
4. See error

## Expected Behavior
What you expected to happen.

## Screenshots
If applicable, add screenshots.

## Environment
- OS: [e.g. Windows 10, macOS Big Sur, Ubuntu 20.04]
- Browser: [e.g. Chrome 95, Firefox 94]
- Version: [e.g. 1.0.0]
```

## 💡 Feature Request Template

```markdown
## Feature Description
A clear description of the feature you'd like to see.

## Use Case
Describe the use case and why this would be valuable.

## Proposed Solution
If you have ideas on how to implement this.

## Alternatives Considered
Any alternative solutions you've thought about.
```

## 📚 Resources

- [Ansible Documentation](https://docs.ansible.com/)
- [React Documentation](https://reactjs.org/docs/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Bootstrap Documentation](https://getbootstrap.com/docs/)

## 🏆 Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes for significant contributions
- Special thanks in project announcements

## 📞 Getting Help

- Open an issue for bugs or feature requests
- Join discussions in existing issues
- Check existing documentation and FAQs

## 📄 License

By contributing, you agree that your contributions will be licensed under the same license as the project (MIT License).

---

**Thank you for making Ansible Beautify better! 🎉** 
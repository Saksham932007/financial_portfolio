# Security Policy

## Supported Versions

Currently supported versions with security updates:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

## Reporting a Vulnerability

We take security seriously. If you discover a security vulnerability, please follow these steps:

### 1. Do NOT Open a Public Issue

Please do not create a public GitHub issue for security vulnerabilities.

### 2. Report Privately

Email security details to: [Create an email or use GitHub Security Advisories]

Or use GitHub's private vulnerability reporting feature:
1. Go to the repository
2. Click "Security" tab
3. Click "Report a vulnerability"

### 3. Include Details

Please include:
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)
- Your contact information

### 4. Response Timeline

- **Initial Response**: Within 48 hours
- **Status Update**: Within 7 days
- **Fix Timeline**: Varies by severity

## Security Best Practices

### For Users

1. **API Keys**
   - Never commit `.env` files
   - Use environment variables
   - Rotate keys regularly
   - Keep keys private

2. **Dependencies**
   - Keep dependencies updated
   - Review `requirements.txt` regularly
   - Use virtual environments

3. **Data Security**
   - Don't share portfolio files publicly
   - Secure your output directory
   - Review logs before sharing

4. **Network Security**
   - Use HTTPS for all API calls
   - Verify SSL certificates
   - Use secure networks

### For Contributors

1. **Code Review**
   - Review all dependencies
   - Check for hardcoded secrets
   - Validate input data
   - Handle errors securely

2. **Sensitive Data**
   - No API keys in code
   - No personal information
   - No financial credentials
   - Use .gitignore properly

3. **Dependencies**
   - Only trusted sources
   - Check for CVEs
   - Pin versions
   - Regular audits

## Known Security Considerations

### API Keys
- Gemini API keys must be kept secret
- Store in `.env` file only
- Never log API keys
- Use environment variables in production

### Data Privacy
- Market data is public
- Recommendations stored locally
- No data sent to third parties (except APIs)
- User responsible for data security

### Network Requests
- All API calls use HTTPS
- Validate responses
- Handle rate limiting
- Timeout protection

### Input Validation
- Ticker symbols validated
- JSON parsing secured
- File operations sandboxed
- Error handling in place

## Disclosure Policy

When a vulnerability is reported:

1. **Confirmation**: We confirm receipt within 48 hours
2. **Assessment**: We assess severity and impact
3. **Fix Development**: We develop and test a fix
4. **Disclosure**:
   - Private notification to reporter
   - Security advisory published
   - Patch released
   - Public disclosure (coordinated)

## Security Updates

Subscribe to security updates:
- Watch the repository
- Enable GitHub notifications
- Check CHANGELOG.md regularly
- Follow release notes

## Acknowledgments

We appreciate security researchers and users who report vulnerabilities responsibly.

Contributors who report valid security issues may be acknowledged in:
- CHANGELOG.md
- Security advisories
- Project documentation

---

**Thank you for helping keep this project secure!**

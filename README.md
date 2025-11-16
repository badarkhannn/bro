# 🤖 Browser-Use Automation Orchestrator

An intelligent, interactive Python program that asks users what they want to automate and builds browser automation dynamically using browser-use.

## ✨ Features

- **Interactive Question-Based Setup** - Just describe what you want, answer questions, done!
- **Dynamic Automation Building** - Constructs browser-use workflows on the fly
- **Complete Workflow Support**:
  - 🌐 Web navigation
  - 🔐 Login automation
  - 📥 Data extraction/scraping
  - 📤 Form filling
  - 📸 Screenshot capture
  - 💾 Multiple output formats (text, JSON, CSV)
- **Smart Error Handling** - Self-correcting automation
- **Secure Credential Management** - Handles sensitive data safely

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Get API Key

Get your free Browser-Use API key (includes $10 credit):
👉 [https://cloud.browser-use.com/new-api-key](https://cloud.browser-use.com/new-api-key)

### 3. Configure Environment

```bash
cp .env.example .env
```

Edit `.env` and add your API key:
```
BROWSER_USE_API_KEY=your_actual_key_here
```

### 4. Run the Orchestrator

```bash
python browser_automation_orchestrator.py
```

## 📖 Usage Examples

### Example 1: Simple Web Scraping

```
👉 Your task: Scrape top 5 posts from Hacker News
🌐 URL: https://news.ycombinator.com
🔐 Login required? n
📥 Extract data? y
   👉 Fields: title, score, link
📤 Fill forms? n
💾 Output: 2 (JSON)
👁️  Headless? y
📸 Vision? y
```

### Example 2: Login and Download

```
👉 Your task: Login to dashboard and download monthly report
🌐 URL: https://example.com/login
🔐 Login required? y
   👤 Username: user@example.com
   🔑 Password: mypassword123
📥 Extract data? n
📤 Fill forms? n
💾 Output: 4 (Screenshot)
👁️  Headless? n
📸 Vision? y
```

### Example 3: Form Automation

```
👉 Your task: Fill out contact form on company website
🌐 URL: https://example.com/contact
🔐 Login required? n
📥 Extract data? n
📤 Fill forms? y
   👉 name=John Doe
   👉 email=john@example.com
   👉 message=Hello, I'm interested in your services
   👉 done
💾 Output: 1 (Text)
👁️  Headless? y
📸 Vision? y
```

## 🎯 What Can It Automate?

✅ **Web Scraping**
- Product prices
- News articles
- Social media posts
- Job listings
- Real estate data

✅ **Form Automation**
- Contact forms
- Registration forms
- Survey submissions
- Data entry tasks

✅ **Authentication**
- Login flows
- Multi-step authentication
- Session management

✅ **Data Extraction**
- Tables and lists
- PDFs and documents
- Images and media
- Structured data

✅ **Monitoring**
- Price tracking
- Content change detection
- Availability checks

✅ **Complex Workflows**
- Multi-page navigation
- Tab management
- Sequential tasks
- Conditional logic

## 🛠️ Architecture

```
┌─────────────────────────────────────┐
│  User Interactive Input             │
│  (Questions & Answers)              │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│  Automation Orchestrator            │
│  - Parse requirements               │
│  - Build dynamic plan               │
│  - Validate inputs                  │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│  Browser-Use Agent                  │
│  - Execute navigation               │
│  - Perform actions                  │
│  - Extract data                     │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│  Results & Output                   │
│  - Format data (JSON/CSV/Text)      │
│  - Save screenshots                 │
│  - Display summary                  │
└─────────────────────────────────────┘
```

## 🔧 Configuration Options

### Browser Settings
- **Headless Mode**: Run browser in background (faster, no UI)
- **Vision Mode**: Enable AI screenshot analysis (recommended)
- **Max Steps**: Maximum automation steps (default: 100)

### Output Formats
1. **Text** - Console output (good for simple tasks)
2. **JSON** - Structured data file (best for scraping)
3. **CSV** - Spreadsheet format (great for data analysis)
4. **Screenshot** - Visual capture (useful for verification)

### Security
- Credentials are handled as sensitive data
- Not sent to LLM when vision mode is disabled
- Stored securely during execution only

## 🧠 How It Works

### Step 1: Understanding Your Task
The orchestrator asks:
- What do you want to automate?
- Where should it start? (URL)
- Does it need login?
- What data to extract/input?
- How to format output?

### Step 2: Planning
Based on your answers, it generates:
- Sequential workflow steps
- Required browser actions
- Data handling strategy
- Error recovery plan

### Step 3: Execution
The browser-use agent:
- Navigates to URLs
- Interacts with elements
- Fills forms
- Extracts data
- Handles errors

### Step 4: Results
You receive:
- Execution summary
- Extracted data (in chosen format)
- URLs visited
- Screenshots (if requested)

## 🛡️ Safety Features

- ✅ Confirmation before execution
- ✅ Secure credential handling
- ✅ No data persistence after task
- ✅ User control at every step
- ✅ Clear error messages

## 📚 Advanced Usage

### Custom Workflows

You can modify the orchestrator to add:
- Scheduled automations (using APScheduler)
- Multi-agent coordination
- Database integration
- API webhooks
- Email notifications

### Extending Capabilities

The modular design allows easy extension:

```python
# Add custom automation types
def _handle_custom_workflow(self):
    # Your custom logic here
    pass
```

## 🐛 Troubleshooting

**Issue**: API Key not found
```
❌ ERROR: BROWSER_USE_API_KEY not found in environment!
```
**Solution**: Create `.env` file with your API key

**Issue**: Browser fails to start
**Solution**: Install Chromium: `uvx browser-use install`

**Issue**: Automation gets stuck
**Solution**: Reduce `max_steps` or enable vision mode

**Issue**: Login not working
**Solution**: Disable vision when using sensitive data

## 🤝 Contributing

Want to add features? Ideas welcome:
- Multi-language support
- Pre-built automation templates
- Visual workflow builder
- Integration with other tools

## 📄 License

MIT License - Free to use and modify

## 🙏 Credits

Built with:
- [browser-use](https://github.com/browser-use/browser-use) - Browser automation framework
- [Pydantic](https://pydantic.dev/) - Data validation
- [Python asyncio](https://docs.python.org/3/library/asyncio.html) - Async execution

## 📞 Support

- 📖 Documentation: [https://docs.browser-use.com](https://docs.browser-use.com)
- 💬 Discord: [https://link.browser-use.com/discord](https://link.browser-use.com/discord)
- 🐛 Issues: [GitHub Issues](https://github.com/browser-use/browser-use/issues)

---

**Made with ❤️ for automation enthusiasts**

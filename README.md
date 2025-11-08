# Browser Use Patched

A patched version of the `browser-use` library that adds additional features for web browser automation.

## Description

`browser-use-patched` extends the original `browser-use` library by adding:
- Enhanced methods for DOM representation
- Complete page loading wait management
- Page-specific data persistence
- Improved browser state formatting for LLMs

## Installation

### Method 1: Direct installation from GitHub

```bash
pip install git+https://github.com/Jourdelune/browser_use_patched.git
```

### Method 2: Installation from source code

1. Clone the repository:
```bash
git clone https://github.com/Jourdelune/browser_use_patched.git
cd browser_use_patched
```

2. Install the library:
```bash
pip install -e .
```

### Method 3: With uv (recommended for development)

```bash
# Clone the repository
git clone https://github.com/Jourdelune/browser_use_patched.git
cd browser_use_patched

# Install with uv
uv sync
```

## Requirements

- Python >= 3.12
- `browser-use` >= 0.9.5 (installed automatically)

## Usage

```python
from browser_use_patched import Browser, Page, Agent, ChatOpenAI

# Create a browser instance
browser = Browser()

# Create a new page
page = await browser.new_page("https://example.com")

# Wait for complete loading
await page.wait_until_fully_loaded()

# Get DOM representation for LLM
dom_representation = await page.get_llm_dom_representation()

# Save page-specific data
await page.push_data({"url": "https://example.com", "timestamp": "2025-11-08"})
```

## Added Features

### Extended Page Class

- `get_llm_dom_representation()`: Gets DOM representation optimized for LLMs
- `get_evaluation_dom_representation()`: Gets DOM representation for evaluation
- `wait_until_fully_loaded()`: Waits until the page is completely loaded
- `push_data(data)`: Saves data to a page-specific JSON file

### Extended Browser Class

- `format_browser_state_for_llm()`: Formats browser state for LLM consumption

## Configuration

The library uses the following environment variables:

- `DATA_DIR`: Directory to store data files (default: `./data`)

You can configure these variables in a `.env` file:

```env
DATA_DIR=./data
```

## Development

To contribute to the project:

1. Fork the repository
2. Create a branch for your feature
3. Install development dependencies with `uv sync`
4. Make your changes
5. Test your changes
6. Submit a pull request

## License

This project extends `browser-use` and respects its license.

## Author

- **Jourdelune** - [jourdelune863@gmail.com](mailto:jourdelune863@gmail.com)
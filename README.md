# Transylvania

Korean to English translation using [Argos Translate](https://github.com/argosopentech/argos-translate).

## Installation

Requires Python 3.12+.

```bash
# Clone the repository
git clone https://github.com/jeffreycstark/transylvania.git
cd transylvania

# Install dependencies
uv sync

# Download the Korean→English language pack
uv run download-languages
```

## Usage

### Command Line

```bash
# Translate text directly
uv run translate "안녕하세요"
# Output: Hello

# Translate from stdin
echo "오늘 날씨가 좋습니다" | uv run translate
# Output: Today's weather is good

# Check if language pack is installed
uv run translate --check

# Install language pack via CLI
uv run translate --install
```

### Python API

```python
from transylvania import translate, Translator

# Simple function
result = translate("안녕하세요")
print(result)  # Hello

# Class-based usage
translator = Translator()
result = translator.translate("감사합니다")
print(result)  # Thank you

# Batch translation
texts = ["안녕", "감사합니다", "좋은 하루 되세요"]
results = translator.translate_batch(texts)
```

## Development

```bash
# Create virtual environment with uv
uv venv --python 3.12

# Install in development mode
uv sync

# Run tests
uv run python -m pytest
```

## License

MIT

# Contributing to MnemoCLI 🏛️

First off, thank you for considering contributing to MnemoCLI! It’s people like you who make this a better tool for the memory athlete community.

## 🛠️ Development Setup

MnemoCLI requires **Python 3.10+**. 

1. **Fork and Clone** the repository.
2. **Create a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   # OR
   .\venv\Scripts\activate   # Windows
   ```
3. **Install Dependencies**:
   ```bash
   pip install -e .
   ```
   *The `-e` flag installs the package in "editable" mode, so changes to the code are reflected immediately when you run the `mnemocli` command.*

## 🌐 Adding New Languages
The easiest way to contribute is by adding or improving word lists!
1. Navigate to `mnemocli/languages/`.
2. Create a new JSON file (e.g., `spanish.json`).
3. Follow the existing format:
   ```json
   {
     "spanish_words": ["palabra1", "palabra2", "..."]
   }
   ```
4. Ensure the list contains at least 500-1000 common, concrete nouns for better visualization.

## 🖇️ Pull Request Process
1. Create a new branch for your feature or bugfix: `git checkout -b feat/your-feature-name`.
2. Ensure your code follows PEP 8 standards.
3. If you added a new mode, ensure it is integrated into `cli.py`.
4. Submit a Pull Request with a clear description of what has changed.

## 🐞 Reporting Bugs
Please use the **Bug Report** template when opening an issue so we can help you as quickly as possible.

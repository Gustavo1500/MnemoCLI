# 🏛️ MnemoCLI 🏛️
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![PyPI version](https://img.shields.io/pypi/v/mnemocli-loci.svg)](https://pypi.org/project/mnemocli-loci/)

**MnemoCLI** is a minimalist, high-performance command-line mental gymnasium designed to help you master the **Method of Loci** (Memory Palaces). 

Whether you are a student memorizing for exams, a language learner building vocabulary, or a memory athlete training for a competition, MnemoCLI provides a focused environment to sharpen your cognitive recall and encoding speed.

---

## 🛠 Installation

MnemoCLI requires **Python 3.10+**.

### Option A: Stable Release (Recommended)
Install the latest verified version directly from PyPI:
```bash
pip install mnemocli-loci
```

### Option B: Bleeding Edge (Development)
If you want the absolute latest features and word-list updates before they hit the official release, install directly from the GitHub repository:
```bash
pip install git+https://github.com/Gustavo1500/mnemocli.git
```

### 🔄 How to Update
| Method | Command to Update | Description |
| :--- | :--- | :--- |
| **PyPI** | `pip install -U mnemocli-loci` | Updates to the latest **stable** version. |
| **GitHub** | `pip install --force-reinstall git+https://github.com/Gustavo1500/mnemocli.git` | Pulls the latest **commit** from the main branch. |

**Note for Linux/macOS users:** If you encounter a "break-system-packages" error, it is recommended to install via `pipx install mnemocli` or use a Python Virtual Environment.

---

## 🎮 Training Modes

### 1. Palace Navigation
*   **Normal Run:** A steady walk-through of your palace stations.
*   **Random Drill:** The system calls out a locus number; visualize that station instantly.
*   **Palace Rush:** A timed sprint to recall your entire palace (supports Reverse mode).
*   **Middle-Out:** Start at the center of your palace and expand outward in both directions.

### 2. Content Memorization
*   **Random Numbers:** Generates sequences of digits (0-9). Practice your Major System or PAO.
*   **Random Words:** Pulls words from extensive dictionaries (**English** or **Portuguese**).

### 3. The Proving Grounds
*   **Standard Mode:** A daily maintenance session. It starts with a warm-up and follows with randomized drills until your timer expires.
*   **Olympic Mode:** Randomized competition events (Numbers or Words) with a 5-minute limit and four difficulty tiers (Beginner to Pro). Your stats are saved for progress tracking.

---

## 📖 Usage Guide

Once installed, you can launch the app from anywhere in your terminal using the `mnemocli` command.

### Command Syntax
```bash
mnemocli [mode] [arguments]
```

### Arguments & Flags
Depending on the mode you select, you will need to provide specific flags:

| Flag | Long Form | Description | Required For |
| :--- | :--- | :--- | :--- |
| `-la` | `--loci_amount` | The total number of stations in your memory palace. | `standard`, `random_drill`, `palace_rush`, `middle_out`, `normal_run`, `even_run`, `odd_run`. |
| `-a` | `--amount` | The number of items (words or digits) to generate for a session. | `random_words`, `random_numbers`. |
| `-t` | `--time` | The time limit in **minutes**. Set to `0` for no limit. | `standard`, `random_words`, `random_numbers`. |

*Note: In `random_words` or `random_numbers` modes, if you provide `-la` but omit `-a`, the item amount will default to the number of loci provided.*

### Examples

**Daily 10-minute palace maintenance (50 stations):**
```bash
mnemocli standard -la 50 -t 10
```

**Memorize 40 Random Words (Time limit of 8 minutes):**
```bash
mnemocli random_words -a 40 -t 8
```

**View your Olympic progress graph:**
```bash
mnemocli graph
```

**Check data storage location and version:**
```bash
mnemocli info
```

---

## ⚙️ Configuration & Data

Upon first run, MnemoCLI creates a hidden directory in your home folder:
*   **Linux/macOS:** `~/.mnemocli`
*   **Windows:** `C:\Users\<User>\.mnemocli`

### Customization
You can edit `~/.mnemocli/config.ini` to change:
*   Default training language (English/Portuguese).
*   Default session timers.
*   Which modes are included in your "Standard" daily workout.

### Data Safety
To wipe your history and reset the app to factory settings, run:
```bash
mnemocli cleanup
```

---

## 🌐 Language Support
MnemoCLI includes curated word lists with **2,300+ entries** for:
- 🇺🇸 🇬🇧 English
- 🇧🇷 🇵🇹 Portuguese

**Contributions are welcome!** To add a new language, follow the JSON format in the `mnemocli/languages/` folder and submit a Pull Request.

---

## ⚖️ License

This project is licensed under the **GNU General Public License v3.0**. 

- **Freedom to modify:** You can change the code however you like.
- **Freedom to share:** You can redistribute the code.
- **Stay Open:** If you modify and share this project, your version must also be licensed under the GPL v3.0 (Copyleft).

See the [LICENSE](LICENSE) file for the full legal text.

---

## 🧩 Contribution & Philosophy

MnemoCLI is built on the belief that a better memory leads to a more organized and creative life. This tool is for everyone—from the casual hobbyist to the competitive pro. 

**Want to help?** We welcome word-list updates, bug fixes, and new training modes! Please read our [**Contributing Guidelines**](CONTRIBUTING.md) to get started.

If you find a bug or have a feature request, please [open an issue](https://github.com/Gustavo1500/mnemocli/issues).

**I have built this tool to help me master the Method of Loci, and I hope it can help you too. All feedback and contributions are greatly appreciated!**

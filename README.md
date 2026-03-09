# 🏛️ MnemoCLI 🏛️
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

**MnemoCLI** is a minimalist, high-performance command-line mental gymnasium designed to help you master the **Method of Loci** (Memory Palaces). Whether you are a student memorizing for exams, a language learner building vocabulary, or a memory athlete training for a competition, MnemoCLI provides a flexible environment to sharpen your cognitive recall.

Memory is an ancient art that becomes a powerful modern tool through consistent practice. MnemoCLI is designed to be your primary workbench for that practice.

---

## 🌟 Why MnemoCLI?

Practice is necessary for mastery and reaching true fluency in the Art of Memory. MnemoCLI is designed to help you achieve this via various drills and exercises, whether you are practicing navigation within a specific palace or attempting to memorize random numbers and words. The goal is for you to reach a level of fluency where the Method of Loci becomes second nature. 

By moving past the beginner stage—where one might simply place a dozen images and rely on slow spaced repetition—this tool allows you to build deep mastery over the technique and your specific palaces. With enough practice using these drills, the act of encoding and recalling information will shift from a conscious struggle to feeling completely effortless.

---

## 🌐 Language Support & Customization

MnemoCLI is built to be accessible across different languages and is designed for easy community expansion:

- **Current Support:** Includes word lists for **English** and **Portuguese**, with over **2,300+ words** available for each. 
- **Community Contributions:** If you have a refined list for an existing language or want to see a new language supported, your contributions are welcome! Simply follow the existing JSON format in the `json/` folder and submit a pull request or share your file.

---

## 🎮 Training Modes

### 1. Palace Navigation (The Blueprint)
- **Normal Run:** A steady walk-through of your palace to warm up.
- **Random Drill:** The system calls out a locus number; you must visualize that specific station instantly.
- **Palace Rush:** A timed sprint to recall your entire palace as fast as possible. With a reverse mode as well.
- **Even/Odd Run:** Practice jumping between non-linear stations to ensure your mental map is robust.

### 2. Content Memorization (The Cargo)
- **Random Numbers:** Generates sequences of digits (0-9). Essential for practicing the Major System or PAO.
- **Random Words:** Pulls words from the extensive dictionaries in English or Portuguese.

### 3. The Proving Grounds
- **Standard Mode:** A balanced training session starting with a warm-up and following with randomized drills until the set timer expires.
- **Olympic Mode:** Randomized competition events (Numbers or Words) with 5-minute limits and four difficulty tiers (Beginner to Pro).

---

## 🛠 Installation & Setup

### Requirements
Ensure you have Python 3.10+ installed. MnemoCLI relies on the following dependencies:
- `rich==14.3.3` (For terminal formatting and tables)
- `readchar==4.2.1` (For responsive keyboard input)

### Setup
1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/mnemocli.git
   cd mnemocli
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

## 📖 Usage Guide

### Command Syntax
```bash
python main.py [mode] [arguments]
```

### Key Arguments
- `-la, --loci_amount`: The number of stations in your palace.
- `-a, --amount`: The number of items (numbers/words) to generate.
- `-t, --time`: Your session or memorization limit in **minutes** (Default: 10).

### Examples

**A 10-minute "Standard" daily palace maintenance:**
```bash
python main.py standard -la 50 -t 10
```

**Memorize 40 Random Words (No time limit):**
```bash
python main.py random_words -a 40 -t 0
```

**Start a randomized 5-minute "Olympic" challenge:**
```bash
python main.py olympic
```

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

If you find a bug, have a feature request, or want to contribute a more curated dictionary for any language, please open an issue or submit a pull request.

**I have built this tool to help me master the Method of Loci, and I hope it can help you too. All feedback and contributions are greatly appreciated!**

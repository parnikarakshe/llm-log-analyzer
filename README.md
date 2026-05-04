<<<<<<< HEAD
# 🔍 LLM Log Analyzer

> An AI-powered log analysis pipeline that automatically triages failures, classifies errors by severity, identifies root causes, and generates structured bug reports — powered by Google Gemini.

---

## 📌 Why I Built This

Modern software systems generate thousands of log lines every hour. Manually reading through them to find failures, understand root causes, and file bug reports is slow and error-prone.

This project automates that entire workflow using an LLM pipeline:
- Feed it a raw log file
- It sends chunks to Gemini for intelligent analysis
- It outputs a full bug triage report in both JSON and a visual HTML dashboard

Inspired by agentic infrastructure patterns where AI handles failure triage without waiting for humans — directly mirroring how production systems like NVIDIA Omniverse manage quality workflows.

---

## 🚀 Features

- **Automated failure triage** — finds every ERROR, WARNING, and CRITICAL line
- **Root cause analysis** — Gemini suggests why each failure likely occurred
- **Bug report generation** — one-line bug titles ready to file
- **Severity classification** — issues sorted into CRITICAL / ERROR / WARNING
- **Visual HTML dashboard** — color-coded report you can open in any browser
- **JSON output** — structured data for downstream processing or integration
- **Retry logic** — automatically retries if the API fails, never crashes mid-run
- **CLI interface** — flexible command-line arguments for any log file or output path

---

## 📁 Project Structure

```
log-analyzer/
├── log_parser.py           # reads log files and splits into chunks
├── llm_client.py           # sends chunks to Gemini, handles retries
├── report_generator.py     # builds JSON + HTML reports from results
├── main.py                 # CLI entry point — run this file
├── sample.log              # sample log file for testing
├── config.example.py       # API key template (copy to config.py)
├── requirements.txt        # Python dependencies
└── README.md
```

---

## ⚙️ Setup

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/llm-log-analyzer.git
cd llm-log-analyzer
```

### 2. Install dependencies
```bash
pip install google-genai
```

### 3. Get a free Gemini API key
- Go to [aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)
- Sign in with Google
- Click **"Create API key in new project"**
- Copy the key

### 4. Add your API key
```bash
cp config.example.py config.py
```
Open `config.py` and paste your key:
```python
GEMINI_API_KEY = "your-actual-key-here"
```

---

## 🖥️ Usage

### Basic run (uses sample.log by default)
```bash
python main.py
```

### Analyze a custom log file
```bash
python main.py --log path/to/your/logfile.log
```

### Custom output file name
```bash
python main.py --log sample.log --output my_report
```

### Custom chunk size (lines sent to Gemini per call)
```bash
python main.py --log sample.log --output report --chunk-size 10
```

### See all options
```bash
python main.py --help
```

---

## 📊 Sample Output

**Terminal:**
```
========================================
AI LOG ANALYZER
========================================
Log file   : sample.log
Output     : report
Chunk size : 5
========================================

Step 1: Reading log file...
         Found 20 lines → 4 chunks

Step 2: Analyzing with Gemini...
         Chunk 1 of 4...
         Chunk 2 of 4...
         Chunk 3 of 4...
         Chunk 4 of 4...

Step 3: Generating reports...
========================================
ANALYSIS COMPLETE
========================================
Total issues : 12
Critical     : 3
Errors       : 6
Warnings     : 3
JSON saved   : report.json
HTML saved   : report.html
========================================
```

**JSON report (`report.json`):**
```json
{
  "analyzed_at": "2026-05-03T22:30:00",
  "total_issues": 12,
  "critical": [
    {
      "severity": "CRITICAL",
      "timestamp": "2026-05-01 08:10:46",
      "description": "Service crashed due to out of memory",
      "root_cause": "Memory leak likely caused by unclosed database connections",
      "suggested_fix": "Add connection pooling and memory profiling",
      "bug_title": "Service crash: out of memory at 08:10:46"
    }
  ],
  "errors": [...],
  "warnings": [...]
}
```

**HTML dashboard** — opens in browser with color-coded severity badges, timestamps, root causes, and fix suggestions in a dark-themed table.

---

## 🏗️ How It Works

```
sample.log
    │
    ▼
log_parser.py
  reads file → splits into chunks of N lines
    │
    ▼
llm_client.py
  for each chunk:
    → sends to Gemini with structured prompt
    → parses JSON response
    → retries up to 3x if API fails
    │
    ▼
report_generator.py
  combines all chunk results
  → sorts by severity
  → writes report.json
  → writes report.html
```

The chunking approach solves a real LLM limitation: context windows. Instead of sending 10,000 log lines at once (which would exceed limits and lose detail), the pipeline processes manageable chunks and aggregates results.

---

## ⚠️ Known Limitations & Where It Breaks

These are documented honestly because understanding failure modes is part of building trustworthy systems:

- **Large log files** (10,000+ lines) will hit Gemini free-tier rate limits — add `time.sleep(2)` between chunks as a workaround
- **Root cause suggestions are probabilistic** — Gemini infers causes from patterns, not from actual code inspection
- **JSON parsing can fail** on rare Gemini responses — handled by retry logic, but a small % of chunks may return empty results
- **Single file only** — does not currently support streaming logs or watching a file in real time
- **No deduplication** — if the same error repeats 50 times, it appears 50 times in the report

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.x | Core language |
| Google Gemini API (`gemini-1.5-flash`) | LLM for log analysis |
| `google-genai` | Official Gemini Python SDK |
| `argparse` | CLI interface |
| `json` | Structured output |
| HTML + CSS | Visual dashboard |

---

## 🔮 Future Improvements

- [ ] Multi-agent architecture — separate parser, triage, and reporter agents
- [ ] Eval system — score Gemini's output against known ground truth
- [ ] Real-time log monitoring — watch a file and analyze new lines as they appear
- [ ] Slack/email integration — send critical alerts automatically
- [ ] Support for multiple log formats (JSON logs, Apache logs, etc.)
- [ ] Web UI — drag and drop a log file, see results in browser

---

## 🤝 Contributing

Pull requests are welcome. For major changes, open an issue first to discuss what you'd like to change.

---

## 📄 License

MIT License — free to use, modify, and distribute.

---

*Built as a learning project exploring agentic AI workflows and LLM-powered infrastructure tooling.*
=======
# llm-log-analyzer
AI-powered log analysis pipeline using Gemini to triage failures and generate bug reports
>>>>>>> 63de621d0b213dcd7f81bcb2c177be8f4abf953a

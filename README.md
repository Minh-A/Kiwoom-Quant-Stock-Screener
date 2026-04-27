# Kiwoom Stock Data Collector

Python project for collecting and screening KOSPI/KOSDAQ stocks with Kiwoom OpenAPI+.

The collector logs in through Kiwoom OpenAPI+, requests index and daily candle data, calculates a daily fluctuation estimation indicator, and writes matching stock codes to a local result file.

## Security Cleanup

Before publication, sensitive or local-only artifacts were removed from the GitHub version:

- Removed a hardcoded Slack bot token from `Conditional/Condition3_main.py`.
- Removed the same hardcoded Slack bot token from `Conditional/Condition4_Beta.py`.
- Replaced Slack notification logic with environment variables in `utils/notifier.py`.
- Removed generated `__pycache__` files that contained local Windows source paths.
- Ignored generated stock result files under `files/`.

See `docs/security-cleanup.md` for details.

## Requirements

This project requires a Windows environment because Kiwoom OpenAPI+ is exposed through an ActiveX control.

Required local setup:

- Windows
- Kiwoom OpenAPI+ installed
- Python 32-bit environment compatible with Kiwoom OpenAPI+
- PyQt5

Install Python dependencies:

```bash
pip install -r requirements.txt
```

## Optional Slack Notification

Slack notifications are disabled unless a token is supplied locally.

Create a local `.env` or set environment variables directly:

```bash
SLACK_BOT_TOKEN=
SLACK_CHANNEL=#stock
STOCK_COLLECT_OUTPUT_DIR=files
```

Do not commit real tokens or account credentials.

## Run

```bash
python main.py
```

The default condition file imported by `kiwoom/kiwoom.py` is `Conditional.Condition4_Beta`.

Generated stock-screening results are written to `files/` by default and ignored by Git.

## Project Structure

```text
.
├── Conditional/
│   ├── Condition3_main.py
│   └── Condition4_Beta.py
├── docs/
│   └── security-cleanup.md
├── files/
│   └── README.md
├── kiwoom/
│   ├── ErrorCode.py
│   └── kiwoom.py
├── utils/
│   ├── notifier.py
│   └── output.py
├── .env.example
├── main.py
├── README.md
└── requirements.txt
```

## Notes

This repository is for data collection and screening experiments only. It does not include trading-order logic, account credentials, or Kiwoom login information.

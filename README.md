# Kiwoom Quant Stock Screener

Python project for finding KOSPI/KOSDAQ stocks that pass a custom quant screening rule built on Kiwoom OpenAPI+ data.

This is not a generic stock-data collector. Kiwoom OpenAPI+ is used as the data source, but the core portfolio value is the author's own rule-based quant condition. The program requests market index data and stock daily candles, calculates custom volatility indicators, compares each stock against market-level movement, and writes only the stock codes that satisfy the screening conditions.

## Core Idea

The project screens stocks with a custom **Daily Fluctuation Estimation Indicator (DFEI)**:

```text
DFEI = (daily high - daily low) / (daily close - daily open)
```

The condition logic uses this indicator to detect stocks whose daily movement pattern satisfies the author's predefined quant rule instead of simply listing all available stocks.

The screening flow is:

1. Log in through Kiwoom OpenAPI+.
2. Request KOSPI/KOSDAQ index daily data.
3. Calculate market-level DFEI and moving fluctuation thresholds.
4. Request each stock's daily candle data.
5. Calculate each stock's DFEI over the configured lookback period.
6. Compare stock-level movement against the market-derived threshold.
7. Save only stocks that pass every condition.

Implemented condition sets:

- `Conditional/Condition3_main.py`: 40-day baseline condition that filters out stocks with excessive volatility relative to the market threshold.
- `Conditional/Condition4_Beta.py`: 600-day beta condition that searches for stocks with sustained movement above the custom threshold.

Generated outputs are therefore **custom quant-screened stock candidates**, not raw stock lists.

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

This repository is for custom quant screening experiments only. It does not include trading-order logic, account credentials, or Kiwoom login information.

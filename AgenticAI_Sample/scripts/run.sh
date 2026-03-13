#!/usr/bin/env bash
set -e
MODE="${1:-mock}"
DATA="${2:-data/tickets_sample.json}"
python run.py --mode "$MODE" --data "$DATA"

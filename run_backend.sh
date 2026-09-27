#!/usr/bin/env bash
source .venv/bin/activate
python -m uvicorn legalEaseAPI.main:app --host 127.0.0.1 --port 8000 --reload

#!/usr/bin/env bash
set -e
uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 &
BACK_PID=$!
sleep 1
streamlit run frontend/app.py
kill $BACK_PID

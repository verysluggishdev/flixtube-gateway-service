#!/bin/bash
source venv/bin/activate
uvicorn gateway.main:app --reload
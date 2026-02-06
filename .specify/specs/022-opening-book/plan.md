# Implementation Plan: Opening Book Lookup

**Branch**: `022-opening-book` | **Date**: 2026-02-06 | **Spec**: [spec.md](./spec.md)

## Summary

Opening book database and lookup engine for matching early game positions to known theory. Supports faction-specific openings.

## Technical Context

**Language/Version**: Python 3.11  
**Primary Dependencies**: Pydantic  
**Storage**: JSON files (embedded)  
**Testing**: pytest  
**Target Platform**: Primordia-AI  
**Project Type**: Backend library  

## Project Structure

```text
Primordia-AI/src/
├── openings/
│   ├── book.py            # [NEW] Opening book manager
│   └── lookup.py          # [NEW] Lookup engine
└── data/
    └── openings.json      # [NEW] Opening database
```

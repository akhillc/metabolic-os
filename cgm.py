#!/usr/bin/env python3
"""
cgm.py — Dexcom G7 data fetcher for Metabolic OS
Pulls CGM data via the Dexcom Share API (pydexcom)

Usage:
  python cgm.py current                        current glucose + trend
  python cgm.py summary --hours 24             24h summary (avg/min/max/TIR)
  python cgm.py export --hours 24 --format json  raw data export

Setup:
  1. Enable Dexcom Share in the Dexcom G7 app (Settings → Share)
  2. Copy .env.example to .env and fill in your credentials
  3. pip install pydexcom python-dotenv
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone

# ── Dependency check ─────────────────────────────────────────────────────────

def check_deps():
    missing = []
    try:
        import pydexcom  # noqa: F401
    except ImportError:
        missing.append('pydexcom')
    try:
        import dotenv  # noqa: F401
    except ImportError:
        missing.append('python-dotenv')
    if missing:
        print(f"Missing packages: {', '.join(missing)}")
        print(f"Install with: pip install {' '.join(missing)}")
        sys.exit(1)

check_deps()

from pydexcom import Dexcom, Region  # noqa: E402
from dotenv import load_dotenv  # noqa: E402

# ── Config ────────────────────────────────────────────────────────────────────

load_dotenv()

DEXCOM_USERNAME = os.getenv('DEXCOM_USERNAME')
DEXCOM_PASSWORD = os.getenv('DEXCOM_PASSWORD')
# Region: 'us' (default), 'ous' (outside US), or 'jp' (Japan)
_region_str = os.getenv('DEXCOM_REGION', 'us').lower()
DEXCOM_REGION = Region(_region_str) if _region_str in ('us', 'ous', 'jp') else Region.US

# Glucose ranges (mg/dL) — standard metabolic targets
RANGE_LOW     = 70
RANGE_HIGH    = 140   # tight range for metabolic control
URGENT_LOW    = 55
URGENT_HIGH   = 180

TREND_ARROWS = {
    'DoubleUp':       '⬆⬆ Rising fast (+3mg/min)',
    'SingleUp':       '⬆  Rising (+2mg/min)',
    'FortyFiveUp':    '↗  Rising slowly (+1mg/min)',
    'Flat':           '→  Stable',
    'FortyFiveDown':  '↘  Falling slowly (-1mg/min)',
    'SingleDown':     '⬇  Falling (-2mg/min)',
    'DoubleDown':     '⬇⬇ Falling fast (-3mg/min)',
    'NotComputable':  '?  Trend unavailable',
    'RateOutOfRange': '?  Rate out of range',
    None:             '—  No trend data',
}

# ── Auth ──────────────────────────────────────────────────────────────────────

def get_dexcom():
    if not DEXCOM_USERNAME or not DEXCOM_PASSWORD:
        print("ERROR: DEXCOM_USERNAME and DEXCOM_PASSWORD must be set in .env")
        print("Copy .env.example to .env and fill in your credentials.")
        sys.exit(1)
    try:
        return Dexcom(username=DEXCOM_USERNAME, password=DEXCOM_PASSWORD, region=DEXCOM_REGION)
    except Exception as e:
        print(f"ERROR: {type(e).__name__}: {e}")
        sys.exit(1)

# ── Glucose classification ────────────────────────────────────────────────────

def classify(value):
    if value < URGENT_LOW:   return 'URGENT LOW', '\033[91m'
    if value < RANGE_LOW:    return 'LOW', '\033[93m'
    if value <= RANGE_HIGH:  return 'IN RANGE', '\033[92m'
    if value <= URGENT_HIGH: return 'HIGH', '\033[93m'
    return 'URGENT HIGH', '\033[91m'

RESET = '\033[0m'

# ── Commands ──────────────────────────────────────────────────────────────────

def cmd_current(args):
    dex = get_dexcom()
    reading = dex.get_current_glucose_reading()

    if reading is None:
        print("No current reading available. Check your sensor connection.")
        return

    value      = reading.value
    trend_desc = TREND_ARROWS.get(reading.trend_description, '—')
    status, color = classify(value)
    time_str   = reading.datetime.strftime('%I:%M %p') if reading.datetime else 'unknown'

    print(f"\n{'─'*44}")
    print(f"  {color}● {value} mg/dL{RESET}  [{status}]")
    print(f"  {trend_desc}")
    print(f"  Recorded at {time_str}")
    print(f"{'─'*44}")
    print()
    print("── Claude paste format ─────────────────────────")
    print(f"CGM (Dexcom G7) @ {time_str}: {value} mg/dL — {trend_desc.strip()} [{status}]")
    print()

def cmd_summary(args):
    hours = args.hours
    dex   = get_dexcom()
    readings = dex.get_glucose_readings(hours=hours)

    if not readings:
        print(f"No readings found in the last {hours} hours.")
        return

    values = [r.value for r in readings]
    avg    = sum(values) / len(values)
    lo     = min(values)
    hi     = max(values)

    in_range   = sum(1 for v in values if RANGE_LOW <= v <= RANGE_HIGH)
    below_range = sum(1 for v in values if v < RANGE_LOW)
    above_range = sum(1 for v in values if v > RANGE_HIGH)
    tir  = round(in_range   / len(values) * 100, 1)
    tbr  = round(below_range / len(values) * 100, 1)
    tar  = round(above_range / len(values) * 100, 1)

    # SD (glycemic variability)
    mean = avg
    sd   = (sum((v - mean) ** 2 for v in values) / len(values)) ** 0.5
    cv   = round(sd / mean * 100, 1)

    # Spike detection: readings > 30 mg/dL above previous in 15 min
    spikes = 0
    for i in range(1, len(readings)):
        delta = readings[i-1].value - readings[i].value  # readings are newest-first
        if delta > 30:
            spikes += 1

    print(f"\n{'─'*44}")
    print(f"  CGM Summary — last {hours}h ({len(readings)} readings)")
    print(f"{'─'*44}")
    print(f"  Average:   {avg:.0f} mg/dL")
    print(f"  Range:     {lo}–{hi} mg/dL")
    print(f"  Std Dev:   {sd:.0f} mg/dL  (CV {cv}%)")
    print()
    print(f"  Time in range ({RANGE_LOW}–{RANGE_HIGH}):  {tir}%")
    print(f"  Time above range:              {tar}%")
    print(f"  Time below range:              {tbr}%")
    if spikes:
        print(f"  Spikes (>30 mg/dL rapid rise): {spikes}")
    print(f"{'─'*44}")
    print()
    print("── Claude paste format ─────────────────────────")
    print(f"CGM Summary ({hours}h) — {len(readings)} readings")
    print(f"Avg {avg:.0f} mg/dL | Range {lo}–{hi} | SD {sd:.0f} (CV {cv}%)")
    print(f"Time in range ({RANGE_LOW}–{RANGE_HIGH} mg/dL): {tir}% | Above: {tar}% | Below: {tbr}%")
    if spikes:
        print(f"Glucose spikes detected: {spikes}")
    print()

def cmd_export(args):
    hours  = args.hours
    fmt    = args.format
    dex    = get_dexcom()
    readings = dex.get_glucose_readings(hours=hours)

    if not readings:
        print(f"No readings found in the last {hours} hours.")
        return

    if fmt == 'json':
        data = {
            'exported_at': datetime.now(timezone.utc).isoformat(),
            'hours': hours,
            'count': len(readings),
            'readings': [
                {
                    'time': r.datetime.isoformat() if r.datetime else None,
                    'value': r.value,
                    'trend': r.trend_description,
                }
                for r in readings
            ]
        }
        print(json.dumps(data, indent=2))
    else:
        # CSV
        print('time,value_mgdl,trend')
        for r in readings:
            t = r.datetime.isoformat() if r.datetime else ''
            print(f"{t},{r.value},{r.trend_description or ''}")

# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description='Dexcom G7 CGM data fetcher for Metabolic OS',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    sub = parser.add_subparsers(dest='command', required=True)

    # current
    sub.add_parser('current', help='Current glucose reading + trend arrow')

    # summary
    p_sum = sub.add_parser('summary', help='Time-period summary (avg, min, max, TIR)')
    p_sum.add_argument('--hours', type=int, default=24, metavar='N',
                       help='Hours to look back (default: 24)')

    # export
    p_exp = sub.add_parser('export', help='Raw data export (JSON or CSV)')
    p_exp.add_argument('--hours', type=int, default=24, metavar='N',
                       help='Hours to look back (default: 24)')
    p_exp.add_argument('--format', choices=['json', 'csv'], default='json',
                       help='Output format (default: json)')

    args = parser.parse_args()

    if args.command == 'current':
        cmd_current(args)
    elif args.command == 'summary':
        cmd_summary(args)
    elif args.command == 'export':
        cmd_export(args)

if __name__ == '__main__':
    main()

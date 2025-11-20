#!/usr/bin/env python3
"""
Smoke test for telegram module integration
Tests that all modules have proper /start endpoints that accept chat_id
"""

import requests
import sys
import json

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8080"

# Modules that should have telegram-compatible /start endpoints
TELEGRAM_MODULES = [
    "/arena/v4/start",
    "/master_path/v3/start",
    "/objections/v3/start",
    "/sleeping_dragon/v4/start",
    "/exam/v2/start",
    "/voice_arena/v1/start",
    "/dialog_memory/v1/start",
]

def test_probe(url):
    """Test that module responds to probe requests"""
    try:
        r = requests.post(url, json={"probe": True, "chat_id": 0}, timeout=5)
        if r.ok:
            data = r.json()
            if data.get("ok") and data.get("available"):
                return True, "Probe OK"
        return False, f"Probe failed: {r.status_code}"
    except Exception as e:
        return False, f"Probe error: {e}"

def test_start(url):
    """Test that module accepts chat_id and returns reply"""
    try:
        r = requests.post(url, json={"chat_id": 99999}, timeout=5)
        if r.ok:
            data = r.json()
            if "reply" in data or "sid" in data or "session_id" in data:
                return True, "Start OK"
        return False, f"Start failed: {r.status_code}"
    except Exception as e:
        return False, f"Start error: {e}"

def main():
    results = {}
    print(f"Testing telegram module integration at {BASE}\n")
    
    for endpoint in TELEGRAM_MODULES:
        url = BASE + endpoint
        module_name = endpoint.split("/start")[0]
        
        print(f"Testing {module_name}...")
        
        # Test probe
        probe_ok, probe_msg = test_probe(url)
        
        # Test start with chat_id
        start_ok, start_msg = test_start(url)
        
        results[module_name] = {
            "probe": {"ok": probe_ok, "message": probe_msg},
            "start": {"ok": start_ok, "message": start_msg}
        }
        
        status = "✓" if (probe_ok and start_ok) else "✗"
        print(f"  {status} Probe: {probe_msg}, Start: {start_msg}")
    
    print("\n" + "="*50)
    all_ok = all(r["probe"]["ok"] and r["start"]["ok"] for r in results.values())
    if all_ok:
        print("✓ All modules passed telegram integration tests!")
        return 0
    else:
        print("✗ Some modules failed telegram integration tests")
        print(json.dumps(results, indent=2))
        return 1

if __name__ == "__main__":
    sys.exit(main())

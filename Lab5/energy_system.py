"""Energy consumption and tariff calculator.

Records meter readings, computes a three-tier electricity bill, flags
meters with unusually high usage and stores readings in meters.json.
"""
import json
from datetime import datetime

# Meter totals, keyed by meter id
meters = {}
BASE_RATES = (3.5, 5.0, 7.5)
SPIKE_LIMIT = 500
DATA_FILE = "meters.json"

def record_reading(meter_id, units, history=None):
    """Add a reading to a meter's total and log it in history.

    Raises ValueError for negative readings, which a meter cannot produce.
    """
    if history is None:
        history = []
    if units < 0:
        raise ValueError(f"Reading for {meter_id} cannot be negative: {units}")
    history.append((meter_id, units, str(datetime.now())))
    meters[meter_id] = meters.get(meter_id, 0) + units
    return history

def compute_bill(meter_id, tier_rates):
    """Return the bill for a meter using three tier rates."""
    units = meters.get(meter_id, 0)
    if units <= 100:
        return units * tier_rates[0]
    if units <= 300:
        return 100 * tier_rates[0] + (units - 100) * tier_rates[1]
    return 100 * tier_rates[0] + 200 * tier_rates[1] + (units - 300) * tier_rates[2]

def raise_rates(rates, percent):
    """Return a new list of rates increased by the given percentage."""
    factor = 1 + percent / 100
    return [rate * factor for rate in rates]

def flag_spikes():
    """Return the ids of meters whose total exceeds SPIKE_LIMIT."""
    return [meter_id for meter_id, units in meters.items() if units > SPIKE_LIMIT]

def load_meter_data(file=DATA_FILE):
    """Replace the in-memory meter totals with the contents of file."""
    try:
        with open(file, encoding="utf-8") as handle:
            data = json.load(handle)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}
    meters.clear()
    meters.update(data)

def save_meter_data(file=DATA_FILE):
    """Write the meter totals to file as JSON."""
    with open(file, "w", encoding="utf-8") as handle:
        json.dump(meters, handle)

def main():
    """Run a short demo of the tariff calculator."""
    history = []
    record_reading("M-01", 120, history)
    record_reading("M-02", 640, history)
    try:
        record_reading("M-03", -50, history)
    except ValueError as err:
        print("Rejected:", err)
    print("Readings stored so far:", len(history))
    rates = raise_rates(BASE_RATES, 10)
    print(f"Bill M-01: {compute_bill('M-01', rates):.2f}")
    print(f"Bill M-03: {compute_bill('M-03', rates):.2f}")
    print("Spikes:", flag_spikes())
    adjustment = input("Extra units for M-01 (Enter for 0): ") or "0"
    try:
        record_reading("M-01", float(adjustment), history)
    except ValueError:
        print("Invalid reading, using 0")
    save_meter_data()
    load_meter_data()
    print(f"Bill M-01 after reload: {compute_bill('M-01', rates):.2f}")

if __name__ == "__main__":
    main()

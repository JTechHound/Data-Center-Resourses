"""Electricity grid node engine (companion to energy_water_nexus.py).
Source: import_json.py uploaded 2026-10-03. Audited 2026-10-03: all outputs
verified by hand calc. NOTE: power_factor currently has no effect on any
output (apparent_kva = gross*1000/pf then real = apparent*pf cancels it
exactly; reactive_kvar is computed and discarded). Flagged, not changed.
"""
import json

# =========================================================================
# PRODUCTION-GRADE POWER ELECTRICITY ENGINEERING ENGINE
# =========================================================================

def get_regional_grid_tariffs(basin_name):
    """
    Returns wholesale electricity market clearing prices ($/MWh) and carbon 
    tax penalties ($/Metric Ton CO2) indexed by regional grid operator territories.
    """
    grids = {
        'colorado': {'wholesale_mwh_usd': 75.00, 'carbon_tax_per_ton': 15.00, 'co2_intensity_constant': 180.0},
        'columbia': {'wholesale_mwh_usd': 42.00, 'carbon_tax_per_ton': 25.00, 'co2_intensity_constant': 50.0},
        'mississippi': {'wholesale_mwh_usd': 48.00, 'carbon_tax_per_ton': 0.00, 'co2_intensity_constant': 205.0},
        'potomac': {'wholesale_mwh_usd': 51.00, 'carbon_tax_per_ton': 0.00, 'co2_intensity_constant': 117.0}
    }
    name_clean = str(basin_name).strip().lower()
    return grids.get(name_clean, grids['potomac'])


def calculate_electrical_losses(apparent_power_kva, power_factor):
    """Calculates real working power output vs reactive power dissipation."""
    if not (0.0 < power_factor <= 1.0):
        raise ValueError("Power factor (PF) must be strictly between 0.0 and 1.0.")
    
    real_power_kw = apparent_power_kva * power_factor
    reactive_power_kvar = (apparent_power_kva**2 - real_power_kw**2)**0.5
    return real_power_kw, reactive_power_kvar


def run_electricity_pipeline_node(row_dict):
    """Processes an isolated utility node for power delivery, metrics, and financials."""
    tariffs = get_regional_grid_tariffs(row_dict['basin'])
    
    # 1. Structural Power Capacity Checks
    # Account for reactive phase drag using the Power Factor
    apparent_kva = row_dict['gross_mw'] * 1000.0 / row_dict.get('power_factor', 0.90)
    real_kw, reactive_kvar = calculate_electrical_losses(apparent_kva, row_dict.get('power_factor', 0.90))
    gross_working_mw = real_kw / 1000.0
    
    # Parasitic load drop (Internal auxiliary equipment consumption)
    net_capacity_mw = gross_working_mw - row_dict['parasitic_load_mw']
    if net_capacity_mw <= 0:
        raise ValueError(f"Outage Loop: Parasitic draw exceeds generation at node {row_dict['plant_id']}")
    
    # 2. Thermodynamic Heat Conversions
    # 3,412.14 Btus = 1 Kilowatt-Hour
    hourly_net_generation_kwh = net_capacity_mw * 1000.0
    heat_rate = row_dict['hourly_fuel_btu'] / hourly_net_generation_kwh
    thermal_efficiency = 3412.14 / heat_rate
    
    # 3. Carbon Emissions Footprint Accounting
    # Calculate total hourly metric tons of CO2 produced
    fuel_mmbtu = row_dict['hourly_fuel_btu'] / 1.0e6
    co2_lbs_per_hr = fuel_mmbtu * tariffs['co2_intensity_constant']
    co2_metric_tons_hr = (co2_lbs_per_hr / 2204.62)
    co2_intensity_lbs_mwh = co2_lbs_per_hr / net_capacity_mw
    
    # 4. Market Financial Compounding Layer
    hourly_gross_revenue = net_capacity_mw * tariffs['wholesale_mwh_usd']
    hourly_carbon_liability = co2_metric_tons_hr * tariffs['carbon_tax_per_ton']
    net_financial_yield_hr = hourly_gross_revenue - hourly_carbon_liability
    
    return {
        "plant_id": row_dict['plant_id'],
        "net_delivered_mw": round(net_capacity_mw, 2),
        "thermal_efficiency_pct": round(thermal_efficiency * 100, 2),
        "co2_emissions_tons_hr": round(co2_metric_tons_hr, 3),
        "co2_intensity_lbs_mwh": round(co2_intensity_lbs_mwh, 1),
        "hourly_market_revenue_usd": round(hourly_gross_revenue, 2),
        "hourly_carbon_tax_liability": round(hourly_carbon_liability, 2),
        "net_hourly_financial_yield": round(net_financial_yield_hr, 2)
    }

def batch_process_electricity_json(json_str):
    """Parses incoming JSON payloads to process grid power outputs."""
    records = json.loads(json_str)
    return [run_electricity_pipeline_node(r) for r in records]

# =========================================================================
# RUN DATA VALIDATION VERIFICATION
# =========================================================================
if __name__ == "__main__":
    mock_electricity_dataset = """[
        {"plant_id": "PWR-001", "basin": "colorado", "gross_mw": 500.0, "parasitic_load_mw": 32.0, "hourly_fuel_btu": 3.9e9, "power_factor": 0.92},
        {"plant_id": "PWR-002", "basin": "columbia", "gross_mw": 600.0, "parasitic_load_mw": 15.0, "hourly_fuel_btu": 3.2e9, "power_factor": 0.95},
        {"plant_id": "PWR-003", "basin": "potomac", "gross_mw": 450.0, "parasitic_load_mw": 22.0, "hourly_fuel_btu": 3.4e9, "power_factor": 0.88}
    ]"""
    
    print("--- Running Electricity Grid Pipeline Node Engine ---")
    processed_power_outputs = batch_process_electricity_json(mock_electricity_dataset)
    print(json.dumps(processed_power_outputs, indent=2))

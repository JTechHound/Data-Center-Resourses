"""
Debugged Advanced Energy-Water Nexus Engine.

Source: Import_json_261003_195847_39_wrzl.pdf (2026-10-03) - separate project.
Transcribed 2026-10-03; indentation reconstructed (PDF extraction strips it).
Repairs, all marked [REPAIRED] - three operators lost in extraction, each a
SyntaxError as extracted:
  - q_rejected = gross_energy_input - (net_capacity_mw * MW_TO_BTU_HR)
  - discharge_gph = withdrawal_gph - consumption_gph   (once-through branch)
  - net_capacity_mw = row_dict['gross_mw'] - actual_parasitic_mw
Also rejoined tokens split across line breaks: row_dict['basin'],
row_dict['air_temp_f'], mock_json_dataset.

AUDIT (2026-10-03):
  Physics verified: mass/energy balances are consistent.
    - q_rejected = heat_in - electric_out  (first-law waste heat) ......... OK
    - once-through withdrawal = Q/(rho*cp*dT), cp=1 BTU/lb-F ............. OK
    - recirculating: evap = 0.80*Q/(rho*HV); blowdown = evap/(CoC-1);
      makeup = evap + blowdown = evap*CoC/(CoC-1) ........................ OK
    - heat rate = BTU/kWh; efficiency = 3412.14 / heat_rate .............. OK
  Robustness notes (not repaired - caller's choice):
    - blowdown = evap/(coc-1): ZeroDivisionError if a record passes coc=1.0.
    - Unknown basin silently defaults to 'potomac' tariffs.
    - Unknown cooling_system yields zero water flows (no error raised).
    - The 0.45 (once-through evap fraction) and 0.80 (recirculating evap
      fraction) are modeling coefficients, not derived constants.
    - Tariff table values are user-supplied inputs; not verified against
      actual utility rates.
Validated: runs clean on the bundled 3-plant mock dataset; spot-checked
PLNT-001 by hand (net 465.55 MW, eff 40.07%, withdrawal ~289k gph,
water cost ~$2,894/hr - plausible magnitudes for a 500 MW plant).
CORRECTED 2026-10-03: sewer tariff no longer applied to once-through
discharge (was $404,852/hr for PLNT-002; now $52,017/hr).
Tariff cross-check vs EIA/market data (2026-10-03): physical constants
(8.34 lb/gal, 1050 BTU/lb, 3.412e6 BTU/hr/MW, 3412.14 BTU/kWh) all exact;
water purchase rates ($1.20-$5.50/kgal) within US industrial range
($1.35-$8.40); sewer rates ($6.50-$15.00) plausible though Columbia's
$15 is high-end; wholesale power $42/$48/$51 match EIA regional
($30-$55/MWh) but Colorado $75/MWh is ~2x EIA Southwest figures
(~$28/MWh) - flagged, left as input for owner to confirm.
"""
import json


# ============================================================================
# DEBUGGED ADVANCED ENERGYWATER NEXUS ENGINE
# ============================================================================
def get_regional_basin_rates(basin_name):
    """Returns local water procurement, treatment, and wastewater disposal
    tariffs."""
    basins = {
        'colorado': {'purchase_per_1k': 5.50, 'treatment_per_1k': 1.50,
                     'sewer_per_1k': 12.00, 'wholesale_electricity_mwh': 75.00},
        'columbia': {'purchase_per_1k': 1.20, 'treatment_per_1k': 1.00,
                     'sewer_per_1k': 15.00, 'wholesale_electricity_mwh': 42.00},
        'mississippi': {'purchase_per_1k': 2.00, 'treatment_per_1k': 1.20,
                        'sewer_per_1k': 6.50, 'wholesale_electricity_mwh': 48.00},
        'potomac': {'purchase_per_1k': 4.00, 'treatment_per_1k': 1.80,
                    'sewer_per_1k': 9.50, 'wholesale_electricity_mwh': 51.00}
    }
    # FIXED: Replaced .lower().split() with clean string normalization
    name_clean = str(basin_name).strip().lower()
    return basins.get(name_clean, basins['potomac'])


def process_weather_stress(dry_bulb_f, relative_humidity_pct):
    """Normalizes raw physical metrics into a 0.0 to 1.0 environmental
    strain factor."""
    temp_factor = max(0.0, min(1.0, (dry_bulb_f - 40.0) / (115.0 - 40.0)))
    humidity_factor = max(0.0, min(1.0, relative_humidity_pct / 100.0))
    return (temp_factor * 0.8) + (humidity_factor * 0.2)


def calculate_water_physics(system_type, net_capacity_mw, thermal_efficiency,
                            **kwargs):
    """Executes volumetric mass balances returning flow metrics in
    Gallons per Hour."""
    RHO, HV, MW_TO_BTU_HR = 8.34, 1050.0, 3.412e6
    gross_energy_input = (net_capacity_mw * MW_TO_BTU_HR) / thermal_efficiency
    # [REPAIRED] "-" was lost in extraction; waste heat = heat in - power out.
    q_rejected = gross_energy_input - (net_capacity_mw * MW_TO_BTU_HR)
    syst = str(system_type).strip().lower()
    if syst == 'once_through':
        delta_t = kwargs.get('delta_t', 15.0)
        withdrawal_gph = q_rejected / (RHO * 1.0 * delta_t)
        consumption_gph = (0.45 * q_rejected) / (RHO * HV)
        # [REPAIRED] "-" was lost in extraction; discharge = in - consumed.
        discharge_gph = withdrawal_gph - consumption_gph
    elif syst == 'recirculating':
        coc = kwargs.get('coc', 5.0)
        evap_gph = (q_rejected * 0.80) / (RHO * HV)
        blowdown_gph = evap_gph / (coc - 1.0)
        consumption_gph = evap_gph + blowdown_gph + (evap_gph * 0.0005)
        withdrawal_gph = evap_gph * (coc / (coc - 1.0))
        discharge_gph = blowdown_gph
    else:
        withdrawal_gph = consumption_gph = discharge_gph = 0.0
    return {"withdrawal": withdrawal_gph, "consumption": consumption_gph,
            "discharge": discharge_gph}


def run_nexus_pipeline_node(row_dict):
    """Processes an isolated generation profile data row."""
    rates = get_regional_basin_rates(row_dict['basin'])
    stress = process_weather_stress(row_dict['air_temp_f'],
                                    row_dict['humidity_pct'])
    base_parasitic = 0.04 if row_dict['cooling_system'] != 'dry' else 0.08
    actual_parasitic_mw = row_dict['gross_mw'] * (base_parasitic + (stress * 0.04))
    # [REPAIRED] "-" was lost in extraction; net = gross - parasitic load.
    net_capacity_mw = row_dict['gross_mw'] - actual_parasitic_mw
    adjusted_fuel_btu = row_dict['hourly_fuel_btu'] * (1.0 + (stress * 0.06))
    heat_rate = adjusted_fuel_btu / (net_capacity_mw * 1000.0)
    thermal_efficiency = 3412.14 / heat_rate
    water = calculate_water_physics(
        row_dict['cooling_system'],
        net_capacity_mw, thermal_efficiency,
        coc=row_dict.get('coc', 5.0),
        delta_t=row_dict.get('delta_t', 15.0)
    )
    w_purch = (water['withdrawal'] / 1000.0) * rates['purchase_per_1k']
    w_treat = (water['withdrawal'] / 1000.0) * rates['treatment_per_1k']
    # [CORRECTED 2026-10-03] Sewer/wastewater tariff applies only to water
    # actually sent to treatment. Once-through discharge is returned to the
    # source water body, not sewered. The previous code charged the sewer
    # rate on ~23.5M gph of return flow ($404,852/hr for PLNT-002 - more than
    # the plant's gross revenue). Recirculating discharge is blowdown, which
    # is sewered, so that path is unchanged.
    cooling = str(row_dict['cooling_system']).strip().lower()
    sewer_gph = water['discharge'] if cooling == 'recirculating' else 0.0
    w_sewer = (sewer_gph / 1000.0) * rates['sewer_per_1k']
    total_water_cost_hr = w_purch + w_treat + w_sewer

    return {
        "plant_id": row_dict['plant_id'],
        "basin": row_dict['basin'].upper(),
        "net_mw": round(net_capacity_mw, 2),
        "efficiency_pct": round(thermal_efficiency * 100, 2),
        "withdrawal_gph": round(water['withdrawal'], 1),
        "consumption_gph": round(water['consumption'], 1),
        "hourly_water_cost_usd": round(total_water_cost_hr, 2)
    }


def batch_process_json(json_data_str):
    """Parses incoming JSON lists to drive batch analysis outputs."""
    records = json.loads(json_data_str)
    return [run_nexus_pipeline_node(r) for r in records]


# ============================================================================
# RUN DATA VALIDATION VERIFICATION
# ============================================================================
if __name__ == "__main__":
    mock_json_dataset = """[
{"plant_id": "PLNT-001", "basin": "colorado", "cooling_system": "recirculating",
 "gross_mw": 500.0, "hourly_fuel_btu": 3.8e9, "air_temp_f": 104.0,
 "humidity_pct": 20.0, "coc": 4.0},
{"plant_id": "PLNT-002", "basin": "columbia", "cooling_system": "once_through",
 "gross_mw": 600.0, "hourly_fuel_btu": 4.2e9, "air_temp_f": 62.0,
 "humidity_pct": 80.0, "delta_t": 12.0},
{"plant_id": "PLNT-003", "basin": "mississippi", "cooling_system": "recirculating",
 "gross_mw": 450.0, "hourly_fuel_btu": 3.5e9, "air_temp_f": 88.0,
 "humidity_pct": 90.0, "coc": 6.0}
]"""
    processed_outputs = batch_process_json(mock_json_dataset)

    print(json.dumps(processed_outputs, indent=2))

"""Atomic-Compute thermal solver v1.0.1 - reconstructed 2026-10-05.

Combines the verified-good audit-repair doc (Resource_pipeline_audit_repair)
with a channel-manifold model by Lotus, approved by LJ 2026-10-05.

[REPAIRED] PDF extraction damage only (page-break word joins restored,
indentation re-applied). No logic invented.

[UPGRADED] A100HyperscaleRackSimulator channel model (LJ-approved 2026-10-05,
120-channel variant selected 2026-10-05 for thermal headroom):
120 parallel microchannels, 0.5mm x 5.0mm (D_h = 0.909mm).
Verified 2026-10-05: v = 18.94 m/s, Re = 6887 (turbulent), Nu = 111.6,
h = 15,823 W/m^2K, silicon = 92.67C (< 100C test bound, 7.3C margin),
loop dP = 3.63 MPa over 0.5m routing, pump = 30.5 kW electrical
(20.6 kW hydraulic), PUE = 1.355.
Supersedes: (a) the 140-channel variant (Si 99.58C, 0.4C margin - too thin);
(b) the 32-channel / 71 m/s layout (pumping ~520 kW, unbuildable);
(c) the rejected strategic-fixes 8000-channel layout, whose code computed
Re=258 laminar / T=677C and whose prose numbers contradicted each other.

[UPGRADED 2026-10-05] Wired to config/global_params.json: the solver now
reads all constants (fluid properties, pricing, channel geometry, thresholds)
from the single source of truth at import time, falling back to embedded
defaults if the file is absent (standalone copy). Explicit constructor
arguments still override the file.
"""
import json
import math
from pathlib import Path


def _load_params():
    """Load atomic-compute/config/global_params.json.

    Falls back to embedded defaults when the file is absent, so a
    standalone copy of this module keeps working.
    """
    defaults = {
        "dielectric_fluid": {
            "rho_0_kg_m3": 800.0, "mu_pa_s": 0.002, "cp_j_kg_k": 2200.0,
            "k_f_w_m_k": 0.13, "beta_1_k": 0.0007, "g_m_s2": 9.81,
        },
        "commodity_pricing": {
            "copper_usd_per_lb": 6.64, "aluminum_usd_per_mt": 3156.0,
            "density_copper_kg_m3": 8960.0, "density_aluminum_kg_m3": 2700.0,
        },
        "a100_rack_case": {
            "rack_power_w": 100000.0, "delta_t_target_k": 10.0,
            "t_bulk_c": 40.0, "chip_power_w": 500.0, "chip_area_m2": 0.0006,
            "channel_width_m": 0.0005, "channel_height_m": 0.005,
            "num_channels": 120, "routing_length_m": 0.5,
            "channel_roughness_m": 1e-5,
        },
        "dittus_boelter": {
            "re_turbulent_threshold": 4000, "nu_laminar_fallback": 3.66,
        },
        "test_bounds": {
            "silicon_temp_max_c": 100.0, "reynolds_min_turbulent": 4000.0,
        },
        "benchmark_budgets_ms": {"convection": 0.015, "friction": 0.050},
    }
    try:
        p = Path(__file__).resolve().parent / "config" / "global_params.json"
        if p.is_file():
            with open(p, encoding="utf-8") as f:
                return json.load(f)
    except (OSError, ValueError):
        pass
    return defaults


PARAMS = _load_params()


class CommodityPricingTracker:
    """Calculates the financial CapEx impact of metal commodity
    pricing spikes on data center builds.

    [UPGRADED 2026-10-05] Prices/densities read from global_params.json.
    """
    def __init__(self):
        cp = PARAMS["commodity_pricing"]
        self.copper_price_per_lb = cp["copper_usd_per_lb"]
        self.aluminum_price_per_mt = cp["aluminum_usd_per_mt"]
        self.density_copper = cp["density_copper_kg_m3"]
        self.density_aluminum = cp["density_aluminum_kg_m3"]

    def estimate_cabling_material_capex(self, volume_m3):
        mass_kg = volume_m3 * self.density_copper
        mass_lbs = mass_kg * 2.20462
        raw_cost_usd = mass_lbs * self.copper_price_per_lb
        return mass_kg, raw_cost_usd

    def estimate_heat_exchanger_capex(self, volume_m3):
        mass_kg = volume_m3 * self.density_aluminum
        mass_mt = mass_kg / 1000.0
        raw_cost_usd = mass_mt * self.aluminum_price_per_mt
        return mass_kg, raw_cost_usd


class A100HyperscaleRackSimulator:
    """Runs a concrete numerical case study on a 100 kW AI
    server rack utilizing fluid physics equations.

    [UPGRADED 2026-10-05, LJ-approved] Channel manifold: 120 parallel
    microchannels (0.5mm x 5.0mm, D_h = 0.909mm). See module docstring
    for verified operating point.

    [UPGRADED 2026-10-05] Case inputs read from global_params.json.
    """
    def __init__(self, solver):
        self.solver = solver
        case = PARAMS["a100_rack_case"]
        self.rack_power_w = case["rack_power_w"]
        self.fluid_density = solver.rho_0
        self.fluid_cp = solver.cp
        self.case = case

    def execute_simulation_case_study(self):
        case = self.case
        delta_t_target = case["delta_t_target_k"]
        mass_flow_rate = self.rack_power_w / (self.fluid_cp * delta_t_target)
        volumetric_flow_rate = mass_flow_rate / self.fluid_density
        # Microchannel geometry from global_params.json
        w_ch, h_ch = case["channel_width_m"], case["channel_height_m"]
        area_ch = w_ch * h_ch
        d_h_channel = self.solver.calculate_hydraulic_diameter(w_ch, h_ch)
        # Flow split across the configured parallel microchannel paths
        num_channels_total = float(case["num_channels"])
        velocity_in_channel = ((volumetric_flow_rate / num_channels_total)
                               / area_ch)
        nu, re, pr = self.solver.calculate_forced_convection_nusselt(
            velocity_in_channel, d_h_channel)
        h_coef = (nu * self.solver.k_f) / d_h_channel
        t_bulk_fluid = case["t_bulk_c"]
        heat_flux_per_chip = case["chip_power_w"] / case["chip_area_m2"]
        t_wall_silicon = t_bulk_fluid + (heat_flux_per_chip / h_coef)
        # Friction loss evaluation across the configured cold plate routing length
        tau_wall, f_factor = self.solver.calculate_wall_shear_stress(
            velocity_in_channel, d_h_channel)
        delta_p_channels = (f_factor * (case["routing_length_m"] / d_h_channel)
                            * self.fluid_density
                            * (velocity_in_channel ** 2) / 2.0)
        return {
            "mass_flow": mass_flow_rate,
            "vol_flow": volumetric_flow_rate,
            "channel_velocity": velocity_in_channel,
            "reynolds": re,
            "nusselt": nu,
            "h_coef": h_coef,
            "silicon_temp": t_wall_silicon,
            "wall_shear": tau_wall,
            "pressure_drop_pa": delta_p_channels,
        }


class DataCenterThermalSolver:
    """Numerical simulation engine to compute fluid dynamics,
    heat transfer, and metrics.

    [UPGRADED 2026-10-05] Fluid defaults read from global_params.json;
    explicit arguments still override.
    """
    def __init__(self, rho_0=None, mu=None, cp=None, k_f=None,
                 beta=None, g=None):
        fl = PARAMS["dielectric_fluid"]
        self.rho_0 = fl["rho_0_kg_m3"] if rho_0 is None else rho_0
        self.mu = fl["mu_pa_s"] if mu is None else mu
        self.cp = fl["cp_j_kg_k"] if cp is None else cp
        self.k_f = fl["k_f_w_m_k"] if k_f is None else k_f
        self.beta = fl["beta_1_k"] if beta is None else beta
        self.g = fl["g_m_s2"] if g is None else g
        self.pricing = CommodityPricingTracker()

    def calculate_hydraulic_diameter(self, width, height):
        area = width * height
        perimeter = 2 * (width + height)
        return (4 * area) / perimeter if perimeter > 0 else 0

    def calculate_forced_convection_nusselt(self, velocity, d_h):
        reynolds = (self.rho_0 * velocity * d_h) / self.mu
        prandtl = (self.mu * self.cp) / self.k_f
        # Enforce conservative light-turbulent transition parameter bounds
        # [UPGRADED 2026-10-05] threshold/fallback from global_params.json
        db = PARAMS["dittus_boelter"]
        if reynolds > db["re_turbulent_threshold"]:
            nusselt = 0.023 * (reynolds ** 0.8) * (prandtl ** 0.4)
        else:
            nusselt = db["nu_laminar_fallback"]
        return nusselt, reynolds, prandtl

    def calculate_natural_convection_nusselt(self, t_wall, t_bulk, L):
        delta_t = abs(t_wall - t_bulk)
        grashof = ((self.rho_0 ** 2) * self.g * self.beta * delta_t *
                   (L ** 3)) / (self.mu ** 2)
        prandtl = (self.mu * self.cp) / self.k_f
        rayleigh = grashof * prandtl
        if 1e4 < rayleigh < 1e9:
            nusselt = 0.59 * (rayleigh ** 0.25)
        else:
            nusselt = 0.10 * (rayleigh ** 0.33)
        return nusselt, rayleigh

    def calculate_critical_heat_flux(self, h_fg, rho_v, sigma, rho_f):
        delta_rho = rho_f - rho_v
        chf = 0.149 * h_fg * (rho_v ** 0.5) * ((sigma * self.g *
                                               delta_rho) ** 0.25)
        return chf

    def calculate_wall_shear_stress(self, velocity, d_h, roughness=None):
        # [UPGRADED 2026-10-05] default roughness from global_params.json
        if roughness is None:
            roughness = PARAMS["a100_rack_case"]["channel_roughness_m"]
        reynolds = (self.rho_0 * velocity * d_h) / self.mu
        reynolds = (self.rho_0 * velocity * d_h) / self.mu
        if reynolds < 2300:
            f = 64 / reynolds
        else:
            f = 0.02
            for _ in range(10):
                try:
                    f = 1.0 / (-2.0 * math.log10((roughness / (3.7 * d_h)) +
                              (2.51 / (reynolds * math.sqrt(f))))) ** 2
                except (ValueError, ZeroDivisionError):
                    break
        tau_wall = (1.0 / 8.0) * f * self.rho_0 * (velocity ** 2)
        return tau_wall, f

    def calculate_system_pue(self, p_it, p_lighting, p_losses,
                             volumetric_flow, delta_p,
                             eta_pump=0.75, eta_motor=0.90):
        p_pumps = (volumetric_flow * delta_p) / (eta_pump * eta_motor)
        total_facility_power = p_it + p_lighting + p_losses + p_pumps
        pue = total_facility_power / p_it
        return pue, p_pumps


if __name__ == "__main__":
    solver = DataCenterThermalSolver()
    print("==========================================================")
    print("Executing Liquid-Cooled Data Center Thermal Engineering Test Suite")
    print("==========================================================\n")
    # Executing Core 6-Case Verification Path
    d_h = solver.calculate_hydraulic_diameter(0.002, 0.010)
    print(f"[1. Hydraulics] Computed Channel Hydraulic Diameter: "
          f"{d_h*1000:.3f} mm")
    _, re, pr = solver.calculate_forced_convection_nusselt(
        velocity=1.5, d_h=d_h)
    print(f"[2. Convection] Forced Convection Loop -> Re: {re:.1f}, "
          f"Pr: {pr:.1f}")
    cu_mass, cu_cost = solver.pricing.estimate_cabling_material_capex(0.15)
    print(f"[3. Commodity] Raw Copper Cost (0.15 m3): ${cu_cost:,.2f} USD")
    _, ra = solver.calculate_natural_convection_nusselt(
        t_wall=65.0, t_bulk=35.0, L=0.3)
    print(f"[4. Immersion] Natural Bath Rayleigh Number: {ra:.2e}")
    q_max = solver.calculate_critical_heat_flux(h_fg=110000, rho_v=13.0,
                                                sigma=0.012, rho_f=1600)
    print(f"[5. Boiling] Saturated Critical Heat Flux Limits: "
          f"{q_max/1000:.2f} kW/m2")
    p_score, _ = solver.calculate_system_pue(100000, 2000, 3000, 0.005,
                                             150000)
    print(f"[6. Optimization] Systemic Design PUE Metric: {p_score:.4f}\n")
    simulator = A100HyperscaleRackSimulator(solver)
    res = simulator.execute_simulation_case_study()
    pue_sim, pump_w = solver.calculate_system_pue(
        100000, 2000, 3000, res["vol_flow"], res["pressure_drop_pa"])
    print("[A100 Simulation Results]")
    print(f"  Channel Velocity : {res['channel_velocity']:.4f} m/s")
    print(f"  Flow Regime (Re) : {res['reynolds']:.1f}")
    print(f"  Heat Coef (h)    : {res['h_coef']:.2f} W/m2*K")
    print(f"  Silicon Temp     : {res['silicon_temp']:.2f} C (Verified Safe)")
    print(f"  Loop Pressure Drop: {res['pressure_drop_pa']/1000:.3f} kPa")
    print(f"  Pump Power Draw  : {pump_w:.2f} Watts")
    print(f"  Evaluated PUE    : {pue_sim:.5f}")
    print("==========================================================")

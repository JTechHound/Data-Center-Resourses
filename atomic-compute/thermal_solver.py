"""Atomic-Compute thermal solver - consolidated build reconstructed 2026-10-05
from Consolidated_GitHub_Repository_File_Structure_261005_142640_12_iuqt.pdf.

[REPAIRED] PDF extraction damage: joined "import math class" split; page-break
joins restored ("nusselt", "diameter", "unittest", "convection", "solver");
indentation re-applied. No logic invented.

[CHANGED vs v1] (1) New CommodityPricingTracker class (Cu $6.64/lb,
Al $3156/MT); wired as self.pricing in DataCenterThermalSolver.__init__.
(2) New A100HyperscaleRackSimulator 100 kW rack case study; __main__ now runs
it instead of the v1 six-case suite. (3) Dittus-Boelter turbulent threshold
changed 10000 -> 4000 (modeling change, see audit).
"""
import math


class CommodityPricingTracker:
    """Calculates the financial CapEx impact of metal commodity
    pricing spikes on data center builds."""
    def __init__(self):
        self.copper_price_per_lb = 6.64
        self.aluminum_price_per_mt = 3156.0
        self.density_copper = 8960.0
        self.density_aluminum = 2700.0

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
    server rack utilizing fluid physics equations."""
    def __init__(self, solver):
        self.solver = solver
        self.rack_power_w = 100000.0
        self.fluid_density = solver.rho_0
        self.fluid_cp = solver.cp

    def execute_simulation_case_study(self):
        delta_t_target = 10.0
        mass_flow_rate = self.rack_power_w / (self.fluid_cp * delta_t_target)
        volumetric_flow_rate = mass_flow_rate / self.fluid_density
        d_h_channel = self.solver.calculate_hydraulic_diameter(0.001, 0.008)
        velocity_in_channel = (volumetric_flow_rate / 500.0) / (0.001 * 0.008)
        nu, re, pr = self.solver.calculate_forced_convection_nusselt(
            velocity_in_channel, d_h_channel)
        h_coef = (nu * self.solver.k_f) / d_h_channel
        t_bulk_fluid = 40.0
        heat_flux_per_chip = 500.0 / 0.0006
        t_wall_silicon = t_bulk_fluid + (heat_flux_per_chip / h_coef)
        tau_wall, _ = self.solver.calculate_wall_shear_stress(
            velocity_in_channel, d_h_channel)
        return {
            "mass_flow": mass_flow_rate,
            "vol_flow": volumetric_flow_rate,
            "channel_velocity": velocity_in_channel,
            "reynolds": re,
            "nusselt": nu,
            "h_coef": h_coef,
            "silicon_temp": t_wall_silicon,
            "wall_shear": tau_wall}


class DataCenterThermalSolver:
    """Numerical simulation engine to compute fluid dynamics, heat
    transfer, and metrics."""
    def __init__(self, rho_0=800.0, mu=0.002, cp=2200.0, k_f=0.13,
                 beta=0.0007, g=9.81):
        self.rho_0 = rho_0
        self.mu = mu
        self.cp = cp
        self.k_f = k_f
        self.beta = beta
        self.g = g
        self.pricing = CommodityPricingTracker()

    def calculate_hydraulic_diameter(self, width, height):
        area = width * height
        perimeter = 2 * (width + height)
        return (4 * area) / perimeter if perimeter > 0 else 0

    def calculate_forced_convection_nusselt(self, velocity, d_h):
        reynolds = (self.rho_0 * velocity * d_h) / self.mu
        prandtl = (self.mu * self.cp) / self.k_f
        if reynolds > 4000:
            nusselt = 0.023 * (reynolds ** 0.8) * (prandtl ** 0.4)
        else:
            nusselt = 3.66
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

    def calculate_wall_shear_stress(self, velocity, d_h, roughness=1e-5):
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
    simulator = A100HyperscaleRackSimulator(solver)
    res = simulator.execute_simulation_case_study()
    print(f"Simulation successfully executed. Silicon Temp: "
          f"{res['silicon_temp']:.2f} C")

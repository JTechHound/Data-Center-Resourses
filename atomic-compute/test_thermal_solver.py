"""v1.0.1 test suite - reconstructed 2026-10-05 from the audit-repair doc
(Resource_pipeline_audit_repair__261005_143830_14_lr14.pdf).

[REPAIRED] PDF extraction damage only (page-break word joins restored,
indentation re-applied). Test renamed per source:
test_100_kw_rack_mass_flow_physics -> test_a100_rack_silicon_thermal_bounds,
with added turbulent-regime assertion (Re > 4000).
"""
import unittest
import math
from thermal_solver import DataCenterThermalSolver, A100HyperscaleRackSimulator, PARAMS

# [UPGRADED 2026-10-05] Test bounds read from global_params.json (single source).
BOUNDS = PARAMS["test_bounds"]


class TestAtomicComputeEngine(unittest.TestCase):
    """Automated testing framework for the Atomic Compute
    verification engine."""
    def setUp(self):
        self.solver = DataCenterThermalSolver()
        self.simulator = A100HyperscaleRackSimulator(self.solver)

    def test_hydraulic_diameter_square(self):
        d_h = self.solver.calculate_hydraulic_diameter(width=0.010,
                                                       height=0.010)
        self.assertAlmostEqual(d_h, 0.010, places=5)

    def test_critical_heat_flux_limits(self):
        chf = self.solver.calculate_critical_heat_flux(h_fg=110000, rho_v=13.0,
                                                       sigma=0.012, rho_f=1600)
        self.assertGreater(chf, 0.0)

    def test_commodity_pricing_conversions(self):
        cu_mass, cu_cost = self.solver.pricing.estimate_cabling_material_capex(0.1)
        al_mass, al_cost = self.solver.pricing.estimate_heat_exchanger_capex(0.1)
        self.assertGreater(cu_mass, al_mass)
        self.assertGreater(cu_cost, al_cost)

    def test_a100_rack_silicon_thermal_bounds(self):
        """Verifies updated high-velocity modeling pulls temperature
        safely below 100C threshold."""
        res = self.simulator.execute_simulation_case_study()
        self.assertGreater(res["mass_flow"], 0.0)
        self.assertGreater(res["reynolds"],
                           BOUNDS["reynolds_min_turbulent"])  # turbulent regime
        self.assertLess(res["silicon_temp"],
                        BOUNDS["silicon_temp_max_c"])  # thermal bound


if __name__ == "__main__":
    unittest.main()

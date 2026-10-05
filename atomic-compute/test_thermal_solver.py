"""Consolidated build test suite - reconstructed 2026-10-05 from
Consolidated_GitHub_Repository_File_Structure_261005_142640_12_iuqt.pdf.

[REPAIRED] PDF extraction damage only (page-break word joins restored,
indentation re-applied). Logic is verbatim from the source.

VALIDATION STATUS (run 2026-10-05): 3/4 pass.
FAIL: test_100_kw_rack_mass_flow_physics - silicon_temp = 3153.66 C,
not < 100.0. The A100 case study's own numbers are internally inconsistent
(500 W on 0.0006 m^2 = 833 kW/m^2 through a laminar channel with
h = 267 W/m^2K -> dT = 3114 K). See build audit notes. Not "fixed" here -
the correct remedy is a modeling decision (smaller D_h, turbulent regime,
or per-rack vs per-chip power), left to the repo owner.
"""
import unittest
import math
from thermal_solver import DataCenterThermalSolver, A100HyperscaleRackSimulator


class TestAtomicComputeEngine(unittest.TestCase):
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

    def test_100_kw_rack_mass_flow_physics(self):
        res = self.simulator.execute_simulation_case_study()
        self.assertGreater(res["mass_flow"], 0.0)
        self.assertLess(res["silicon_temp"], 100.0)


if __name__ == "__main__":
    unittest.main()

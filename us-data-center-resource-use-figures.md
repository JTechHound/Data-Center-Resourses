# U.S. Data Center Resource Use — National Figures

**Compiled:** October 26, 2026
**Scope:** Public sources only (DOE/Lawrence Berkeley National Laboratory, EIA, CBRE, JLL, company sustainability disclosures, peer-reviewed/preprint research). Figures are reported as published, with ranges where sources disagree. See §5 for why figures differ.
**Note:** This is a figures compilation for the Data-Center-Resourses project. It is not pushed to the GitHub repo — that happens on the owner's word.

---

## 1. Electricity — national totals and growth

The anchor source is Lawrence Berkeley National Laboratory's *United States Data Center Energy Usage Report: 2025 Update* (DOE lab, published June 2026), a bottom-up model counting server and AI-accelerator shipments, per-device power draw, cooling, and facility infrastructure. Cryptocurrency mining is excluded from its scope.

| Year | U.S. data center electricity | Share of U.S. electricity | Source |
| --- | --- | --- | --- |
| 2014 | 58 TWh | — | LBNL 2024 Report |
| 2018 | 76 TWh | 1.9% | LBNL 2024 Report |
| 2023 | 176 TWh | 4.4% | LBNL 2024 Report |
| 2024 | 192 TWh | 4.7% | LBNL 2025 Update (last historical year) |
| 2028 (projected) | 464 TWh (Reference Case) | — | LBNL 2025 Update |
| 2030 (projected) | 649 TWh (Reference Case); range 521–843 TWh | 11.8% (range 9.5–15.3%) | LBNL 2025 Update |

Other published points on the same trend:

- LBNL 2025 Update: data centers would account for about **33% of total U.S. load growth from 2024 to 2030**, while non-data-center load grows about 926 TWh (24%) over the same period.
- Goldman Sachs Research: U.S. data center power demand **31 GW in 2025 → 41 GW in 2026 → 66 GW in 2027**; data centers' share of U.S. peak summer demand from about 4% (2025) to over 8% (2027).
- EIA Short-Term Energy Outlook: total U.S. electricity consumption at record highs — **4,193 billion kWh in 2025, 4,283 billion kWh in 2026** — after more than a decade of roughly flat national demand.
- Grid pressure, PJM and ERCOT: EIA reports retail electricity sales forecast to grow at an average of **11% in 2025 and 2026 in ERCOT** and 4% in PJM, with data centers the main driver. ERCOT's large-load interconnection queue grew from about **63 GW at end-2024 to ~226 GW by November 2025 to ~474 GW by June 2026**, around 90% of it data centers — but under 1% of queued load is actually drawing power. A queue is a wish list, not a build plan.
- Connection waits: the national median time from interconnection request to commercial operation has more than doubled, from under 2 years in the 2000s to about **5 years (61 months)** for projects reaching operation in 2025.
- Global context: IEA puts global data center electricity near **1,000 TWh by 2026**, more than double the 460 TWh of 2022.

## 2. Where it sits — top U.S. markets by inventory

CBRE, H2 2025 total inventory (MW). North American primary-market supply reached 10,903 MW in H1 2026, up 33.7% year over year, with vacancy at a record-low 1.4% and 7,481.1 MW under construction (80.4% preleased).

| Market | H2 2025 inventory (MW) | H2 2025 available (MW) |
| --- | --- | --- |
| Northern Virginia ("Data Center Alley") | 4,039.6 | 21.5 |
| Atlanta | 1,459.2 | 28.5 |
| Dallas–Fort Worth | 1,067.3 | 26.0 |
| Chicago | 904.6 | 10.7 |
| Phoenix | 807.3 | 10.5 |
| Silicon Valley | 489.2 | 23.2 |
| Hillsboro, OR | 475.4 | 1.0 |
| Central Washington | 402.0 | 11.7 |

Pipeline and construction notes (figures vary by broker and date — see §5):

- Northern Virginia: **4,496.5 MW inventory in H1 2026** (CBRE), vacancy 0.2%, with 2,420.2 MW under construction, up 16.5% year over year. Loudoun County facilities with disclosed capacity draw roughly 4 GW from the grid as of 2026, with several more gigawatts approved or under construction across the region. JLL lists 5.9 GW planned in Northern Virginia.
- Atlanta overtook Northern Virginia for capacity under construction in H1 2026 at **2,882 MW**.
- Phoenix led U.S. construction activity in early 2026 with about **1.3 GW underway**; JLL lists 4.2 GW planned.
- Dallas–Fort Worth: JLL lists 3.9 GW planned; at least 142 data centers under construction statewide in Texas by one broker's count.
- Las Vegas/Reno: 3.5 GW planned (JLL).
- Columbus, OH: fastest-growing Midwest hub, roughly 25,000 construction workers in the New Albany business park alone.
- JLL overall: 31.6 GW of capacity planned across North America, phased over five-plus years; more than 100 GW of colocation and hyperscale capacity could break ground or deliver between 2025 and 2030; up to **$1 trillion of data center development between 2025 and 2030**.
- California separately: data centers used **10.8 TWh in 2023** (about 6% of national data center energy), up from 5.5 TWh in 2019, projected as high as 25 TWh by 2028 — roughly the power use of 2.4 million U.S. homes.

## 3. Water — direct use, indirect use, and where it bites

Water figures split into two very different numbers, and most company disclosures report only the smaller one:

- **Direct (on-site cooling):** U.S. data centers consumed about **66 billion liters (~17.4 billion gallons) on site in 2023** (LBNL). Projections put direct use at **38–73 billion gallons a year by 2028** (range across published estimates).
- **Indirect (electricity generation):** about **800 billion liters (~211 billion gallons) in 2023** (LBNL) — roughly 12 times the direct figure. About 92.4% of the total water footprint sits at power plants, per LBNL-based analysis. No major company includes generation water in its sustainability disclosures.

Company disclosures (self-reported, scopes differ — see §5):

| Company | Reported water | Year / note |
| --- | --- | --- |
| Google | 6.4 billion gal (2023); 6.1 billion gal consumed of 7.8 billion withdrawn (2024); 10.9 billion gal (2025, per Axis Intelligence) | ~95% of Google's water goes to data centers; 2025 figure is 2.4x its 2021 level |
| Microsoft | 1.7 billion gal (2023, +34% year over year); ~2.75 billion gal (2024) | Aggregate totals; site-level data not broken out |
| Meta | 813 million gal (2023); ~1.49 billion gal (2024) | ~95% for data centers; owned sites only |
| Amazon | 2.5 billion gal withdrawn (2025) | First public aggregate figure; 0.12 liters per kWh claimed vs 0.84 industry average cited |

Facility scale and cooling:

- Evaporative cooling consumes roughly **20,000–50,000 gallons per day per MW of IT load**; a large hyperscale facility can use **up to 5 million gallons a day**, roughly the daily use of a town of 50,000 people.
- Evaporated water is consumed, not returned to the local water system.

Where it bites locally:

- About **two-thirds of U.S. data centers built or in development since 2022 sit in high-water-stress areas** (Bloomberg analysis); about 40% of planned and existing U.S. data centers are in areas of high or extremely high water scarcity (World Resources Institute).
- Potomac River Basin: data centers account for about **8% of total regional water consumption, projected to reach 29% by 2050** (Interstate Commission on the Potomac River Basin).
- A single Meta data center in Newton County, Georgia accounts for about **10% of the county's entire water supply**.
- Phoenix area: data center cooling water projected to rise about **870%**, from roughly 385 million gallons a year toward 3.7 billion, even as Arizona absorbs federally mandated Colorado River shortage reductions.
- Arizona: a planned Meta project could draw as much as **1 billion gallons a year** from an aquifer used for farming.
- California: on-site data center water use grew from **1,078 acre-feet (2019) to 2,302 acre-feet (2023)** — enough for the annual needs of almost 7,000 California households.
- Global AI water: experts estimate global AI demand could require **1.1–1.7 trillion gallons of water a year by 2027**.

## 4. Carbon — hyperscale emissions and grid intensity

The tightest facility-level study is a Harvard/UCLA preprint covering **403 U.S. hyperscale data centers, May 2024–April 2025**, using EPA eGRID plant-level data:

- Electricity: **68–99 TWh** (central scenario ≈ 1.8% of total U.S. electricity).
- CO2: **37–54 million metric tons** (central estimate ≈ 45–52 million across reporting summaries).
- About **54–60% of attributed generation from fossil fuels**.
- Electricity-weighted carbon intensity: about **545–564 gCO2/kWh**, roughly **48% above** the contemporaneous U.S. grid average of about 369–370 gCO2/kWh.

Broader published estimates (wider scope than hyperscale-only):

- One 2025 estimate puts all U.S. data centers at **over 100 million metric tons of CO2 a year**, more than 2% of total U.S. emissions.
- One study projects U.S. data center emissions rising from about **90 million metric tons in 2025 to 404 million metric tons by 2030** without carbon capture.
- IEA (global): data center electricity emissions from about **180 million tons today to about 300 million tons by 2035**; coal supplies roughly 30% of the energy for these facilities globally.
- Concrete local case: Meta's "Hyperion" hyperscale project in Louisiana prompted the local utility to propose three new natural gas plants to meet up to **5 GW of demand** — about twice the electricity used by the entire city of New Orleans on a hot summer day.
- California: data center carbon emissions nearly doubled from **1.2 million tons (2019) to 2.4 million tons (2023)**.

## 5. Why figures differ — read this before reusing any number

- **Disclosure is not mandatory.** Data centers face no general requirement to publicly disclose water or energy use by site, unlike factories, power plants, and large irrigators above reporting thresholds. Company totals exclude leased sites, third-party-operated sites, and (always) electricity-generation water.
- **Scopes differ.** LBNL covers all U.S. data centers but excludes cryptocurrency mining. The Harvard study covers 403 hyperscale facilities only. Broker inventories (CBRE, JLL) measure different things (inventory vs planned vs under construction) at different dates.
- **Queues are not builds.** Interconnection queues (notably ERCOT's ~474 GW) include speculative requests; under 1% of ERCOT's queued load is drawing power.
- **Projections are scenarios, not forecasts.** LBNL's 2030 range (521–843 TWh) depends on GPU shipments, AI-server lifetimes, and inference workloads. Treat the Reference Case (649 TWh) as a middle scenario, not a prediction.
- **Water: direct vs indirect.** Any figure that does not say which it is should be assumed direct (on-site) only. The indirect footprint through power generation is roughly an order of magnitude larger.

---

## Sources

- Lawrence Berkeley National Laboratory, *United States Data Center Energy Usage Report: 2025 Update* (DOE, June 2026) — https://www.energy.gov/documents/united-states-data-center-energy-usage-report-2025-update
- LBNL 2024 Report summary (DOE news release, Dec 2024) — https://newscenter.lbl.gov/2025/01/15/berkeley-lab-report-evaluates-increase-in-electricity-demand-from-data-centers/
- CBRE, Northern Virginia largest U.S. data center market, H2 2025 inventory table — https://www.cbre.com/press-releases/northern-virginia-extends-lead-as-largest-u-s-data-center-market-in-2025
- JLL, data center availability and planned capacity — http://jll.com/en-us/newsroom/data-center-availability-crisis-deepens-as-vacancy-hits-historic-low
- Grid/queue figures (ERCOT, PJM, interconnection waits) — https://gridlas.com/findings.html
- Construction pipeline (Atlanta, Phoenix, Columbus, Texas) — https://www.classet.ai/blog/where-data-center-construction-hiring-is-happening-2026
- LBNL water figures (direct ~17.4B gal, indirect ~211B gal, 2023) — https://axis-intelligence.com/ai-data-center-water-usage-statistics/
- Company water disclosures (Google, Microsoft, Meta, Amazon) — https://aiweekly.co/alerts/amazon-discloses-25b-gallons-of-data-center-water-use-in-2025 · https://www.webpronews.com/ai-data-centers-drink-deep-but-barely-dent-the-nations-water-supply/
- Evaporative cooling rates and facility scale — https://www.datacenterknowledge.com/cooling/can-evaporative-cooling-in-data-centers-still-make-sense-
- Hyperscale carbon study (403 facilities, May 2024–April 2025) — https://arxiv.org/html/2606.05420v1
- California data center impacts (Next 10 report) — https://piedmontexedra.com/2025/11/data-centers-are-putting-new-strain-on-californias-grid-a-new-report-estimates-the-impacts

#!/usr/bin/env python3
"""Fetch the cited sources for the HerdLens report into a literature folder."""
import os
import re
import csv
import html as htmllib
import subprocess
import concurrent.futures as cf

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "文献调研")
os.makedirs(OUT, exist_ok=True)

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/154.0.0.0 Safari/537.36")

# num, slug, citation, url, expect ("pdf" | "html")
REFS = [
    (1, "Defra_LITP_policy_paper",
     "Department for Environment, Food and Rural Affairs, \u201cLivestock Information Transformation "
     "Programme (LITP),\u201d GOV.UK policy paper, updated 23 July 2026.",
     "https://www.gov.uk/government/publications/livestock-information-transformation-programme-litp/"
     "livestock-information-transformation-programme-litp", "html"),

    (2, "Defra_EID_mandatory_press_release",
     "Defra, \u201cElectronic ID for cattle mandatory in step forward for UK biosecurity,\u201d "
     "GOV.UK press release, 2 June 2025.",
     "https://www.gov.uk/government/news/electronic-id-for-cattle-mandatory-in-step-forward-for-uk-biosecurity",
     "html"),

    (3, "Roberts2012_RFID_retention_5yr",
     "A. J. Roberts, L. E. Wallace, M. Harbac, and J. A. Paterson, \u201cCase study: Retention and readability "
     "of radio frequency identification transponders in beef cows over a 5-year period,\u201d The Professional "
     "Animal Scientist, vol. 28, no. 2, pp. 221\u2013226, Apr. 2012.",
     "https://www.ars.usda.gov/ARSUserFiles/30300000/PAS%202012%2028%20221-226.pdf", "pdf"),

    (4, "ScottishGov_cattle_ID_consultation",
     "Scottish Government, \u201cCattle identification and traceability: consultation,\u201d 2024.",
     "https://www.gov.scot/publications/consultation-cattle-identification-traceability-scotland/pages/3",
     "html"),

    (5, "BCMS_what_to_do_after_calf_born",
     "Rural Payments Agency / BCMS, \u201cWhat to do after a calf is born,\u201d GOV.UK guidance, updated 2022.",
     "https://www.gov.uk/guidance/what-to-do-after-a-calf-is-born", "html"),

    (6, "BCMS_moving_cattle",
     "Rural Payments Agency / BCMS, \u201cMoving cattle: what cattle keepers need to know,\u201d "
     "GOV.UK guidance, updated 2023.",
     "https://www.gov.uk/guidance/moving-cattle-what-cattle-keepers-need-to-know", "html"),

    (7, "FAS_cross_compliance_breaches",
     "Farming Advice Service, \u201cCross compliance inspections: common breaches and guidance,\u201d 2022.",
     "https://www.farmingadviceservice.org.uk/sites/default/files/docs/2022-06/Cross%20compliance%20common"
     "%20breaches%20and%20the%20guidance%20Final%200.1.pdf", "pdf"),

    (8, "OIM_CMA_UK_internal_market_EID_report",
     "Office of the Internal Market, Competition and Markets Authority, \u201cFinal report: potential effects "
     "on the operation of the UK internal market from proposed regulatory differences relating to bovine "
     "electronic identification,\u201d GOV.UK, 29 Oct. 2025.",
     "https://www.gov.uk/government/publications/potential-effects-on-the-operation-of-the-uk-internal-market-"
     "from-proposed-regulatory-differences-relating-to-bovine-electronic-identification/final-report", "html"),

    (9, "HarperAdams_BEID_pilot_final_report",
     "S. M. Rutter, I. Huang, and K. Behrendt, \u201cDefra and Welsh Government Bovine Electronic "
     "Identification (BEID) pilot projects: joint final report,\u201d Harper Adams University and Welsh "
     "Government, Oct. 2024.",
     "https://www.gov.wales/sites/default/files/publications/2024-10/defra-and-welsh-government-bovine-"
     "electronic-Identification-beid-pilot-projects-joint-final-report.pdf", "pdf"),

    (10, "DAERA_voluntary_EID_QandA",
     "Department of Agriculture, Environment and Rural Affairs (Northern Ireland), \u201cQ&A for the "
     "voluntary introduction of electronic identification in cattle,\u201d 2026.",
     "https://www.daera-ni.gov.uk/articles/qa-voluntary-introduction-electronic-identification-cattle", "html"),

    (11, "RPA_cattle_identification_visits",
     "Rural Payments Agency, \u201cCattle identification visits: what to expect,\u201d GOV.UK guidance.",
     "https://www.gov.uk/guidance/cattle-identification-inspections", "html"),

    (12, "Defra_bTB_compensation_tables_2025",
     "Defra, \u201cBovine TB historical compensation value tables,\u201d GOV.UK, Aug. 2025.",
     "https://www.gov.uk/government/publications/bovine-tb-historical-compensation-value-tables/august-2025",
     "html"),

    (13, "Visscher2002_pedigree_errors_UK_dairy",
     "P. M. Visscher, J. A. Woolliams, D. Smith, and J. L. Williams, \u201cEstimation of pedigree errors in "
     "the UK dairy population using microsatellite markers and the impact on selection,\u201d Journal of "
     "Dairy Science, 2002.",
     "https://agris.fao.org/search/en/providers/122535/records/65dfff9b6eef00c2cea37b73", "html"),

    (14, "IsraelWeller2000_misidentification_genetic_gain",
     "C. Israel and J. I. Weller, \u201cEffect of misidentification on genetic gain and estimation of "
     "breeding value in dairy cattle populations,\u201d Journal of Dairy Science, vol. 83, no. 1, 2000.",
     "https://doi.org/10.3168/jds.S0022-0302(00)74858-9", "html"),

    (15, "Newton2022_genomics_parentage_value",
     "J. E. Newton et al., \u201cThe value proposition for using genomics to confirm parentage in Australian "
     "dairy systems,\u201d in Proc. 12th World Congress on Genetics Applied to Livestock Production "
     "(WCGALP), 2022.",
     "https://opal.latrobe.edu.au/articles/conference_contribution/The_value_proposition_for_using_genomics"
     "_to_confirm_parentage_in_Australian_dairy_systems/25565946", "html"),

    (16, "Edmondson_milk_residues",
     "P. Edmondson, \u201cTime to tackle milk residues and beat the yanks!,\u201d Veterinary Practice.",
     "https://www.veterinary-practice.com/article/time-to-tackle-milk-residues-and-beat-the-yanks", "html"),

    (17, "Pate_Scottish_dairy_antibiotic_use",
     "L. Pate et al., \u201cFactors influencing Scottish dairy farmers' antibiotic use,\u201d "
     "Veterinary Record Open, 2023.",
     "https://bvajournals.onlinelibrary.wiley.com/doi/10.1002/vetr.2997", "html"),

    (18, "Defra_bTB_strategy_England_2026",
     "Defra, \u201cNew strategy to tackle bovine TB in England,\u201d June 2026.",
     "https://www.gov.uk/government/collections/bovine-tb", "html"),

    (19, "Lords_HL1670_bTB_slaughter_2025",
     "Baroness Hayman of Ullock, written answer HL1670, House of Lords, 6 July 2026.",
     "https://www.theyworkforyou.com/wrans?id=2026-07-06.HL1670.h", "html"),

    (20, "BCMS_report_cattle_deaths",
     "Rural Payments Agency / BCMS, \u201cReport and record cattle that die on a holding,\u201d "
     "GOV.UK guidance.",
     "https://www.gov.uk/guidance/report-and-record-cattle-that-die-on-a-holding", "html"),

    (21, "DairyRoadmap_home",
     "Dairy Roadmap (Dairy UK, AHDB, NFU), \u201cDairy Roadmap: driving progress on the "
     "environment,\u201d 2025/26.",
     "https://dairyroadmap.co.uk/", "html"),

    (22, "Shearwell_SDL150_race_readers",
     "Shearwell Data Ltd, \u201cRace readers SDL150,\u201d product specification, 2024.",
     "https://shearwell.co.uk/race-readers-sdl150", "html"),

    (23, "Datamars_TruTest_XRP2_panel_reader",
     "Datamars / Tru-Test, \u201cXRP2 cattle panel EID reader,\u201d UK trade price list, 2025-26.",
     "https://www.shopdatamars.co.uk/product-category/grant-eligible-products/", "html"),

    (24, "FW_cow_collars_labour_saving",
     "Farmers Weekly, \u201cHow cow collars saved 150 hours of labour in breeding season,\u201d 2025.",
     "https://www.fwi.co.uk/livestock/livestock-breeding/how-cow-collars-saved-150-hours-of-labour-in-"
     "breeding-season", "html"),

    (25, "Afimilk_AfiAct_II_price",
     "Mill Dairy Service, \u201cAfimilk AfiAct II pedometer plus,\u201d UK trade price list, 2025.",
     "https://www.milldairyservice.co.uk/afimilk-afiact-tag-ii-pedometer-plus/", "html"),

    (26, "FW_buyers_guide_dairy_monitoring",
     "Farmers Weekly, \u201cBuyer's guide to the latest dairy monitoring technologies.\u201d",
     "https://www.fwi.co.uk/livestock/buyers-guide-latest-dairy-monitoring-technologies", "html"),

    (27, "CattleEye_pricing_and_GEA_acquisition",
     "CattleEye, \u201cPricing,\u201d and GEA, \u201cGEA adds proven AI solution to portfolio with "
     "CattleEye acquisition,\u201d press release, Mar. 2024.",
     "https://cattleeye.com/en-gb/buy", "html"),

    (28, "FW_CattleEye_lameness_detection",
     "Farmers Weekly, \u201cHow a low-cost camera improves lameness detection for dairy farm.\u201d",
     "https://www.fwi.co.uk/livestock/dairy/how-a-low-cost-camera-improves-lameness-detection-for-dairy-farm",
     "html"),

    (29, "FW_LF_vs_UHF_EID_comparison",
     "Farmers Weekly, \u201cUltra-high or low frequency cattle EID tags: which is best?,\u201d 2024.",
     "https://www.fwi.co.uk/livestock/ultra-high-or-low-frequency-cattle-eid-tags-which-is-best", "html"),

    (30, "AHDB_GB_producer_numbers",
     "Agriculture and Horticulture Development Board, \u201cGB producer numbers,\u201d updated 11 June 2026.",
     "https://ahdb.org.uk/dairy/GB-producer-numbers", "html"),

    (31, "FarmersGuardian_invest_in_EID",
     "Farmers Guardian, \u201cWhy you should invest now to get the most out of EID technology "
     "on-farm.\u201d",
     "https://farmersguardian.com/news/4516906", "html"),

    (32, "FAS_Scotland_milk_price_Sep2026",
     "Farm Advisory Service Scotland, \u201cBusiness and policy September 2026: milk,\u201d 2026.",
     "https://www.fas.scot/article/business-and-policy-september-2026-milk", "html"),

    (33, "Defra_farm_accounts_England_2024_25",
     "Defra, \u201cFarm accounts in England: chapter 2 key results 2024/25,\u201d GOV.UK statistical release.",
     "https://www.gov.uk/government/statistics/farm-accounts-in-england", "html"),

    (34, "AHDB_Kingshay_dairy_costings",
     "Kingshay / AHDB, \u201cKingshay dairy costings,\u201d rolling twelve months to June 2026.",
     "https://ahdb.org.uk/dairy/kingshay-dairy-costings", "html"),

    (35, "Yu2025_Holstein_reID_multicamera",
     "P. Yu, T. Burghardt, A. W. Dowsey, and N. W. Campbell, \u201cHolstein-Friesian re-identification using "
     "multiple cameras and self-supervision on a working farm,\u201d Computers and Electronics in "
     "Agriculture, vol. 237, 2025.",
     "https://arxiv.org/abs/2410.12695", "html"),

    (36, "DairyRoadmap_farmer_targets",
     "Dairy UK, AHDB and NFU, \u201cThe Dairy Roadmap: farmer targets,\u201d accessed 2026.",
     "https://dairyroadmap.co.uk/farmers-targets/", "html"),

    (37, "BusinessCompanion_cattle_identification_regulations",
     "Business Companion / Trading Standards, \u201cCattle identification: the Cattle Identification "
     "Regulations 2007,\u201d England guidance.",
     "https://www.businesscompanion.info/en/quick-guides/livestock/cattle-identification", "html"),

    (38, "Defra_structure_of_agricultural_industry_regions",
     "Defra, \u201cStructure of the agricultural industry in England and the UK at June: region "
     "dataset 2025.\u201d",
     "https://www.gov.uk/government/statistical-data-sets/structure-of-the-agricultural-industry-in-"
     "england-and-the-uk-at-june", "html"),

    (39, "Defra_Agriculture_in_UK_2025_ch8_livestock",
     "Defra, \u201cAgriculture in the United Kingdom 2025: chapter 8 livestock.\u201d",
     "https://www.gov.uk/government/statistics/agriculture-in-the-united-kingdom-2025/chapter-8-livestock",
     "html"),

    (40, "Negreiro2024_Siamese_Holstein_growth",
     "A. Negreiro et al., \u201cSiamese networks for identification of Holstein cattle during growth and "
     "across different physiological stages,\u201d in Proc. 11th European Conference on Precision Livestock "
     "Farming (ECPLF), Bologna, 2024, pp. 467\u2013474.",
     "https://experts.illinois.edu/en/publications/siamese-networks-for-identification-of-holstein-cattle-"
     "during-gro", "html"),

    (41, "Lamanna2025_wearable_collar_review",
     "B. Lamanna, M. Bovo, and L. Cavallini, \u201cWearable collar technologies for dairy cows: a "
     "systematized review,\u201d Animals, vol. 15, no. 3, p. 458, 2025.",
     "https://www.mdpi.com/2076-2615/15/3/458", "html"),

    (42, "Kingshay_antimicrobial_focus_2025",
     "Kingshay, \u201cAntimicrobial focus report,\u201d summarised in The Scottish Farmer and DairyNews, "
     "Feb. 2026.",
     "https://www.thescottishfarmer.co.uk/business_sales/25912340.huge-opportunity-lower-antibiotic-use-"
     "dairy-herds/", "html"),

    (43, "Defra_FETF_2025_guidance",
     "Defra, \u201cFarming Equipment and Technology Fund 2025 guidance,\u201d Defra Farming Blog, "
     "7 May 2025.",
     "https://defrafarming.blog.gov.uk/2025/05/07/farming-equipment-and-technology-fund-2025-guidance-"
     "now-available", "html"),

    (44, "OldMill_milk_cost_of_production_2024_25",
     "Old Mill and the Farm Consultancy Group, \u201cMilk cost of production report 2024/25,\u201d Oct. 2025.",
     "https://om.uk/assets/uploads/2025/10/OM_Milk_Report_Brochure-2025-Published-Spreads.pdf", "pdf"),
]

# Supplementary material used in the analysis but not cited in the reference list.
SUPP = [
    (45, "CattleEye_lameness_validation_PMC",
     "A. Anagnostopoulos et al., \u201cInitial validation of an intelligent video surveillance system for "
     "automatic detection of dairy cattle lameness,\u201d Frontiers in Veterinary Science, 2023.",
     "https://pmc.ncbi.nlm.nih.gov/articles/pmid/37383350/", "html"),

    (46, "USDA_APHIS_EID_tag_retention_rule",
     "USDA APHIS, \u201cFinal rule response: official EID tag retention requirements,\u201d 2021 docket "
     "APHIS-2021-0020.",
     "https://downloads.regulations.gov/APHIS-2021-0020-2011/content.pdf", "pdf"),

    (47, "AHDB_UK_and_EU_cow_numbers",
     "AHDB, \u201cUK and EU cow numbers,\u201d updated 6 Oct. 2026 (source: Defra).",
     "https://ahdb.org.uk/dairy/uk-and-eu-cow-numbers", "html"),

    (48, "DairyUK_Roadmap_climate_ambition_PDF",
     "Dairy UK, AHDB and NFU, \u201cThe Dairy Roadmap climate ambition: supporting UK net zero,\u201d "
     "Nov. 2021.",
     "https://www.dairyuk.org/wp-content/uploads/2021/11/Dairy-Roadmap-Climate-Ambition-Final-Version.pdf",
     "pdf"),

    (49, "SocialMarketFoundation_farm_tech_productivity",
     "Social Market Foundation, \u201cMoovin' on up: (how) can we use new technologies to improve "
     "productivity on Britain's livestock farms?\u201d",
     "https://www.smf.co.uk/publications/farm-tech-productivity", "html"),

    (50, "Shearwell_CIS_ear_tag_catalogue",
     "Cattle Information Service, \u201cCIS cattle ear tag catalogue,\u201d supplier catalogue "
     "(commercial price reference).",
     "https://thecis.co.uk/Media/Default/Ear%20Tags/CIS-Cattle-Ear-Tag-Catalogue-Edition-1-WEB-SPS.pdf", "pdf"),
]

ALL = REFS + SUPP


def fetch(item):
    num, slug, cite, url, expect = item
    tag = f"R{num:02d}"
    pdf_path = os.path.join(OUT, f"{tag}_{slug}.pdf")
    html_path = os.path.join(OUT, f"{tag}_{slug}.html")
    txt_path = os.path.join(OUT, f"{tag}_{slug}.txt")
    for p in (pdf_path, html_path, txt_path):
        if os.path.exists(p):
            os.remove(p)
    cmd = ["curl", "-sS", "-L", "-A", UA, "--max-time", "60",
           "-H", "Accept: */*", "-o", "-", "-w", "\n__CODE__%{http_code}__TYPE__%{content_type}",
           url]
    try:
        res = subprocess.run(cmd, capture_output=True, timeout=90)
        raw = res.stdout
    except Exception as e:
        return (num, "error", f"curl failed: {e}")
    if not raw:
        return (num, "error", "empty response")
    marker = raw.rfind(b"\n__CODE__")
    if marker < 0:
        return (num, "error", "no status marker")
    meta = raw[marker:].decode("utf8", "ignore")
    body = raw[:marker]
    code = re.search(r"__CODE__(\d+)", meta)
    ctype = re.search(r"__TYPE__([^\s;]+)", meta)
    code = code.group(1) if code else "???"
    ctype = (ctype.group(1) if ctype else "").lower()

    if code != "200" or len(body) < 500:
        return (num, "blocked", f"HTTP {code}, {len(body)} bytes")

    if body[:4] == b"%PDF" or "pdf" in ctype:
        with open(pdf_path, "wb") as f:
            f.write(body)
        return (num, "pdf", f"{os.path.basename(pdf_path)} ({len(body)//1024} KB)")

    text = body.decode("utf8", "ignore")
    with open(html_path, "w", encoding="utf8") as f:
        f.write(text)
    plain = strip_html(text)
    with open(txt_path, "w", encoding="utf8") as f:
        f.write(f"SOURCE: {url}\nCITATION: {cite}\n\n{plain}")
    return (num, "html", f"{os.path.basename(html_path)} + .txt ({len(plain)//1024} KB text)")


def strip_html(s):
    s = re.sub(r"(?is)<(script|style|noscript|svg)[^>]*>.*?</\1>", " ", s)
    s = re.sub(r"(?is)<br\s*/?>", "\n", s)
    s = re.sub(r"(?is)</(p|div|li|h[1-6]|tr|section|article)>", "\n", s)
    s = re.sub(r"(?s)<[^>]+>", " ", s)
    s = htmllib.unescape(s)
    s = re.sub(r"[ \t\r\f\v]+", " ", s)
    s = re.sub(r"\n\s*\n\s*\n+", "\n\n", s)
    return s.strip()


if __name__ == "__main__":
    results = {}
    with cf.ThreadPoolExecutor(max_workers=8) as ex:
        for num, status, detail in ex.map(fetch, ALL):
            results[num] = (status, detail)
            print(f"R{num:02d} {status:8s} {detail}")

    rows = []
    for num, slug, cite, url, _ in ALL:
        status, detail = results.get(num, ("pending", ""))
        rows.append({"Ref": f"[{num}]", "Citation": cite,
                     "URL": url, "Status": status, "Local file": detail})
    with open(os.path.join(OUT, "00_文献索引.csv"), "w", newline="", encoding="utf8") as f:
        w = csv.DictWriter(f, fieldnames=["Ref", "Citation", "URL", "Status", "Local file"])
        w.writeheader()
        w.writerows(rows)

    ok = sum(1 for v in results.values() if v[0] in ("pdf", "html"))
    bad = [k for k, v in results.items() if v[0] not in ("pdf", "html")]
    with open(os.path.join(OUT, "00_文献索引.md"), "w", encoding="utf8") as f:
        f.write("# 文献调研索引 \u2014 HerdLens 奶牛识别方案报告\n\n")
        f.write(f"抓取结果：{ok} / {len(ALL)} 条已下载到本文件夹，{len(bad)} 条需要手动获取。\n")
        f.write("所有链接最后访问时间：2026 年 10 月。\n\n")
        f.write("## 已下载\n\n")
        for r in rows:
            if r["Status"] in ("pdf", "html"):
                f.write(f"**[{r['Ref'].strip('[]')}]** {r['Citation']}\n")
                f.write(f"- URL: {r['URL']}\n")
                f.write(f"- 本地文件: `{r['Local file']}`\n\n")
        f.write("\n## 需要手动获取（付费墙 / 站点拦截）\n\n")
        for r in rows:
            if r["Status"] not in ("pdf", "html"):
                f.write(f"**[{r['Ref'].strip('[]')}]** {r['Citation']}\n")
                f.write(f"- URL: {r['URL']}\n")
                f.write(f"- 状态: {r['Status']} \u2014 {r['Local file']}\n\n")
    print(f"\ndone: {ok}/{len(ALL)} downloaded; blocked: {bad}")

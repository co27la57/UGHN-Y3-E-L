#!/usr/bin/env python3
"""Write the retrieval note for the Harper Adams BEID pilot (WAF-blocked) and
rebuild the literature index from what is actually on disk."""
import os
import csv
import glob
import importlib.util

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "文献调研")

spec = importlib.util.spec_from_file_location("fr", os.path.join(BASE, "fetch_references.py"))
fr = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fr)
ALL = fr.ALL

# Corrected URLs discovered while chasing the blocked items.
FIX = {
    7: "https://www.gov.uk/government/collections/keeping-cattle-bison-and-buffalo-in-england-and-wales",
    11: "https://www.gov.uk/guidance/cattle-identification-inspections-what-to-expect",
    20: "https://www.gov.uk/guidance/report-and-record-cattle-deaths-on-the-holding",
    41: "https://europepmc.org/article/PMC/PMC11815998",
    45: "https://europepmc.org/article/MED/37383350",
}

HOWTO = {
    4: "Cloudflare 人机验证拦截。改用学校 VPN，或直接看官方咨询 PDF 的 Google 缓存；也可改用 OIM/CMA 报告 [8] 中的同一事实（该报告已下载）。",
    9: "CloudFront 403。建议：学校 VPN 后打开 gov.wales 页面下载 3 MB PDF；或走 Defra Science Search / 图书馆馆际互借。关键数据已摘录在本文件夹的执行摘要文件中，可直接引用。",
    14: "ScienceDirect 机器人验证。通过格拉斯哥大学图书馆的 ScienceDirect 订阅登录后下载，或用 Google Scholar 找 PDF 版本。",
    15: "Cloudflare 202 拦截。La Trobe 机构库 OPAL，校园网内可直接打开；也可用 Google Scholar 找同名条目。",
    16: "站点已迁移到 Improve Veterinary Education，原链接跳转未完成。建议直接在新站检索 'milk residues' 或改用 AHDB 的残留防控材料替代。",
    17: "Wiley 机器人验证（Ray ID 属 Cloudflare）。用学校图书馆的 Wiley Online Library 订阅登录。",
    19: "theyworkforyou 访问超时。可改用 UK Parliament 官方 Hansard 检索 HL1670，或引用 Defra 年度 bTB 统计。",
    22: "shearwell.co.uk 返回 403（拒绝自动化访问）。建议手动在浏览器打开，或改用经销商标价页（MyFarmWorks / Farming Solutions）截图存档。",
    23: "shopdatamars.co.uk 返回 403。同 [22]，手动浏览器打开；或使用 Wise Agriculture / Tanner Trading 的同型号标价。",
    31: "farmersguardian.com 返回 403。手动浏览器打开，或改引 Farmers Weekly 的同主题报道。",
    37: "businesscompanion.info 返回 403。手动浏览器打开；法规原文可直接查 legislation.gov.uk 的 The Cattle Identification Regulations 2007。",
    46: "regulations.gov 返回 403。改用 regulations.gov 网页版检索 APHIS-2021-0020，或引用 USDA APHIS 最终规则摘要。",
    48: "dairyuk.org 触发 Cloudflare 验证。作业题目本身给出的链接就是这个 PDF，建议在学校网络下手动下载；Dairy Roadmap 官网 dairyroadmap.co.uk（已下载 [21][36]）包含同样的目标数值。",
    49: "smf.co.uk 触发 Cloudflare 验证。可用学校 VPN 或 Google Scholar 缓存；此项为补充材料，非核心引用。",
}

R09_EXTRACT = """R09 \u2014 Harper Adams / Defra & Welsh Government BEID 试点联合最终报告
执行摘要原文摘录（原 PDF 被 gov.wales 的 WAF 拦截，未能自动下载；以下为官方页面公开的执行摘要全文，可直接引用）

作者：S. Mark Rutter, Iona Huang, Karl Behrendt \u2014 Harper Adams University, Edgmond, Newport, Shropshire TF10 8NB
发布：Welsh Government，2024-10-10，共 51 页
PDF：https://www.gov.wales/sites/default/files/publications/2024-10/defra-and-welsh-government-bovine-electronic-Identification-beid-pilot-projects-joint-final-report.pdf
页面：https://www.gov.wales/node/64280

--- 摘录开始 ---

The English and Welsh Governments aim to introduce the mandatory electronic identification (EID) of cattle in
England and Wales in the near future. This will require farmers to fit a statutory EID tag in the ears of calves
born after the implementation date. There are two different types of radio frequency identification (RFID)
technologies that can be used with cattle: low frequency (LF) and ultra-high frequency (UHF). LF is a long
established animal ID technology and is already mandated for use in sheep in the UK and many other parts of the
world including the EU, whereas the use of UHF for animal ID is comparatively new. UHF EID tags provide
additional functionality over LF tags as they have a longer read range and multiple UHF tags can be read at once.

To help inform decision making at DEFRA and in the Welsh Government, they both commissioned Harper Adams
University to carry out pilot projects (one in England and one in Wales). The DEFRA pilot project looked at both
LF and UHF technology on five commercial cattle farms, two markets and an abattoir. The Welsh pilot project
included three beef farms and an abattoir. The Welsh pilot project focussed on LF technology and did not include
UHF. Decisions about UHF in Wales are being informed by the DEFRA-funded English trials. This Joint Final
Report covers both the Welsh and English pilot projects.

Generally, with static (fixed) readers, UHF performed better than LF. UHF read 99.6% of tagged, free moving
animals in a 2.75m wide alleyway, and 100% in a single cow width raceway. Low frequency alleyway readers are not
yet available in the UK, although an LF panel reader in a raceway read 99.4% of moving tagged animals.
Retro-fitting a UHF reader to a cattle crush is easier than retro-fitting LF readers, although replacement EID
doors (where the LF antennas are incorporated into a crush door) are available for some popular types of crush,
and worked very well on one of the pilot farms. Identifying animals in a crush or whilst being held in a raceway
using hand-held EID readers was on average about three times faster and more accurate than manual identification.

It was difficult to read a number of cattle in a pen with hand-held readers, irrespective of tag frequency. When
the target pen was surrounded on three sides by pens occupied by non-target animals, the UHF hand-held reader had
an accuracy of 67%, i.e. non-target animals were read on average on 33% of occasions instead of target animals.
This was less of a problem when the immediately adjacent pens were empty and only the pens on the diagonals were
occupied, which achieved a UHF hand-held accuracy of 96%. Non-target animal reading is a concern with UHF
hand-held readers as misidentification poses a risk to traceability and food safety. Misidentifying an animal
when it has been treated with a veterinary medicine could result in it going to slaughter during the withdrawal
period. Due to the shorter read range, non-target animal reading is less of a concern with LF hand-held readers.

The English farmers gained experience with both LF and UHF equipment as part of the DEFRA pilot project. They
showed a preference for UHF for a number of reasons, including being able to identify animals at a distance and
read a group of moving animals in an alleyway. They also liked that UHF was WYSIWYG ('what you see is what you
get' - i.e. the number on the display matches the visual identifier printed the ear tag) without the
complications of 'tag bucket files' (which link the EID number on the tag's chip with the animal's full herd
number and individual identifier as printed on the ear tag). The UHF hand-held reader used in the pilot also had
greater functionality. Note that the last three benefits (WYSIWYG, no tag buckets and reader functionality) are
not related to tag frequency. Non-WYSIWYG EID reading is seen as a barrier to adoption and should be avoided.
Should the mandated tags be required to follow either ISO 11784 for LF or ISO 6881 for UHF, then both LF and UHF
will be WYSIWYG without the need for tag bucket files.

--- 摘录结束 ---

本报告中用到的三处数据均出自以上摘要：
1. LF 面板读门在 raceway 中对行进中带标牛只的读取率 99.4%（支撑 UR1 的 99% 目标）
2. 手持电子读取比人工目视识别平均快约 3 倍且更准（支撑可负担性里的劳动力节省估算）
3. UHF 手持在四周有牛的栏舍中准确率仅 67%（支撑"多头牛并排/串读"的论证）
"""


def local_files(num, slug):
    tag = f"R{num:02d}"
    hits = []
    for ext in ("pdf", "html", "txt"):
        p = os.path.join(OUT, f"{tag}_{slug}.{ext}")
        if os.path.exists(p):
            kb = os.path.getsize(p) // 1024
            hits.append(f"{tag}_{slug}.{ext} ({kb} KB)")
    return hits


if __name__ == "__main__":
    with open(os.path.join(OUT, "R09_HarperAdams_BEID_执行摘要摘录.txt"), "w", encoding="utf8") as f:
        f.write(R09_EXTRACT)

    rows = []
    for num, slug, cite, url, _ in ALL:
        url = FIX.get(num, url)
        files = local_files(num, slug)
        if num == 9 and not files:
            files = ["R09_HarperAdams_BEID_执行摘要摘录.txt (官方执行摘要全文)"]
        status = "\u2713 已下载" if files else "\u2717 需手动获取"
        rows.append({
            "Ref": f"[{num}]",
            "Citation": cite,
            "URL": url,
            "Status": status,
            "Local file": " ; ".join(files) if files else "",
            "How to obtain": HOWTO.get(num, ""),
        })

    with open(os.path.join(OUT, "00_文献索引.csv"), "w", newline="", encoding="utf8") as f:
        w = csv.DictWriter(f, fieldnames=["Ref", "Citation", "URL", "Status", "Local file", "How to obtain"])
        w.writeheader()
        w.writerows(rows)

    got = [r for r in rows if r["Status"].startswith("\u2713")]
    miss = [r for r in rows if r["Status"].startswith("\u2717")]
    with open(os.path.join(OUT, "00_文献索引.md"), "w", encoding="utf8") as f:
        f.write("# 文献调研 \u2014 HerdLens 奶牛识别方案\n\n")
        f.write(f"共 {len(rows)} 条（报告正文引用 44 条 + 补充材料 6 条）。")
        f.write(f"**已下载 {len(got)} 条，需手动获取 {len(miss)} 条。**\n\n")
        f.write("链接最后访问：2026 年 10 月。文件命名 `RNN_主题.pdf / .html / .txt`，")
        f.write("`.txt` 是网页正文抽取版，便于直接检索关键词。\n\n")
        f.write("---\n\n## 一、已下载\n\n")
        for r in got:
            f.write(f"**{r['Ref']}** {r['Citation']}\n\n")
            f.write(f"- URL: {r['URL']}\n")
            f.write(f"- 本地: `{r['Local file']}`\n\n")
        f.write("---\n\n## 二、需手动获取（WAF / 付费墙 / 机器人验证）\n\n")
        for r in miss:
            f.write(f"**{r['Ref']}** {r['Citation']}\n\n")
            f.write(f"- URL: {r['URL']}\n")
            f.write(f"- 获取方式: {r['How to obtain']}\n\n")
    print(f"index rebuilt: {len(got)} downloaded, {len(miss)} manual")
    print("files in folder:", len(glob.glob(os.path.join(OUT, "R*"))))

# -*- coding: utf-8 -*-
"""Part 8 批判性分析 · 引用文献中文译解 -> A4 PDF
只译解报告第 8 部分实际引用的 [19][20][21]（AHDB / Defra 官方统计）。
"""
import os
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

OUT = os.path.dirname(os.path.abspath(__file__))
PDF = os.path.join(OUT, "Part8_市场文献_中文译解.pdf")

pdfmetrics.registerFont(TTFont('CN', '/System/Library/Fonts/STHeiti Light.ttc', subfontIndex=1))

# ---- palette (light theme) ----
INK   = HexColor('#2C2A26')
INK2  = HexColor('#55534C')
INK3  = HexColor('#8A877E')
LINE  = HexColor('#DAD7CF')
LINE2 = HexColor('#BFBCB2')
ACC   = HexColor('#185FA5')   # blue
ACCBG = HexColor('#EAF2FB')
AMB   = HexColor('#8A5410')
AMBBG = HexColor('#FBF0DF')
GREY  = HexColor('#F4F2EB')

W, H = 595.27, 841.89
LM, RM, TM, BM = 44, 44, 50, 44
CW = W - LM - RM
BOTTOM = BM + 10

def _iscjk(ch):
    o = ord(ch)
    return o >= 0x2E80 or 0x3000 <= o <= 0x303F or 0xFF00 <= o <= 0xFFEF

def runs(s):
    out, cur, k = [], '', (_iscjk(s[0]) if s else False)
    for ch in s:
        if _iscjk(ch) == k:
            cur += ch
        else:
            out.append((cur, k)); cur, k = ch, _iscjk(ch)
    if cur:
        out.append((cur, k))
    return out

def mwidth(s, size, bold=False):
    x = 0.0
    for seg, k in runs(s):
        f = 'CN' if k else ('Helvetica-Bold' if bold else 'Helvetica')
        x += pdfmetrics.stringWidth(seg, f, size)
    return x

def mt(c, x, y, s, size=9.5, col=INK, bold=False):
    for seg, k in runs(s):
        if k:
            c.setFont('CN', size); c.setFillColor(col)
            c.drawString(x, y, seg)
            if bold:
                c.drawString(x + 0.35, y, seg)
            x += pdfmetrics.stringWidth(seg, 'CN', size)
        else:
            f = 'Helvetica-Bold' if bold else 'Helvetica'
            c.setFont(f, size); c.setFillColor(col)
            c.drawString(x, y, seg)
            x += pdfmetrics.stringWidth(seg, f, size)
    return x

def tokenize(s):
    toks = []; i = 0; n = len(s)
    while i < n:
        ch = s[i]
        if _iscjk(ch):
            toks.append(('c', ch)); i += 1
        elif ch == ' ':
            toks.append(('s', ' ')); i += 1
        else:
            j = i
            while j < n and (not _iscjk(s[j])) and s[j] != ' ':
                j += 1
            toks.append(('w', s[i:j])); i = j
    return toks

def wrap(s, maxw, size):
    toks = tokenize(s)
    exp = []
    for kind, val in toks:
        if kind == 'w' and pdfmetrics.stringWidth(val, 'Helvetica', size) > maxw:
            buf = ''
            for ch in val:
                if buf and pdfmetrics.stringWidth(buf + ch, 'Helvetica', size) > maxw:
                    exp.append(('w', buf)); buf = ch
                else:
                    buf += ch
            if buf:
                exp.append(('w', buf))
        else:
            exp.append((kind, val))
    lines = []; cur = []; curw = 0.0
    for kind, val in exp:
        if kind == 's':
            if cur:
                cur.append(val); curw += pdfmetrics.stringWidth(val, 'Helvetica', size)
            continue
        f = 'CN' if kind == 'c' else 'Helvetica'
        w = pdfmetrics.stringWidth(val, f, size)
        if curw + w > maxw and cur:
            lines.append(''.join(cur).rstrip()); cur = []; curw = 0.0
        cur.append(val); curw += w
    if cur:
        lines.append(''.join(cur).rstrip())
    return lines or ['']


class Flow:
    def __init__(self, c):
        self.c = c; self.page = 1; self.y = H - TM
        self._footer()

    def _footer(self):
        c = self.c
        c.setStrokeColor(LINE); c.setLineWidth(0.5)
        c.line(LM, BM - 8, W - RM, BM - 8)
        mt(c, LM, BM - 19, "Part 8 引用文献中文译解", 7.5, INK3)
        rtxt = "第 %d 页" % self.page
        mt(c, W - RM - mwidth(rtxt, 7.5), BM - 19, rtxt, 7.5, INK3)

    def newpage(self):
        self.c.showPage(); self.page += 1; self.y = H - TM; self._footer()

    def need(self, h):
        if self.y - h < BOTTOM:
            self.newpage()

    def spacer(self, h=6):
        self.y -= h

    def rule(self, col=LINE, lw=0.6, gap=4):
        self.c.setStrokeColor(col); self.c.setLineWidth(lw)
        self.c.line(LM, self.y, W - RM, self.y)
        self.y -= gap

    def para(self, text, size=9.5, col=INK, leading=None, x0=None, x1=None,
             gap=4, bold=False):
        leading = leading or size * 1.55
        x0 = x0 if x0 is not None else LM
        x1 = x1 if x1 is not None else W - RM
        for ln in wrap(text, x1 - x0, size):
            self.need(leading)
            mt(self.c, x0, self.y - size, ln, size, col, bold=bold)
            self.y -= leading
        self.y -= gap

    def bullet(self, text, size=9.5, col=INK, gap=3):
        leading = size * 1.55
        x0 = LM + 13; x1 = W - RM
        for i, ln in enumerate(wrap(text, x1 - x0, size)):
            self.need(leading)
            if i == 0:
                self.c.setFillColor(ACC)
                self.c.circle(LM + 4, self.y - size * 0.5, 1.7, stroke=0, fill=1)
            mt(self.c, x0, self.y - size, ln, size, col)
            self.y -= leading
        self.y -= gap

    def heading(self, num, text, meta=None):
        self.need(46)
        self.spacer(4)
        self.c.setFillColor(ACC)
        self.c.rect(LM, self.y - 12, 3.2, 14, stroke=0, fill=1)
        mt(self.c, LM + 10, self.y - 10, text, 12, INK, bold=True)
        self.y -= 18
        if meta:
            self.para(meta, size=8.5, col=INK3, gap=2)
        self.rule(col=LINE, lw=0.7, gap=6)

    def note(self, label, text, fill=AMBBG, edge=HexColor('#E6D3AE'), lab_col=AMB):
        size = 8.7; leading = size * 1.5
        inner_w = CW - 22
        lines = wrap(text, inner_w, size)
        box_h = (len(lines) + 1) * leading + 12
        self.need(box_h + 6)
        top = self.y
        self.c.setFillColor(fill); self.c.setStrokeColor(edge); self.c.setLineWidth(0.6)
        self.c.roundRect(LM, top - box_h, CW, box_h, 4, stroke=1, fill=1)
        yy = top - 8 - size
        mt(self.c, LM + 11, yy, label, size, lab_col, bold=True)
        yy -= leading
        for ln in lines:
            mt(self.c, LM + 11, yy, ln, size, INK2)
            yy -= leading
        self.y = top - box_h - 6

    def formula(self, text):
        self.need(40)
        top = self.y
        self.c.setFillColor(GREY); self.c.setStrokeColor(LINE2); self.c.setLineWidth(0.6)
        self.c.roundRect(LM, top - 30, CW, 30, 4, stroke=1, fill=1)
        w = mwidth(text, 12.5, bold=True)
        mt(self.c, (W - w) / 2.0, top - 20, text, 12.5, ACC, bold=True)
        self.y = top - 30 - 6

    def table(self, header, rows, col_w, col_align, size=8.4, hsize=8.4, pad=4.5):
        n = len(col_w)
        hlines = [wrap(str(header[i]), col_w[i] - 8, hsize) for i in range(n)]
        hh = max(len(l) for l in hlines) * hsize * 1.3 + 2 * pad
        rh = size * 1.5 + 2 * pad
        total = hh + rh * len(rows)
        self.need(total + 6)
        x0 = LM
        # header
        self.c.setFillColor(ACCBG)
        self.c.rect(x0, self.y - hh, sum(col_w), hh, stroke=0, fill=1)
        cx = x0
        for i in range(n):
            yy = self.y - pad - hsize
            for ln in hlines[i]:
                self._cell(cx, yy, ln, col_w[i], col_align[i], hsize, bold=True)
                yy -= hsize * 1.3
            cx += col_w[i]
        self.y -= hh
        # body
        for row in rows:
            cx = x0
            for i in range(n):
                self._cell(cx, self.y - pad - size, str(row[i]), col_w[i],
                           col_align[i], size)
                cx += col_w[i]
            self.c.setStrokeColor(LINE); self.c.setLineWidth(0.4)
            self.c.line(x0, self.y - rh, x0 + sum(col_w), self.y - rh)
            self.y -= rh
        # outer border
        self.c.setStrokeColor(LINE2); self.c.setLineWidth(0.6)
        self.c.rect(x0, self.y, sum(col_w), total, stroke=1, fill=0)
        self.y -= 8

    def _cell(self, x, baseline, txt, w, align, size, bold=False):
        wpx = mwidth(txt, size, bold=bold)
        if align == 'l':
            tx = x + 5
        elif align == 'r':
            tx = x + w - 5 - wpx
        else:
            tx = x + (w - wpx) / 2.0
        mt(self.c, tx, baseline, txt, size, INK if not bold else ACC, bold=bold)


def build():
    c = canvas.Canvas(PDF, pagesize=(W, H))
    f = Flow(c)

    # ---------- title ----------
    mt(c, LM, f.y - 20, "Part 8 批判性分析 · 引用文献中文译解", 19, INK, bold=True)
    f.y -= 26
    mt(c, LM, f.y - 11, "市场规模与口径    |    对应引用 [19] [20] [21]", 11, ACC, bold=True)
    f.y -= 16
    mt(c, LM, f.y - 9, "数据来源：AHDB、Defra（英国官方统计）    译制：2026-10-17    仅供学习核对，数据以官方原文为准", 8.5, INK3)
    f.y -= 16
    f.rule(col=ACC, lw=1.2, gap=10)

    f.para("本文件只译解报告第 8 部分「批判性分析 · 市场规模与口径」实际引用的三条文献。"
           "第 8 部分用它们来界定可及市场（TAM）与区域口径，因此这里只摘译与本部分相关的数据与统计口径，并非全文直译。",
           size=9.5, gap=3)
    f.note("说明：", "经核对，第 8 部分仅引用 [19][20][21] 三条，且均为 AHDB / Defra 网络统计来源；"
                    "文献调研文件夹中的 12 个 PDF 未在第 8 部分被引用（它们服务于第 1、3、6、10、11、12 等其他部分）。",
           fill=ACCBG, edge=HexColor('#BBD4EE'), lab_col=ACC)

    # ---------- [19] ----------
    f.heading("19", "[19] AHDB：大不列颠奶业生产者数量（GB producer numbers）",
              "更新于 2026 年 6 月 11 日    |    AHDB 对主要乳品买家（major milk buyers）的调查")
    f.para("2026 年 4 月的调查估计，大不列颠约有 6,850 家奶业生产者，较上年减少 2.7%（约 190 家），延续近年的持续下降趋势。", gap=3)
    f.para("口径提示：6,850 家是大不列颠（GB）口径，不含北爱尔兰；统计对象是「向主要买家销售牛奶的生产者」，"
           "不等于所有饲养奶牛的农场数。", size=8.8, col=INK2, gap=5)
    f.table(["调查时点", "生产者数量", "同比变化", "同比 %"],
            [["2019 年 10 月", "8,720", "-", "-"],
             ["2020 年 4 月", "8,380", "-", "-"],
             ["2020 年 10 月", "8,310", "-410", "-4.7"],
             ["2021 年 4 月", "8,040", "-340", "-4.1"],
             ["2021 年 10 月", "8,000", "-310", "-3.7"],
             ["2022 年 4 月", "7,880", "-160", "-2.0"],
             ["2022 年 10 月", "7,850", "-150", "-1.9"],
             ["2023 年 4 月", "7,570", "-310", "-3.9"],
             ["2023 年 10 月", "7,500", "-350", "-4.5"],
             ["2024 年 4 月", "7,230", "-340", "-4.5"],
             ["2024 年 10 月", "7,200", "-300", "-4.0"],
             ["2025 年 4 月", "7,040", "-190", "-2.6"],
             ["2025 年 10 月", "7,010", "-190", "-2.6"],
             ["2026 年 4 月", "6,850", "-190", "-2.7"]],
            [200, 120, 100, 87], ['l', 'r', 'r', 'r'])
    f.note("附注：", "可下载数据集另含按地区、按月的食品标准局（FSA）登记数据，涵盖水牛、山羊、绵羊及奶牛生产者；"
                    "但 FSA 数字代表每月收到的加工申报、存在时间滞后，未必真实反映农户退出行业的速度，使用时应谨慎。")
    f.para("来源：https://ahdb.org.uk/dairy/gb-producer-numbers", size=8, col=ACC, gap=2)

    # ---------- [20] ----------
    f.heading("20", "[20] Defra：2025 年 6 月 1 日英国牲畜种群（Livestock populations in the UK）",
              "更新于 2026 年 10 月 2 日    |    英格兰 6 月农业与园艺调查（June Survey）")
    f.para("英国牛及犊牛总数约 930 万头，较上年下降 1.3%，延续近十年的缓慢下降趋势。", gap=3)
    f.para("其中奶牛群约 180 万头（精确值 1,849,459 头），较上年微增 0.7%，近十年基本稳定；"
           "肉牛群约 130 万头（精确值 1,289,723 头），下降 4.1%。奶牛已占繁殖母牛群近 60%。", gap=5)
    f.table(["年份（6 月 1 日）", "肉牛群（头）", "奶牛群（头）", "繁殖母牛群合计（头）"],
            [["2021", "1,485,283", "1,850,042", "3,335,325"],
             ["2022", "1,462,980", "1,841,845", "3,304,825"],
             ["2023", "1,407,171", "1,836,164", "3,243,335"],
             ["2024", "1,344,374", "1,836,442", "3,180,816"],
             ["2025", "1,289,723", "1,849,459", "3,139,182"]],
            [110, 130, 130, 137], ['l', 'r', 'r', 'r'])
    f.note("口径提示：", "奶牛数据来自牛只追溯系统（CTS），覆盖所有养牛场，不受抽样误差影响；"
                        "英格兰 2025 年 6 月调查向 55,000 家商业农场抽样，回收 27,000 份（回收率 51%）。")
    f.para("来源：https://www.gov.uk/government/statistics/livestock-populations-in-the-united-kingdom/livestock-populations-in-the-united-kingdom-at-1-june-2025",
           size=7.6, col=ACC, gap=2)

    # ---------- [21] ----------
    f.heading("21", "[21] Defra：英格兰区域农业概况（Agricultural facts: England regional profiles）",
              "数据年份 2024（截至 2024 年 6 月）    |    更新于 2025 年 10 月 30 日    |    来源：Defra 6 月调查")
    f.para("第 8 部分引用其中三个北部区域的关键指标，用于推算英格兰北部的潜在奶牛场数量。下表为报告直接采用的数值。", gap=5)
    f.table(["区域", "农业面积（千公顷）", "平均农场面积（公顷）", "奶牛群（千头）", "奶牛场占农场比例"],
            [["西北部", "893", "72", "271", "10%"],
             ["约克郡与亨伯", "1,086", "91", "75", "3.4%"],
             ["东北部", "581", "138", "13", "1.5%"],
             ["英格兰合计", "8,877", "87", "1,046", "4.9%"]],
            [105, 110, 110, 92, 90], ['l', 'r', 'r', 'r', 'r'])
    f.note("口径提示：", "以上均为商业农场（commercial holdings）口径，奶牛数仅计商业农场。参考：西北部 2024 年农业总收入 4.96 亿英镑（同比 +64%），"
                        "牛奶为最大产出（9.54 亿英镑）；西北部奶牛场平均农场营业收入（FBI）约 82,300 英镑。")
    f.para("来源：https://www.gov.uk/government/statistics/agricultural-facts-england-regional-profiles",
           size=8, col=ACC, gap=2)

    # ---------- 推算解说 ----------
    f.heading("+", "附：第 8 部分如何由上述数据推算市场规模", "TAM 推算方法与口径（中文解说）")
    f.para("缺少逐户客户清单时，报告用下式粗略估算某区域的奶业农场数量：", gap=6)
    f.formula("N = (A ÷ Am) × d")
    f.para("其中 A = 区域农业面积（公顷），Am = 平均农场面积（公顷），d = 奶业农场占农场的比例。"
           "(A ÷ Am) 得到区域农场总数，再乘以奶业农场占比 d，即得奶业农场数量 N。", gap=5)
    f.table(["区域", "A（公顷）", "Am（公顷）", "d", "农场总数 (A÷Am)", "推算 N（家）"],
            [["西北部", "893,000", "72", "10%", "约 12,403", "约 1,240"],
             ["约克郡与亨伯", "1,086,000", "91", "3.4%", "约 11,934", "约 406"],
             ["东北部", "581,000", "138", "1.5%", "约 4,210", "约 63"],
             ["合计", "-", "-", "-", "-", "约 1,709"]],
            [110, 90, 82, 52, 100, 73], ['l', 'r', 'r', 'r', 'r', 'r'])
    f.note("重要提示：", "由于原始数据四舍五入，且「奶业农场分类」与「牛奶生产者登记」口径不同，"
                        "约 1,700 家（合计约 1,709）是本报告的推算值，并非官方发布的精确客户数量。")
    f.para("可服务市场（SAM）与销售目标：", size=9.5, bold=True, gap=3)
    f.bullet("假设 40% 的潜在农场适用（经筛选通道空间、电子耳标覆盖、劳动负担、围栏能力、现金流及既有系统后），SAM = 1,700 × 40% = 680 家。")
    f.bullet("该 40% 尚未获得客户调查支持，属规划假设。")
    f.bullet("若三年累计安装 50 套，约占区域潜在市场（1,700 家）的 2.9%、约占假设可服务市场（680 家）的 7.4%。")
    f.bullet("销售目标：第一年 10 套、第二年 15 套、第三年 25 套；须由现场验证、安装能力与实际订单支撑。")

    # ---------- 关键数字速查 ----------
    f.heading("★", "关键数字速查", "第 8 部分引用的核心数据一览")
    f.table(["指标", "数值", "来源"],
            [["大不列颠奶业生产者", "6,850 家（2026-04，同比 -2.7%）", "[19]"],
             ["英国奶牛群", "1,849,459 头（2025-06，同比 +0.7%）", "[20]"],
             ["英国牛及犊牛总数", "约 930 万头（同比 -1.3%）", "[20]"],
             ["西北部奶牛群", "271 千头", "[21]"],
             ["约克郡与亨伯奶牛群", "75 千头", "[21]"],
             ["东北部奶牛群", "13 千头", "[21]"],
             ["推算北部奶业农场（TAM）", "约 1,700 家（本报告推算）", "推算"],
             ["可服务市场 SAM（40% 假设）", "680 家（本报告假设）", "假设"]],
            [205, 232, 70], ['l', 'l', 'c'])

    # ---------- 参考文献 ----------
    f.heading("≡", "参考文献", "编号沿用报告第 13 节参考文献表；均为 [Online] 网络来源")
    f.para("[19] AHDB, \"GB producer numbers,\" updated 11 Jun. 2026. [Online]. "
           "Available: https://ahdb.org.uk/dairy/gb-producer-numbers", size=8.2, col=INK2, gap=4)
    f.para("[20] Defra, \"Livestock populations in the United Kingdom at 1 June 2025,\" updated 2 Oct. 2026. [Online]. "
           "Available: https://www.gov.uk/government/statistics/livestock-populations-in-the-united-kingdom/livestock-populations-in-the-united-kingdom-at-1-june-2025",
           size=8.2, col=INK2, gap=4)
    f.para("[21] Defra, \"Agricultural facts: England regional profiles,\" 30 Oct. 2025 (2024 data). [Online]. "
           "Available: https://www.gov.uk/government/statistics/agricultural-facts-england-regional-profiles",
           size=8.2, col=INK2, gap=6)
    f.rule(col=LINE, gap=6)
    f.para("本文件为学习/核对用的中文译解，所有数值以官方原文为准；如与报告正文或官方更新有出入，以官方最新发布为准。",
           size=8, col=INK3)

    c.save()
    print("saved:", PDF)


if __name__ == "__main__":
    build()

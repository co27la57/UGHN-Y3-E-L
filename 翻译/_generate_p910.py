# -*- coding: utf-8 -*-
"""Part 10 提供解决方案的技术描述 · 引用文献 PDF 中文译解 -> A4 PDF
译解 §10 实际引用、且文献调研文件夹中有 PDF 的四条：[13][14][11][12]。
§9 用户需求未引用任何文献。
"""
import os
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

OUT = os.path.dirname(os.path.abspath(__file__))
PDF = os.path.join(OUT, "Part10_引用文献_中文译解.pdf")

pdfmetrics.registerFont(TTFont('CN', '/System/Library/Fonts/STHeiti Light.ttc', subfontIndex=1))

INK   = HexColor('#2C2A26'); INK2 = HexColor('#55534C'); INK3 = HexColor('#8A877E')
LINE  = HexColor('#DAD7CF'); LINE2 = HexColor('#BFBCB2')
ACC   = HexColor('#185FA5'); ACCBG = HexColor('#EAF2FB')
AMB   = HexColor('#8A5410'); AMBBG = HexColor('#FBF0DF'); GREY = HexColor('#F4F2EB')
TEAL  = HexColor('#0F6E56'); TEALBG = HexColor('#E3F2EC')

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
            c.setFont('CN', size); c.setFillColor(col); c.drawString(x, y, seg)
            if bold:
                c.drawString(x + 0.35, y, seg)
            x += pdfmetrics.stringWidth(seg, 'CN', size)
        else:
            f = 'Helvetica-Bold' if bold else 'Helvetica'
            c.setFont(f, size); c.setFillColor(col); c.drawString(x, y, seg)
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
    toks = tokenize(s); exp = []
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
        self.c = c; self.page = 1; self.y = H - TM; self._footer()

    def _footer(self):
        c = self.c
        c.setStrokeColor(LINE); c.setLineWidth(0.5); c.line(LM, BM - 8, W - RM, BM - 8)
        mt(c, LM, BM - 19, "Part 10 引用文献 PDF 中文译解", 7.5, INK3)
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
        self.c.setStrokeColor(col); self.c.setLineWidth(lw); self.c.line(LM, self.y, W - RM, self.y); self.y -= gap

    def para(self, text, size=9.3, col=INK, leading=None, x0=None, x1=None, gap=4, bold=False):
        leading = leading or size * 1.55
        x0 = x0 if x0 is not None else LM
        x1 = x1 if x1 is not None else W - RM
        for ln in wrap(text, x1 - x0, size):
            self.need(leading)
            mt(self.c, x0, self.y - size, ln, size, col, bold=bold)
            self.y -= leading
        self.y -= gap

    def bullet(self, text, size=9.0, col=INK, gap=2.5, dot=ACC):
        leading = size * 1.5
        x0 = LM + 13; x1 = W - RM
        for i, ln in enumerate(wrap(text, x1 - x0, size)):
            self.need(leading)
            if i == 0:
                self.c.setFillColor(dot); self.c.circle(LM + 4, self.y - size * 0.5, 1.6, stroke=0, fill=1)
            mt(self.c, x0, self.y - size, ln, size, col)
            self.y -= leading
        self.y -= gap

    def heading(self, text, meta=None, col=ACC):
        self.need(44)
        self.spacer(5)
        self.c.setFillColor(col); self.c.rect(LM, self.y - 12, 3.2, 14, stroke=0, fill=1)
        mt(self.c, LM + 10, self.y - 10, text, 11.5, INK, bold=True)
        self.y -= 18
        if meta:
            self.para(meta, size=8.4, col=INK3, gap=2)
        self.rule(col=LINE, lw=0.7, gap=6)

    def note(self, label, text, fill=AMBBG, edge=HexColor('#E6D3AE'), lab_col=AMB):
        size = 8.6; leading = size * 1.5
        lines = wrap(text, CW - 22, size)
        box_h = (len(lines) + 1) * leading + 12
        self.need(box_h + 6)
        top = self.y
        self.c.setFillColor(fill); self.c.setStrokeColor(edge); self.c.setLineWidth(0.6)
        self.c.roundRect(LM, top - box_h, CW, box_h, 4, stroke=1, fill=1)
        yy = top - 8 - size
        mt(self.c, LM + 11, yy, label, size, lab_col, bold=True)
        yy -= leading
        for ln in lines:
            mt(self.c, LM + 11, yy, ln, size, INK2); yy -= leading
        self.y = top - box_h - 6

    def subhead(self, text):
        self.need(20)
        mt(self.c, LM, self.y - 10, text, 9.6, ACC, bold=True)
        self.y -= 15

    def table(self, header, rows, col_w, col_align, size=8.2, hsize=8.2, pad=4.5):
        n = len(col_w); lead = size * 1.32; hlead = hsize * 1.28
        hlines = [wrap(str(header[i]), col_w[i] - 2 * pad, hsize) for i in range(n)]
        hh = max(len(l) for l in hlines) * hlead + 2 * pad
        body = [[wrap(str(row[i]), col_w[i] - 2 * pad, size) for i in range(n)] for row in rows]
        rh = [max(len(cl) for cl in cell) * lead + 2 * pad for cell in body]
        total = hh + sum(rh)
        self.need(min(total, 380) + 6)
        x0 = LM
        self.c.setFillColor(ACCBG); self.c.rect(x0, self.y - hh, sum(col_w), hh, stroke=0, fill=1)
        cx = x0
        for i in range(n):
            yy = self.y - pad - hsize
            for ln in hlines[i]:
                self._cell(cx, yy, ln, col_w[i], col_align[i], hsize, bold=True); yy -= hlead
            cx += col_w[i]
        self.y -= hh
        for ri, cell in enumerate(body):
            cx = x0
            for i in range(n):
                yy = self.y - pad - size
                for ln in cell[i]:
                    self._cell(cx, yy, ln, col_w[i], col_align[i], size); yy -= lead
                cx += col_w[i]
            self.c.setStrokeColor(LINE); self.c.setLineWidth(0.4)
            self.c.line(x0, self.y - rh[ri], x0 + sum(col_w), self.y - rh[ri])
            self.y -= rh[ri]
        self.c.setStrokeColor(LINE2); self.c.setLineWidth(0.6)
        self.c.rect(x0, self.y, sum(col_w), hh + sum(rh), stroke=1, fill=0)
        self.y -= 8

    def _cell(self, x, baseline, txt, w, align, size, bold=False):
        wpx = mwidth(txt, size, bold=bold)
        if align == 'l':
            tx = x + 5
        elif align == 'r':
            tx = x + w - 5 - wpx
        else:
            tx = x + (w - wpx) / 2.0
        mt(self.c, tx, baseline, txt, size, (ACC if bold else INK), bold=bold)


def build():
    c = canvas.Canvas(PDF, pagesize=(W, H))
    f = Flow(c)

    # ---------- title ----------
    mt(c, LM, f.y - 20, "Part 10 引用文献 · PDF 中文译解", 18, INK, bold=True)
    f.y -= 25
    mt(c, LM, f.y - 11, "提供解决方案的技术描述    |    对应引用 [12] [13] [14] [11]", 11, ACC, bold=True)
    f.y -= 15
    mt(c, LM, f.y - 9, "来源：Tru-Test / Datamars、Arrowquip 产品资料    译制：2026-10-17    仅供学习核对", 8.5, INK3)
    f.y -= 15
    f.rule(col=ACC, lw=1.2, gap=9)

    f.para("本文件译解报告第 10 部分「提供解决方案的技术描述」实际引用、且文献调研文件夹中有 PDF 的四条文献。"
           "第 9 部分「用户需求及其论证」未引用任何文献，故无内容。以下按原文结构分节译出，保留关键规格与价格。", gap=4)
    f.note("译解范围：", "§10 正文另引用 [1][3][4][5][8][9][15][16][25]（Defra/BCMS/HSE/ICAR/Banner/Pepperl+Fuchs/ISO），"
                        "均为网络来源、文件夹中无对应 PDF，故本文件不含。另：[11] 在报告中为 XRP2 读卡器产品页，"
                        "此处以文件夹内的 Datamars 官方价目表（XRP2i 读卡器商业报价）作为其 PDF 载体译出。",
           fill=ACCBG, edge=HexColor('#BBD4EE'), lab_col=ACC)

    # ================= [13] Arrowquip alley =================
    f.heading("[13] Arrowquip：Easy Flow Elite 可调式牛栏通道（§10.2 机械结构及尺寸）",
              "Easy Flow Elite Adjustable Cattle Alley  |  arrowquip.com/cattle-equipment/cattle-alleys/easy-flow-alley")
    f.subhead("产品概述")
    f.para("一款可防止牛只转身与摔倒的牛栏通道，面向需要安全、低应激牛只流动与快速可靠控制的牧场主。"
           "改进型 Easy Flow Elite 比常规牛栏更安全、更安静、更高效：摇篮形截面、全宽度可调，通过简单调节即可适配各种体型的牛只。", gap=3)
    f.bullet("弹簧加载锁定系统 + 安全插销：从一侧拉动调节缆即可快速改变通道宽度。")
    f.bullet("遵循低应激处理原则：凹焊（caulked）平整钢板覆盖，并在撞击插销上加尼龙衬套以降低噪音。")
    f.bullet("配备 3E（Easy Entry and Exit，便捷进出）系统：牛只看不到你不想让它看的东西；改动侧板即可施加压力区（pressure zone）处理技术来调控流速。")
    f.bullet("可选配滚动通道门（rolling alley gates）与踢板（kicker panels）进行扩展，配置方案近乎无限。")
    f.subhead("规格参数")
    f.table(["项目", "参数"],
            [["产品代码", "800-EF"],
             ["可选型号数", "2 款"],
             ["可选配件数", "5 类"],
             ["保修", "5 年"],
             ["尺寸（宽 x 高 x 长）", "35.5 英寸 x 80 英寸 x 98 英寸；或 35.5 英寸 x 80 英寸 x 122 英寸"],
             ["重量", "574 磅 / 673 磅"],
             ["宽度可调范围", "31.5 - 20.7 英寸"],
             ["挡板离地高度", "42 英寸（可加高，便于施加平衡点处理技术）"]],
            [150, 357], ['l', 'l'])
    f.subhead("可选型号与配件")
    f.bullet("8 英尺型 800-EF8：35.5 x 80 x 98 英寸，574 磅。", dot=TEAL)
    f.bullet("10 英尺型 800-EF10：35.5 x 80 x 122 英寸，673 磅。", dot=TEAL)
    f.bullet("30° / 45° 踢板（Kicker Panel）：用于把通道段弯曲成所需布置。", dot=TEAL)
    f.bullet("可拆卸挡板（Removable Panels）：进一步定制覆盖钢板的高度。", dot=TEAL)

    # ================= [14] Arrowquip race =================
    f.heading("[14] Arrowquip UK：牛只分流通道（Cattle Sorting Race）（§10.2）",
              "Cattle Sorting Race  |  arrowquip.co.uk/cattle-equipment/cattle-races/cattle-sorting-races/")
    f.subhead("产品概述")
    f.para("多种型号，最多可将牛只分流至三个方向；支持两种分流方式——通道系统内分流，以及挤压器后（post-crush）分流。"
           "把分流门（Drafting Gates）与分流通道置于挤压器之后即可实现 post-crush 分流：相比在围栏内人工分群，"
           "让牛只通过系统分流更安全、更快速。操作者可单手控制分流、另一手控制轭门来调节流速；分流门两侧可完全打开，"
           "便于接近牛只头部并穿过系统。高覆盖钢板可消除干扰、在高压情境下把应激降到最低；弹簧门配滑轮系统可快速换向而不中断流动。", gap=4)
    f.subhead("产品特性")
    f.bullet("配置选项丰富，可按需组合。")
    f.bullet("弹簧加载分流门 + 滑轮绳索：轻拉绳索即可把牛引向目标方向。")
    f.bullet("包裹侧板：1219 mm 钢板，限制牛看到操作员，使分流更顺畅。")
    f.bullet("左右手布置均可（用相同部件）。")
    f.subhead("产品规格")
    f.table(["规格项", "说明"],
            [["分流方向", "最多 3 个方向（分流或转向）"],
             ["侧板", "1219 mm 包裹钢板（消除干扰）"],
             ["钢板厚度", "1.63 mm 钢板"],
             ["结构", "粉末涂层钢 + 高品质材料，经久耐用"],
             ["操作", "可用相同部件配成左手或右手操作"],
             ["配套", "分流门 + 基础分流通道支持 post-crush 分流；设计用于配合 Q-Catch 87 系列挤压器"]],
            [110, 397], ['l', 'l'])
    f.subhead("可选型号")
    f.table(["型号", "重量", "尺寸（宽 x 高 x 长）", "用途"],
            [["单向分流 30°", "216 kg", "1682 x 2066 x 1320 mm", "向一侧偏转；30° 小角度、对流动干扰最小"],
             ["双向分流 30°", "276 kg", "2374 x 2066 x 1320 mm", "向主通道左侧或右侧偏转"],
             ["Post-Crush 分流门（新）", "333 kg", "1637-2469 x 2099 x 2413-2691 mm", "置于挤压器后分流至不同圈；单手操作分流、另一手控轭门；侧门可 180° 全开"]],
            [120, 60, 150, 177], ['l', 'r', 'l', 'l'])

    # ================= [11] Datamars price =================
    f.heading("[11] Datamars / Tru-Test：XRP2i 读卡器价目表（§10.5 RFID 模块 · 商业参考）",
              "Grant Eligible Products  |  shopdatamars.co.uk（英国贸易价目，不含税，2025-26）")
    f.para("Datamars Livestock 英国官网「可申补贴产品」页面。下表摘出与第 10.5 节 RFID 读卡器直接相关的条目"
           "（EID 读卡器及配套指示器、电子耳标），价格为不含税贸易价（Tax excl.）。", gap=4)
    f.table(["产品", "类别", "价格（不含税）"],
            [["Tru-Test XRP2i EID 面板读卡器（大天线）", "EID 读卡器", "£1,807.75"],
             ["Tru-Test XRP2i EID 面板读卡器（小天线）", "EID 读卡器", "£1,638.25"],
             ["Tru-Test XRP2i EID 面板读卡器（裸机）", "EID 读卡器", "£1,353.00"],
             ["Tru-Test XRS2i EID 手持杆式读卡器", "EID 读卡器", "£1,350.00"],
             ["Tru-Test XR5000 指示器", "可申补贴产品", "£2,298.00"],
             ["Tru-Test ID5000 指示器", "可申补贴产品", "£1,787.45"],
             ["Tru-Test JR5000 指示器", "可申补贴产品", "£1,250.00"],
             ["TagFaster EID 单屠宰标签", "标签", "£0.91"],
             ["TagFaster 双标签", "标签", "£1.09"]],
            [255, 120, 132], ['l', 'l', 'r'])
    f.note("备注：", "页面多数条目带「GRANT ELIGIBLE（可申补贴）」标记；另有 Flexi Mobile 4000C、Dairy Drafter、"
                    "Active Tag Gateway 等为 POA（价格面议）。此价目表用于第 12 节可负担性/预算核对。")

    # ================= [12] XRP2 quickstart =================
    f.heading("[12] Tru-Test：XRP2 面板读卡器快速启动指南（§10.5 RFID 模块）",
              "XRP2 Panel Reader Quickstart Guide  |  tru-test.com（安装与使用说明）")
    f.subhead("1. 开箱清单")
    f.bullet("XRP2 面板读卡器；大/小天线（或单独供货）；5 m 天线延长线（选配）。")
    f.bullet("读卡器-串口线（接 Tru-Test 称重指示器）；串口-USB 转接线（接 PC）。")
    f.bullet("电源适配器（按地区不同）；USB 闪存盘（内含 Data Link PC 软件与资料）；电瓶夹线；安装支架。")
    f.subhead("2. 供电")
    f.para("可用 12 V 电瓶供电（红夹接正极 +、黑夹接负极 -）；船用电池比汽车电池更耐亏电损伤。也可用随附电源适配器接市电。"
           "读卡器无电源开关，接电即自动开机；红色电源灯亮表示已开机，若红灯闪烁则表示电瓶电压过低。")
    f.subhead("3. 两种使用方式")
    f.bullet("独立（Standalone）：每次扫描的标签存入内置内存，事后导出。")
    f.bullet("联机（Connected）：每次扫描的标签立即发送给已连接设备（如指示器）。")
    f.subhead("4. 安装读卡器与天线")
    f.bullet("可安装在平面（木梁、混凝土）或金属管上；大天线可直接背装在读卡器上。切勿在天线上钻孔或拧穿表面，用预留安装孔。")
    f.bullet("读卡器与天线应装在挤压器/通道/称重箱/分流器的外侧，避免被牛只动作损坏。")
    f.bullet("必须限制牛只流动，确保天线读取范围内每次只有一头牛。")
    f.bullet("天线相对于金属栏杆/管道的位置会影响读取；天线定位对有效读取 EID 标签至关重要。可用两根天线，或与其他读卡器同步使用。")
    f.subhead("5. 连接指示器（选配）")
    f.para("蓝牙连接：先开指示器、再开读卡器；两者初始均关闭，置于 5 m 内，先开指示器并确认蓝牙开启，再给读卡器上电，"
           "等待约 1 分钟完成配对，蓝色蓝牙灯亮、LCD 显示已连设备名；随后扫一枚标签测试。无蓝牙时用随附读卡器-串口线连接。")
    f.subhead("6. 记录 EID 标签")
    f.bullet("联机模式：把牛赶入挤压器，经过天线时标签被读取并发送到指示器内存；读卡器 LCD 显示编号、绿色读取灯闪烁并蜂鸣，表示读取成功。")
    f.bullet("独立模式：按开始键新建记录会话（蜂鸣、LCD 显示会话号），牛经过天线即读入内置内存，同样有灯闪+蜂鸣提示。")
    f.subhead("7. 数据导出与云软件")
    f.para("两种导出方式：Data Link PC 软件（USB 连接后点击取数）或 Data Link Android 应用；均可保存会话文件、"
           "传输到 Datamars Livestock 云端（livestock.datamars.com）在线查看增重与生产性能、按群或按头追踪。")
    f.subhead("8. 读卡器设置菜单")
    f.table(["菜单项", "选项 / 说明"],
            [["蓝牙 BLUETOOTH", "Auto（默认，自动回连）/ Manual（连 Android 手机时用）/ Off（关闭）；FIND BT DEVICES 手动搜索；PAIRED DEVICES 已配对列表"],
             ["去重 DUPLICATES", "On（默认）：同一会话不重复记录同一 EID；Off：重复也记录"],
             ["输出模式 OUTPUT MODE", "Single（默认）：同一条 EID 只记录并发送一次；Cont：只记录一次但每次读到都发送"],
             ["数据格式 DATA FORMAT", "改变 EID 的存储与输出：Dec1（默认，国家码与国内码间有空格，如 964 123456789012）/ Dec2（无空格）/ Hex / ISO（符合 ISO 24631-6）/ ISO23（动物码以 A 开头）"],
             ["诊断 DIAGNOSTICS", "4 个诊断屏：供电电压、天线电压与调谐值、噪声水平、读取速率；数值异常时见排障一节"],
             ["软件版本 / 语言", "显示软件版本；LCD 语言可选英语/西语/葡语/法语/德语"]],
            [120, 387], ['l', 'l'])
    f.subhead("9. 排障要点")
    f.bullet("线缆松弛易被牛角剐蹭损坏：约每 200 mm 用扎带固定一次。")
    f.bullet("读取差/读不到：把天线与金属（如挤压器栏杆）拉开距离，用非金属物固定。")
    f.bullet("金属栏杆会影响天线性能：尝试把天线换到别的位置。")
    f.bullet("切勿让电源线跨过天线正面或背面：把电源线布置到远离天线处（如挤压器另一侧），避免干扰。")
    f.bullet("天线 20 m 内的带电系统（电围栏、日光灯等）会造成干扰：用诊断功能测试，尝试关闭；若是干扰源则移开天线或该系统。")
    f.subhead("10. 保养与合规")
    f.bullet("勿浸水；置于阴凉干燥处；用湿布、温水加皂擦拭（其他清洁剂可能损坏设备）；勿长期置于极端温度环境；不接线时盖好防尘盖。")
    f.bullet("合规：FCC Part 15、Class B 数字设备（摘译；完整声明见原文 Compliance 一节）。")

    # ---------- 参考文献 ----------
    f.heading("参考文献", "编号沿用报告第 13 节；均为产品/商业资料")
    f.para("[11] Tru-Test Datamars, \"XRP2 panel reader and antenna.\" [Online]. "
           "Available: https://us.tru-test.com/products/eid/xrp2-panel-reader-and-antennas", size=8.1, col=INK2, gap=3)
    f.para("[12] Tru-Test, \"XRP2 panel reader and antenna quickstart guide.\" [Online]. "
           "Available: https://us.tru-test.com/sites/default/files/webdam_assets/142271317.pdf", size=8.1, col=INK2, gap=3)
    f.para("[13] Arrowquip, \"Easy Flow Elite adjustable cattle alley.\" [Online]. "
           "Available: https://arrowquip.com/cattle-equipment/cattle-alleys/easy-flow-alley", size=8.1, col=INK2, gap=3)
    f.para("[14] Arrowquip UK, \"Cattle sorting races.\" [Online]. "
           "Available: https://arrowquip.co.uk/cattle-equipment/cattle-races/cattle-sorting-races/", size=8.1, col=INK2, gap=5)

    f.subhead("术语对照")
    f.table(["英文术语", "中文"],
            [["EID (Electronic Identification)", "电子标识（电子耳标）"],
             ["Panel Reader", "面板读卡器"],
             ["Antenna", "天线"],
             ["Crush", "挤压器（牛用保定架）"],
             ["Race / Alley", "通道 / 牛栏"],
             ["Sorting / Drafting", "分流 / 分群"],
             ["Post-crush drafting", "挤压器后分流"],
             ["Low-stress handling", "低应激处理"],
             ["Kicker panel", "踢板（弯折挡板）"],
             ["Indicator", "（称重）指示器"],
             ["Standalone / Connected", "独立 / 联机模式"],
             ["Grant eligible", "可申（政府）补贴"]],
            [220, 287], ['l', 'l'], size=8.0, hsize=8.0)

    f.rule(col=LINE, gap=5)
    f.para("本文件为学习/核对用的中文译解，规格与价格以官方原文为准。XRP2 快速启动指南原文为 48 页完整手册，此处译出与第 10.5 节相关的快速启动核心章节（第 1-11 页）。",
           size=8, col=INK3)

    c.save()
    print("saved:", PDF)


if __name__ == "__main__":
    build()

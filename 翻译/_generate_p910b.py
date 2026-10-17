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
    global PDF
    PDF = os.path.join(OUT, "Part10_引用文献_中文译解_第二批.pdf")
    c = canvas.Canvas(PDF, pagesize=(W, H))
    f = Flow(c)

    mt(c, LM, f.y - 19, "Part 10 引用文献 · PDF 中文译解（第二批）", 17, INK, bold=True)
    f.y -= 24
    mt(c, LM, f.y - 11, "补充 [1] [3] [4] [5] [8] [9] [15] [16]    |    2026-10-17 下载入库", 10.5, ACC, bold=True)
    f.y -= 14
    mt(c, LM, f.y - 9, "来源：Defra、BCMS、HSE、Banner Engineering、Pepperl+Fuchs    仅供学习核对，以官方原文为准", 8.4, INK3)
    f.y -= 14
    f.rule(col=ACC, lw=1.2, gap=8)

    f.para("本文件译解 Part 10「提供解决方案的技术描述」第二批引用文献，共 8 条（2026-10-17 下载入库）。"
           "与此前《Part10_引用文献_中文译解.pdf》（覆盖 [11][12][13][14]）合计，覆盖 Part 10 全部有本地 PDF 的引用。"
           "以下按原文结构摘译与 §10 相关的要点，并标注其对应的报告小节。", gap=4)
    f.note("编号说明：", "Part 10 现引用 [1][3][4][5][8][9][11][12][13][14][15][16]；[11][12][13][14] 见第一批译解，本文件覆盖其余 8 条。"
                        "原 [25] ISO 13849-1 因无法获取已从报告移除，其后编号前移（CIGR [26] 变为 [25]、Cerqueira [27] 变为 [26]）。",
           fill=ACCBG, edge=HexColor('#BBD4EE'), lab_col=ACC)

    # [1] LITP
    f.heading("[1] Defra：牲畜信息转型计划 LITP（§10.6 / §10.13 追溯系统背景）",
              "Livestock Information Transformation Programme  |  gov.uk，更新于 2026-07-23")
    f.bullet("LITP 是 Defra 针对英格兰的变革项目，用新技术更快、更准确地追溯牲畜流通。")
    f.bullet("从产地到消费者识别并追溯牲畜，有助于保护动物健康、支持农户、保障食品安全。")
    f.bullet("LITP 将取代英格兰现行按物种划分的追溯系统；首个落地服务面向牛，实现近乎实时的流通报告，并引入牛只电子标识（BEID）。")
    f.bullet("BEID 的意义：更快更有据的疫病控制决策、更好的动物健康与福利数据、更强的食品安全保障、提升生产力、更顺畅贸易。")
    f.bullet("合作方：APHA、RPA 与 BCMS、行业（TDUG 追溯设计用户组）、各权力下放政府（ScotEID / EIDCymru / 北爱尔兰）。")
    f.para("与 §10 关联：这是 §10.13「LIS 与农场软件接口」的法规背景——官方追溯框架要求区分「场内内部通行」与「依法应报告的流通」。",
           size=8.6, col=INK2, gap=2)

    # [3] BCMS ear tags
    f.heading("[3] BCMS / RPA：申购或更换官方牛耳标（§10.3 / §10.12）",
              "Get new or replacement official ear tags for cattle  |  gov.uk，更新于 2022-11-08")
    f.para("所有牛必须佩戴官方耳标以识别个体，属法定要求；不合规可致牛群流动限制、补贴削减或被起诉。", gap=3)
    f.bullet("耳标须向 BCMS 注册的认可供应商购买。英格兰/威尔士出生或 EU 以外进口的牛，耳标须清晰显示：皇冠标志、国家代码（UK）、牛群标记（herd mark）、6 位官方耳标号。")
    f.bullet("无官方耳标不得移动；耳标及官方编号不得在不同动物间复用；每头牛的官方编号终身不变（1998 年前出生/进口等除外）。")
    f.bullet("内容涵盖：申购新耳标、更换遗失/损坏/缺失/错误耳标、1998 年前出生或进口动物的规则、进出口/迁移的额外规则。")
    f.para("与 §10 关联：对应 §10.12「两侧官方可视标识不足时按官方程序核查、绝不创建替代正式编号」，以及验证表「耳标状态矩阵」（完好/失效/缺失/外壳损坏可读）。",
           size=8.6, col=INK2, gap=2)

    # [4] BCMS movements
    f.heading("[4] BCMS / RPA：记录与报告牛只移动（§10.13）",
              "Record and report cattle movements  |  gov.uk，更新于 2022-11-08")
    f.bullet("所有养牛人须在 holding register（herd register / 农场记录）与 cattle passport 中记录牛/ bison / buffalo 进出本场的日期。")
    f.bullet("须在 3 天内向 BCMS 报告移动；渠道：CTS Online、兼容农场软件（CTS Web Services）、CTS 自助电话、邮寄。")
    f.bullet("市场和屠宰场可代报，但养牛人仍对按时通报负法律责任。")
    f.bullet("记录时限：holding register 与 passport 的 movement history 均须在移动后 36 小时内完成。")
    f.para("与 §10 关联：§10.13 区分「可报告流通（reportable movements）」与场内「内部通行」，以及「保存提交与回执、防重复、离线缓存」的接口设计依据。",
           size=8.6, col=INK2, gap=2)

    # [5] BCMS holding register
    f.heading("[5] BCMS / RPA：保存牛只养殖登记册（§10.13）",
              "Keep a holding register for cattle  |  gov.uk，更新于 2023-06-28")
    f.bullet("须为每个 holding 单独保存 holding register，记录：移动、出生、死亡、官方耳标号变更；并保持最新、随时可供检查员查验。")
    f.bullet("更新时限：移动 36 小时；换耳标且编号变更 36 小时；乳用动物出生 7 天；其他牛出生 30 天；死亡 7 天。")
    f.bullet("每头法定记录项：官方耳标号、出生日期、性别、官方品种代码、本场出生牛的遗传母/代孕母耳标号、进出场移动日期、CPH 编号或迁入/迁出饲养人姓名地址等。")
    f.para("与 §10 关联：§10.13 本地事件日志与「第一版可审计导出」的字段与时限依据。",
           size=8.6, col=INK2, gap=2)

    # [8] HSE livestock
    f.heading("[8] HSE：牲畜作业安全（§10.10 防夹、失电及人工接管）",
              "Livestock  |  hse.gov.uk/agriculture/topics/livestock.htm")
    f.para("处理牲畜始终存在受伤风险（挤压、踢、撞、抵扎）。降低风险需：维护良好的处理设施、适合所处理动物的 race 与 crush、训练有素的员工、对性情恶劣动物的严格淘汰。", gap=3)
    f.subhead("Race（通道）要点")
    f.bullet("动物应能顺利进入（宜有漏斗口），收集栏要有足够空间；圆形收集栏可让工人站在驱赶门后驱赶。")
    f.bullet("动物须能看清通往 crush 及更远；通道可弯曲但避免急转；动物倾向走向亮处。")
    f.bullet("侧板须足够高防跳并牢固固定；覆盖侧板以减少阴影等视觉干扰；控制领头动物等待；铰链/滑动门从工作面操作。")
    f.bullet("绝不允许 race 后方有未固定动物时在 crush 作业。")
    f.subhead("Crush（保定架）要点")
    f.bullet("应能安全完成多数常规操作（含口服治疗、打耳标、后部作业），宜有锁定式前门与自锁 yoke。")
    f.para("与 §10 关联：§10.10「人员可在栏外释放牛只/接管」，以及「防夹由机械防护 + 经验证的受阻响应构成、超声绝不单独作为防夹」的安全依据。",
           size=8.6, col=INK2, gap=2)

    # [9] welfare code
    f.heading("[9] Defra：牛只福利操作准则（§10.2 机械结构与福利）",
              "Code of recommendations for the welfare of livestock: cattle  |  gov.uk，更新于 2024-01-25（56 页，摘译相关部分）")
    f.subhead("处理（准则 §14-16）")
    f.bullet("牛应按自身节奏移动，不得催促；尤其在拐角和湿滑处轻柔引导；避免过多噪音、兴奋或武力。")
    f.bullet("不得对头、乳房等敏感部位施压或击打；引导工具不得有尖锐末端；尽量避免对成年牛使用电驱赶棒。")
    f.bullet("定期评估驱赶道路状况；混凝土地面与人行道须防滑，且不对牛蹄造成过大压力或过度磨损。")
    f.bullet("所有饲养员应能使用大小合适、高效的处理栏；保持 pens / races / crushes / floors 良好、无可能伤牛的尖锐边缘或突出物；race 宜缓弯而非直角。")
    f.subhead("设施（Accommodation）")
    f.bullet("建材须无害且可清洗消毒；圈舍与固定装置不得有可能致伤的尖锐边缘或突出物。")
    f.bullet("动物须随时可到干燥垫料或排水良好的躺卧区；不得以造成不必要痛苦的方式限制动物活动。")
    f.para("与 §10 关联：§10.2「防滑排水、无尖锐突出物、门轨铰链防护、缓弯边界、围栏外操作位置」等福利结构设计的官方依据（[9]）。",
           size=8.6, col=INK2, gap=2)

    # [15] Banner
    f.heading("[15] Banner Engineering：超声波传感器 101（§10.4 超声布置及判定）",
              "Ultrasonic Sensors 101: Answers to Your Frequently Asked Questions  |  bannerengineering.com")
    f.bullet("超声波传感器产生 >20 kHz 超高频声波（超出人耳范围），由电能驱动陶瓷换能器发射并接收声波。")
    f.bullet("测距原理：换能器受电振动，压缩/膨胀空气形成波传向目标；发射声波后「监听」反射回波，据此测距或检测目标有无。")
    f.bullet("用声而非光，可在光电传感器不适用的场合工作；目标颜色/反射率不影响，适用于高眩光、透明物检测与液位测量。")
    f.bullet("与光学/雷达相比：对透明物、液位、高反光/金属表面有优势，潮湿环境亦可用；但对温度波动和风敏感（雷达不受影响）。")
    f.bullet("噪声与干扰：与传感器同频的声噪（哨声、压缩气/气动嘶嘶声）会干扰输出；两只同频传感器靠近会产生声串扰；电磁设备振动也可能被电学器件拾取。")
    f.para("与 §10 关联：§10.4 超声「测距判占位、无回波/陈旧/故障即 uncertain」的传感器原理背景。",
           size=8.6, col=INK2, gap=2)

    # [16] P+F
    f.heading("[16] Pepperl+Fuchs：超声波传感器同步与共模 FAQ（§10.4）",
              "Ultrasonic Sensor FAQ: Synchronization and Common Mode  |  blog.pepperl-fuchs.com，2019")
    f.bullet("主题：当无法保证传感器间最小安装距离时的同步（Synchronization）与共模（Common Mode），用于抑制串扰与切换故障。")
    f.bullet("同步输入开路时传感器为正常模式；外部触发（施加规定电位 L+/L-）可禁用/再启用；阻塞期间不发射超声脉冲，输出「冻结」，释放后至少一个测量周期才更新输出。")
    f.bullet("可用于外部同步或复用模式（由外部时钟发生器触发各传感器），以缩小最小安装距离、防止相互串扰造成的误切换。")
    f.para("与 §10 关联：§10.4「评估厂商支持的错时发射（time-shifted transmission）以限制串扰 [16]」——即本 FAQ 主题。",
           size=8.6, col=INK2, gap=4)

    # references
    f.heading("参考文献", "编号沿用报告第 13 节；均为网络来源")
    for line in [
        "[1] Defra, \"Livestock Information Transformation Programme,\" updated 23 Jul. 2026. [Online]. Available: https://www.gov.uk/government/publications/livestock-information-transformation-programme-litp/livestock-information-transformation-programme-litp",
        "[3] BCMS and RPA, \"Get new or replacement official ear tags for cattle,\" updated 8 Nov. 2022. [Online]. Available: https://www.gov.uk/guidance/get-new-or-replacement-official-ear-tags-for-cattle",
        "[4] BCMS and RPA, \"Record and report cattle movements,\" updated 8 Nov. 2022. [Online]. Available: https://www.gov.uk/guidance/report-and-record-cattle-movements",
        "[5] BCMS and RPA, \"Keep a holding register for cattle to record births, movements and deaths,\" updated 28 Jun. 2023. [Online]. Available: https://www.gov.uk/guidance/keep-a-holding-register-for-cattle",
        "[8] Health and Safety Executive, \"Livestock.\" [Online]. Available: https://www.hse.gov.uk/agriculture/topics/livestock.htm",
        "[9] Defra, \"Code of recommendations for the welfare of livestock: Cattle,\" updated 25 Jan. 2024. [Online]. Available: https://www.gov.uk/government/publications/code-of-recommendations-for-the-welfare-of-livestock-cattle/code-of-recommendations-for-the-welfare-of-livestock-cattle",
        "[15] Banner Engineering, \"Ultrasonic sensors 101: Answers to your frequently asked questions.\" [Online]. Available: https://www.bannerengineering.com/sg/en/company/expert-insights/ultrasonic-sensors-101.html",
        "[16] Pepperl+Fuchs, \"Ultrasonic sensor FAQ: Synchronization and common mode,\" 2019. [Online]. Available: https://blog.pepperl-fuchs.com/en/2019/ultrasonic-sensor-faq-synchronization-and-common-mode/",
    ]:
        f.para(line, size=7.8, col=INK2, gap=3)
    f.rule(col=LINE, gap=5)
    f.para("本文件为学习/核对用的中文译解。Defra 牛只福利准则原文 56 页，此处仅摘译与 §10.2 相关的处理与设施部分。",
           size=7.8, col=INK3)

    c.save()
    print("saved:", PDF)


if __name__ == "__main__":
    build()

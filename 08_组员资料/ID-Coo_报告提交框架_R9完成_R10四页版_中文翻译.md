# ID-Coo 报告提交框架（中文翻译版）

> **翻译说明**
> - 本文档翻译自团队最新 Word 版《ID-Coo_报告提交框架_EN_R9完成_R10四页版.docx》（2026-10-17 修复版：图1 已按 drawio 源重建、VPC 图已缩至版心宽、误删的参考文献 [19]–[22] 已恢复），**仅供中文审阅**；提交 Cadmus 的正式文本以英文版为准。
> - 本版特点：**§9 已由组员4 补全**为叙述体十条 Must have 需求；**§10 为修订后叙述体**（原状态机/接口/分流决策/验证阶段四张表已并入行文，文中不再有表格）；图1 为重建版（含"单独人工处理出口"标注），图中文字保留英文。
> - 参考文献为 26 条重编号版（如 [4]=XRP2 指南、[18]=CIGR、[20]=Defra 福利准则、[24]=ISO 13849-1、[26]=BCMS 场所登记册），与我方早期 R10 终稿旧编号（[11][12][25] 等）不同，拼稿时须统一。
> - 空白填写页在原文中为留白页，本文以"（留白页）"标注。

---

## 原创性声明表（Declaration of Originality）

【插入学校自有页眉】

**原创性声明表**

本表必须填写并签名，随所有作业一并提交。
请用大写字母（BLOCK CAPITALS）填写以下信息。

- 姓名：……………………………………………………………………………………
- 学号：………………………………………………………………………………………
- 课程名称：…………………………………………………………………………………
- 作业编号/名称：…………………………………………………………………………

本表末尾附有《格拉斯哥大学剽窃与学术诚信准则》的链接。请仔细阅读该准则，**然后**阅读并签署下面的声明。

**我确认本作业为本人独立完成，并且我已：**

- ☐ 阅读并理解《学生手册》中的剽窃指导，包括《格拉斯哥大学剽窃与学术诚信准则》
- ☐ 阅读并理解关于生成式人工智能（AI）的指导，包括：i. 学校提供的；ii. 学院提供的；iii. 与本项考核具体相关的
- ☐ 已在正文和参考文献中清楚标注本作品使用的所有来源
- ☐ 对所有引自书籍、期刊及网络来源的文字，已按学院接受的引用格式完整标注（含页码）并使用引号
- ☐ 已为所有非本人完成的表格、图、图例、数据和代码提供来源
- ☐ 已确保未经 acknowledgement 未使用本人过去或现在的任何作品、或任何其他学生的作品，包括此前或同时在本人所在或任何其他教育机构（含中学）提交过评估的作品
- ☐ 未寻求或使用任何外部机构的付费服务，包括查重机构或校对服务
- ☐ 未使用任何生成考核内容的网站或软件而未明确声明
- ☐ 已确保：若本项考核允许使用生成式 AI，我已清楚声明其使用，注明所使用的具体工具（如 ChatGPT、Copilot、Bard、DeepSeek）及使用方式
- ☐ 此外，我理解任何与此作品相关的虚假声明都将导致按大学规章启动行为处理程序

**声明：**
我知悉并理解大学的剽窃与学术诚信政策；我声明本作业为本人独立完成（已在文中以引用注明者除外），且我已遵循上述良好学术实践。

签名：……………………………………………………………………………………

## 格拉斯哥大学剽窃与学术诚信准则

《格拉斯哥大学剽窃与学术诚信准则》载于大学规章：
https://www.gla.ac.uk/myglasgow/apg/policies/uniregs/regulations2025-26/feesandgeneral/studentsupportandconductmatters/reg32/

如仍不确定何为剽窃，或需要关于如何避免剽窃的建议——**立即求助！**
可联系以下任一人员寻求帮助：授课讲师 / 课程负责人 / 论文导师 / 学习顾问 / 学生学习发展服务部。
另请阅读课程或项目手册中关于良好学术实践的建议。

## 贡献声明（Declaration of Contribution）

请将本段替换为你们的贡献声明：

> "声明团队成员各自贡献了什么，以及任务分工中是否出现问题。以不正当方式覆盖本声明而未作贡献的成员将被扣分，其他成员的分数将相应上调。若无明显问题，则全组成员获得相同分数。为此需要进行单独评估：你和团队成员须评估自己的作品并互相评估队友。反思质量也将纳入评估。"

---

## 1. 确定 EID 的限制条件及与 LIS 相关的法规（半页）

【模板要求】需要查阅政府文档和农业杂志以获取参考文献，获得必要的背景知识。

正文（组员1 已完成）：

根据环境、食品与农村事务部（Defra）的说明，低频（LF）电子识别（EID）预计将于 2027 年作为英格兰新牛只 traceability 服务的一部分引入。现有牛只追踪系统（CTS）将运行至 EID 全面实施 [1]。按已公布的计划，2027 年起出生的犊牛须佩戴 LF 电子识别标签。这些标签可在移动过程中通过扫描识别牛只，无需人工读取并输入标签编号。EID 耳标提供的更强 traceability 将增强英国预防、发现和应对动物疾病暴发的能力，从而保护农户和农村经济 [2]。

EID 有四个主要限制。第一，耳标可能丢失或变得无法读取 [3]。第二，附近的金属杆或管道可能影响天线性能，且读区每次只应容纳一头牛，以便编号能被可靠归属 [4]。第三，LF 技术读取范围有限，读卡器的位置可能影响识别性能 [4]。最后，苏格兰的一个耳标研究项目指出耳标撕裂是潜在的动物福利问题 [5]。

关于与 LIS 相关的法规，现行规定要求：发现官方耳标丢失或损坏后，须在 28 天内订购并佩戴替换标签；在佩戴替换标签前，受影响牛只须留在原场所 [6]。农户还须保存其所照料牛只的相关记录，包括耳标信息、出生登记和牛只护照 [7]。牛只迁入或迁出场所的任何移动，须在三天内向英国牛只移动服务局（BCMS）报告 [8]。这些要求确保牛只身份、来源和生平历史有据可查，为 traceability 记录管理提供必要信息。

## 2. 农场环境中奶牛误识别的后果（半页）

【模板要求】需要理解牛只需要识别的深层原因，以及识别如何在日常基础上影响农场运营、个体奶牛、LIS 系统和牛奶收购方信息。

正文（组员1 已完成）：

准确的识别将每头奶牛与其生产、健康和治疗记录关联，为日常管理和可靠的 traceability 提供基础。反之，奶牛的误识别会导致管理错误和不准确的 traceability 信息。

首先，如果产奶量记录到了错误的牛上，饲料分配和生产性能监测就变得不可靠。农户可能给一头牛过量饲喂，却忽视另一头牛的营养需求，导致营养摄入过量、饲料浪费和生产效率下降。AHDB 强调，个体产奶量记录对于准确实施"以产定饲"策略至关重要 [9]。此外，识别错误可能导致员工治疗了错误的动物，同时延误了对受影响牛只的照料。更严重的是，识别错误可能使处于抗生素休药期的奶牛的牛奶进入贮奶罐。如果该批次未通过残留检测，则无法销售，可能需要销毁 [10]。不准确的治疗记录还会降低向牛奶收购方所提供信息的可靠性，阻碍受污染批次的调查，并可能扰乱生产者与收购方之间的牛奶供应安排 [10]。

错误的移动记录——例如将 A 牛的移动记录在 B 牛的识别编号下——会损害牛群移动信息的准确性。此类错误还可能误导疾病调查：现行 CTS 保存法定的牛只移动记录，而规划中的 LIS 服务旨在改善牛结核病控制可获得的数据 [11]。Defra 计划将法定的牛只出生、移动和死亡记录存入支持新 LIS 牛只服务的未来中央数据库，进一步说明准确牛只识别的重要性 [12]。

因此，农户应保存准确、真实的牛只记录，并核验任何不确定的身份，以确保国家 traceability 数据的可靠性。

## 3. 构思方案（A3 纸照片或 murals 生成——须清晰可读）

【模板要求】回答关于该创意的下列问题（拍摄 A3 纸照片或用 murals 生成——须清晰可读）。

（本节在英文版中为价值主张画布空白模板图 + 留白填写页。以下为模板图：空白价值主张画布，Strategyzer 格式，含"价值主张/客户细分"两栏与"产品与服务、收益创造、痛点缓解、客户任务、收益、痛点"六区。）

## 4. 识别团队成员与差异化因素（≤1 页）

【模板要求】从该分析中，逐一确定你们公司/产品与所选竞争者之间的 parity 点和 difference 点。

（留白页，待组员2 填写。）

## 5. 竞争分析深入（≤2 页）

【模板要求】从该分析出发，进行波特五力、SWOT、PESTEL 分析。至少选择 2 种技术分析你们产品/服务组合的背景。无需展示模板图，直接用工具过一遍分析。从分析中确定你们的产品/服务组合必须具备哪些理想属性以满足客户，以及区别于竞争的差异化因素。

（留白页，待组员2 填写。）

## 6. 产品/服务分析与竞争——独特卖点（1 句话）

【模板要求】你们解决方案的独特卖点是什么？基于分析，哪些信息对你们客户群体最重要？

（留白页，待组员2 填写。）

## 7. 填写商业模式画布（A3 纸或 murals 生成——须清晰可读）

【模板要求】填写商业模式画布。

（本节在英文版中为空白商业模式画布模板图 + 留白填写页。）

## 8. 批判性分析（≤1 页）

正文（组员3 已完成）：

### 8.1 市场规模

目标客户是拥有现有处理通道、电子耳标且确有核验负担的英格兰北部奶牛场。AHDB 的 6,850 家英国奶牛生产者 [13] 和 Defra 的 184.9 万头英国奶牛 [14] 均未直接给出英格兰北部的农场数量。

本报告因此根据 Defra 2024 年区域概况 [15] 估算：总农场数（农业面积 ÷ 平均农场规模，表 1.1）乘以奶牛养殖场占比（图 1.7），得西北约 1,240 家、约克郡-亨伯约 406 家、东北约 63 家，合计约 1,700 家。这是基于官方数据的估算而非公布数字，存在不确定性。

### 8.2 可服务份额与销售目标

按筛选条件（现有通道、耳标、核验负担高）假设 40% 可服务，得可服务市场（SAM）约 680 家。40% 为情景假设，尚未经客户调查验证。三年销售 50 台约相当于 TAM 的 2.9%、SAM 的 7.4%——这是销售目标，不是市场预测。

### 8.3 理想属性与客户需求的匹配

竞争分析（R5）得出六项理想属性，每项均有技术依据并对应一项客户需求：

- **可靠的属性归属**（机械分隔 + 超声占位感知 + LF RFID）——解决漏读、双读和转录错误
- **清晰的异常分类**（双出口条件分流 + 事件记录）——解决异常牛难以重新定位的问题
- **安全处理**（栏边操作 + 安全控制）——实现围栏外的安全操作
- **本地运行**——应对网络中断，保存记录
- **易于维护**——缓解维护成本不确定性
- **可量化的收益**——使投资可对照经济回报核验

前两项属性对应题目核心失效模式（一次读到两个编号；完全漏读），构成价值主张的技术基础。

### 8.4 客户—产品匹配与必要调整

该细分市场与产品的能力边界相匹配——ID-Coo 依赖现有通道、耳标和核验负担——因此筛选条件反映真实匹配而非随意选择；小型牛群、异常率极低的农场或已有成熟系统的农场被排除。

仍有一处实施调整：逐头隔离可能成为吞吐瓶颈，且首次安全分隔未经验证，因此第一版采用人工确认单头进牛，验证通过后才自动化。这限制了交付节奏，但不改变价值主张。总体而言，商业可行性取决于验证安全分隔、RFID 归属、出口一致性和净收益。

## 9. 用户需求及其论证（≤1 页）

【模板要求】用你们的产品/服务组合创意，写下产品需要做的一切。用户需求定义解决问题所需的内容。在此阶段，用户需求概述产品需要做什么，而不是问题将如何解决（最多 10 条需求）。论证其背后的理由。本练习确保所有用户需求都与开篇定义的问题对齐。逐条论证所识别用户需求的必要性及其如何帮助解决问题。使用 MOSCOW 分析框架，确保全部 10 条需求均为 must have。

正文（组员4 已完成，叙述体）：

第 8 节确定了客户需要的属性：可靠的属性归属、清晰的异常处理结果、安全处理、本地连续性、可维护性和可衡量的价值。以下十条用户需求说明产品/服务必须达成的结果，均为 MoSCoW 框架下的 Must have。第 10 节描述所提出的设计。

**UR1**：当存在有效的电子标识时，系统必须将每次通行关联到正确的牛。错误的身份会破坏治疗记录和牛群记录，因此可靠的属性归属对于第 2 节所定义的问题至关重要。

**UR2**：对无法确认的身份，系统必须保持其未解决状态，并提供给人员进行安全复核，复核无法继续时暂停进牛。耳标可能丢失或无法读取 [3]、[6]；猜测身份会重蹈原始记录错误。

**UR3**：系统不得将同时通过或紧密跟进的牛记录为一头已确认的牛。否则相邻牛只的标识可能被归属到错误的牛上，削弱第 8 节所要求的身份保障。

**UR4**：人员必须能够在不进入牛只通道的情况下操作、停止并接管流程。牛只处理存在受伤风险 [25]，因此日常使用需要外部操控。

**UR5**：系统必须确认实际采取的出口，并把每次通行闭合为一个完整、真实的事件记录。延迟的读数或错误的路线不得留下看似完整但虚假的记录。

**UR6**：服务必须在网络中断期间继续基本的身份核验，并保存通行与异常记录。农场处理不能依赖持续联网，丢失记录将导致日后无法复核。

**UR7**：服务必须提供可审计的身份、时间、异常和路线记录，同时区分内部通行与须申报的牛只移动。农户需要可用的证据，而不把场内分流误认为法定移动 [8]、[26]。

**UR8**：服务必须在试点中于 90 分钟内处理 200 头牛，包括重复读取和复核，且不造成过度排队。否则核验会延误正常处理；第 8 节已指出逐头处理可能是瓶颈。

**UR9**：系统必须在常规清洁后保持可靠，并能在潮湿、污秽的农场条件下识别和排除故障而不长时间停机。频繁中断将使日常使用不切实际。

**UR10**：安装的产品和持续服务必须相对于总拥有成本提供可衡量的净收益。如第 8 节所述，农场需要通过实际劳动节省和运营成本来证明投资的合理性。

## 10. 提供解决方案的技术描述（≤4 页）

【模板要求】例如传感器布置、数据汇聚、功能框图、软件描述、接口和定价，提交给直属主管。

正文（组员4 修订版，叙述体；图中文字为英文）：

### 10.1 物理结构

ID-Coo 采用单列通道：等待区 → 门 G0 → 缓冲段 A → 门 G1 → 检测段 B → 门 G2。随后分流门 D 将牛导向两个去向之一——返回牛群，或经围栏门 H 进入待复核围栏（图 1）。两个出口均朝前；D 只作引导，不推挤牛身。

第一版设一个缓冲段和一个检测段。增加上游段只会增加等待空间、不会提高"读取—分流"循环的速度，反而增加门与故障点。宽约 526–800 毫米的可调通道（8 英尺与 10 英尺模块）指示结构包络 [16]、[17]。防倒退挡杆可能有助于控制倒退，但不能代替分隔门。

CIGR 给出 650–749 kg 荷斯坦-弗里斯兰奶牛的薯甲高 1.44 m、体长 1.75 m、胸宽 0.60 m [18]。一项 1,054 头牛的实地研究报告平均薯甲高 1.411 m、躯干长 1.708 m [19]。这些数据用于确定段长、净宽与天线高度。最终尺寸与门的活动范围须经现场勘测确认；标准模块不一定能容纳一头牛。其他品种须重新进行尺寸核查。

通道须满足防滑排水、无尖锐突出物、门轨与铰链有防护、头腿间隙安全、出口边界连续 [20]。人员从栏外操作；头部固定为可选项。（UR4、UR8、UR9）

待复核围栏暂存待人工核验身份的牛，不用于疾病隔离。须设防返回入口、独立处理出口与栏外操作空间。门 H 只能在牛完全通过后关闭。围栏满员或支路堵塞时停止送牛。

容量按 C ≥ λq × th + Cm（异常率 × 处理间隔 + 余量）规划。由于这是平均负荷关系，围栏还须设满员监测。预算情景假设复用可容纳约 6 头牛的既有围栏。CIGR 一般建议容量按挤奶厅一侧配置，但挤奶厅出口处的分流除外。饲养围栏应提供饮水、饲料与躺卧空间 [18]；容量与设施须经现场勘测确认。

**图 1 — 通道与分流功能布局图**（2026-10-17 重建版：补回了"单独人工处理出口"标注与通道标签；drawio 源已同步）

### 10.2 感知设备与能力边界

LF RFID 读卡器按 ISO 11784/11785（HDX 与 FDX-B）扫描已佩戴 LF EID 标签的牛。未佩戴 LF EID 标签的牛须走人工身份核验或替代流程；单次未读到不能诊断为标签损坏 [1]。Tru-Test XRP2/XRP2i 为功能参考；最终读卡器及 B 段头耳通过区外侧的天线位置取决于现场勘测 [4]、[21]。

六个规划中的超声测点（U-A、U-IN、U-B1、U-B2、U-N、U-Q）监测占位与通行；U-B1/U-B2 优先评估顶部向下安装。距离 d = c × Δt / 2 与空通道基准比较。每个测点报告*空*、*占用*或*不确定*。无回波、数据过期或故障均意味着*不确定*；一个回波不能证明只有一头牛 [22]。将评估厂家支持的错时发射以抑制串扰 [23]。六个测点为暂定配置；入口或分流处的盲区须增加覆盖。

即使 B 段只有一头牛，天线也可能读到相邻标签。因此试验必须确立读取归属，而非从"门已关闭"推断（见 10.7）。外壳破裂但仍可读的耳标、缺失的非电子耳标，仍需人工目检。（UR1–UR3、UR9）

### 10.3 控制硬件、电气与安全

图 2 展示功能接口，不是施工布线。电压、驱动额定值、电缆保护与接地取决于所选设备与现场。PLC 直接向门驱动发送动作请求；独立的安全相关控制监视经风险评估选定的保护装置，可独立停止或抑制驱动；软件与数据接口不能绕过它。现场选定的机箱、连接器与电缆须能承受冲洗、侵入与腐蚀；常规清洁后须检查运行情况。（UR9）

安全功能与所需性能等级按现场风险评估、参照 ISO 13849-1 确定 [24]；不声称已达到任何等级。机械防护与经验证的受阻响应保护门动作。超声测点单独不能提供防夹保护。

失电时停止危险运动，每个门保持确定状态；短时后备电源保存事件并发出故障信号。人员可在栏外释放牛只。重启时控制器先核验门位与占位，而不是接续被打断的动作。培训与检查遵循 HSE 指导 [25]。（UR4、UR5）

**图 2 — 控制、安全与数据功能接口图**

### 10.4 控制算法与分流逻辑

规则状态机将每次通行作为独立事件处理；第一版不需要机器学习。人员确认 A 段只有一头牛后，控制器将其放入 B 段、读取耳标、设置出口并确认实际路线。

过程联锁防止 G0/G1 与 G1/G2 同时打开。扫描要求 B 段两个门均关闭、牛在读区且无疑似跟入。D 必须在 G2 打开前到位，且在其运动范围被占用时不能切换。传感器与门位反馈确认出口；单靠定时器不行。

延迟的读数保留在其原事件中，不能改变下一头牛的流向。过程联锁不能证明首次进牛安全，因此第一版保留人员确认，并将该时间计入经济测算。自动进牛须先验证分隔、防夹保护与异常处理。

未读到的牛在 B 段内仍保留事件编号。机械状态不确定时停止自动分流；连续无读数会触发读卡器诊断，以免整群牛被错误分流。（UR1–UR5）

### 10.5 数据、软件与农场主界面

每个事件记录其编号、时间、占位与门位状态、原始与去重读数、设备状态、判定原因、计划与实际出口、操作人员及修改历史。

事件编号与官方身份保持分离。若未读到标签，身份栏保持空白直至人员核验；原始异常与后续关联保持可审计。若官方可视标识也不足，人员按官方程序处理，而不是编造编号。

农场主界面区分"电子核验通过、身份待复核、设备/通道故障、人工已处理"四种状态；显示当前事件、围栏负荷、未处理个案与维护记录，人工操作受权限控制。读卡器故障绝不显示为"耳标损坏"诊断。（UR5–UR7）

### 10.6 LIS 与农场软件接口

第一版在本地保存记录并导出以供审计；不假定直接接入 LIS。若将来获得规范与授权，适配层将区分内部通行与须申报的移动、校验字段、保存提交与回执、防止重复，并在中断后核对恢复 [1]、[8]、[26]。

界面显示"本地已保存、待处理、失败、已确认回执"四种状态。官方身份变更与法定申报须人工批准。（UR6、UR7）

### 10.7 定价、吞吐量与验证

规划含安装价格为 £18,500（不含增值税与重大土建），加 £720/年服务费与假设的 £60/年电费（见第 12 节）。该价格假设复用现有通道与待复核围栏，同时覆盖传感器、门与安全设备。回收期按最终报价、服务与能源成本及实测净劳动节省重新计算。（UR10）

目标吞吐为 150 头/小时（每头牛约 24 秒，含进入、门动作、读取与处理）。试验要求 200 头牛 90 分钟内完成（约 133 头/小时），含重试与复核。若未达标，调整地点或流程；安全检查不打折。（UR8、UR10）

试验对照暂定目标 ≥99.5% 报告已确认读数正确率，并单独报告覆盖率，以及误分流、异常、实际与计划出口、接管次数与净劳动时间。同一牛群的重复通行不构成独立样本；零观测错误不等于零风险。安全分隔、读取归属与释放先于经济性验证。（UR1–UR10）

## 11. 可持续发展（半页）

【模板要求】讨论你们的设计如何与乳业路线图对齐，说明解决方案如何实现可持续性：https://www.dairyuk.org/wp-content/uploads/2021/11/Dairy-Roadmap-Climate-Ambition-Final-Version.pdf。提供与设计一致的技术细节，并对照所述原则批判性评估你们设计的适宜性（是否需要修改技术描述以使设计与可持续发展路线图对齐）。

（留白页，待组员5 填写。）

## 12. 可负担性（半页）

【模板要求】论证你们产品/服务组合的安装费用与经常性服务费是多少。这是否与你们客户的财务能力相符？论证你们的答案。

（留白页，待组员5 填写。）

## 参考文献（26 条）

[1] Department for Environment, Food and Rural Affairs（英国环境、食品与农村事务部），"Livestock Information Transformation Programme (LITP)（牲畜信息转型计划）"，GOV.UK，2026-07-23。[在线] https://www.gov.uk/government/publications/livestock-information-transformation-programme-litp/livestock-information-transformation-programme-litp （访问日期：2026-10-15）

[2] Department for Environment, Food and Rural Affairs，"Electronic ID for cattle mandatory in step forward for UK biosecurity（牛只强制电子 ID：英国生物安全迈出的一步）"，GOV.UK，2025-06-02。[在线] https://www.gov.uk/government/news/electronic-id-for-cattle-mandatory-in-step-forward-for-uk-biosecurity （访问日期：2026-10-15）

[3] A. J. Roberts, L. E. Wallace, M. Harbac, and J. A. Paterson，"Case study: Retention and readability of radio frequency identification transponders in beef cows over a 5-year period（案例研究：肉牛 RFID 应答器 5 年留存率与可读性）"，*The Professional Animal Scientist*，vol. 28, no. 2, pp. 221–226, 2012。[在线] https://www.ars.usda.gov/ARSUserFiles/30300000/PAS%202012%2028%20221-226.pdf （访问日期：2026-10-15）

[4] Datamars Limited，*XRP2 Panel Reader and Antenna Quickstart Guide*（XRP2 面板式读卡器与天线快速入门指南），n.d.[在线] https://us.tru-test.com/resources/xrp2-panel-reader-quickstart-guide-enesptfrde （访问日期：2026-10-15）

[5] SEFARI，"Sheep and cattle traceability: The impact of environmental and other factors in Scotland on ear tag loss（苏格兰羊牛 traceability：环境及其他因素对耳标丢失的影响）"，研究项目，n.d.[在线] https://sefari.scot/research/projects/sheep-and-cattle-traceability-the-impact-of-environmental-other-factors-in （访问日期：2026-10-15）

[6] British Cattle Movement Service and Rural Payments Agency（英国牛只移动服务局与农村支付署），"Get new or replacement official ear tags for cattle（为牛只申领新官方耳标或替换耳标）"，GOV.UK，2022-11-08。[在线] https://www.gov.uk/guidance/get-new-or-replacement-official-ear-tags-for-cattle （访问日期：2026-10-15）

[7] *The Cattle Identification Regulations 2007*（2007 年牛只识别条例），S.I. 2007/529，英国。[在线] https://www.legislation.gov.uk/uksi/2007/529/contents （访问日期：2026-10-15）

[8] British Cattle Movement Service and Rural Payments Agency，"Record and report cattle movements（记录并报告牛只移动）"，GOV.UK，n.d.[在线] https://www.gov.uk/guidance/report-and-record-cattle-movements （访问日期：2026-10-15）

[9] Agriculture and Horticulture Development Board（英国农业与园艺发展委员会），"How to monitor the performance of a dairy diet（如何监测奶牛日粮表现）"，AHDB，n.d.[在线] https://ahdb.org.uk/knowledge-library/how-to-monitor-the-performance-of-a-dairy-diet （访问日期：2026-10-15）

[10] Food Standards Agency（英国食品标准局），"Information and guidance on the testing of milk for antibiotic residues（牛奶抗生素残留检测信息与指导）"，GOV.UK，2018-01-26。[在线] https://www.gov.uk/government/publications/milk-hygiene-and-antibiotic-residues/information-and-guidance-on-the-testing-of-milk-for-antibiotic-residues （访问日期：2026-10-15）

[11] C. Godfray, G. Hewinson, B. Silverman, M. Winter, and J. Wood, *Bovine TB Strategy Review Update*（牛结核病战略评审更新），Department for Environment, Food and Rural Affairs, 2025。[在线] https://assets.publishing.service.gov.uk/media/68d563169ce370a7e0a0fcfe/Godfray_bTB_Evidence_Review_Update_2025.pdf （访问日期：2026-10-15）

[12] Department for Environment, Food and Rural Affairs，"Changes to bovine identification, registration and movement in England: Summary of responses and government response（英格兰牛只识别、登记与移动变更：回应摘要与政府回应）"，GOV.UK，n.d.[在线] https://www.gov.uk/government/consultations/changes-to-bovine-identification-registration-and-movement-in-england/outcome/summary-of-responses-and-government-response （访问日期：2026-10-15）

[13] Agriculture and Horticulture Development Board，"GB producer numbers（英国生产者数量）"，AHDB，2026-06-11。[在线] https://ahdb.org.uk/dairy/gb-producer-numbers （访问日期：2026-10-15）

[14] Department for Environment, Food and Rural Affairs，"Livestock populations in the United Kingdom at 1 June 2025（2025 年 6 月 1 日英国牲畜存栏）"，GOV.UK, 2025。[在线] https://www.gov.uk/government/statistics/livestock-populations-in-the-united-kingdom/livestock-populations-in-the-united-kingdom-at-1-june-2025 （访问日期：2026-10-15）

[15] Department for Environment, Food and Rural Affairs，"Agricultural facts: England regional profiles（农业事实：英格兰区域概况）"，GOV.UK，2025-10-30。[在线] https://www.gov.uk/government/statistics/agricultural-facts-england-regional-profiles （访问日期：2026-10-15）

[16] Arrowquip，"Easy Flow Elite adjustable cattle alley（Easy Flow Elite 可调牛只通道）"，n.d.[在线] https://arrowquip.com/cattle-equipment/cattle-alleys/easy-flow-alley （访问日期：2026-10-15）

[17] Arrowquip UK，"Cattle sorting race（牛只分流通道）"，n.d.[在线] https://arrowquip.co.uk/cattle-equipment/cattle-races/cattle-sorting-races/ （访问日期：2026-10-15）

[18] CIGR Section II Working Group No. 14, *The Design of Dairy Cow and Replacement Heifer Housing*（奶牛与后备母牛舍设计），2014。[在线] https://amsacta.unibo.it/4272/1/Dairy_Housing_report_2015.pdf （访问日期：2026-10-15）

[19] J. O. L. Cerqueira, J. P. P. Araújo, P. S. Vaz, J. Cantalapiedra, I. Blanco-Penedo, and J. J. R. Niza-Ribeiro，"Relationship between zoometric measurements in Holstein-Friesian cow and cubicle size in dairy farms（荷斯坦-弗里斯兰牛体尺与奶牛场卧栏尺寸的关系）"，*International Journal of Morphology*，vol. 31, no. 1, pp. 55–63, 2013, doi: 10.4067/S0717-95022013000100008.

[20] Department for Environment, Food and Rural Affairs，"Code of recommendations for the welfare of livestock: Cattle（牲畜福利建议准则：牛）"，GOV.UK，2024-01-25。[在线] https://www.gov.uk/government/publications/code-of-recommendations-for-the-welfare-of-livestock-cattle/code-of-recommendations-for-the-welfare-of-livestock-cattle （访问日期：2026-10-15）

[21] Tru-Test Datamars，"XRP2 panel reader and antenna（XRP2 面板式读卡器与天线）"，n.d.[在线] https://us.tru-test.com/products/eid/xrp2-panel-reader-and-antennas （访问日期：2026-10-15）

[22] Banner Engineering，"Ultrasonic sensors 101: Answers to your frequently asked questions（超声传感器 101：常见问题解答）"，n.d.[在线] https://www.bannerengineering.com/sg/en/company/expert-insights/ultrasonic-sensors-101.html （访问日期：2026-10-15）

[23] Pepperl+Fuchs，"Ultrasonic sensor FAQ: Synchronization and common mode（超声传感器常见问题：同步与共模）"，2019-01-02。[在线] https://blog.pepperl-fuchs.com/en/2019/ultrasonic-sensor-faq-synchronization-and-common-mode/ （访问日期：2026-10-15）

[24] International Organization for Standardization（国际标准化组织），"Safety of machinery—Safety-related parts of control systems—Part 1: General principles for design（机械安全——控制系统安全相关部件——第 1 部分：设计通用准则）"，ISO 13849-1:2023, 2023。[在线] https://www.iso.org/standard/73481.html （访问日期：2026-10-15）

[25] Health and Safety Executive（英国健康与安全执行局），"Livestock（牲畜）"，n.d.[在线] https://www.hse.gov.uk/agriculture/topics/livestock.htm （访问日期：2026-10-15）

[26] British Cattle Movement Service and Rural Payments Agency，"Keep a holding register for cattle to record births, movements and deaths（为牛只保存场所登记册以记录出生、移动与死亡）"，GOV.UK，2023-06-28。[在线] https://www.gov.uk/guidance/keep-a-holding-register-for-cattle （访问日期：2026-10-15）

# 01 · 需求 / 活 PRD 〔本项目活记忆 · AI 维护〕

> **作用**:这是本项目唯一的需求文档。所有新功能、缺陷、技术债都追加到这里,不要另起多个 PRD 文件。
> **更新时机**:每次有新需求、需求变更、验收标准变化时更新。

---

## 1. 需求来源

| 类型 | 来源 | 进入方式 |
|---|---|---|
| 功能需求 Feature | 用户 / 老师 / 产品 / 客户 | 写成用户故事 |
| 缺陷 Bug | 测试 / 线上日志 / 用户反馈 | 写复现步骤和期望结果 |
| 技术债 Tech Debt | 开发 / Review / CI/CD 故障 | 写影响和修复目标 |

---

## 2. Issue 生命周期

| 阶段 | 状态 | 动作 |
|---|---|---|
| 提出 | Open | 写清场景、目标、验收标准 |
| 排期 | Backlog / Todo | 决定优先级和负责人 |
| 开发 | In Progress | 从 main 开 feature 分支 |
| 评审 | In Review | 提 PR,等待 CI 和 Review |
| 合并 | Done | PR 合并 main,自动关闭 Issue |
| 验收 | Verified | 按验收标准确认 |

**追踪规则**:分支名带 Issue 号,PR 描述写 `closes #<编号>`。

---

## 3. 用户故事模板

```text
### US-<编号> <一句话标题> · 状态: Backlog
作为 <角色>,
我想要 <能力>,
以便 <价值>。

验收标准:
- AC1: Given <前提>,When <动作>,Then <可验证结果>。
- AC2: <补充标准>

技术备注:
- <可选:约束、边界、风险>
```

---

## 4. 需求清单

### US-1 初始化项目工程化与 CI/CD · 状态: Backlog

作为 **项目开发者**,
我想要 项目具备基础工程结构、测试、CI 与 CD,
以便 后续每次开发都能自动检查并自动部署。

验收标准:
- AC1: 从 `main` 开 feature 分支完成初始化,不直接 push main。
- AC2: PR 触发 CI,至少包含格式检查、静态检查、单元测试、构建检查。
- AC3: CI 全绿后合并 main。
- AC4: 合并 main 自动触发 CD,部署后健康检查通过。
- AC5: 完成后更新 `standards/PROGRESS.md`。

技术备注:
- 仓库名 banksys_lixiaohua,开源仓库。
- CD 需 GitHub Secrets:`SSH_PRIVATE_KEY` / `SSH_HOST` / `SSH_USER`,建仓后先配置。

### US-2 数据分析交互页面 · 状态: Backlog

作为 **银行营销分析人员**,
我想要 在 Web 页面上交互式地浏览、筛选并可视化营销数据集,
以便 快速理解客户特征与认购情况的关系,辅助营销决策。

验收标准:
- AC1: Given 打开分析页面,When 页面加载完成,Then 展示数据集概览(行数、列数、目标 `subscribe` 分布)。
- AC2: Given 页面已加载,When 选择某个分类特征(如 `job` / `marital` / `education`),Then 展示该特征的分布图及各取值下的认购率条形图。
- AC3: Given 页面已加载,When 选择某个数值特征(如 `age` / `duration` / `campaign`),Then 展示其直方图,并按认购与否分组对比。
- AC4: Given 页面已加载,When 设置筛选条件(分类多选 + 数值范围),Then 所有图表和统计随筛选联动更新。
- AC5: Given 容器启动,When 访问 `http://localhost:<PORT>`,Then 分析页面可正常打开,无报错。

技术备注:
- 图表用 plotly 或 streamlit 原生组件,统一风格;分析计算写成 `app/core/analysis.py` 纯函数,UI 只做渲染。

### US-3 离线模型训练管线 · 状态: Backlog

作为 **数据科学家**,
我想要 一条可重复的离线训练管线(从 train.csv 训练、评估、输出模型产物与指标),
以便 生产一个可部署的认购预测模型,且结果可复现、效果可验证。

验收标准:
- AC1: Given 执行 `python -m models.train`,Then 训练完成并输出 `models/artifacts/`(模型 + 特征编码器 + `metrics.json`),不报错。
- AC2: Given 固定随机种子,When 同环境重复执行训练,Then 指标与产物可复现(记录种子值)。
- AC3: Given CI 环境,When 运行 `python -m models.train --check-auc`,Then 模型 AUC ≥ 0.80 通过,否则 CI 红灯。
- AC4: Given 训练完成,When 用 test.csv 推理,Then 输出预测结果文件(含 `id` 与认购概率),格式可读。
- AC5: Given 目标列存在类别不平衡,Then 训练配置中明确处理方式(如 `class_weight`),并在指标中同时报告 AUC 与 F1。

技术备注:
- 特征列:age/job/marital/education/default/housing/loan/contact/month/day_of_week/duration/campaign/pdays/previous/poutcome/emp_var_rate/cons_price_index/cons_conf_index/lending_rate3m/nr_employed → `subscribe`。
- 注意 `duration` 与结果强相关(数据泄露风险),是否使用及其理由必须写入训练代码注释与 PROGRESS。
- 测试:训练管线在 CI 用小样本(如 500 行)冒烟验证,保证干净 runner 上可跑。

### US-4 在线预测系统 · 状态: Backlog

作为 **银行营销坐席**,
我想要 在页面上通过点选方式填写客户特征,点击预测后得到「是否认购」的结果与概率,
以便 在联系客户前快速评估认购可能性,优先跟进高潜客户。

验收标准:
- AC1: Given 打开预测页面,When 页面加载完成,Then 展示全部模型特征的点选输入(分类特征用下拉框,数值特征用滑块/数字输入)。
- AC2: Given 已填写特征,When 点击「预测」按钮,Then 展示预测结果(认购/不认购)与认购概率(0~1 百分比)。
- AC3: Given 提交输入,Then 输入经校验(数值范围、必填项),非法输入给出明确提示且不崩溃。
- AC4: Given 模型产物缺失或损坏,When 打开预测页面,Then 显示明确错误提示,应用不崩溃。
- AC5: Given 预测逻辑,Then 核心逻辑为纯函数(`app/core/predictor.py`),有单元测试覆盖。

技术备注:
- 特征输入与训练特征完全一致;测试时用样本数据进行端到端预测验证。

### US-5 容器化与 CD 自动部署 · 状态: Backlog

作为 **项目运维/开发者**,
我想要 应用打包为 Docker 镜像,合并 main 后自动部署到服务器并通过健康检查,
以便 全自动交付一个可通过浏览器访问的线上服务。

验收标准:
- AC1: Given 根目录,When 执行 `docker build`,Then 构建成功,镜像名 `banksys_lixiaohua:latest`。
- AC2: Given 构建成功,When 运行容器,Then 容器内端口固定 8888,`/_stcore/health` 返回 200 且内容为 ok。
- AC3: Given 主机 8888 端口被占用,When 运行部署脚本,Then 自动在 8888~8898 区间回退选空闲端口并打印最终端口。
- AC4: Given 部署脚本,When 重复执行,Then 幂等(先 `docker rm -f banksys_lixiaohua` 停删自身旧容器再起新容器),脚本含 `set -e`。
- AC5: Given CD 触发,When 合并 main,Then 由 GitHub Actions runner 自动部署,仅引用 GitHub Secrets,无硬编码密钥,失败则 Actions 红灯。

技术备注:
- 生产镜像只装运行依赖(requirements.txt),测试/lint 工具只在 CI 安装。
- Dockerfile 支持 `PIP_INDEX_URL` 构建参数,国内服务器可用清华源。

---

## 5. 非功能需求

- **安全**:密钥只进 Secrets,不进 Git。
- **可维护**:一需求一小 PR(尽量 <400 行),避免大爆炸式提交。
- **可测试**:核心逻辑(分析计算、特征编码、预测)必须有单元测试。
- **可部署**:部署后必须有健康检查(`/_stcore/health`)或等价验证。

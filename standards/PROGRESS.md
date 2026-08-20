# PROGRESS · banksys_lixiaohua 〔本项目活记忆 · 状态机〕

> **作用**:这是项目的"存档点"。任意 AI、任意重启会话,读它即可知道当前做到哪、下一步做什么、踩过什么坑。
> **更新时机**:每完成一个有意义步骤、每次会话结束前。
> **格式要求**:时间倒序,最新在上;短、准、可接力。

---

## 当前状态 (最后更新: 2026-08-20 · by AI)

- **阶段**:`初始化(六步流程第③步:feature/1-init 骨架模块完成,本地自检全绿,待确认后推送 PR)`
- **上一步完成**:Secrets 已配齐(gh secret list 核对通过);开分支 `feature/1-init`;完成工程骨架模块:pyproject/requirements 拆分、最小 Streamlit 入口 + core 常量、Dockerfile(8888 + PIP_INDEX_URL + /_stcore/health)、ci.yml、cd.yml(rsync+端口回退+健康检查)、README;本地自检全绿:ruff format/check ✅,pytest 6 passed 覆盖率 94% ✅,冒烟:健康检查 ok、首页 200 ✅。
- **下一步 (TODO 第一条)**:人类确认模块 → 推送分支 → 发 PR(feature/1-init)。
- **阻塞项**:无(等人类确认)。

---

## 待办清单 (TODO,按优先级)

- [x] 读取全部规范(README、00/01/PROGRESS、02~06)与数据样例
- [x] 填写 `00-project-context.md`(项目身份、技术栈、目录地图、质量门槛、部署取值)
- [x] 填写 `01-requirements.md`(US-1~US-5 用户故事 + 验收标准)
- [x] 初始化本文件(第一批 TODO)
- [x] **人类确认 00/01/PROGRESS**(✋ 确认门通过)
- [x] ① 建仓:创建开源仓库 `banksys_lixiaohua`(GuessYouGuess 账号)+ 最小引导提交;提示人类配 Secrets(✋ 确认门 1,进行中)
- [x] ② 从 main 开 feature 分支 `feature/1-init`
- [x] ③ 搭工程骨架:目录结构、requirements(+dev)、Dockerfile、.gitignore、README、ci.yml、cd.yml
- [ ] ③ US-2 数据分析页面:`app/core/analysis.py` + 页面 + 测试
- [ ] ③ US-3 离线训练管线:`models/train.py`(固定种子、class_weight、`--check-auc` 门禁)+ 产物 + 测试
- [ ] ③ US-4 在线预测:`app/core/predictor.py` + 点选表单页面 + 测试
- [x] ④ 本地自检(骨架):ruff 全绿;pytest 6 passed 覆盖 94%;冒烟健康检查 ok
- [ ] ⑤ 推送分支 + AI 发 PR + CI 复检(docker build 在 CI)
- [ ] ⑥ 人工 Review → 人类合并 → CD 自动部署 → 健康检查 → 报端口
- [ ] 会话结束前更新本文件

---

## 关键决策记录 (ADR)

| 日期 | 决策 | 理由 |
|---|---|---|
| 2026-08-20 | 端口:容器内固定 8888,主机 8888~8898 区间回退 | 05 规范:容器内端口固定、主机端口自动找空闲 |
| 2026-08-20 | 健康检查用 Streamlit 自带 `/_stcore/health`(返回 ok) | 无需额外端点,curl 可直接验证 |
| 2026-08-20 | 数据 `data/*.csv`(公开教学数据 ~3.7MB)与模型产物 `models/artifacts/` 进 Git | 公开数据可入库,保证 CI/服务器可复现;产物超 20MB 再改方案 |
| 2026-08-20 | 数据泄露:预测页面不提供 `duration` 输入,模型特征中是否含 `duration` 由训练时定并写明理由 | `duration` 与结果强相关,营销场景事前不可知 |
| 2026-08-20 | 模型门禁 AUC ≥ 0.80,CI 用 `python -m models.train --check-auc`;CI 冒烟用小样本 | 数据/ML 项目特有门禁,见 03 标准第 5 节 |

---

## 已知坑 (GOTCHAS)

- 暂无真实故障。预判:Windows 控制台编码、CI 干净 runner 上数据路径、docker 端口占用(exit 125)——见 05 标准第 7 节。

---

## 里程碑 (DONE)

- [x] 项目三文档(00/01/PROGRESS)完成,待人类确认

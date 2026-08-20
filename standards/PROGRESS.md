# PROGRESS · banksys_lixiaohua 〔本项目活记忆 · 状态机〕

> **作用**:这是项目的"存档点"。任意 AI、任意重启会话,读它即可知道当前做到哪、下一步做什么、踩过什么坑。
> **更新时机**:每完成一个有意义步骤、每次会话结束前。
> **格式要求**:时间倒序,最新在上;短、准、可接力。

---

## 当前状态 (最后更新: 2026-08-20 · by AI)

- **阶段**:`六步流程第⑤步完成:PR #2 CI 全绿,等待人工审核合并(第⑥步)`
- **上一步完成**:推送 feature/1-init(SSH 443 通道,HTTPS 被墙);Issue #1 + PR #2 已建;CI 两轮全绿(1m41s/1m37s,含 docker build);升级 checkout@v5 / setup-python@v6 消除 Node20 弃用警告。
- **下一步 (TODO 第一条)**:人类 Review PR #2 → 合并 main → CD 自动部署(第⑥步)。
- **阻塞项**:等人类审核合并;网络注意:github.com 主站被墙,git 用 SSH 443(ssh.github.com:443)已生效。

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

- **CD 部署失败两次(18s/14s 红)**:PR #2/#3 合并触发 CD 均失败,`cd /opt/banksys_lixiaohua: No such file or directory`。根因:① `appleboy/ssh-action@v1.0.3` 无 `rsync/source/target` 输入,文件未同步;② 误判"升级 v1.2.5 支持 rsync",实际 v1.2.5 的 `sync` 是"多主机同步执行命令"、不传文件(warning 列出了全部合法输入,升级前应先 `gh api .../action.yml` 核实)。解决:改用三段式——ssh-action `mkdir -p /opt/banksys_lixiaohua` → `appleboy/scp-action@v1.0.0` 传文件(`source` 逗号分隔、`rm: true`)→ ssh-action 跑部署脚本。验证:合并 fix/3-cd-scp-action 后看 CD 健康检查。已写入 05 §7(含纠正)。
- 预判:Windows 控制台编码、CI 干净 runner 上数据路径、docker 端口占用(exit 125)——见 05 标准第 7 节。

---

## 里程碑 (DONE)

- [x] 项目三文档(00/01/PROGRESS)完成,待人类确认

# 00 · 项目上下文 〔本项目活记忆 · AI 维护〕

> **作用**:这是项目的"身份档案"。AI 接管项目时先读这里,了解项目目标、技术栈、目录、部署取值。
> **更新时机**:架构、技术栈、目录结构、端口、部署目录、重要约束变化时更新。

---

## 1. 项目是什么

- **项目名称**:`banksys_lixiaohua`(银行营销认购预测系统)
- **一句话目标**:基于银行电话营销数据集,提供「数据交互分析」与「客户是否认购在线预测」两个功能的 Web 应用,并跑通完整 CI + CD。
- **使用者/受益者**:银行营销分析人员(分析客户特征与认购关系)、营销坐席(预测前快速评估客户认购可能性);课程评审。
- **核心功能**:
  - 数据分析交互页面:浏览、筛选、可视化营销数据,展示特征与认购的关系。
  - 离线训练 + 在线预测:用 train.csv 离线训练分类模型,产物供在线预测页面加载;用户点选输入客户特征,预测是否认购及概率。
- **输入/数据**:`data/train.csv`(22500 行,含目标列 `subscribe`)、`data/test.csv`(7500 行,无标签)。来自公开银行营销数据集(UCI bank marketing 变体,含宏观经济指标列)。公开教学数据,约 3.7MB,**进 Git**。

## 2. 技术栈

| 层 | 选型 | 理由 |
|---|---|---|
| 语言/运行时 | Python 3.11 | 课程要求;数据/ML 生态成熟 |
| Web 框架 | Streamlit | 数据分析和交互表单页面零前端成本,一页分析一页预测 |
| ML 库 | scikit-learn(pandas 做数据处理) | 分类任务经典工具,产物可 pkl 序列化、可复现 |
| 测试 | pytest | 课程标准,CI 同源 |
| 格式/静态检查 | ruff(format + check) | 课程标准,一个工具两件事 |
| 打包/运行 | Docker | 统一运行环境,CI/CD 复用 |
| CI/CD | GitHub Actions | 通用、可视化、适合教学与团队协作 |

## 3. 目录地图

```text
banksys_lixiaohua/
├── standards/                 # AI 项目记忆与通用规范(00/01/PROGRESS + 02~06)
├── app/                       # Streamlit 应用
│   ├── app.py                 # 入口(主页面:项目导航 + 数据概览)
│   ├── pages/                 # 多页面
│   │   ├── 1_数据分析.py       # 功能一:数据交互分析页面
│   │   └── 2_在线预测.py       # 功能二:点选输入 + 认购预测页面
│   └── core/                  # 业务逻辑,与 UI 分离,纯函数优先(可单测)
│       ├── data_loader.py     # 加载/缓存 CSV,字段定义
│       ├── analysis.py        # 分析计算:概览、分布、交叉分析
│       └── predictor.py       # 加载模型产物 + 特征编码 + 预测
├── models/                    # 离线训练
│   ├── train.py               # 训练管线:python -m models.train
│   └── artifacts/             # 模型产物(model.pkl + encoder + metrics.json),进 Git
├── data/                      # 公开教学数据 train.csv / test.csv,进 Git
├── tests/                     # pytest 单元测试,与 app/core、models 一一对应
├── requirements.txt           # 生产运行依赖(streamlit 等)
├── requirements-dev.txt       # 本地/CI 检查依赖(pytest、ruff、pytest-cov)
├── Dockerfile                 # 镜像名 banksys_lixiaohua,容器内端口 8888
├── .github/workflows/
│   ├── ci.yml                 # PR/push:ruff format+check、pytest+cov、模型门禁、docker build
│   └── cd.yml                 # push main:SSH 同步 → 构建 → 运行 → 健康检查
├── .gitignore
└── README.md
```

> 新增目录前先更新本节,避免项目越做越散。

## 4. 质量门槛

| 类型 | 本项目标准 |
|---|---|
| 格式检查 | `ruff format --check .` |
| 静态检查 | `ruff check .` |
| 单元测试 | `pytest` |
| 覆盖率 | `pytest --cov --cov-fail-under=80` |
| 构建 | `docker build` 成功(CI 跑,本地不强制装 Docker) |
| 业务/模型指标 | 训练管线 AUC ≥ 0.80(CI 中作为项目特有门禁 `python -m models.train --check-auc`);部署后健康检查 `/_stcore/health` 返回 ok |

## 5. 不变约束

- 密钥、密码、私钥、Token **绝不写进代码或文档**,只进 GitHub Secrets / 环境变量(`SSH_PRIVATE_KEY` / `SSH_HOST` / `SSH_USER`)。
- 数据与模型产物:公开教学数据 `data/*.csv` **进 Git**(便于 CI/服务器复现);模型产物 `models/artifacts/` 体积可控(pkl < 20MB)默认进 Git,若超限改为「CI 训练产出 → CD 下载」。
- `main` 分支受保护,日常开发必须走 feature 分支 + PR,AI 绝不自行合并。
- CI 红灯不合并。
- 端口标准:容器内固定 8888,主机端口 8888 起预留回退段(8888~8898),由 CD 脚本自动找空闲端口。

## 6. 部署/CI 占位符取值

| 占位符 | 本项目取值 | 说明 |
|---|---|---|
| `<APP>` | `banksys_lixiaohua` | 应用名/镜像名/容器名 |
| `<DEPLOY_DIR>` | `/opt/banksys_lixiaohua` | 服务器部署目录 |
| `<PORT>` | `8888` | 服务端口(容器内固定;主机 8888~8898 回退) |
| `<PYVER>` | `3.11` | Python 版本 |
| `<HEALTHCHECK>` | `_stcore/health` | Streamlit 自带健康检查端点,返回 `ok` |
| `<SSH_USER>` | 待配置(如 `root` / `deploy`) | 部署用户 |
| `<SSH_HOST>` | 待配置 | 服务器公网 IP 或域名 |

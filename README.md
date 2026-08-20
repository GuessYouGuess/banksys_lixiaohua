# banksys_lixiaohua

基于银行电话营销数据集的 Web 应用,包含两个功能:

1. **数据分析交互页面** — 浏览、筛选、可视化客户特征与认购关系
2. **在线预测系统** — 离线训练模型 + 点选输入预测客户是否认购(含概率)

## 技术栈

Python 3.11 · Streamlit · scikit-learn · pandas · pytest · ruff · Docker · GitHub Actions

## 快速开始(本地)

```bash
# 1) 建环境(conda 或 venv 均可)
conda create -y -n banksys python=3.11
conda activate banksys

# 2) 装依赖(国内可用清华源)
pip install -r requirements.txt -r requirements-dev.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 3) 启动(默认端口 8888)
streamlit run app/app.py --server.port=8888
# 健康检查:curl http://localhost:8888/_stcore/health → ok
```

## 测试与检查

```bash
ruff format --check .   # 格式
ruff check .            # 静态检查
pytest --cov --cov-fail-under=80   # 单元测试 + 覆盖率门槛 80%
```

## Docker

```bash
docker build -t banksys_lixiaohua:latest .
docker run -d --name banksys_lixiaohua --restart unless-stopped -p 8888:8888 banksys_lixiaohua:latest
```

## CI/CD

| 流程 | 触发 | 内容 |
|---|---|---|
| CI | PR / push | ruff format+check · pytest 覆盖率 ≥80% · docker build |
| CD | 合并 main | SSH 同步到服务器 → 构建镜像 → 端口 8888~8898 回退 → 健康检查 |

CD 依赖 GitHub Secrets:`SSH_PRIVATE_KEY` / `SSH_HOST` / `SSH_USER`(服务器需预装 Docker)。

## 目录结构

```text
├── app/            # Streamlit 应用(入口 + pages + core 纯逻辑)
├── models/         # 离线训练管线(python -m models.train)
├── data/           # 公开教学数据 train.csv / test.csv(进 Git)
├── tests/          # pytest 单元测试
├── standards/      # 项目记忆与规范(AI 进入项目先读 README.md)
└── .github/workflows/  # ci.yml / cd.yml
```

> 任意 AI 进入本项目,请先读 `standards/README.md`。

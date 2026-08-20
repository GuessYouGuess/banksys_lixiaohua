# 生产镜像:只装运行依赖,开发工具留在 CI
FROM python:3.11-slim

# 国内服务器可用 --build-arg PIP_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple
ARG PIP_INDEX_URL=https://pypi.org/simple

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --timeout 120 -i "${PIP_INDEX_URL}" -r requirements.txt

COPY app/ ./app/
COPY models/ ./models/
COPY data/ ./data/
COPY pyproject.toml .

# 容器内端口固定 8888
EXPOSE 8888

HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8888/_stcore/health', timeout=3)" || exit 1

CMD ["streamlit", "run", "app/app.py", "--server.port=8888", "--server.address=0.0.0.0", "--server.headless=true"]

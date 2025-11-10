# Python 3.11をベースイメージとして使用
FROM python:3.11-slim

# 作業ディレクトリを設定
WORKDIR /app

# 依存パッケージファイルをコピー
COPY requirements.txt pyproject.toml ./

# 依存パッケージをインストール
RUN pip install --no-cache-dir -r requirements.txt

# ソースコードをコピー
COPY src/ ./src/

# Pythonパスを設定
ENV PYTHONPATH=/app/src

# MCPサーバーを起動
CMD ["python", "-m", "readme_mcp.server"]

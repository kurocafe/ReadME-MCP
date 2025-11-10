# README MCP Server

GitHubリポジトリを自動で分析してREADME.mdを生成するMCPサーバーです。

## 機能

- GitHubリポジトリのURLを受け取る
- リポジトリの情報を分析（言語、スター数、トピックなど）
- README.mdの内容を自動生成

## 技術スタック

- Python 3.11
- MCP (Model Context Protocol)
- PyGithub
- Docker

## セットアップ

### 必要なもの

- Docker
- Docker Compose

### インストール

1. リポジトリをクローン

```bash
git clone <repository-url>
cd ReadME-MCP
```

2. 環境変数の設定（オプション）

```bash
cp .env.example .env
# .envファイルを編集してGitHub APIトークンを設定
```

3. Dockerイメージのビルド

```bash
docker-compose build
```

## 使い方

### サーバーの起動

```bash
docker-compose up
```

### 開発モード

ソースコードの変更を自動で反映させたい場合は、ボリュームマウントが設定されているのでそのまま開発できます。

```bash
docker-compose up
# 別のターミナルでコードを編集
```

## プロジェクト構造

```
readme-mcp/
├── src/
│   └── readme_mcp/
│       ├── __init__.py
│       ├── server.py           # MCPサーバーのメイン処理
│       ├── github_analyzer.py  # GitHubリポジトリ解析
│       └── readme_generator.py # README生成ロジック
├── tests/                      # テストコード
├── Dockerfile                  # Docker設定
├── docker-compose.yml          # Docker Compose設定
├── requirements.txt            # Python依存パッケージ
└── pyproject.toml             # Pythonプロジェクト設定
```

## 開発状況

現在開発中のプロジェクトです。基本的な構造は完成していますが、機能の実装を進めています。

## ライセンス

MIT
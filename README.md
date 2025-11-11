# README MCP Server

GitHubリポジトリを自動で分析してREADME.mdを生成・保存するMCPサーバーです。Claude Desktopと連携して、対話的にREADMEを作成できます。

## 機能

### 1. README自動生成 (`generate_readme`)
- GitHubリポジトリのURLを受け取る
- リポジトリの情報を分析（言語、スター数、フォーク数、トピック、ライセンスなど）
- プロジェクト構造、依存関係ファイル、コントリビューター情報を取得
- 包括的なREADME.mdの内容を自動生成

### 2. GitHub保存機能 (`save_readme_to_github`)
- 生成されたREADMEをGitHubリポジトリに直接コミット
- 既存のREADME.mdがある場合は更新、ない場合は新規作成
- カスタムコミットメッセージをサポート
- コミットURL・SHAを返す

## 技術スタック

- Python 3.11
- MCP (Model Context Protocol)
- PyGithub
- Docker

## セットアップ

### 必要なもの

- Docker & Docker Compose
- Claude Desktop（MCPクライアント）
- GitHub Personal Access Token（書き込み権限必要）

### インストール

1. リポジトリをクローン

```bash
git clone https://github.com/kurocafe/ReadME-MCP.git
cd ReadME-MCP
```

2. GitHub Personal Access Tokenの取得

   a. https://github.com/settings/tokens にアクセス

   b. "Generate new token" → "Tokens (classic)" を選択

   c. **`repo`** スコープ（フルアクセス）にチェック

   d. トークンを生成してコピー

3. 環境変数の設定

```bash
cp .env.example .env
# .envファイルを編集してGitHub APIトークンを設定
```

`.env`ファイルの内容:
```
GITHUB_TOKEN=ghp_your_actual_token_here
```

4. Dockerイメージのビルド

```bash
docker-compose build
```

5. Claude Desktop設定

`~/Library/Application Support/Claude/claude_desktop_config.json` に以下を追加:

```json
{
  "mcpServers": {
    "readme-mcp": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "--env-file",
        "/Users/YOUR_USERNAME/GitHub/ReadME-MCP/.env",
        "readme-mcp-readme-mcp",
        "python",
        "-m",
        "readme_mcp.server"
      ]
    }
  }
}
```

**重要**: `/Users/YOUR_USERNAME/GitHub/ReadME-MCP/.env` のパスを実際のプロジェクトパスに変更してください。

6. Claude Desktopを再起動 (Cmd+Q → 起動)

## 使い方

### Claude Desktopでの使用

セットアップが完了したら、Claude Desktopで以下のように使用できます：

#### ステップ1: READMEを生成

Claude Desktopで以下のように依頼:

```
https://github.com/username/repository のREADMEを生成して
```

生成されたREADMEの内容が表示されます。

#### ステップ2: GitHubに保存（オプション）

内容を確認後、GitHubに保存:

```
生成されたREADMEを https://github.com/username/repository に保存して
```

カスタムコミットメッセージで保存:

```
生成されたREADMEを https://github.com/username/repository に「READMEを自動生成」というメッセージで保存して
```

保存が成功すると、コミットURLとSHAが表示されます。

### 直接実行（開発用）

MCPサーバーを直接起動してテストする場合:

```bash
docker-compose up
```

### 開発モード

ソースコードの変更を自動で反映:

```bash
# ボリュームマウントが設定されているので、コードを編集すると自動反映
docker-compose up

# 別のターミナルでコードを編集
# 変更を反映するにはClaude Desktopを再起動
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

## トラブルシューティング

### 401エラー（Requires authentication）

GitHub tokenが正しく設定されていません：

1. `.env`ファイルが存在するか確認
2. `GITHUB_TOKEN`が正しく設定されているか確認
3. Claude Desktop設定の`--env-file`パスが正しいか確認
4. Claude Desktopを再起動

### 404エラー（Not Found）

リポジトリURLが正しくありません：

- 正しい形式: `https://github.com/owner/repository`
- 末尾のスラッシュは自動で削除されます
- `.git`拡張子も自動で処理されます

### デバッグログの確認

```bash
# 実行中のコンテナのログを確認
docker logs -f $(docker ps --filter "ancestor=readme-mcp-readme-mcp" -q)

# デバッグログのみを表示
docker logs $(docker ps --filter "ancestor=readme-mcp-readme-mcp" -q) 2>&1 | grep DEBUG
```

## 技術詳細

### 実装されている機能

- **URLパース処理**: 様々な形式のGitHub URLに対応（クエリパラメータ、フラグメント、.git拡張子など）
- **リポジトリ分析**: PyGithub APIを使用した包括的な情報取得
- **README生成**: プロジェクトの特性に応じた適切なセクション生成
- **GitHub API連携**: 読み取り・書き込み両方に対応
- **エラーハンドリング**: 詳細なエラーメッセージとログ出力

### 対応している依存関係ファイル

- `package.json` (Node.js)
- `requirements.txt` (Python)
- `Cargo.toml` (Rust)
- `go.mod` (Go)
- `pom.xml` (Java/Maven)
- `build.gradle` (Java/Gradle)
- `Gemfile` (Ruby)

## 開発状況

✅ **完成**: 基本機能の実装が完了し、Claude Desktopと連携して動作します。

## ライセンス

MIT
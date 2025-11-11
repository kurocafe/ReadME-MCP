"""
MCPサーバーのメイン実装
"""

from mcp.server import Server
from mcp.types import Tool, TextContent
import asyncio
import os
from .github_analyzer import GitHubAnalyzer
from .readme_generator import ReadmeGenerator


# MCPサーバーのインスタンスを作成
app = Server("readme-mcp")

# GitHubトークンを環境変数から取得
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# GitHubアナライザーとREADME生成器のインスタンス
github_analyzer = GitHubAnalyzer(access_token=GITHUB_TOKEN)
readme_generator = ReadmeGenerator()


@app.list_tools()
async def list_tools() -> list[Tool]:
    """
    利用可能なツールのリストを返す
    """
    return [
        Tool(
            name="generate_readme",
            description="GitHubリポジトリを分析してREADME.mdを生成します",
            inputSchema={
                "type": "object",
                "properties": {
                    "repository_url": {
                        "type": "string",
                        "description": "GitHubリポジトリのURL（例: https://github.com/user/repo）"
                    }
                },
                "required": ["repository_url"]
            }
        ),
        Tool(
            name="save_readme_to_github",
            description="生成されたREADME.mdをGitHubリポジトリに保存します",
            inputSchema={
                "type": "object",
                "properties": {
                    "repository_url": {
                        "type": "string",
                        "description": "GitHubリポジトリのURL（例: https://github.com/user/repo）"
                    },
                    "readme_content": {
                        "type": "string",
                        "description": "保存するREADME.mdの内容"
                    },
                    "commit_message": {
                        "type": "string",
                        "description": "コミットメッセージ（オプション、デフォルト: 'Update README.md via MCP'）"
                    }
                },
                "required": ["repository_url", "readme_content"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """
    ツールを実行する
    """
    if name == "generate_readme":
        try:
            # リポジトリURLを取得
            repo_url = arguments.get("repository_url")
            if not repo_url:
                return [TextContent(
                    type="text",
                    text="エラー: repository_urlが指定されていません"
                )]

            # GitHubリポジトリを解析
            repo_info = github_analyzer.analyze_repository(repo_url)

            # README.mdを生成
            readme_content = readme_generator.generate(repo_info)

            return [TextContent(
                type="text",
                text=f"README.mdの生成が完了しました:\n\n{readme_content}"
            )]

        except ValueError as e:
            return [TextContent(
                type="text",
                text=f"エラー: {str(e)}"
            )]
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"予期しないエラーが発生しました: {str(e)}"
            )]

    elif name == "save_readme_to_github":
        try:
            # 必須パラメータを取得
            repo_url = arguments.get("repository_url")
            readme_content = arguments.get("readme_content")
            commit_message = arguments.get("commit_message", "Update README.md via MCP")

            if not repo_url:
                return [TextContent(
                    type="text",
                    text="エラー: repository_urlが指定されていません"
                )]
            if not readme_content:
                return [TextContent(
                    type="text",
                    text="エラー: readme_contentが指定されていません"
                )]

            # GitHubにREADME.mdを保存
            result = github_analyzer.save_readme_to_repository(
                repo_url=repo_url,
                readme_content=readme_content,
                commit_message=commit_message
            )

            return [TextContent(
                type="text",
                text=f"{result['message']}\n\nコミットURL: {result['commit_url']}\nコミットSHA: {result['commit_sha']}"
            )]

        except ValueError as e:
            return [TextContent(
                type="text",
                text=f"エラー: {str(e)}"
            )]
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"予期しないエラーが発生しました: {str(e)}"
            )]

    raise ValueError(f"Unknown tool: {name}")


async def main():
    """
    サーバーを起動する
    """
    from mcp.server.stdio import stdio_server

    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())

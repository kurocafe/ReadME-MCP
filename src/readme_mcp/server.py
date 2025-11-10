"""
MCPサーバーのメイン実装
"""

from mcp.server import Server
from mcp.types import Tool, TextContent
import asyncio


# MCPサーバーのインスタンスを作成
app = Server("readme-mcp")


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
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """
    ツールを実行する
    """
    if name == "generate_readme":
        # TODO: 実装予定
        return [TextContent(
            type="text",
            text="README生成機能は現在開発中です"
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

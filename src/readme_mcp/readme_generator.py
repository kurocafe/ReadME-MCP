"""
README.mdを生成するモジュール
"""


class ReadmeGenerator:
    """
    リポジトリ情報からREADME.mdを生成するクラス
    """

    def _generate_installation_section(self, repo_info: dict) -> list[str]:
        """
        インストールセクションを生成

        Args:
            repo_info: リポジトリ情報

        Returns:
            セクションの行リスト
        """
        sections = []
        sections.append("## Installation")
        sections.append("")

        # クローンコマンド
        if repo_info.get('clone_url'):
            sections.append("```bash")
            sections.append(f"git clone {repo_info['clone_url']}")
            sections.append(f"cd {repo_info['name']}")
            sections.append("```")
            sections.append("")

        # 依存関係ファイルに基づいたインストール手順
        dependency_files = repo_info.get('dependency_files', [])

        if 'package.json' in dependency_files:
            sections.append("Install dependencies with npm:")
            sections.append("```bash")
            sections.append("npm install")
            sections.append("```")
            sections.append("")

        if 'requirements.txt' in dependency_files:
            sections.append("Install Python dependencies:")
            sections.append("```bash")
            sections.append("pip install -r requirements.txt")
            sections.append("```")
            sections.append("")

        if 'Cargo.toml' in dependency_files:
            sections.append("Build with Cargo:")
            sections.append("```bash")
            sections.append("cargo build")
            sections.append("```")
            sections.append("")

        if 'go.mod' in dependency_files:
            sections.append("Install Go dependencies:")
            sections.append("```bash")
            sections.append("go mod download")
            sections.append("```")
            sections.append("")

        return sections

    def _generate_project_structure_section(self, repo_info: dict) -> list[str]:
        """
        プロジェクト構造セクションを生成

        Args:
            repo_info: リポジトリ情報

        Returns:
            セクションの行リスト
        """
        sections = []
        main_dirs = repo_info.get('main_directories', [])

        if main_dirs:
            sections.append("## Project Structure")
            sections.append("")
            sections.append("```")
            for directory in main_dirs[:5]:  # 上位5つのディレクトリのみ表示
                sections.append(f"├── {directory}/")
            sections.append("```")
            sections.append("")

        return sections

    def generate(self, repo_info: dict) -> str:
        """
        リポジトリ情報からREADME.mdを生成

        Args:
            repo_info: GitHubAnalyzerから取得したリポジトリ情報

        Returns:
            生成されたREADME.mdの内容
        """
        sections = []

        # タイトル
        sections.append(f"# {repo_info['name']}")
        sections.append("")

        # 説明
        if repo_info.get('description'):
            sections.append(repo_info['description'])
            sections.append("")

        # バッジ（stars, forks, license）
        badges = []
        if repo_info.get('stars'):
            badges.append(f"![Stars](https://img.shields.io/badge/stars-{repo_info['stars']}-yellow)")
        if repo_info.get('forks'):
            badges.append(f"![Forks](https://img.shields.io/badge/forks-{repo_info['forks']}-blue)")
        if repo_info.get('license'):
            badges.append(f"![License](https://img.shields.io/badge/license-{repo_info['license']}-green)")

        if badges:
            sections.append(" ".join(badges))
            sections.append("")

        # 言語・トピックス
        if repo_info.get('language'):
            sections.append(f"**Language:** {repo_info['language']}")
            sections.append("")

        if repo_info.get('topics'):
            topics = ", ".join([f"`{topic}`" for topic in repo_info['topics']])
            sections.append(f"**Topics:** {topics}")
            sections.append("")

        # インストール方法
        installation_sections = self._generate_installation_section(repo_info)
        sections.extend(installation_sections)

        # プロジェクト構造
        structure_sections = self._generate_project_structure_section(repo_info)
        sections.extend(structure_sections)

        # コントリビューター
        if repo_info.get('top_contributors'):
            sections.append("## Contributors")
            sections.append("")
            for contributor in repo_info['top_contributors']:
                sections.append(f"- [@{contributor}](https://github.com/{contributor})")
            sections.append("")

        # 最終更新日
        if repo_info.get('last_updated'):
            sections.append(f"**Last Updated:** {repo_info['last_updated']}")
            sections.append("")

        # リポジトリへのリンク
        if repo_info.get('url'):
            sections.append("---")
            sections.append("")
            sections.append(f"[View on GitHub]({repo_info['url']})")

        return "\n".join(sections)

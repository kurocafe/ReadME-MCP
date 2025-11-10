"""
README.mdを生成するモジュール
"""


class ReadmeGenerator:
    """
    リポジトリ情報からREADME.mdを生成するクラス
    """

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

        # TODO: より詳細なセクションを追加（インストール方法、使い方など）

        return "\n".join(sections)

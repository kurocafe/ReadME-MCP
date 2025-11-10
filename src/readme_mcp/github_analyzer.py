"""
GitHubリポジトリを解析するモジュール
"""

from github import Github
from typing import Optional
import re


class GitHubAnalyzer:
    """
    GitHubリポジトリの情報を取得・解析するクラス
    """

    def __init__(self, access_token: Optional[str] = None):
        """
        初期化

        Args:
            access_token: GitHubアクセストークン（オプション）
        """
        self.github = Github(access_token) if access_token else Github()

    def parse_repository_url(self, url: str) -> tuple[str, str]:
        """
        GitHubのURLからオーナー名とリポジトリ名を抽出

        Args:
            url: GitHubリポジトリのURL

        Returns:
            (owner, repo_name)のタプル
        """
        # https://github.com/owner/repo の形式から抽出
        pattern = r"github\.com/([^/]+)/([^/]+)"
        match = re.search(pattern, url)

        if not match:
            raise ValueError("Invalid GitHub repository URL")

        owner = match.group(1)
        repo_name = match.group(2).rstrip('.git')

        return owner, repo_name

    def analyze_repository(self, repo_url: str) -> dict:
        """
        リポジトリを解析して情報を取得

        Args:
            repo_url: GitHubリポジトリのURL

        Returns:
            リポジトリ情報の辞書
        """
        owner, repo_name = self.parse_repository_url(repo_url)
        repo = self.github.get_repo(f"{owner}/{repo_name}")

        # 基本情報を取得
        info = {
            "name": repo.name,
            "description": repo.description,
            "owner": owner,
            "language": repo.language,
            "stars": repo.stargazers_count,
            "forks": repo.forks_count,
            "topics": repo.get_topics(),
            "license": repo.license.name if repo.license else None,
        }

        # TODO: ファイル構造やコード内容の解析を追加

        return info

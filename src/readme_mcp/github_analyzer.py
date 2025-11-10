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
        # URLをクリーンアップ
        url = url.strip().rstrip('/')

        # https://github.com/owner/repo の形式から抽出
        pattern = r"github\.com/([^/]+)/([^/]+)"
        match = re.search(pattern, url)

        if not match:
            raise ValueError(f"Invalid GitHub repository URL: {url}")

        owner = match.group(1)
        repo_name = match.group(2)

        # .git拡張子を削除
        repo_name = repo_name.rstrip('.git')

        # /tree/main などの余分なパスを削除
        repo_name = repo_name.split('?')[0].split('#')[0]

        return owner, repo_name

    def get_file_structure(self, repo) -> dict:
        """
        リポジトリのファイル構造を取得

        Args:
            repo: GitHubリポジトリオブジェクト

        Returns:
            ファイル構造情報
        """
        structure = {
            "has_readme": False,
            "dependency_files": [],
            "main_directories": [],
        }

        try:
            contents = repo.get_contents("")

            for content in contents:
                # README.mdの存在確認
                if content.name.lower().startswith("readme"):
                    structure["has_readme"] = True

                # 依存関係ファイルの検出
                dependency_files = [
                    "package.json", "requirements.txt", "Cargo.toml",
                    "go.mod", "pom.xml", "build.gradle", "Gemfile"
                ]
                if content.name in dependency_files:
                    structure["dependency_files"].append(content.name)

                # メインディレクトリの取得
                if content.type == "dir":
                    structure["main_directories"].append(content.name)

        except Exception as e:
            print(f"ファイル構造の取得中にエラー: {e}")

        return structure

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
            "url": repo.html_url,
            "clone_url": repo.clone_url,
        }

        # ファイル構造の解析
        structure = self.get_file_structure(repo)
        info.update(structure)

        # コントリビューター情報（上位3名）
        try:
            contributors = repo.get_contributors()
            info["top_contributors"] = [
                contributor.login for contributor in list(contributors)[:3]
            ]
        except Exception:
            info["top_contributors"] = []

        # 最近の更新日
        info["last_updated"] = repo.updated_at.strftime("%Y-%m-%d") if repo.updated_at else None

        return info

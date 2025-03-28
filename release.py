# -*- coding: utf-8 -*-

"""
Publish esclusive_repo_ai to GitHub as a release.
"""

from pathlib import Path
from github import Github
from esclusive_repo_ai import __version__

release_name = __version__
path_github_token = Path.home().joinpath(
    ".github",
    "pac",
    "easyscalecloud",
    "sanhe-dev.txt",
)
dir_here = Path(__file__).absolute().parent
repo_name = dir_here.name
org = "easyscalecloud"

gh = Github(path_github_token.read_text(encoding="utf-8").strip())
repo = gh.get_repo(f"{org}/{repo_name}")
try:
    release = repo.get_release(release_name)
except Exception as e:
    # create tag and release if not exists
    try:
        default_branch = repo.default_branch
        commit = repo.get_branch(default_branch).commit
        commit_sha = commit.sha
        tag = repo.create_git_tag(
            tag=release_name,
            message=f"Release {release_name}",
            object=commit_sha,
            type="commit",
        )
        repo.create_git_ref(
            ref=f"refs/tags/{release_name}",
            sha=tag.sha,
        )
    except:
        pass
    repo.create_git_release(
        tag=release_name,
        name=release_name,
        message=f"Release {release_name}",
    )
    release = repo.get_release(release_name)

file_name_list = [
    "esclusive_repo_ai.py",
    "prompt.md",
    "requirements.txt",
]
for asset in release.get_assets():
    if asset.name in file_name_list:
        asset.delete_asset()
for file_name in file_name_list:
    path = dir_here.joinpath(file_name)
    release.upload_asset(
        path=f"{path}",
        label=file_name,
    )

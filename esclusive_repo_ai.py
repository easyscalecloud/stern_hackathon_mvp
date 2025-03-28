# -*- coding: utf-8 -*-

# Copyright (C) 2025 Sanhe Hu <sanhehu@easyscalecloud.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

"""
Knowledge Base Builder for GitHub Repositories.

This module provides tools to fetch and consolidate documentation from public GitHub
repositories into a single knowledge base. It handles repository cloning, file filtering,
and content extraction using the docpack library.

The main workflow:

1. Load configuration from a JSON file
2. Clone specified GitHub repositories
3. Extract files matching include/exclude patterns
4. Combine all content into a single knowledge base file
"""

import typing as T
import os
import sys
import enum
import json
import shutil
import subprocess
import dataclasses
from pathlib import Path
from urllib import request
from functools import cached_property

__version__ = "0.1.1"
__license__ = "AGPL-3.0-or-later"
__author__ = "Sanhe Hu"
__author_email__ = "sanhehu@easyscalecloud.com"
__maintainer__ = "Sanhe Hu"
__maintainer_email__ = "sanhehu@easyscalecloud.com"

url_requirements_txt = f"https://github.com/easyscalecloud/stern_hackathon_mvp/releases/download/{__version__}/requirements.txt"
url_prompt_md = f"https://github.com/easyscalecloud/stern_hackathon_mvp/releases/download/{__version__}/prompt.md"

IS_CI = "CI" in os.environ


def get_url_content(url) -> str:
    """
    Fetch and return the content of a URL as a string.
    """
    with request.urlopen(url) as response:
        return response.read().decode("utf-8").strip()


@dataclasses.dataclass
class Paths:
    """
    Path manager for the knowledge base builder.

    This class handles all file paths and directory structures used by the knowledge base
    builder, including temporary files, output locations, and dependency management.
    """

    dir_project_root: Path = dataclasses.field()
    path_python_executable: Path = dataclasses.field()

    @property
    def dir_bin(self) -> Path:
        """Directory containing the Python executable and pip."""
        return self.path_python_executable.parent

    @property
    def path_bin_pip(self) -> Path:
        """Path to the pip executable."""
        return self.dir_bin / "pip"

    @cached_property
    def dir_tmp(self) -> Path:
        """
        Temporary directory for working files.
        """
        dir_tmp = self.dir_project_root / "tmp"
        dir_tmp.mkdir(exist_ok=True)
        return dir_tmp

    @property
    def path_requirements_txt(self) -> Path:
        """Path to the requirements.txt file for dependencies."""
        return self.dir_tmp / "requirements.txt"

    def install_dependencies(self):
        """
        Install required Python dependencies from a remote requirements.txt file.

        Fetches the requirements file from the main branch of the stern_hackathon_mvp
        repository and installs the packages using pip.
        """
        # Fetch requirements from GitHub repository
        content = get_url_content(url_requirements_txt)
        self.path_requirements_txt.write_text(content, encoding="utf-8")
        # Install dependencies using pip
        args = [
            f"{self.path_bin_pip}",
            "install",
            "-q",
            "-r" f"{self.path_requirements_txt}",
        ]
        subprocess.run(args, check=True)

    @property
    def path_esclusive_repo_ai_config_json(self) -> Path:
        return (
            self.dir_project_root
            / ".github"
            / "workflows"
            / "esclusive_repo_ai_config.json"
        )

    @property
    def path_prompt_md(self) -> Path:
        """Path to the prompt.md file for AI Prompt."""
        return self.dir_tmp / "prompt.md"

    @property
    def dir_knowledge_base(self):
        """Directory where knowledge base files will be stored."""
        return self.dir_tmp / "knowledge_base"

    @property
    def path_all_in_one_knowledge_base(self) -> Path:
        """Path to the consolidated knowledge base output file."""
        return self.dir_knowledge_base / "all_in_one_knowledge_base.txt"


paths = Paths(
    dir_project_root=Path.cwd().absolute(),
    path_python_executable=Path(sys.executable).absolute(),
)
paths.install_dependencies()

from github import Github
from docpack.api import GitHubPipeline


class SourceTypeEnum(enum.StrEnum):
    github = "github"


T_SOURCE_TYPE = T.Literal[SourceTypeEnum.github.value,]


@dataclasses.dataclass
class Source:
    """
    Base class for knowledge sources.

    This abstract class defines the interface for different types of knowledge sources
    that can be used to build the knowledge base (e.g., GitHub repositories).
    """

    type: T_SOURCE_TYPE

    @classmethod
    def from_dict(cls, dct: dict[str, T.Any]):
        source_type = dct["type"]
        if source_type not in SOURCE_MAPPING:
            raise ValueError
        klass = SOURCE_MAPPING[source_type]
        source = klass._from_dict(dct)
        return source

    @classmethod
    def _from_dict(cls, dct: dict[str, T.Any]):
        return cls(**dct)

    def build(self):
        """
        Build the knowledge base from this source.

        This method must be implemented by subclasses.
        """
        raise NotImplementedError


T_SOURCE = T.TypeVar("T_SOURCE", bound=Source)


@dataclasses.dataclass
class GitHubSource(Source):
    """
    GitHub repository knowledge source.

    This class handles fetching documentation from GitHub repositories,
    including cloning the repository and extracting files based on include/exclude patterns.

    :param domain: GitHub domain (e.g., github.com)
    :param org: GitHub organization or user name
    :param repo: Repository name
    :param ref: Git reference (branch, tag, or commit)
    :param include: List of glob patterns for files to include
    :param exclude: List of glob patterns for files to exclude
    """

    domain: str = dataclasses.field()
    org: str = dataclasses.field()
    repo: str = dataclasses.field()
    ref: str = dataclasses.field()
    include: list[str] = dataclasses.field()
    exclude: list[str] = dataclasses.field()

    @property
    def clone_url(self) -> str:
        """Generate the HTTPS clone URL for the repository."""
        return f"https://{self.domain}/{self.org}/{self.repo}.git"

    @property
    def dir_repo(self) -> Path:
        """Directory where the repository will be cloned."""
        return paths.dir_tmp.joinpath("repos", self.org, self.repo)

    def clone(self):
        """
        Clone the GitHub repository.

        Creates a shallow clone of the specified branch to minimize download size.
        """
        self.dir_repo.mkdir(parents=True, exist_ok=True)
        args = [
            "git",
            "clone",
            "--branch",
            self.ref,  # Specify the branch or tag to clone
            "--depth",
            "1",  # This creates a shallow clone
            self.clone_url,  # The repository URL
            f"{self.dir_repo}",
        ]
        subprocess.run(args, check=True)

    def fetch(self):
        """
        Extract documentation from the cloned repository.

        Uses `docpack's GitHubPipeline <https://github.com/MacHu-GWU/docpack-project>`_
        to extract files matching include/exclude patterns
        and save them as XML files in the knowledge base directory.
        """
        github_pipeline = GitHubPipeline(
            domain=self.domain,
            account=self.org,
            repo=self.repo,
            branch=self.ref,
            dir_repo=self.dir_repo,
            include=self.include,
            exclude=self.exclude,
            dir_out=paths.dir_knowledge_base,
        )
        github_pipeline.fetch()

    def build(self):
        """
        Build the knowledge base from this GitHub source.
        :return:
        """
        self.clone()
        self.fetch()


# Mapping of source types to their implementation classes
SOURCE_MAPPING = {
    SourceTypeEnum.github.value: GitHubSource,
}


@dataclasses.dataclass
class Config:
    """
    Configuration for the knowledge base builder.

    This class loads and validates the configuration from a JSON file,
    and manages the process of building the knowledge base from all sources.
    """

    sources: list[T_SOURCE] = dataclasses.field(default_factory=list)

    @classmethod
    def from_dict(cls, dct: dict[str, T.Any]):
        sources = list()
        for source_dct in dct.get("sources", []):
            source = Source.from_dict(source_dct)
            sources.append(source)
        return cls(sources=sources)

    @classmethod
    def from_json(cls, path_config: Path):
        dct = json.loads(path_config.read_text(encoding="utf-8"))
        return cls.from_dict(dct)

    def build(self):
        """
        Build the knowledge base from all configured sources.
        """
        for source in self.sources:
            source.build()
        prompt = get_url_content(url_prompt_md)
        lines = [prompt]
        for path in paths.dir_knowledge_base.glob("*.xml"):
            lines.append(path.read_text(encoding="utf-8"))
        content = "\n".join(lines)
        paths.path_all_in_one_knowledge_base.write_text(content, encoding="utf-8")

    def publish(self):
        # See: https://docs.github.com/en/actions/security-for-github-actions/security-guides/automatic-token-authentication
        token = os.environ["GITHUB_TOKEN"]
        gh = Github(token)
        # See: https://docs.github.com/en/actions/writing-workflows/choosing-what-your-workflow-does/store-information-in-variables#default-environment-variables
        repo_name = os.environ["GITHUB_REPOSITORY"].split("/")[1]
        release_name = "knowledge-base"
        repo = gh.get_repo(repo_name)
        try:
            release = repo.get_release(release_name)
        except Exception as e:
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
                repo.create_git_ref(ref=f"refs/tags/{release_name}", sha=tag.sha)
            except:
                pass
            repo.create_git_release(tag=release_name, name=release_name)
            release = repo.get_release(release_name)

        file_label = "all_in_one_knowledge_base.txt"
        for asset in release.get_assets():
            if asset.name == file_label:
                asset.delete_asset()
        release.upload_asset(
            path=f"{paths.path_all_in_one_knowledge_base}",
            label=file_label,
        )


config = Config.from_json(paths.path_esclusive_repo_ai_config_json)

shutil.rmtree(paths.dir_tmp, ignore_errors=True)
paths.dir_tmp.mkdir(exist_ok=True)
config.build()
config.publish()

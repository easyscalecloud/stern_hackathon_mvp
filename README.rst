Stern Hackathon MVP
==============================================================================

    This minimal viable product is for `Microsoft Garage presents Stern Hackathon <https://nyustern.campusgroups.com/sta/rsvp_boot?id=1928010>`_.


ESClusive Repo AI: Democratizing AI for Code Repositories
------------------------------------------------------------------------------
**ESClusive Repo AI** is an innovative GitHub integration that automatically generates comprehensive knowledge bases from code repositories. The Python implementation (``esclusive_repo_ai.py``) handles the entire pipeline - from repository configuration to content extraction and knowledge base consolidation. This MVP solves a critical market gap by enabling both technical and non-technical stakeholders to leverage AI for codebase understanding without specialized tools or subscriptions. With minimal setup (just one line added to CI/CD workflows), it creates a single portable file (``all_in_one_knowledge_base.txt``) containing rich contextual metadata that dramatically improves AI comprehension while providing source-linked references. The solution supports both free open-source usage and premium features for private repositories, perfectly aligning with the Microsoft Garage Hackathon's focus on extending GitHub capabilities to enhance collaboration and innovation.


Future Plans and Roadmap
------------------------------------------------------------------------------
This open-source version supports public repositories only. We'll soon launch a Professional plan at $4.99/month with private repository access and multi-repository AI integration, plus an Enterprise plan for large-scale deployments. While currently GitHub-exclusive, we're expanding to support GitLab, Bitbucket, Azure Repos, AWS CodeCommit, and Google Cloud Source Repositories in upcoming releases.


How to Use
------------------------------------------------------------------------------

    This tutorial covers the open-source version setup.

1. **For repositories without existing GitHub Actions**: Create a ``.github/workflows`` folder in your repository and add a file named ``.github/workflows/esclusive_repo_ai.yml`` with the following content:

.. code-block:: yaml

    # comprehensive github action yml reference: https://docs.github.com/en/free-pro-team@latest/actions/reference/workflow-syntax-for-github-actions
    name: esclusive_repo_ai

    on:
      push: # any push event to master will trigger this
        branches: ["main"]
      pull_request: # any pull request to master will trigger this
        branches: ["main"]
      workflow_dispatch: # allows you to manually trigger run

    permissions:
      contents: write # need this permission to publish knowledge base to GitHub Release

    jobs:
      esclusive_repo_ai:
        name: esclusive_repo_ai
        runs-on: "ubuntu-latest"
        steps:
          - uses: "actions/checkout@v3" # https://github.com/marketplace/actions/checkout
          - uses: "actions/setup-python@v4" # https://github.com/marketplace/actions/setup-python
            with:
              python-version: "3.11"
          - name: "build and publish all in one knowledge base"
            env:
              GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
            # CRITICAL
            run: |
              curl -fsSL https://github.com/easyscalecloud/stern_hackathon_mvp/releases/download/0.1.1/esclusive_repo_ai.py -o esclusive_repo_ai.py
              python3 esclusive_repo_ai.py

2. **For repositories with existing GitHub Actions**: Add the ``permissions`` section and insert these ``steps`` into your existing workflow file under the steps section:

.. code-block:: yaml

    ...

    permissions:
      contents: write # need this permission to publish knowledge base to GitHub Release

    jobs:
      esclusive_repo_ai:
        ...
        steps:
          ...
          - uses: "actions/setup-python@v4" # https://github.com/marketplace/actions/setup-python
            with:
              python-version: "3.11"
          - name: "build and publish all in one knowledge base"
            env:
              GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
            # CRITICAL
            run: |
              curl -fsSL https://github.com/easyscalecloud/stern_hackathon_mvp/releases/download/0.1.1/esclusive_repo_ai.py -o esclusive_repo_ai.py
              python3 esclusive_repo_ai.py

3. **Configure your knowledge base**: Create a ``.github/workflows/esclusive_repo_ai_config.json`` file with configuration settings. The example below shows how to integrate the Python Requests library repository:

.. code-block:: javascript

    {
        "sources": [
            {
                "type": "github",
                "domain": "github.com",
                "org": "psf",
                "repo": "requests",
                "ref": "main",
                "include": [
                    "README.md",
                    "docs/**/*.rst",
                    "src/requests/**/*.py"
                ],
                "exclude": []
            }
        ]
    }

4. **Activation**: The workflow will run automatically when you commit or merge code to the main branch. You can also trigger it manually through the GitHub Actions interface.


How It Looks Like In Real
------------------------------------------------------------------------------
We created a demo repo `easyscalecloud/stern_hackathon_demo <https://github.com/easyscalecloud/stern_hackathon_demo>`_ to show how we build an AI assistant who knows any selected repo (in this example, we pick Python requests library git repo for demonstartion)

- `GitHub Action Workflow Configuration <https://github.com/easyscalecloud/stern_hackathon_demo/blob/main/.github/workflows/esclusive_repo_ai.yml>`_
- `Knowledge Base Configuration <https://github.com/easyscalecloud/stern_hackathon_demo/blob/main/.github/workflows/esclusive_repo_ai_config.json>`_
- `Sample Automation Run <https://github.com/easyscalecloud/stern_hackathon_demo/actions/runs/14137567252/job/39612787751>`_
- `Sample Downloadable all_in_one_knowledge_base.txt file <https://github.com/easyscalecloud/stern_hackathon_demo/releases/download/knowledge-base/all_in_one_knowledge_base.txt>`_, in `GitHub Release <https://github.com/easyscalecloud/stern_hackathon_demo/releases/tag/knowledge-base>`_, you can drag and drop it to any AI.

🚀 Stern Hackathon MVP
==============================================================================

    This minimal viable product is for `Microsoft Garage presents Stern Hackathon <https://nyustern.campusgroups.com/sta/rsvp_boot?id=1928010>`_.


🧠 ESClusive Repo AI: Democratizing AI for Code Repositories
------------------------------------------------------------------------------
**ESClusive Repo AI** is an innovative GitHub integration that automatically generates comprehensive knowledge bases from code repositories. The Python implementation (``esclusive_repo_ai.py``) handles the entire pipeline - from repository configuration to content extraction and knowledge base consolidation. This MVP solves a critical market gap by enabling both technical and non-technical stakeholders to leverage AI for codebase understanding without specialized tools or subscriptions. With minimal setup (just one line added to CI/CD workflows), it creates a single portable file (``all_in_one_knowledge_base.txt``) containing rich contextual metadata that dramatically improves AI comprehension while providing source-linked references. The solution supports both free open-source usage and premium features for private repositories, perfectly aligning with the Microsoft Garage Hackathon's focus on extending GitHub capabilities to enhance collaboration and innovation.


🔮 Future Plans and Roadmap
------------------------------------------------------------------------------
This open-source version supports public repositories only. We'll soon launch a Professional plan at $4.99/month with private repository access and multi-repository AI integration, plus an Enterprise plan for large-scale deployments. While currently GitHub-exclusive, we're expanding to support GitLab, Bitbucket, Azure Repos, AWS CodeCommit, and Google Cloud Source Repositories in upcoming releases.


📕 How to Use
------------------------------------------------------------------------------

    This tutorial covers the open-source version setup.

1. **🔧 Setup GitHub Action Workflow**: Copy `run_esclusive_repo_ai.yml <https://github.com/easyscalecloud/stern_hackathon_mvp/blob/main/run_esclusive_repo_ai.yml>`_ from THIS repo to YOUR GitHub repo at ``.github/workflows/run_esclusive_repo_ai.yml``.
2. **⚙️ Configure your knowledge base**: Create a ``.github/workflows/esclusive_repo_ai_config.json`` file with configuration settings. `This example <https://github.com/easyscalecloud/stern_hackathon_mvp/blob/main/.github/workflows/example_esclusive_repo_ai_config.json>`_ shows how to integrate the `Python Requests library repository <https://github.com/psf/requests>`_.
3. **🚀 Activation**: By default, the workflow will run automatically and the knowledge base file will be updated when you commit or merge code to the main branch. You can also trigger it manually through the GitHub Actions interface.


👀 How It Looks Like In Real
------------------------------------------------------------------------------
We created a demo repo `easyscalecloud/stern_hackathon_demo <https://github.com/easyscalecloud/stern_hackathon_demo>`_ to show how we build an AI assistant who knows any selected repo (in this example, we pick Python requests library git repo for demonstration).

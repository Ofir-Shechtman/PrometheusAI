# Register To Operate First
In order to fetch prometheus metrics and get a JupiterHub cluster you'll need to register to OperateFirst systems.  
This following steps will guide you throw the whole process:
1. Go to [Operate First GitHub Repo](https://github.com/operate-first/apps) and click `Fork`
2. Clone the forked version of Operate First to **linux environment**
3. Add your GitHub username to `cluster-scope/base/user.openshift.io/groups/prometheus-ai/group.yaml` under users list 
4. Commit and push this change to your forked version.
5. Create a new PR to Operate First's master

**Note: You may want to ask the support team to approve your PR (via Slack)**

That's it once your PR is approved you are registered to operate first systems and can:
* Generate `Personal Access Token` for fetching prometheus metrics
* Get a JupiterHub node for running your jobs.
* Make more requests regarding storage, etc.

**Note: You can find examples of previously accepted merge requests under [Useful Links](useful_links.md) section 3**

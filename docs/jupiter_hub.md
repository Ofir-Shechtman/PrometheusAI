# JupyterHub

JupiterHub gives you an environment to run your project.
Follow this [Jupiter Hub Docs](https://www.operate-first.cloud/data-science/ds-workflows/docs/setup_environment/JH_access.md) to get started

## Specific Details:

1. Access [JupyterHub](https://jupyterhub-opf-jupyterhub.apps.smaug.na.operate-first.cloud/), select log in with `operate-first` and sign in using your GitHub Account.
2. After signing in, on the spawner page, select the `Standard Data Science (Python v3.8.6)` in the JupyterHub Notebook
   Image section from the dropdown and select a `Large` container size and hit `Start` to start your server.
3. Once your server has spawned, follow the rest of the doc to learn the basics of the server.


## Request more storage:
When you launch your JupyterHub server, the instance is connected to the storage volume associated with your account.  
This storage may not be enough for you, and you'll need to ask for more storage, here are is the [official doc](https://www.operate-first.cloud/apps/content/odh/jupyterhub/increase_pvc_size_jh.html) for doing so  
The flow is very similar to [registering operate first](register_to_operate_first.md).
Use can also see the [approved PR](https://github.com/operate-first/apps/pull/1567) that we got
You'll need to fork Operate First repository modify files and open a PR, when it'll be approved you'll get the additional storage that you wanted. 
# Github Action Workflows

Workflow run trigger fails to find the artifacts generated by the notebooks workflow.
https://github.com/actions/upload-artifact/issues/53

Workflows can be triggered when files in a directory change, but cannot conditionally run different individual steps depending upon which files changed. There are marketplace extensions that can add some filter functionality.

Initial workflows are created per directory so that they only run when needed.

``` mermaid
graph LR;
    src-->notebook;
    notebook<-. refresh .->data;
    notebook-->pages
    pages-->gh-pages
```

## Python Modules

I have reusable python code in modules that can be imported to all my notebooks. The reusable python code is in `/src` directory and I have also created unit tests and sonar code quality scans for these files.

I only need to run these tests when the `/src` files change.

## Jupyter Notebooks

I have Jupyter notebooks that consume the Python modules and generate data tables and charts.

I need to run the notebooks when the `/notebook` files or the `/src` files change.

The Jupyter notebooks also download and refresh data when needed so I also need to run these notebooks on regular schedule, some quarterly, some at least monthly.

## Github Pages

I convert the Jupyter Notebooks and static `/pages` files to Jekyl format and publish them to Github Pages.

I need to publish Github pages when the data changes, or when the static `/pages` change, or when the `/notebooks` change.

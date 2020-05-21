
# This app I call it `todo`

Secure Azure App Services + SQL PaaS stack using pulumi

![Deploy Production](https://github.com/venura9/pulumi-python-webapp-sql/workflows/Deploy%20Production/badge.svg)

Ref: https://github.com/pulumi/examples/tree/master/azure-py-appservice

# Getting Started with Pulumi

Instructions at: https://www.pulumi.com/docs/get-started/ 

* Install Pulumi
```bash
# Install on macos
$ brew install pulumi

# Install on linux
$ curl -fsSL https://get.pulumi.com | sh
```
* Install Python 3.6 or above

# Lingo 

* Program: a collection of files written in your chosen programming language
* Project: a directory containing a program, with metadata, so Pulumi knows how to run it
* Stack: an instance of your project, each often corresponding to a different cloud environment

# Project Setup

* For this Project

[![Deploy](https://get.pulumi.com/new/button.svg)](https://app.pulumi.com/new)

* For new projects

    * Create via Web App:
    [https://app.pulumi.com/site/new-project](https://app.pulumi.com/site/new-project)

    * Create via CLI
    ```bash
    $ pulumi new
    ```

    * Have a `Pulumi.yaml` in your directory and it will be used to create a new project.    
    ```yaml
    name: todo # change this name and you will end up with a new stack
    runtime: python
    description: Secure Azure App Services + SQL PaaS stack using pulumi
    ```
# Login

```bash
pulumi login [<url>] [flags]

# Pulumi manages the state, you need PULUMI_ACCESS_TOKEN in the environment variables (or you will be prompted)
# Get it from: https://app.pulumi.com/venura9/settings/tokens
pulumi login

# Enterprise 
pulumi login https://api.pulumi.yourcompany.com

# Local fs
pulumi login file://~
pulumi login --local

#Azure Blob
pulumi login azblob://my-pulumi-state-bucket

```

# Azure App Service with SQL Database and Application Insights

Starting point for building web application hosted in Azure App Service.

Provisions Azure SQL Database and Azure Application Insights to be used in combination
with App Service.

## Running the App

1. Create a new stack:

    ```bash
    $ pulumi stack init dev
    ```
    
    ```bash
    # if you want the stack to be created at the same time
    $ pulumi stack select dev -c
    ```

1. Login to Azure CLI (you will be prompted to do this during deployment if you forget this step):

    ```bash
    $ az login
    ```

1. Create a Python virtualenv, activate it, and install dependencies:

    This installs the dependent packages [needed](https://www.pulumi.com/docs/intro/concepts/how-pulumi-works/) for our Pulumi program.

    ```bash
    $ python3 -m venv venv
    $ source venv/bin/activate
    $ pip3 install -r requirements.txt
    ```

1. Define SQL Server password (make it complex enough to satisfy Azure policy):

    ```bash
    
    # generates Pulumi.dev.yaml and adds the vaules, if the file exists with the values you don't need to set the config.
    
    pulumi config set --secret sqlPassword <value>
    pulumi config set sqlUsername <value>
    
    #if the stack is created with `pulumi stack switch dev -c`
    pulumi config set azure:environment public
    pulumi config set azure:location AustraliaEast
    ```

1. Run `pulumi preview` to preview changes (Optional, Good for CI, Pull Requests):

    ``` bash
    $ pulumi preview
    ```

1. Run `pulumi up` to preview and deploy changes:

    ``` bash
    $ pulumi up
    Previewing changes:
    ...

    Performing changes:
    ...
    info: 7 changes performed:
        + 7 resources created
    Update duration: 1m14.59910109s
    ```

1. Check the deployed website endpoint:

    ```bash
    $ pulumi stack output endpoint
    https://azpulumi-as0ef47193.azurewebsites.net
    $ curl "$(pulumi stack output endpoint)"
    ```
 
 ### What if someone changes the resource from another interface?
 
 1. Remind kindly that you shouldn't touch the portal @$#%@^#@^@#^
 1. Run `pulumi refresh`
 1. Run `pulumi preview`
 1. Fix the diff
     

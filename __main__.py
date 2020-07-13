from pulumi import Config, export, asset, Output
from pulumi_azure import core, storage, appservice, appinsights, sql

import pulumi
env =  pulumi.get_stack()
appname = pulumi.get_project()

config = Config()
username = config.require("sqlUsername")
pwd = config.require("sqlPassword")

resource_group = core.ResourceGroup(appname +  '-' + env + '-rg')

sql_server = sql.SqlServer(
    resource_name=appname +  '-' + env + '-sql',
    resource_group_name=resource_group.name,
    administrator_login=username,
    administrator_login_password=pwd,
    version="12.0")

database = sql.Database(
    appname +  '-' + env + '-db',
    resource_group_name=resource_group.name,
    server_name=sql_server.name,
    requested_service_objective_name="S0")

connection_string = Output.all(sql_server.name, database.name, username, pwd) \
    .apply(lambda args: f"Server=tcp:{args[0]}.database.windows.net;initial catalog={args[1]};user ID={args[2]};password={args[3]};Min Pool Size=0;Max Pool Size=30;Persist Security Info=true;")


app_service_plan = appservice.Plan(
    appname +  '-' + env + '-asp',
    resource_group_name=resource_group.name,
    kind="App",
    sku={
        "tier": "Basic",
        "size": "B1",
    })

app_insights = appinsights.Insights(

    name=appname + '-' + env + '-sql', # bypass auto naming
    resource_name=appname +  '-' + env + '-ai',
    resource_group_name=resource_group.name,
    location=resource_group.location,
    application_type="web",
    retention_in_days=90)


webapp=appservice.AppService(
    appname +  '-' + env + '-webapp',
    resource_group_name=resource_group.name,
    app_service_plan_id=app_service_plan.id,
    app_settings={
        "ApplicationInsights:InstrumentationKey": app_insights.instrumentation_key,
        "APPINSIGHTS_INSTRUMENTATIONKEY": app_insights.instrumentation_key,
    },
    connection_strings=[{
        "name": "db",
        "type": "SQLAzure",
        "value": connection_string
    }]
)

export("endpoint", webapp.default_site_hostname.apply(
    lambda endpoint: "https://" + endpoint
))
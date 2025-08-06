from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.resource.resources.models import ResourceGroup
from azure.mgmt.storage import StorageManagementClient

import os

primary_subscription = os.environ.get("SUBSCRIPTION_ID")
resource_client = ResourceManagementClient(
    credential=DefaultAzureCredential(), 
    subscription_id=primary_subscription
    )
storge_client = StorageManagementCleint(
    crednetial=DefaultAzureCredential(),
    subscription_id=primary_subscription
)

rg = "pietestgonewonglol1233"
rg_location = "westus"
rg_setup = ResourceGroup(location=rg_location)

def new_storageaccount():
    try:
        print(f"Attempting to create Resource Group {rg}")
        resource_client.resource_groups.create_or_update(
        resource_group_name=rg,
        parameters=rg_setup
        )
        print(f"{rg} has been created!")

    except Exception as e:
        print("We ran into an issue creating to Resource Group, please read the errro below:")

def remove_storageaccount():
    try:
        print(f"Deleintg Resource Group {rg}")
        resource_client.resource_groups.begin_delete(
            resource_group_name=rg
        )
        print(f"It has been removed from this universe")
    
    except Exception as e:
        print("We ran into an issue")
        print({e})

match = "pie"

for each in resource_client.resource_groups.list():
    if match.lower() in each.name.lower():
        print(each.name.lower())
        resource_client.resource_groups.begin_delete(resource_group_name=each.name)


#new_storageaccount()
#remove_storageaccount()
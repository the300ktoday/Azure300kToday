from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.storage import StorageManagementClient
import os

primary_subscription = os.environ.get("SUBSCRIPTION_ID")

resource_client = ResourceManagementClient(
    credential=DefaultAzureCredential(), 
    subscription_id=primary_subscription
    )
storage_client = StorageManagementClient(
    credential=DefaultAzureCredential(),
    subscription_id=primary_subscription
)

rg = "rg-pietestgonewonglol"
sa = "sapietestgonewonglo1"


def new_resourcegroup():
    try:
        print(f"Attempting to create Resource Group {rg}")
        resource_client.resource_groups.create_or_update(
            resource_group_name=rg,
            parameters={
            "location": "west us"
            }
        )
        print(f"{rg} has been created!")

    except Exception as e:
        print("We ran into an issue creating to Resource Group, please read the errro below:")

def remove_resourcegroup():
    try:
        print(f"Deleintg Resource Group {rg}")
        resource_client.resource_groups.begin_delete(
            resource_group_name=rg
        )
        print(f"It has been removed from this universe")
    
    except Exception as e:
        print("We ran into an issue")
        print({e})

def new_storageaccount():
    try:
        print(f"Creating Storage Account {sa}")
        storage_client.storage_accounts.begin_create(
            resource_group_name=rg,
            account_name=sa,
            parameters= {
                "sku":{
                    "name": "Standard_LRS"
                },
                "kind": "StorageV2",
                "location": "west us",
                "access_tier": "Hot"
            }
        )

    except Exception as e:
        print("Something went wrong")
        print({e})

def new_staticsite():
    try:
        print("Creating static blob site")
        storage_client.blob_services.set_service_properties(
            resource_group_name=rg,
            account_name=sa,
            parameters= {
                "static_website": {
                    "enabled": True,
                    "index_document": "index.html",
                    "error_document_404_path": "404.html"
                }
            }
        )

    except Exception as e:
        print("Something went wrong")
        print({e})


#new_resourcegroup()
#new_storageaccount()
new_staticsite()
#remove_resourcegroup()
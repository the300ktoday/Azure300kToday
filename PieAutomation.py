from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.storage import StorageManagementClient
from azure.storage.blob import StaticWebsite, BlobServiceClient
import os

primary_subscription = os.environ.get("SUBSCRIPTION_ID")
bob_connect_string = os.environ.get("AZURE_STORAGE_CONNECTION_STRING")

resource_client = ResourceManagementClient(
        credential=DefaultAzureCredential(), 
        subscription_id=primary_subscription
    )
storage_client = StorageManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=primary_subscription
    )
blob_client = BlobServiceClient.from_connection_string(
        bob_connect_string
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
        print("We ran into an issue")
        print({e})

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
        static_site_settings = StaticWebsite(
            enabled=True,
            index_document="Index.html",
            error_document404_path="404.html"
        )
        blob_client.set_service_properties(static_website=static_site_settings)

    except Exception as e:
        print("Something went wrong")
        print({e})


#new_resourcegroup()
#new_storageaccount()
new_staticsite()
#remove_resourcegroup()
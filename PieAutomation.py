from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.storage import StorageManagementClient
from azure.storage.blob import StaticWebsite, BlobServiceClient
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

rg = "rg-wearereallyprogsing1"
sa = "sawearereallyprogsing1"


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
        new_storageaccount()

    except Exception as e:
        print("We ran into an issue")
        print({e})

def new_storageaccount():
    try:
        print(f"Creating Storage Account {sa}")
        poller = storage_client.storage_accounts.begin_create(
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
        poller.result()
        print("Storage account has been created")
        new_staticsite()

    except Exception as e:
        print("Something went wrong")
        print({e})

def new_staticsite():
    try:
        key_object = storage_client.storage_accounts.list_keys(rg, sa)
        key_1 = key_object.keys[0].value
        connection_key = f"DefaultEndpointsProtocol=https;AccountName={sa};AccountKey={key_1};EndpointSuffix=core.windows.net"
        blob_client = BlobServiceClient.from_connection_string(
            connection_key)

        print("Creating static blob site")
        static_site_settings = StaticWebsite(
            enabled=True,
            index_document="Index.html",
            error_document404_path="404.html"
        )
        blob_client.set_service_properties(
            static_website=static_site_settings
            )
        print("Static site settings have been setup")

    except Exception as e:
        print("Something went wrong")
        print({e})

def remove_resourcegroup():
    try:
        print(f"Deleintg Resource Group {rg}")
        poller = resource_client.resource_groups.begin_delete(
            resource_group_name=rg
        )
        poller.result()
        print(f"The resource group {rg} has been deleted")
    
    except Exception as e:
        print("We ran into an issue")
        print({e})

new_resourcegroup()
#remove_resourcegroup()

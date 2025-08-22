from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.storage import StorageManagementClient
from azure.storage.blob import StaticWebsite, BlobServiceClient, ContentSettings
from azure.mgmt.frontdoor import FrontDoorManagementClient
from azure.mgmt.frontdoor.models import (
    FrontDoor,
    RoutingRule,
    BackendPool,
    FrontendEndpoint,
    HealthProbeSettings,
    LoadBalancingSettings
)
import os

primary_subscription = os.environ.get("AZURE_SUBSCRIPTION_ID")
rg = "rg-timetokeepgoing101"
sa = "satimetokeepgoing101"
raw_file_404 = r"C:\Github\Azure300kToday\404.html"
raw_file_index = r"C:\Github\Azure300kToday\Index.html"
file_404 = os.path.basename(raw_file_404)
file_index = os.path.basename(raw_file_index)
fdname = "cdnisreallyworkingkinodertoten"
backend_host = "myresumeisonline0329.azurewebsites.net"
frontend_hostname = "myresumeisonline0329.azurefd.net"


resource_client = ResourceManagementClient(
        credential=DefaultAzureCredential(), 
        subscription_id=primary_subscription
    )
storage_client = StorageManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=primary_subscription
    )
frontdoor_client = FrontDoorManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=primary_subscription
    )
    
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
        print(e)

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
        print(e)

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
        new_sitefiles(blob_client)

    except Exception as e:
        print("Something went wrong")
        print(e)

def new_sitefiles(service_client):
    try:
        print(f"Attempting to add files to Container")
        container_name = "$web"
        container_client = service_client.get_container_client(container_name)
        blob_client = container_client.get_blob_client(file_index)
        file_type = ContentSettings(
            content_type="text/html"
        )
        with open(file_index, "rb") as data:
            blob_client.upload_blob(data, overwrite=True, content_settings=file_type)

        blob_client = container_client.get_blob_client(file_404)
        with open (file_404, "rb") as data:
            blob_client.upload_blob(data, overwrite=True, content_settings=file_type)
        new_frontdoor()
    
    except Exception as e:
        print("Something went wrong")
        print(e)

def new_frontdoor():
    backend_pool_name = "Thisisthebackend"
    backend_pool_settings = BackendPool(
        name=backend_pool_name,
        backends=[{
            "address": backend_host,
            "http_port": 80,
            "https_port": 443,
            "enabled_sate": "Enabled"
        }],
        health_probe_settings={
            "path": "/",
            "protocol": "Htpp",
            "interval_in_seconds": 30
        },
        load_balancing_settings={
            "sample_size": 4,
            "successful_samples_required": 2
        }
    )


    front_door_parameters = FrontDoor(
        location="westus",


    )

    frontdoor_client.front_doors.begin_create_or_update(
        resource_group_name=rg,
        front_door_name=fdname,
        front_door_parameters=
    )


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
        print(e)

#new_resourcegroup()
remove_resourcegroup()

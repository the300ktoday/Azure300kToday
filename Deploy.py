# Import the required libraries
from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient
import os

# Your environment variables will be picked up automatically
# The SDK uses the DefaultAzureCredential class to handle authentication
credential = DefaultAzureCredential()

# The subscription ID is also needed for the client
subscription_id = os.environ.get("SUBSCRIPTION_ID")

# Create a ResourceManagementClient
# This client object is your entry point to managing resources
resource_client = ResourceManagementClient(credential, subscription_id)

# Now, you can use the client to perform actions.
# The 'resource_groups' object has methods like 'list', 'create_or_update', 'delete', etc.
print("Listing all resource groups:")
for resource_group in resource_client.resource_groups.list():
    print(f"- {resource_group.name}")
    
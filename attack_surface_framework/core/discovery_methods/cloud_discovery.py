import boto3
from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient
from google.cloud import compute_v1

class CloudDiscovery:
    """
    Handles cloud resource discovery for AWS, Azure, and GCP.
    """

    @staticmethod
    def discover_aws():
        print("Discovering AWS assets...")
        ec2_client = boto3.client("ec2")
        response = ec2_client.describe_instances()
        assets = []
        for reservation in response["Reservations"]:
            for instance in reservation["Instances"]:
                assets.append({
                    "instance_id": instance["InstanceId"],
                    "public_ip": instance.get("PublicIpAddress"),
                    "state": instance["State"]["Name"],
                    "tags": instance.get("Tags", [])
                })
        return assets

    @staticmethod
    def discover_azure(subscription_id):
        print("Discovering Azure assets...")
        credential = DefaultAzureCredential()
        compute_client = ComputeManagementClient(credential, subscription_id)
        assets = []
        for vm in compute_client.virtual_machines.list_all():
            assets.append({
                "name": vm.name,
                "location": vm.location,
                "vm_id": vm.vm_id,
            })
        return assets

    @staticmethod
    def discover_gcp():
        print("Discovering GCP assets...")
        client = compute_v1.InstancesClient()
        assets = []
        project = "your-gcp-project-id"
        for zone in client.aggregated_list(project=project):
            for instance in zone.instances:
                assets.append({
                    "name": instance.name,
                    "zone": instance.zone,
                    "status": instance.status,
                })
        return assets

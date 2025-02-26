import click
import boto3
import os

AWS_PROFILE = 'allpower'
RDP_DIR = 'RDPFiles'
RDCMAN_FILE = 'AWS.rdg'

@click.group()
def main():
    """
    Simple CLI for creating remote desktop configuration files.
    """
    pass

@main.command()
def mac():
    """Creates Mac-compatible RDP files"""
    instances = get_instance_information()
    create_mac_rdp_files(instances)
    click.echo(f"Created RDP files for Mac in the '{RDP_DIR}' folder.")

@main.command()
def rdcman():
    """Creates Remote Desktop Connection Manager (.rdg) File"""
    instances = get_instance_information()
    create_rdcman_config(instances)
    click.echo(f"Created {RDCMAN_FILE}. Please import it into Remote Desktop Connection Manager.")

def get_instance_information():
    """Fetches Windows EC2 instances and their private IPs."""
    instances = {}
    session = boto3.Session(profile_name=AWS_PROFILE)
    ec2_client = session.client('ec2')
    
    try:
        reservations = ec2_client.describe_instances()
    except Exception as e:
        click.echo(f"Error fetching instances: {e}", err=True)
        return instances
    
    for reservation in reservations.get('Reservations', []):
        for instance in reservation.get('Instances', []):
            if instance.get('Platform') == 'windows':
                name = next((tag['Value'] for tag in instance.get('Tags', []) if tag['Key'] == 'Name'), instance['InstanceId'])
                ip_address = instance.get('PrivateIpAddress')
                if ip_address:
                    instances[name] = ip_address
    
    return instances

def create_rdcman_config(instances):
    """Generates an RDCMan configuration file."""
    servers = "".join(
        f"<server><properties><name>{ip}</name><displayName>{name}</displayName></properties></server>"
        for name, ip in instances.items()
    )
    
    rdcman_content = (
        '<?xml version="1.0" encoding="utf-8"?>'
        '<RDCMan programVersion="2.7" schemaVersion="3">'
        '<file><credentialsProfiles /><properties><expanded>True</expanded><name>Servers</name></properties>'
        '<group><properties><expanded>True</expanded><name>AWS Windows Servers</name></properties>'
        f'{servers}'
        '</group></file><connected /><favorites /><recentlyUsed /></RDCMan>'
    )
    
    with open(RDCMAN_FILE, 'w', encoding='utf-8') as file:
        file.write(rdcman_content)

def create_mac_rdp_files(instances):
    """Creates Mac-compatible RDP files."""
    os.makedirs(RDP_DIR, exist_ok=True)
    
    rdp_template = """gatewaybrokeringtype:i:0
use redirection server name:i:0
disable themes:i:0
disable cursor setting:i:0
disable menu anims:i:1
remoteapplicationcmdline:s:
redirected video capture encoding quality:i:0
audiocapturemode:i:0
prompt for credentials on client:i:0
remoteapplicationprogram:s:
gatewayusagemethod:i:2
screen mode id:i:2
use multimon:i:0
authentication level:i:2
desktopwidth:i:0
desktopheight:i:0
redirectclipboard:i:1
loadbalanceinfo:s:
enablecredsspsupport:i:1
promptcredentialonce:i:0
redirectprinters:i:0
autoreconnection enabled:i:1
administrative session:i:0
redirectsmartcards:i:0
authoring tool:s:
alternate shell:s:
remoteapplicationmode:i:0
disable full window drag:i:1
gatewayusername:s:
shell working directory:s:
audiomode:i:0
remoteapplicationappid:s:
username:s:
allow font smoothing:i:1
connect to console:i:0
gatewayhostname:s:
camerastoredirect:s:
drivestoredirect:s:
session bpp:i:32
disable wallpaper:i:0"""
    
    for name, ip in instances.items():
        rdp_content = f"{rdp_template}\nfull address:s:{ip}\ngatewayaccesstoken:s:"
        rdp_file_path = os.path.join(RDP_DIR, f"{name}.rdp")
        with open(rdp_file_path, 'w', encoding='utf-8') as file:
            file.write(rdp_content)

if __name__ == "__main__":
    main()

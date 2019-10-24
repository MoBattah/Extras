#Command-line application for automatically generating RDP files.
import click
import boto3
import os

@click.group()
def main():
    """
    Simple CLI for creating remote desktop configuration files
    """
    pass

@main.command()
def mac():
    """Creates Mac-compatible RDP files"""
    build_dictionary = get_instance_information()
    create_mac_rdp_files(build_dictionary)
    click.echo("Created RDP files for Mac")

@main.command()
def rdcman():
    """Creates Remote Desktop Connection Manager (.rdg) File"""
    build_dictionary = get_instance_information()
    create_rdcman_config(build_dictionary)
    click.echo("Created AWS.rdg")


def get_instance_information():
    instance_dictionary = {}
    session = boto3.Session(profile_name='allpower')
    ec = session.client('ec2')
    reservations = ec.describe_instances()
    for r in reservations['Reservations']:
        for i in r['Instances']:
            instance_id = i['InstanceId']
            try:
                if i['Platform'] == 'windows':
                    for t in i['Tags']:
                        if t['Key'] == 'Name':
                            instance_name = t['Value']
                            ip_address = i['PrivateIpAddress']
                            instance_dictionary[instance_name] = ip_address
            except KeyError:
                pass
    return instance_dictionary

def create_rdcman_config(build_dictionary):
    all_servers_string = ""
    for i in build_dictionary:
        server_string = "<server> <properties> <name>" + build_dictionary[i] + "</name> <displayName>" + i + "</displayName> </properties> </server>"
        all_servers_string = all_servers_string + server_string

    RDCManopen = "<?xml version=\"1.0\" encoding=\"utf-8\"?><RDCMan programVersion=\"2.7\" schemaVersion=\"3\"><file><credentialsProfiles /><properties><expanded>True</expanded><name>Servers</name></properties>"
    Ending = "</group> </file> <connected /> <favorites /> <recentlyUsed /> </RDCMan>"
    DevGroup = "<group> <properties> <expanded>True</expanded> <name>AWS Windows Servers</name> </properties>"
    file = open("AWS.rdg", "w+")
    file.write(RDCManopen + DevGroup + all_servers_string + Ending)
    file.close()

def create_mac_rdp_files(build_dictionary):
    cwd = os.getcwd()
    try:
        os.mkdir('RDPFiles')
    except FileExistsError:
        pass
    os.chdir('RDPFiles')
    for i in build_dictionary:
        filename = i + ".rdp"
        file = open(filename, 'w+')
        config_file = """gatewaybrokeringtype:i:0
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
disable wallpaper:i:0""" + "\nfull address:s:" + build_dictionary[i] + "\ngatewayaccesstoken:s:"
        file.write(config_file)
        file.close()


if __name__ == "__main__":
    main()

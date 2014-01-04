from CLI.HomityHubCLI import HomityHubCLI
from sys import exit, argv
from CLI.Common.utils import bool_or_string

from ConfigParser import SafeConfigParser, NoOptionError

client_config = {}
client_config_parser = SafeConfigParser()
client_config_parser.read('/etc/homity/homityclient.conf')

client_config['hostname'] = client_config_parser.get('homity_client','hostname')
client_config['username'] = client_config_parser.get('homity_client','username')
client_config['password'] = client_config_parser.get('homity_client','password')
client_config['use_ssl'] = bool_or_string(client_config_parser.get('homity_client','use_ssl'))
client_config['verify_ssl'] = bool_or_string(client_config_parser.get('homity_client','verify_ssl'))

def main():
    try:
        HomityHubCLI().main(argv[1:],client_config)

    except Exception as e:
        print(str(e))
        exit(1)

if __name__ == "__main__":
    main()
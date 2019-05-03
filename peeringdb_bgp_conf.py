# -*- coding: utf-8 -*-
"""
Following script will create a GET >> peeringdb API to generate BGP configurations
for all our routers
Run the script: python peeringdb_bgp_conf.py <INPUT ASN#>
Docker Container: docker run --rm -v $(pwd)/log:/log peeringdb <INPUT ASN#>

"""
import requests, json, sys, os
from jinja2 import Environment, FileSystemLoader
from datetime import datetime

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

log_datetime = str(datetime.now().strftime('%Y%m%d-%H%M%S'))


__author__ = "Mihir Mehta"
__copyright__ = "PEERINGDB_BGP"

__version__ = "1.0"
__maintainer__ = "Mihir Mehta"
__status__ = "Development"

def variable_def(variable):
    """
    :Global List of variables
    :param variable:
    :return:
    """
    variable_dict = { 'url_host': 'peeringdb.com' }

    return variable_dict[variable]

def peer_fetch(asn):
    url = 'https://' + variable_def('url_host') + '/api/'
    header = {'content-type': 'application/json'}
    try:
        response = requests.get(url + 'netixlan?asn=' + asn, headers=header, verify=False)
        parsedjson = json.loads(response.text)
        return parsedjson
    except Exception, e:
        print 'Log Error: ' + str(e)

def generateConfig(output,asn):
    """
    :summary: Generating BGP configuration base on Neighbor IP
    :param: list, string
    :rtype output file:
    """
    # Creating name of the output file
    new = 'router_config_' + str(asn) + '_' + log_datetime + '.cfg'

    # This line uses the current directory
    #output_directory = os.getcwd()
    output_directory = "/log/"

    # Check of the file exits:
    writepath = str(os.path.join(output_directory, new))

    # This line uses the current directory
    file_loader = FileSystemLoader('.')

    # Load the enviroment
    env = Environment(loader = file_loader)

    # Getting the template
    template = env.get_template('bgp_template.j2')
    with open(writepath, 'wb') as f:
        for i in output:
            # Add the varibles
            output = template.render(neighborIP=i[0], neighbor_desc=i[1], neighborASN=i[2])
            f.write(output)
            #print output

if __name__ == '__main__':

    fetchASN = sys.argv[1]
    output = peer_fetch(fetchASN)

    if not len(output['data']):
        print "UNKNOWN ASN NUMBER!"
        exit (-1)

    output = [(i["ipaddr4"],i["name"],i["asn"]) for i in output['data']]

    # Generating Configuration
    generateConfig(output,fetchASN)

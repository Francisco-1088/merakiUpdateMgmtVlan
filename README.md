# updateMgmtVlan
This script will quickly update the management VLANs of all Meraki devices of a certain family within a given network. The script uses action batches by default, so it should have no problem updating hundreds or thousands of devices at a time.

## Prerequisites

1. Active Cisco Meraki subscriptions in the orgs where the script will be run
2. API access enabled for these organizations, as well as an API Key with access to them. See how to enable [here](https://documentation.meraki.com/General_Administration/Other_Topics/Cisco_Meraki_Dashboard_API)
3. A working Python 3.0 environment
4. Install libraries in `requirements.txt`

Usage:
*Clone repo to your working directory with `git clone `
*Install libraries with `pip install -r requirements.txt`
*Update `config.py` file with your `api_key`, the desired `vlan_id` you will configure on the devices and the `product` family you wish to update (if looking to update Meraki APs, set this to MR, or if looking to update MS switches, set it to MS)
*Execute with `python main.py`
*When prompted, enter the number associated with the organization you wish to work in as displayed in the list
*When prompted, enter the number associated with the network you wish to work in as displayed in the list
*The script will tell you the number of devices of the selected family that will be updated, enter `Y` if you wish to proceed, or `N` if you wish to abort

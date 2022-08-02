import meraki
import config
import time

dashboard = meraki.DashboardAPI(config.api_key)

# Get Orgs
orgs = dashboard.organizations.getOrganizations()
print("Your API Key has access to the following organizations:")
i = 1
for org in orgs:
  print(f"{i} - {org['name']}")
  i = i+1

org_id = orgs[int(input("Type the number of the org you wish to work on: ")) - 1]['id']
print(f"Working on org {org_id}.")

# Get Networks
networks = dashboard.organizations.getOrganizationNetworks(org_id)
print("Your Org has the following networks:")
i = 1
for net in networks:
  print(f"{i} - {net['name']}")
  i = i+1

net_id = networks[int(input("Type the number of the network you wish to work on: ")) - 1]['id']
print(f"Working on net {net_id}.")

# Get Network Devices

devices = dashboard.networks.getNetworkDevices(net_id)

# Create actions list
actions = []

for device in devices:
    if config.product in device['model']:
        action = {
                "resource": f"/devices/{device['serial']}/managementInterface",
                "operation": "update",
                "body": {
                    "wan1": {
                        "wanEnabled": "not configured",
                        "usingStaticIp": False,
                        "vlan": config.vlan_id
                    },
                }
            }
        actions.append(action)

update_devices = [devices for device in devices if config.product in device['model']]
print(len(update_devices))

choice = input(f"This will update the management VLAN on {len(update_devices)} {config.product} devices to {config.vlan_id}. Proceed? (Y/N)")

if choice == 'Y':
    for i in range(0, len(actions), 100):
        # Check for unfinished batches
        j = False
        while not j:
            print("Checking for unfinished batches")
            current_batches = dashboard.organizations.getOrganizationActionBatches(org_id)
            unfinished_batches = []
            for b in current_batches:
                if b['status']['completed'] == False and b['status']['failed'] == False:
                    unfinished_batches.append(b)
            if len(unfinished_batches) > 4:
                j = False
                print(f"You have {len(unfinished_batches)} unfinished batches:")
                for item in unfinished_batches:
                    print(item['id'])
                print("Waiting to complete some of these before scheduling a new one!")
                time.sleep(10)
            elif len(unfinished_batches) <= 4:
                j = True
        subactions = actions[i:i + 100]
        dashboard.organizations.createOrganizationActionBatch(
            organizationId=org_id,
            actions=subactions,
            confirmed=True,
            synchronous=False
        )
        time.sleep(1)

elif choice == 'N':
    print('Script aborted by user.')
    exit()

else:
    print('Invalid input.')
    exit()

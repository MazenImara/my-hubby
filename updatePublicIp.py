
import requests
from requests.auth import HTTPBasicAuth
import json

PublicIpUrl = 'http://ip.42.pl/raw'
DomainApiUrl = 'https://api.name.com/v4/domains/your-choice.today/url/forwarding'
User = 'mazen.imara'
Token = '8489e7bd64aeeacc86739d4964ab0676a540ec2d' 


def checkIp():
	publicIp = None
	oldIp = None
	status = False
	try:
		publicIp = requests.get(PublicIpUrl).text
	except requests.exceptions.RequestException as e:
		print(e)

	if publicIp:
		try:
			host =getHosts()[0]
			oldIp = host['forwardsTo'].replace('http://', '')
			oldIp = oldIp.split(':')[0]
		except Exception as e:
			print(e)
			
	#publicIp = '192.168.1.1'
	if publicIp and oldIp and publicIp != oldIp:
		status = True
	result = {
		'status': status,
		'newIp': publicIp,
		'oldIp': oldIp

	}
	return result

def getHosts():
	urls = None
	try:
		auth=HTTPBasicAuth(User, Token)
		r = requests.get(DomainApiUrl, auth=auth)
	except requests.exceptions.RequestException as e:
		print(e)

	try:
		urls = r.json()['urlForwarding']		
	except Exception as e:
		print(e)

	if urls != None and len(urls) == 0:
		urls = None
	return urls



def updateUrl(host, urlTo, type):
	res = None
	data = json.dumps({
		'forwardsTo': urlTo,
		'type': type
	})
	try:
		auth=HTTPBasicAuth(User, Token)
		r = requests.put(DomainApiUrl + '/' + host, data=data, auth=auth)
		res = r.text
	except requests.exceptions.RequestException as e:
		print(e)
	print(res)


def updateIp():
	checkip = checkIp()
	hosts = getHosts()	
	if checkip and hosts and checkip['status']:
		print(checkip)
		for host in hosts:
			updateUrl(
				host['host'], 
				host['forwardsTo'].replace(checkip['oldIp'], checkip['newIp']),
				host['type']
			)

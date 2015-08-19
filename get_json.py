#!usr/bin/env python
#-*-coding:utf-8-*-
import json
import urllib

def getJson(url):
	page = urllib.urlopen(url)
	get_json = page.read()
	data = json.loads(get_json)
	return data


def main():
	rid = raw_input("Please input room id:")
	url = "http://api.douyutv.com/api/client/room/"+rid
	data = getJson(url)
	if data['error'] != 0: 
		raise Exception("GET_JSON_ERROR")
	data_string = json.dumps(data,sort_keys=True,indent=2)
	print data_string

if __name__ == "__main__":
	main()

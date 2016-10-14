# scanviz
Network Scan Visualization - Experimental Application

## What is this?
Simple web application for the visualization of nmap scans. Stores scans to Elasticsearch.

## How to use?
Upload your scans, then see visualization. Search scans by hostname in search page


## Features
* Pie chart visualization of all open ports as specified by a date/time range. Range defaults to all time if not set.

* Storage of network scans to Elasticsearch. Scans should be strictly in **JSON format** [specified here](##Scan Format).

* Searching of scans stored in Elasticsearch by hostname.

---

## Development

This is a Flask Application that makes use of d3js for visualization and Elasticsearch for storage.

### Deployment

#### Local Deployment

Get an instance of Elasticsearch running in your local machine.

Refer to [this page](https://www.elastic.co/guide/en/elasticsearch/guide/current/running-elasticsearch.html) for setting it up. Also [the elastic download page](https://www.elastic.co/downloads/elasticsearch) for the various releases of Elasticsearch.

Once you have that set up, install the dependencies specified in `requirements.txt`.

```
pip install -r requirements.txt
```

After which you should be able to run the application. The source includes a script that runs the application through Flask's built in web server. This runs the application in for development.

```
python run.py
```


#### Cloud Deployment

*under construction...*


### Configuration

Refer to `config.py` for the configuration. I might add the config for host IP and port of elasticsearch there later in case you don't plan to use the defaults.

By default scans are stored in the following index and type:
`index = 'dfir'`
`doc type = 'scan'`

## Scan Format
Below is an example JSON scan format.
```
{
	"status": {
		"state": "up",
		"reason": "user-set"
	},
	"vendor": {},
	"addresses": {
		"ipv4": "104.79.64.197"
	},
	"tcp": {
		"80": {
			"product": "",
			"state": "open",
			"version": "",
			"name": "http",
			"conf": "3",
			"extrainfo": "",
			"reason": "syn-ack",
			"cpe": ""
		},
		"443": {
			"product": "",
			"state": "open",
			"version": "",
			"name": "https",
			"conf": "3",
			"extrainfo": "",
			"reason": "syn-ack",
			"cpe": ""
		}
	},
	"datetime": "2016-10-04 21:38:55.168576",
	"hostnames": [{
		"type": "user",
		"name": "www.0tks43.com"
	}]
}
```

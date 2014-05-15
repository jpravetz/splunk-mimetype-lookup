Splunk external lookup scripts
=============================

External lookup script to map:
* mime types to a more generic file type.
* URLs to hostnames (eg. to 'box.com')
A python script is used instead of a csv file so that regex can be used.

Installation
------------

Refer to [Splunk documentation](http://docs.splunk.com/Documentation/Splunk/6.0.2/Knowledge/Addfieldsfromexternaldatasources).

Copy the files mimetype_lookup.py and/or host_lookup.py to $SPLUNK_HOME/etc/searchscripts

Add the following lines to the existing (or new) file $SPLUNK_HOME/etc/system/local/transforms.conf

```
[MimeTypeLookup]
external_cmd = mimetype_lookup.py mimeType fileType
external_type = python
fields_list = mimeType,fileType
# filename = mimetypes.csv
max_matches = 1
min_matches = 0

[HostUrlLookup]
external_cmd =host_lookup.py url host
external_type = python
fields_list = url,host
# filename = hostUrl.csv
max_matches = 1
min_matches = 0

```

Add the following lines to the existing (or new) file $SPLUNK_HOME/etc/system/local/props.conf

```
[mimetype_lookup]
lookup_mimetype = MimeTypeLookup mimeType OUTPUT fileType

[=host_lookup]
lookup_host = HostUrlLookup url OUTPUT host
```

Use this mimetype lookup syntax in searches: ```lookup MimeTypeLookup mimeType```
Use this hostname lookup syntax in searches: ```lookup HostUrlLookup url```





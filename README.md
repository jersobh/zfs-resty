## Rest API for ZFS

### Usage
**Must be run as root**

#### Endpoints

##### /auth
method: POST
params: 
 - username: system username
 - password: user's password

##### /create-pool
method: POST
params:
 - name: Pool name

##### /delete-pool
method: POST
params:     
 - name: Pool name

##### /status
method: GET

##### /io-status
method: GET

##### /add-disk
method: POST
params:     
 - pool: Pool name
 - device: device path eg.: /dev/sdx

##### /add-spare-disk
method: POST
params:
 - pool: Pool name
 - device: device path eg.: /dev/sdx

##### /replace-disk
method: POST
params:
 - pool: Pool name
 - old_device: device path eg.: /dev/sdx
 - new_device: device path eg.: /dev/sdx

##### /mountpoint
method: POST
params:
 - mountpoint: mountpoint path eg.: /path/to/mountpoint 
 - pool: Pool name


#### Authentication
ZFS-Resty uses JWT. To authenticate send a POST request to /auth

#### Args 
```
-p, --port: set the http port (default 8089)
-s, --safe: true/false, (default false) Allow only local network ip's

#### Install requirements and run
```
$ pip install -r requirements.txt
$ sudo python zfs-resty.py <args>

```

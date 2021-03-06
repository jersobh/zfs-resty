![alt text](https://raw.githubusercontent.com/jersobh/zfs-resty/master/logo.png "Logo")

## Rest API for ZFS

### Usage
**Must be run with root privileges**  
All parameters are json parameters. Eg.:
{ 
  "username": "admin",
  "password": "admin"
}

#### Endpoints

##### /auth
Authentication endpoint. Returns a token to be used on Authorization header.  
method: **POST**  
params: 
 - username: system username
 - password: user's password

##### /create-pool
Create a zfs pool  
method: **POST**  
params:
 - name: Pool name

##### /delete-pool
Delete a pool  
method: **POST**  
params:     
 - name: Pool name

##### /devices
Get available devices devices  
method: **GET**  

##### /status
method: **GET**  

##### /io-status
method: **GET**  

##### /add-disk
Add a new disk to pool 
method: **POST**  
params:     
 - pool: Pool name
 - device: device path eg.: /dev/sdx

##### /add-spare-disk
Add a spare disk that will be used in place of a corrupted disk  
method: **POST**  
params:
 - pool: Pool name
 - device: device path eg.: /dev/sdx

##### /replace-disk
method: **POST**  
params:
 - pool: Pool name
 - old_device: device path eg.: /dev/sdx
 - new_device: device path eg.: /dev/sdx

##### /mountpoint
method: **POST**  
params:
 - mountpoint: mountpoint path eg.: /path/to/mountpoint 
 - pool: Pool name


#### Authentication
ZFS-Resty uses JWT. To authenticate send a POST request to /auth. A token will be returned and should be sent for all request's headers as "Authorization: <token>".

#### Args 
```
-p, --port: set the http port (default 8089)
-s, --safe: true/false, (default false) Allow only local network ip's
```

#### Install requirements and run
```
$ pip install -r requirements.txt
$ sudo python zfs-resty.py <args>

```

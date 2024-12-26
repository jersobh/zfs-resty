# ZFS-Resty

![ZFS Resty Logo](https://raw.githubusercontent.com/jersobh/zfs-resty/master/logo.png "Logo")

## Overview
ZFS-Resty is a RESTful API for managing ZFS pools and devices. The application provides endpoints for authentication, creating pools, managing disks, and retrieving ZFS status information.

**Note**: This application requires **root privileges** for certain operations, such as managing ZFS pools.

---

## Table of Contents
- [Endpoints](#endpoints)
- [Authentication](#authentication)
- [Arguments](#arguments)
- [Installation](#installation)
- [Usage](#usage)
- [Examples](#examples)
- [License](#license)

---

## Endpoints

### **Authentication**
Authenticate and retrieve a JWT token for subsequent requests.

- **Endpoint**: `/auth`
- **Method**: `POST`
- **Parameters**:
  - `username` (string): System username
  - `password` (string): User password

---

### **Pool Management**

#### Create a ZFS Pool
- **Endpoint**: `/create-pool`
- **Method**: `POST`
- **Parameters**:
  - `name` (string): Pool name
  - `raid` (string, optional): RAID type
  - `devices` (list): Device paths (e.g., `/dev/sda`)

#### Delete a Pool
- **Endpoint**: `/delete-pool`
- **Method**: `POST`
- **Parameters**:
  - `name` (string): Pool name

#### Add Disk to Pool
- **Endpoint**: `/add-disk`
- **Method**: `POST`
- **Parameters**:
  - `pool` (string): Pool name
  - `device` (string): Device path (e.g., `/dev/sdx`)

#### Add Spare Disk
- **Endpoint**: `/add-spare-disk`
- **Method**: `POST`
- **Parameters**:
  - `pool` (string): Pool name
  - `device` (string): Device path (e.g., `/dev/sdx`)

#### Replace a Disk
- **Endpoint**: `/replace-disk`
- **Method**: `POST`
- **Parameters**:
  - `pool` (string): Pool name
  - `old_device` (string): Path of the old device
  - `new_device` (string): Path of the replacement device

#### Set Mountpoint
- **Endpoint**: `/mountpoint`
- **Method**: `POST`
- **Parameters**:
  - `mountpoint` (string): Mountpoint path (e.g., `/mnt/pool`)
  - `pool` (string): Pool name

---

### **Status and Information**

#### Get Available Devices
- **Endpoint**: `/devices`
- **Method**: `GET`

#### Get ZFS Pool Status
- **Endpoint**: `/status`
- **Method**: `GET`

#### Get I/O Status
- **Endpoint**: `/io-status`
- **Method**: `GET`

---

## Authentication
ZFS-Resty uses JWT for authentication. To authenticate:
1. Send a `POST` request to `/auth` with your system `username` and `password`.
2. A token will be returned in the response.
3. Include this token in the `Authorization` header of all subsequent requests:
   ```
   Authorization: <token>
   ```

---

## Arguments
The application supports the following command-line arguments:

- `-p`, `--port`: Set the HTTP port (default: `8089`).
- `-s`, `--safe`: Restrict access to local network IPs (default: `false`).

---

## Installation

### Using the Install Script
1. Run the installation script:
   ```bash
   chmod +x install.sh
   ./install.sh
   ```

### Manual Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/jersobh/zfs-resty.git
   cd zfs-resty
   ```

2. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   sudo python zfs-resty.py
   ```

---

## Examples

### Authenticate
Request:
```bash
curl -X POST http://localhost:8089/auth -H "Content-Type: application/json" -d '{"username": "admin", "password": "admin"}'
```

Response:
```json
{
  "token": "your-jwt-token"
}
```

### Create a Pool
Request:
```bash
curl -X POST http://localhost:8089/create-pool -H "Authorization: Bearer <token>" -H "Content-Type: application/json" -d '{"name": "mypool", "raid": "mirror", "devices": ["/dev/sda", "/dev/sdb"]}'
```

Response:
```json
{
  "success": "Pool 'mypool' created successfully"
}
```

---

## License
This project is licensed under the MIT License.

---

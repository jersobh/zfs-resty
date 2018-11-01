import asyncio


# Create a Pool
async def create_pool(name='default-pool', mode='', devices=''):
    cmd = f'zpool create {name} {mode} {devices}'
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)

    stdout, stderr = await proc.communicate()

    if stdout:
        return stdout.decode()
    if stderr:
        return stderr.decode()


# Delete Pool
async def delete_pool(name):
    cmd = f'zpool destroy {name}'
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)

    stdout, stderr = await proc.communicate()

    if stdout:
        return stdout.decode()
    if stderr:
        return stderr.decode()


# Get Pool status
async def get_status():
    cmd = 'zpool status'
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)

    stdout, stderr = await proc.communicate()

    if stdout:
        return stdout.decode()
    if stderr:
        return stderr.decode()


# Get HDD devices info
async def get_disk_info():
    cmd = 'fdisk -l'
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)

    stdout, stderr = await proc.communicate()

    if stdout:
        result = {}
        output = stdout.decode()

        for line in output.split("\n"):
            if not line.startswith("/"):
                continue
            parts = line.split()

            inf = {}
            if parts[1] == "*":
                inf['bootable'] = True
                del parts[1]
            else:
                inf['bootable'] = False
            inf['start'] = int(parts[1])
            inf['end'] = int(parts[2])
            inf['blocks'] = int(parts[3].rstrip("+"))
            inf['size'] = parts[4]
            inf['type'] = " ".join(parts[6 :])
            result[parts[0]] = inf
        return result
    if stderr:
        return stderr.decode()


# Get pool I/O stats
async def get_IO_stats(pool):
    cmd = f'zpool iostat -v {pool}'
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)

    stdout, stderr = await proc.communicate()

    if stdout:
        return stdout.decode()
    if stderr:
        return stderr.decode()


# Add a new disk to pool
async def add_new_disk(pool, device):
    cmd = f'zpool -f add {pool} {device}'
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)

    stdout, stderr = await proc.communicate()

    if stdout:
        return stdout.decode()
    if stderr:
        return stderr.decode()


# Add a spare disk
async def add_spare_disk(pool, device):
    cmd = f'zpool -f create {pool} spare {device}'
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)

    stdout, stderr = await proc.communicate()

    if stdout:
        return stdout.decode()
    if stderr:
        return stderr.decode()


# Replace a corrupted disk
async def replace_disk(pool, old_device, new_device):
    cmd = f'zpool replace {pool} {old_device} {new_device}'
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)

    stdout, stderr = await proc.communicate()

    if stdout:
        return stdout.decode()
    if stderr:
        return stderr.decode()


# set custom mountpoint
async def set_mountpoint(mountpoint, pool):
    cmd = f'zpool set mountpoint={mountpoint} {pool}'
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)

    stdout, stderr = await proc.communicate()

    if stdout:
        return stdout.decode()
    if stderr:
        return stderr.decode()


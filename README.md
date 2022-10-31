# Recover NightOwl SVR Password
This script recovers the admin password for the NightOwl F6-series of devices, using a documented master password. The master password is useful for regaining access to the device, but in order to reset the actual admin password, or make any system changes, you need a valid admin-level account. This script *should* get that for you, otherwise you can capture network packets while you visit the Users section to get the password.

<img width="759" alt="nightOwl" src="https://user-images.githubusercontent.com/1743650/198940392-7006054c-d45f-4fd4-a137-f12215b90370.png">

## Good Recovery:
```
% ./NightOwl_F6-get-admin-password.py -t 10.1.1.5

Target: 10.1.1.5
Port:   9000
Verbose: False

Seems like it took the master pass, let's proceed.

Stored creds:

USERNAME: admin
PASSWORD: 4321abcd
```

## Failed Recovery:
```
% ./NightOwl_F6-get-admin-password.py -t 10.1.1.5

Target: 192.168.1.246
Port:   9000
Verbose: False

Something went wrong, exiting script...
```

For other potential master passwords, see: https://support.nightowlsp.com/hc/en-us/articles/360009216554-Night-Owl-Legacy-Devices

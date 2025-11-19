<!-- # KEF Wireless Speaker Control (LS50WII, LSX II and LS60) -->

# KEF Wireless Speaker Control for LS50WII, LSX II and LS60

## Description

A media player component for Home Assistant that controls a KEF Wireless Speaker.

Supports the following devices:
- LSX II
- LS50WII (untested)
- LS60 (untested)

## Manual installation

1. Open the directory (folder) for your HA configuration (where you find configuration.yaml).
2. If you do not have a custom_components directory (folder) there, you need to create it.
3. In the custom_components directory (folder) create a new folder called kef_control.
4. Download all the files from the custom_components/kef_control/ directory (folder) in this repository.
5. Place the files you downloaded in the new directory (folder) you created.
6. Add the following to your configuration.yaml:

```yaml
media_player:
  - platform: kef_control
    host: "192.168.1.100" # IP address of your KEF speaker
```
7. Restart Home Assistant

## Credits

This component is based heavily on the work of @N0ciple and their [pykefcontrol](https://github.com/N0ciple/pykefcontrol) library.

## Disclaimer

This component is not provided, supported or maintained by any of the companies named above. They can change their hardware, software or web services at a way that can break this component. Fingers crossed!

Devices other than the LSX II haven't been tested and may have issues, since I don't have any to test with.

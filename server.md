# Build the Robot on the Server

## Rent a Server

Make sure:

- Ubuntu 22.04 LTS.
- Has a GPU with at **least** 24 GB of memory.

## Start the code

See [instructions-quick start](./README.md#quick-start).

## Check that GPU is using

```bash
nvidia-smi
```

The output should resembles this in terms of GPU usage:

```
Sun Jul 28 14:21:02 2024       
+---------------------------------------------------------------------------------------+
| NVIDIA-SMI 535.129.03             Driver Version: 535.129.03   CUDA Version: 12.2     |
|-----------------------------------------+----------------------+----------------------+
| GPU  Name                 Persistence-M | Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp   Perf          Pwr:Usage/Cap |         Memory-Usage | GPU-Util  Compute M. |
|                                         |                      |               MIG M. |
|=========================================+======================+======================|
|   0  NVIDIA GeForce RTX 4090        On  | 00000000:3D:00.0 Off |                  Off |
| 31%   32C    P2              66W / 450W |  22685MiB / 24564MiB |      0%      Default |
|                                         |                      |                  N/A |
+-----------------------------------------+----------------------+----------------------+
                                                                                         
+---------------------------------------------------------------------------------------+
| Processes:                                                                            |
|  GPU   GI   CI        PID   Type   Process name                            GPU Memory |
|        ID   ID                                                             Usage      |
|=======================================================================================|
+---------------------------------------------------------------------------------------+
```

## Add Proxy Configuration (Optional)

To further speed up the server, you can add a proxy configuration.

### Install a Proxy Server (Clash)

```bash
wget https://down.clash.la/Clash/Core/Releases/clash-linux-amd64-v3-v1.18.0.gz -O clash.gz
gzip -d clash.gz
chmod +x clash
mv clash /usr/local/bin
```

### Create a Configuration File

```bash
mkdir -p ~/.config/clash
vim ~/.config/clash/config.yaml # copy your Clash subscription configuration here
wget https://cdn.jsdelivr.net/gh/Dreamacro/maxmind-geoip@release/Country.mmdb -O Country.mmdb
mv Country.mmdb ~/.config/clash
```

Make sure that your proxy server has **rules**, since we will both access GLM and GPT. You can use the following rule configuration:

```yaml
proxy-groups:
  - name: 'America'
    type: select
    proxies:
      - ...

rules:
    - DOMAIN-SUFFIX,openai.com,America
    - DOMAIN-SUFFIX,cn,DIRECT
    - ...
```

### Run the Proxy Server

```bash
clash -d ~/.config/clash
```

### Check the Proxy Server

```bash
export http_proxy=http://127.0.0.1:7890
export https_proxy=http://127.0.0.1:7890
curl -I https://www.google.com
```

### Set the Proxy Server as a System Service (Optional)

You can set the proxy server as a system service so you don't have to start it manually every time.

```bash
sudo nano /etc/systemd/system/clash.service
```

Add this into the file:

```ini
[Unit]
Description=Clash Proxy
After=network.target

[Service]
Type=simple
ExecStart=/usr/local/bin/clash -d /home/your-username/.config/clash
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Then run:

```bash
sudo systemctl enable clash
sudo systemctl start clash
```
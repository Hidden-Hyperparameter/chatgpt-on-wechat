# Build the Robot on the Server

## Rent a Server

Make sure:

- The server has a public static IP address.
- Ubuntu 22.04 LTS.
- Has a GPU with at least 24 GB of memory.

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
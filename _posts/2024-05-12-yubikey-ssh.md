---
layout: post
title: "Using your Yubikey for SSH"
date: 2024-05-12 17:30:00 -0300
tags: [Security, Computers]
description: Elevate your security guards with a Yubikey
---

Yubikey is a great security product. They are also very reliable. My first Yubikey is still working and has been in service for almost ten years. In addition to their capabilities of hardware-based second-factor authentication, they can also be used to sign in servers with SSH.

![Yubikey AI generated image](/assets/images/yubikey-1/header.jpeg)


In this post, I want to talk about the [resident or discoverable mode](https://developers.yubico.com/Passkeys/Passkey_concepts/Discoverable_vs_non-discoverable_credentials.html) of storing SSH keys, this way you store the private key inside the Yubikey. A Yubikey 5 can hold a maximum of 25 keys (one key per slot).

- [Understanding the counter effects](#understanding-the-counter-effects)
- [Requirements](#requirements)
- [Generating the key](#generating-the-key)
- [Adding the new key](#adding-the-new-key)
- [Managing your keys with ykman](#managing-your-keys-with-ykman)


# Understanding the counter effects

Depending on your threat model, you may prefer to use the non-resident or non-discoverable mode, where the Yubikey doesn't hold the private key; thus, if the Yubikey gets lost or stolen, an attacker could export the private key from it if it is not appropriately secured. While this does not make me happy, I prefer to take that risk and keep my private key available across computers.


# Requirements
* Ykman installed.
* A Yubkey 5 with firmware > 5.2.3 and already set up with a pin.

# Generating the key
Depending on your needs, the Yubkey can be configured with different security factors. You must decide what's your approach; here's a list from less secure to most secure:

**No PIN or touch required**

```bash
ssh-keygen -t ed25519-sk -O resident -O no-touch-required
```

**No touch, but PIN required**

```bash
ssh-keygen -t ed25519-sk -O resident -O verify-required -O no-touch-required
```

**No PIN, but touch required**

```bash
ssh-keygen -t ed25519-sk -O resident
```

**PIN and touch are required**

```bash
ssh-keygen -t ed25519-sk -O resident -O verify-required
```

You can also play with other options, such as `-O application=ssh:Yourtexthere`, to add a `Yourtexthere` description to your key.

# Adding the new key

First, start an `ssh-agent`, then add the Yubikey key into your system.

```bash
eval "$(ssh-agent -s)"
ssh-add -K
```

If you want to add the key persistently in your system, use `ssh-keygen -K`. Bear in mind that this command will dump your private key into your `pwd`. Note that the private key is still protected with the Yubikey; by itself, it is useless.

You can also add it to the SSH configuration and other keys, where my Secure Enclave key first runs and then the Yubikey FIDO2 key.

```
host *.home
    IdentityFile ~/.ssh/sekey-ssh.pub
    IdentityFile ~/.ssh/id_ed25519_sk_rk
    User nico
    IdentitiesOnly yes
```

SSH Login example:

```bash
% ssh bastion.home
sign_and_send_pubkey: signing failed for ECDSA "/Users/nico/.ssh/sekey-ssh.pub" from agent: communication with agent failed
Confirm user presence for key ED25519-SK SHA256:KVqby93OXhl+yIRd2FRjB8cXVYQ/xX0wqhO1oo6lhPQ
User presence confirmed
Welcome to Ubuntu 22.04 LTS (GNU/Linux 6.5.11-4-pve x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage
Last login: Sun May 12 20:55:24 2024 from 192.168.1.251
nico@bastion:~$
```

# Managing your keys with ykman
These are some useful commands to check and delete your keys if needed.

```bash
% ykman fido credentials list

Enter your PIN:
Credential ID  RP ID         Username              Display name
58a4065c...    redacted.com  info@redacted.cloud  ...
56d50dc9...    ssh:          openssh               openssh
```

To delete an existing key, use `delete`

```bash
% ykman fido credentials delete 56d50dc9
```
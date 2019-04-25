# Writeup #1

## Contexte

L'ISO fournie est executé dans *VirtualBox* avec un adaptateur
réseau attaché sur **Bridged Adapter** sur **en0: Ethernet** afin
de pouvoir travailler sur le poste en local.

## Collecte d’informations

### Analyse de la VM

VirtualBox fournit des outils en ligne de commande permettant
de query certaines informations a propos de la VM. Il est possible
dans un premier temps de récuperer la version du **kernel/release** ainsi
que son IP associé via de simples commandes:

```bash
VBoxManage guestproperty enumerate $VM_NAME | grep "OS/Release"
VBoxManage guestproperty enumerate $VM_NAME | grep "V4/IP"
```

Ce qui nous donne:

```
Name: /VirtualBox/GuestInfo/OS/Release, value: 3.2.0-91-generic-pae [...]
Name: /VirtualBox/GuestInfo/Net/0/V4/IP, value: 10.11.200.46 [...]
```

## La recherche de vulnérabilités

## L’exploitation

## La post exploitation

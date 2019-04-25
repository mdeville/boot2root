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

Dans le cas ou les guests additions de VirtualBox ne sont pas installes sur la
machine virtuelle, il faudra alors recuperer l'adresse MAC de la machine
(Settings -> Network -> Advanced -> MAC address)

Et ensuite executer les commandes suivantes:

```
ANALYSER_IP=$(hostname -I | cut -d" " -f1)
netdiscover -r $ANALYSER_IP/24
```

De la on doit avoir l'adresse IP ainsi que l'adresse MAC de la machine
virtuelle.

D'autre part, lors du démarage de la machine virtuelle, il est possible
en restant appuyé sur la touche **Shift** d'accéder au menu de boot afin
de pouvoir lancer le kernel du système manuellement, et optionnellement lui
passer certains paramètres.

![Boot Menu](https://raw.githubusercontent.com/deville-m/boot2root/master/.github/boot1.png)

## La recherche de vulnérabilités

### Recuperation de la version du du daemon OpenSSH

Lors d'une connection simple avec **netcat**, le serveur renvois
d'apres la [RFC](http://www.openssh.com/txt/rfc4253.txt) une **identification string**

```
[...]
4.2.  Protocol Version Exchange

   When the connection has been established, both sides MUST send an
   identification string.  This identification string MUST be

      SSH-protoversion-softwareversion SP comments CR LF
[...]
```

De ce fait, il est possible via l'IP recuperee precedement d'en
connaitre sa version:

```bash
nc -w1 $TARGET 22
```

Ce qui nous donne:

```
SSH-2.0-OpenSSH_5.9p1 Debian-5ubuntu1.7
```

### Scanning de port

En utilisant l'outil **Nmap**, il est possible d'effectuer un scan
plus avance avec des informations sur les services bindes sur l'host.

```bash
nmap -A -T4 -Pn --reason -vvv $TARGET
```

A partir de la sortie du logiciel, nous pouvons determiner l'existance
de plusieurs services sur la machine virtuelle (sortie tronque):

```
[...]
21/tcp  open  ftp      syn-ack vsftpd 2.0.8 or later
  |_ftp-anon: got code 500 "OOPS: vsftpd: refusing to run with writable root inside chroot()".
22/tcp open ssh syn-ack OpenSSH 5.9p1 Debian 5ubuntu1.7 (Ubuntu Linux; protocol 2.0)
[...]
80/tcp  open  http     syn-ack Apache httpd 2.2.22 ((Ubuntu))
  | http-methods:
  |_  Supported Methods: GET HEAD POST OPTIONS
  |_http-server-header: Apache/2.2.22 (Ubuntu)
  |_http-title: Hack me if you can
143/tcp open imap syn-ack Dovecot imapd
[...]
993/tcp open ssl/imap syn-ack Dovecot imapd
Service Info: Host: 127.0.1.1; OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

### Liste des services

- OpenSSH [OpenSSH 5.9p1 Debian 5ubuntu1.7]
- VSFTPD [vsftpd 2.0.8 or later]
- Apache HTTPD + SSL [Apache httpd 2.2.22 Ubuntu]
- Dovecot IMAPD + SSL [UNKNOWN]

### Recherche de vulnerabilites

A partir de la liste des services, il est desormais possible de
rechercher des CVE a l'aide de l'outil searchsploit:

```bash
QUERY=(
	"OpenSSH 5.9p1"
	"vsftpd 2.0.""
	"Apache httpd 2.2""
)

for i in "${QUERY[@]}"; do
    searchsploit $i
done
```

## L’exploitation

Comme nous avons pu remarquer, il nous est possible de modifier
les parametres du kernel. En lisant la [documentation](https://www.kernel.org/doc/Documentation/admin-guide/kernel-parameters.txt)
une option peut nous paraitre bien interessante:

```
	init=		[KNL]
			Format: <full_path>
			Run specified binary instead of /sbin/init as init
			process.
```

De ce fait il nous est possible de remplacer le binaire d'**init** par un autre
comme par exemple un shell:



## La post exploitation

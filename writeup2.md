# Writeup #2

Comme nous avons vu dans l'ancien writeup, il
nous a ete possible de devenir **root** en remplacant
simplement le binaire d'**init** par un shell dans les paramètres
kernel.

A partir du shell root, nous pouvons désormais naviguer
dans le filesystem.

## Recherche

En fouinant dans différents dossiers, nottement dans les **$HOME**
utilisateurs, nous pouvons remarquer un dossier assez intéressant:

![Dossier IMAP](https://raw.githubusercontent.com/deville-m/boot2root/master/.github/mail1.png)

Le dossier possede la nomenclature d'un dossier **IMAP**, cohérent du
fait qu'un daemon tourne actuellement sur le serveur. En lisant
les mails envoyés, nous pouvons remarquer une information assez
*sensible*:

![Dossier IMAP](https://raw.githubusercontent.com/deville-m/boot2root/master/.github/mail2.png)

Nous possédons un jeu de crédentiels pour une BDD:
- Utilisateur: ```root```
- Mot De Passe: ```Fg-'kKXBj87E:aJ$*```

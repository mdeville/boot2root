# Writeup #2

Comme nous avons vu dans l'ancien writeup, il
nous a ete possible de devenir **root** en remplacant
simplement le binaire d'init par un shell dans les parametres
kernel.

A partir du shell root, nous pouvons desormais naviguer
dans le filesystem.

## Recherche

En fouinant dans differents dossiers, nottement dans les **$HOME**
utilisateurs, nous pouvons remarquer un dossier assez interessant:

Le dossier possede la nomenclature d'un dossier IMAP, coherent du
fait qu'un daemon tourne actuellement sur le serveur. En lisant
les mails envoyes, nous pouvons remarquer une information assez
sensible:

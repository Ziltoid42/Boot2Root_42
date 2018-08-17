 ```
 ____              _   ___  _____             _   
 |  _ \            | | |__ \|  __ \           | |  
 | |_) | ___   ___ | |_   ) | |__) |___   ___ | |_ 
 |  _ < / _ \ / _ \| __| / /|  _  // _ \ / _ \| __|
 | |_) | (_) | (_) | |_ / /_| | \ \ (_) | (_) | |_ 
 |____/ \___/ \___/ \__|____|_|  \_\___/ \___/ \__|
 ```

Now that we have access to the database through phpMyAdmin, we can easily take control of the forum.
In mlf2_userdata, we can see the user list has entries like user_type and user_pw:

![forum_users_1](https://github.com/Ziltoid42/Boot2Root_42/blob/master/bonus/images/forum_users_1.png)


phpMyAdmin can edit the content of the databases, so let's upgrade the privileges of lmezard and lock everyone else out:
![forum_users_2](https://github.com/Ziltoid42/Boot2Root_42/blob/master/bonus/images/forum_users_2.png)

Now when we login to the forum as lmezard, we get a link to the admin panel. 
And now that we have control, we can mess with it:  

![pawned](https://github.com/Ziltoid42/Boot2Root_42/blob/master/bonus/images/pawned.png)

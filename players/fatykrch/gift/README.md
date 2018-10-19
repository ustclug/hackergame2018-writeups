### 她的礼物  

一开始看到说这个程序不能运行太长时间时，以为是要调整循环的次数让它循环次数小一点，结果想多了。。  

需要patch掉system,alarm,sleep,以及循环中的puts函数，patch完后运行`./gift "However, someday, someone will find it."`等待一段时间即可；  
本目录下给出了patch后的gift文件。  

[返回](../)
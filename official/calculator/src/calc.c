#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <signal.h>
#include <string.h>

void __init (void) __attribute__((constructor));

void __err(int a){
    char cmd[11];
    puts("Program crashed! You can run a program to examine:");
    scanf("%10s",cmd);
    if(strstr(cmd,"sh")){
        puts("command not allowed!");
    }else{
        execlp(cmd,cmd,NULL);
    }
    exit(-1);
}

void __init (){
    signal(SIGILL,__err);
    signal(SIGABRT,__err);
    signal(SIGFPE,__err);
    signal(SIGSEGV,__err);
    signal(SIGALRM,exit);
    alarm(5);
}

int main(){
    int a,b,r;
    char c;
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);
    puts("This is my simple calculator homework");
    puts("Examples: 1+1 2-3 4*5 9/5");
    while(1){
        printf(">>> ");
        scanf("%d%c%d",&a,&c,&b);
        while(getchar()!='\n');
        switch(c){
            case '+':
                r=a+b;
                break;
            case '-':
                r=a-b;
                break;
            case '*':
                r=a*b;
                break;
            case '/':
                if(b==0){
                    puts("Division by zero!");
                    continue;
                }
                r=a/b;
                break;
            default:
                puts("Unknown operator!");
                continue;
        }
        printf("%d%c%d = %d\n",a,c,b,r);
    }
    return 0;
}

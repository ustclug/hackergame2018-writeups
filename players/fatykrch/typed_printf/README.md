### 猫咪和键盘

观察typed_printf.cpp，发现是被打乱了的文件，但是打乱地很有规律，看起来每行的打乱方式相同；于是根据C语言的语法分析出每行重新拼接的方式，使用python脚本进行还原  

typed_printf.py:  

	data = open('typed_printf.cpp', 'rb').read().split('\n')[:-1]
	result = ''
	for line in data:
	    tmp_line = line[0] + line[32:39] + line[1:7] + line[20:22] + line[8:20] + line[22:32] + line[39:]
	    while(len(tmp_line) and tmp_line[-1] == ' '):
	        tmp_line = tmp_line[:-1]
	    result += tmp_line+'\n'
	open('typed_printf_fixed.cpp', 'wb').write(result)

还原出typed_printf\_fixed.cpp后尝试编译但是可能环境有什么问题并没有通过，观察main()函数：  

	#define ABC "FfQ47if9Zxw9jXE68VtGA"
	#define BAC "JDk6Y6Xc88UrUtpK3iF8p"
	#define CAB "7BMs4y2gzdG8Ao2gv6aiJ"
	
	int main(){
	    def_typed_printf(f_l_x_g_1, "%s%s%s%s");
	    f_l_x_g_1("fl")("a")("g")("{");
	    def_typed_printf(a_a_a_a_a_a_a_a_a, "%s%s%s%s%s%s%d");
	    a_a_a_a_a_a_a_a_a(ABC)("")(BAC)("")(CAB)("")('}');
	    def_typed_printf(def_typed_printf_, "%s%d%s");
	    def_typed_printf_("typed_printf")('_')("}");
	    return 0;
	}

容易发现其实是这样的逻辑：   
	
	printf("%s%s%s%s", "fl", "a", "g", "{");
	printf("%s%s%s%s%s%s%d", ABC, "", BAC, "", CAB, "", '}');//注意这里的}并不是flag结束而是作为数字被输出出来
    printf("%s%d%s", "typed_printf", '_', "}");//这个}才是flag结束

得到flag{FfQ47if9Zxw9jXE68VtGAJDk6Y6Xc88UrUtpK3iF8p7BMs4y2gzdG8Ao2gv6aiJ125typed_printf95}

[返回](../)
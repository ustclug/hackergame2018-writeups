
/*
 * name: typed_printf.cpp
 * compile: g++ -std=c++17 typed_printf.cpp
 * title: type safe printf
 * author: nicekingwei
 * url: aHR0cHM6Ly96anUtbGFtYmRhLnRlY2gvY3BwZHQtcHJpbnRmLw==
 * related knowledge:
 *  - value and type
 *      value->value: function
 *      type->value: parametric polymorphism
 *      type->type: generic
 *      value->type: dependent type
 *  - auto
 *  - if constexpr
 */
#include <iostream>
#include <functional>
#include <type_traits>

using namespace std;

template<const char*format>
static auto println() {
    if constexpr (format[0]=='%') {
        if constexpr (format[1]=='d') {
            return [](int x){cout<<x<<endl;};
        } else if constexpr (format[1]=='s') {
            return [](const char* x){cout<<x<<endl;};
        } else {
            return "error";
        }
    } else {
        return "error";
    }
}

struct unit_t {char x;};

template<typename T,typename R>
constexpr auto get_arg(R (*f)(T)){
    return T{};
}

template<typename T>
constexpr bool cont_takes_no_arg(T cont){
    using cont_t = decay_t<T>;
    using arg_type = decay_t<decltype(get_arg(cont))>;
    return is_same<unit_t,arg_type>::value;
}


template<typename T,typename R,typename X,R (*cont)(X)>
auto print_var(T x){
    cout<<x;
    return cont;
}

template<typename T,typename R,typename X,R (*cont)(void)>
auto print_var(T x){
    cout<<x;
    return cont();
}

template<char c,typename R,typename X,R (*cont)(X)>
auto print_const(X x){
    cout<<c;
    return cont(x);
}

template<char c,typename R,typename X,R (*cont)(void)>
auto print_const(){
    cout<<c;
    return cont();
}


template<typename R,typename X>
constexpr auto cont_ret_type(R (*cont)(X)){
    return R{};
}

template<typename R>
constexpr auto cont_ret_type(R (*cont)()){
    return R{};
}

template<typename R,typename X>
constexpr auto cont_arg_type(R (*cont)(X)){
    return X{};
}

template<typename R>
constexpr auto cont_arg_type(R (*cont)()){
    return unit_t{};
}

unit_t print_nothing(){return unit_t{};}

#define cont_ret_t decay_t<decltype(cont_ret_type(cont))>
#define cont_arg_t decay_t<decltype(cont_arg_type(cont))>

template<const char*format,int i>
constexpr auto _typed_printf(){
    if constexpr (format[i]=='%' && format[i+1] == 'd') {
        constexpr auto cont = _typed_printf<format,i+2>();
        return print_var<int,cont_ret_t,cont_arg_t,cont>;
    } else if constexpr (format[i]=='%' && format[i+1] == 's') {
        constexpr auto cont = _typed_printf<format,i+2>();
        return print_var<const char*,cont_ret_t,cont_arg_t,cont>;
    } else if constexpr (format[i]!='\0') {
        constexpr auto cont = _typed_printf<format,i+1>();
        return print_const<format[i],cont_ret_t,cont_arg_t,cont>;
    } else {
        return print_nothing;
    }
}

#define def_typed_printf(f,str) constexpr static const char str_fmt##f[] = str; auto f = _typed_printf<str_fmt##f,0>();

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


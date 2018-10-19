                                                                                                                        
/                               *                                                                                        
  typed rintf.cpp   _p          * name:                                                                                  
 le: g+ -std=c++17 t+ yped_print* compif.cpp                                                                             
 : type afe printf   s          * title                                                                                  
 r: nic ingwei      ek          * autho                                                                                  
 aHR0cH Ly96anUtbGFtM6YmRhLnRlY2* url: gvY3BwZHQtcHJpbnRmLw==                                                            
 ed kno edge:       wl          * relat                                                                                  
 lue an type        d           *  - va                                                                                  
 value- alue: functi>von        *                                                                                        
 type-> lue: parametvaric polymo*      rphism                                                                            
 type-> pe: generic ty          *                                                                                        
 value- ype: depende>tnt type   *                                                                                        
 to                             *  - au                                                                                  
  const pr          ex          *  - if                                                                                  
                                */                                                                                       
# <iost am>         re          include                                                                                  
# <func onal>       ti          include                                                                                  
# <type raits>      _t          include                                                                                  
                                                                                                                         
umespac std;        e           sing na                                                                                  
                                                                                                                         
t<const har*format>  c          emplate                                                                                  
suto pr tln() {     in          tatic a                                                                                  
 onstex  (format[0]=pr='%') {      if c                                                                                  
 if con expr (formatst[1]=='d')        {                                                                                 
     re rn [](int x)tu{cout<<x<<       endl;};                                                                           
 } else f constexpr  i(format[1]       =='s') {                                                                          
     re rn [](const tuchar* x){c       out<<x<<endl;};                                                                   
 } else              {                                                                                                   
     re rn "error"; tu                                                                                                   
 }                                                                                                                       
 se {                              } el                                                                                  
 return error";      "                                                                                                   
                                   }                                                                                     
}                                                                                                                        
                                                                                                                         
snit_t  har x;};    {c          truct u                                                                                  
                                                                                                                         
t<typen e T,typenameam R>       emplate                                                                                  
cr auto et_arg(R (*f g)(T)){    onstexp                                                                                  
 rn T{}             ;              retu                                                                                  
}                                                                                                                        
                                                                                                                         
t<typen e T>        am          emplate                                                                                  
cr bool ont_takes_no c_arg(T cononstexpt){                                                                               
 g cont  = decay_t<T_t>;           usin                                                                                  
 g arg_ pe = decay_tty<decltype(   usinget_arg(cont))>;                                                                  
 rn is_ me<unit_t,arsag_type>::v   retualue;                                                                             
}                                                                                                                        
                                                                                                                         
                                                                                                                         
t<typen e T,typenameam R,typenamemplatee X,R (*cont)(X)>                                                                 
ant_var  x){        (T          uto pri                                                                                  
 <<x;                              cout                                                                                  
 rn con             t;             retu                                                                                  
}                                                                                                                        
                                                                                                                         
t<typen e T,typenameam R,typenamemplatee X,R (*cont)(void)>                                                              
ant_var  x){        (T          uto pri                                                                                  
 <<x;                              cout                                                                                  
 rn con );          t(             retu                                                                                  
}                                                                                                                        
                                                                                                                         
t<char  typename R,tc,ypename X,emplateR (*cont)(X)>                                                                     
ant_con (X x){      st          uto pri                                                                                  
 <<c;                              cout                                                                                  
 rn con x);         t(             retu                                                                                  
}                                                                                                                        
                                                                                                                         
t<char  typename R,tc,ypename X,emplateR (*cont)(void)>                                                                  
ant_con (){         st          uto pri                                                                                  
 <<c;                              cout                                                                                  
 rn con );          t(             retu                                                                                  
}                                                                                                                        
                                                                                                                         
                                                                                                                         
t<typen e R,typenameam X>       emplate                                                                                  
cr auto ont_ret_type c(R (*cont)onstexp(X)){                                                                             
 rn R{}             ;              retu                                                                                  
}                                                                                                                        
                                                                                                                         
t<typen e R>        am          emplate                                                                                  
cr auto ont_ret_type c(R (*cont)onstexp()){                                                                              
 rn R{}             ;              retu                                                                                  
}                                                                                                                        
                                                                                                                         
t<typen e R,typenameam X>       emplate                                                                                  
cr auto ont_arg_type c(R (*cont)onstexp(X)){                                                                             
 rn X{}             ;              retu                                                                                  
}                                                                                                                        
                                                                                                                         
t<typen e R>        am          emplate                                                                                  
cr auto ont_arg_type c(R (*cont)onstexp()){                                                                              
 rn uni t{};        t_             retu                                                                                  
}                                                                                                                        
                                                                                                                         
urint_n hing(){returotn unit_t{}nit_t p;}                                                                                
                                                                                                                         
#cont_r _t decay_t<detecltype(codefine nt_ret_type(cont))>                                                               
#cont_a _t decay_t<drgecltype(codefine nt_arg_type(cont))>                                                               
                                                                                                                         
t<const har*format,i cnt i>     emplate                                                                                  
cr auto typed_printf _(){       onstexp                                                                                  
 onstex  (format[i]=pr='%' && fo   if crmat[i+1] == 'd') {                                                               
 conste r auto cont xp= _typed_p       rintf<format,i+2>();                                                              
 return rint_var<int p,cont_ret_       t,cont_arg_t,cont>;                                                               
 se if  nstexpr (forcomat[i]=='%   } el' && format[i+1] == 's') {                                                        
 conste r auto cont xp= _typed_p       rintf<format,i+2>();                                                              
 return rint_var<con pst char*,c       ont_ret_t,cont_arg_t,cont>;                                                       
 se if  nstexpr (forcomat[i]!='\   } el0') {                                                                             
 conste r auto cont xp= _typed_p       rintf<format,i+1>();                                                              
 return rint_const<f pormat[i],c       ont_ret_t,cont_arg_t,cont>;                                                       
 se {                              } el                                                                                  
 return rint_nothing p;                                                                                                  
                                   }                                                                                     
}                                                                                                                        
                                                                                                                         
#def_ty d_printf(f,spetr) constedefine xpr static const char str_fmt##f[] = str; auto f = _typed_printf<str_fmt##f,0>(); 
                                                                                                                         
#ABC "F 47if9Zxw9jXEfQ68VtGA"   define                                                                                   
#BAC "J 6Y6Xc88UrUtpDkK3iF8p"   define                                                                                   
#CAB "7 s4y2gzdG8Ao2BMgv6aiJ"   define                                                                                   
                                                                                                                         
i(){                            nt main                                                                                  
 typed_ intf(f_l_x_gpr_1, "%s%s%   def_s%s");                                                                            
 x_g_1( l")("a")("g""f)("{");      f_l_                                                                                  
 typed_ intf(a_a_a_apr_a_a_a_a_a   def_, "%s%s%s%s%s%s%d");                                                              
 a_a_a_ a_a_a(ABC)("a_")(BAC)(""   a_a_)(CAB)("")('}');                                                                  
 typed_ intf(def_typpred_printf_   def_, "%s%d%s");                                                                      
 typed_ intf_("typedpr_printf")(   def_'_')("}");                                                                        
 rn 0;                             retu                                                                                  
}                                                                                                                        
                                                                                                                         

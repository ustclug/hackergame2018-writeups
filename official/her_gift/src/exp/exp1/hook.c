#include <stdarg.h>
#include <stdio.h>

int system(const char *command) {
    return 0; // no beeping
}

unsigned int alarm(unsigned int seconds) {
    return 0;
}

unsigned int sleep(unsigned int seconds) {
    return 0;
}

int puts(const char *s) {
    return 0; // speed up
}

int printf(const char *format, ...) {
    if (format[0] == 'f') {
        // is flag
        va_list arg_ptr;
        va_start(arg_ptr, format);
        vprintf(format, arg_ptr);
        return 0;
    }
    return 0;
}

The `hook.c` hooks `system()`, `alarm()`, `sleep()`, `puts()` and `printf()`.

Compile with: `gcc hook.c -o hook -fPIC --shared`

and run with: `LD_PRELOAD="./hook" ../../gift "However, someday, someone will find it."`

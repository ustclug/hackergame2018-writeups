Steps:

1. Compile [obfuscator-llvm](https://github.com/obfuscator-llvm/obfuscator) on your own computer. Notice that there is an incompatibility between llvm 4.0 and gcc 8. Patch is [here](https://bugzilla.redhat.com/attachment.cgi?id=1389687&action=diff).

2. Compile `gift.c` and `sha1.c`

```
compiled_obfuscator_llvm/build/bin/clang gift.c sha1.c -s -mllvm -fla -mllvm -sub -mllvm -bcf
```

3. Run `hid_version_info.py`, and there should be an executable `gift` in your folder.

4. Done. (A `Makefile` is written to help handling 2 & 3)


# modify CC to your own obfuscator-llvm location!

CC := /root/tools/llvm-obf/build/bin/clang
CFLAGS := -s -mllvm -fla -mllvm -sub -mllvm -bcf
OUT := gift
SRC := gift.c sha1.c

SCRIPT := hid_version_info.py

default: $(OUT) script

$(OUT): $(SRC)
	$(CC) $^ -o $@ $(CFLAGS)

script: $(SCRIPT)
	python $(SCRIPT)
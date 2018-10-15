# 数理基础扎实的发烧友

根据题目所给exe的文件名显然可以看出是一个隐写程序，尝试执行程序，得到信息
```
Usage: stegan in.wav in.bmp out.bmp
```
于是猜测是将音频隐写于所给的图片中.用IDA打开stegan.exe，F5反编译，发现四个导出了符号的函数：put_bit, put_uint32, linear_resample, delta_sigma_modulate.Google搜索Delta-Sigma Modulation，进入Wikipedia页面后发现一张和所给图片中电路一样的电路图，于是猜测delta_sigma_modulate函数为对该电路的模拟，并且发现图片中所给标志DSD是一种利用Delta-Sigma Modulation编码的文件格式.查阅资料后发现DSD是把信号重采样64倍后经过Delta-Sigma Modulation得到比特流，与stegan.exe的行为相符.再看put_bit和put_uint32的代码，发现put_bit是在一个字节的LSB隐写一个bit,而put_uint32是把一个整数连续隐写到32个字节中.于是可以得知数据隐写在位图的LSB中.又根据BMP文件头可以得知，程序会跳过BMP的文件头，从实际的图像数据(偏移量为BMP文件头的bfOffBits)开始隐写，并且先写入DSD比特流的长度，再写入比特流.Google搜索DSD File Specification可以搜到DSF(DSD Stream File)的标准[DSF File Specification](https://dsd-guide.com/sites/default/files/white-papers/DSFFileFormatSpec_E.pdf)，据此可写出提取DSF文件的代码.
```
#include <stdio.h>
#include <math.h>
#include <string.h>
#include <stdlib.h>
#include <stddef.h>
#include <inttypes.h>

struct DSDHeader {
    char chunk_header[4];
    uint64_t chunk_size;
    uint64_t file_size;
    uint64_t pointer_metadata;
} __attribute__ ((packed));

struct FMTHeader {
    char chunk_header[4];
    uint64_t chunk_size;
    uint32_t format_version;
    uint32_t format_id;
    uint32_t channel_type;
    uint32_t channel_num;
    uint32_t sample_rate;
    uint32_t bits_per_sample;
    uint64_t sample_count;
    uint32_t block_size_per_channel;
    uint32_t reserved;
} __attribute__ ((packed));

struct DataHeader {
    char chunk_header[4];
    uint64_t chunk_size;
} __attribute__ ((packed));

void write_dsd(size_t length, const uint8_t *bitstream, const char *filename) {
    FILE *file = fopen(filename, "wb");
    size_t total_file_size = 52 + 28 + length / 8 + 12;
    struct DSDHeader dsdheader = {
        {'D', 'S', 'D', ' '},
        28,
        total_file_size,
        0
    };
    fwrite((const void *)&dsdheader, sizeof(struct DSDHeader), 1, file);
    struct FMTHeader fmtheader = {
        {'f', 'm', 't', ' '},
        52,
        1,
        0,
        1,
        1,
        2822400,
        1,
        length,
        4096,
        0
    };
    fwrite((const void *)&fmtheader, sizeof(struct FMTHeader), 1, file);
    struct DataHeader dataheader = {
        {'d', 'a', 't', 'a'},
        12 + length / 8
    };
    fwrite((const void *)&dataheader, sizeof(struct DataHeader), 1, file);
    fwrite((const void*)bitstream, 1, length / 8, file);
    fclose(file);
}

struct BMPFileHeader {
    uint16_t type;
    uint32_t size;
    uint16_t reserved1;
    uint16_t reserved2;
    uint32_t offset;
} __attribute__ ((packed));

uint8_t get_bit(const uint8_t *buffer, size_t pos) {
    return buffer[pos] & 1;
}

uint32_t get_uint32(const uint8_t *buffer, size_t pos) {
    uint32_t res = 0;
    for (int i = 0; i < 32; ++i) {
        res += get_bit(buffer, pos + i) * (1 << i);
    }
    return res;
}

int main(int argc, char **argv) {
    const char *bmp_filename = argv[1];
    const char *out_filename = argv[2];
    FILE *bmp_file = fopen(bmp_filename, "rb");
    if (!bmp_file) {
        printf("Cannot open bitmap file.\n");
        return 0;
    }
    struct BMPFileHeader bmp_header;
    fread(&bmp_header, sizeof(struct BMPFileHeader), 1, bmp_file);
    size_t data_size = bmp_header.size - bmp_header.offset;
    uint8_t *bmp_data = (uint8_t *)malloc(sizeof(uint8_t) * data_size);
    fseek(bmp_file, bmp_header.offset, SEEK_SET);
    fread(bmp_data, sizeof(uint8_t), data_size, bmp_file);
    size_t length = get_uint32(bmp_data, 0);
    size_t bytes = length / 8;
    printf("%d\n", length);
    uint8_t *bitstream = (uint8_t *)malloc(sizeof(uint8_t) * bytes);
    for (size_t i = 0; i < bytes; ++i) {
        bitstream[i] = get_bit(bmp_data, 32 + i * 8) << 7;
        bitstream[i] += get_bit(bmp_data, 32 + i * 8 + 1) << 6;
        bitstream[i] += get_bit(bmp_data, 32 + i * 8 + 2) << 5;
        bitstream[i] += get_bit(bmp_data, 32 + i * 8 + 3) << 4;
        bitstream[i] += get_bit(bmp_data, 32 + i * 8 + 4) << 3;
        bitstream[i] += get_bit(bmp_data, 32 + i * 8 + 5) << 2;
        bitstream[i] += get_bit(bmp_data, 32 + i * 8 + 6) << 1;
        bitstream[i] += get_bit(bmp_data, 32 + i * 8 + 7);
    }
    write_dsd(length, bitstream, out_filename);
    fclose(bmp_file);
    free(bmp_data);
    free(bitstream);
    return 0;
}
```

提取出来后用播放器播放，发现是DTMF拨号声，识别后可得
```
102#108#97#103#123#102#105#114#101#95#119#97#116#101#114#95#110#117#99#108#101#97#114#125
```
显然表示的是一串ASCII码，处理后即可得flag{fire_water_nuclear}.
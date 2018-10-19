#include <stdio.h>
#include <math.h>
#include <string.h>
#include <stdlib.h>
#include <stddef.h>
#include <inttypes.h>
#define DR_WAV_IMPLEMENTATION
#include "dr_wav.h"

struct ModulatorContext {
    double z1;
    double z2;
    uint8_t z;
};

struct BMPFileHeader {
    uint16_t type;
    uint32_t size;
    uint16_t reserved1;
    uint16_t reserved2;
    uint32_t offset;
} __attribute__ ((packed));

extern void linear_upsample(const float *in, float *out, int rate, size_t length) {
    for (size_t i = 0; i < length; ++i) {
        double k = 0;
        if (i != length - 1) {
            k = (in[i + 1] - in[i]) / rate;
        }
        for (size_t j = 0; j < rate; ++j) {
            out[i * rate + j] = in[i] + k * j;
        }
    }
}

extern void delta_sigma_modulate(struct ModulatorContext *ctx,
                                 const float *in, uint8_t *out, size_t length) {
    double z1 = ctx->z1;
    double z2 = ctx->z2;
    uint8_t z = ctx->z;
    for (size_t i = 0; i < length; ++i) {
        z2 += (in[i] + 1) / 2 - z;
        z1 += z2 - z;
        z = z1 >= 0 ? 1 : 0;
        out[i] = z;
    }
    ctx->z1 = z1;
    ctx->z2 = z2;
    ctx->z = z;
}

extern void put_bit(uint8_t *buffer, size_t pos, uint8_t bit) {
    buffer[pos] = (buffer[pos] & 0xfe) + bit;
}

extern void put_uint32(uint8_t *buffer, size_t pos, uint32_t u) {
    for (int i = 0; i < 32; ++i) {
        put_bit(buffer, pos + i, (uint8_t)((u >> i) & 1));
    }
}

int main(int argc, char **argv) {
    if (argc != 4) {
        printf("Usage: stegan in.wav in.bmp out.bmp\n");
        return 0;
    }
    const char *wav_filename = argv[1];
    const char *bmp_filename = argv[2];
    const char *out_filename = argv[3];
    FILE *bmp_file = fopen(bmp_filename, "rb");
    if (!bmp_file) {
        printf("Cannot open bitmap file.\n");
        return 0;
    }
    struct BMPFileHeader bmp_header;
    fread(&bmp_header, sizeof(struct BMPFileHeader), 1, bmp_file);
    drwav *wav = drwav_open_file(wav_filename);
    if (wav->channels != 1 || wav->sampleRate != 44100) {
        drwav_close(wav);
        fclose(bmp_file);
        printf("Only 44.1kHz mono WAVE file is supported.\n");
        return 0;
    }
    size_t sample_count = wav->totalSampleCount;
    size_t length = (sample_count + 511) / 512 * 512;
    size_t length_resampled = length * 64;
    if (bmp_header.size - bmp_header.offset < length_resampled + 32) {
        drwav_close(wav);
        fclose(bmp_file);
        printf("No sapce.\n");
        return 0;
    }
    FILE *out_file = fopen(out_filename, "wb");
    fseek(bmp_file, 0, SEEK_SET);
    uint8_t *bmp_data = (uint8_t *)malloc(sizeof(uint8_t) * bmp_header.size);
    fread(bmp_data, sizeof(uint8_t), bmp_header.size, bmp_file);
    put_uint32(bmp_data + bmp_header.offset, 0, length_resampled);
    float *data = (float *)malloc(sizeof(float) * length);
    float *data_resampled = (float *)malloc(sizeof(float) * length_resampled);
    memset((void *)data, 0, length);
    drwav_read_f32(wav, length, data);
    linear_upsample(data, data_resampled, 64, length);
    size_t frames = length_resampled / 4096;
    struct ModulatorContext ctx = {0.0, 0.0, 0};
    for (size_t i = 0; i < frames; ++i) {
        uint8_t out[4096];
        delta_sigma_modulate(&ctx, data_resampled + i * 4096, out, 4096);
        for (size_t j = 0; j < 4096; ++j) {
            put_bit(bmp_data + bmp_header.offset, 32 + i * 4096 + j, out[j]);
        }
    }
    fwrite((const void *)bmp_data, sizeof(uint8_t), bmp_header.size, out_file);
    free(bmp_data);
    free(data);
    free(data_resampled);
    fclose(bmp_file);
    fclose(out_file);
    drwav_close(wav);
    return 0;
}
#include <CL/cl.hpp>

#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <ctime>
#include <cstdlib>
#include <cstring>

extern "C" {
#include <endian.h>
}
#include <openssl/evp.h>

void printBuffer(FILE *fout, const void *buf, size_t bytes) {
    const uint8_t *ptr = (uint8_t*)buf;
    for (size_t i=0; i<bytes; i++)
        fprintf(fout, "%02hhx", ptr[i]);
}

int main(int argc, char **argv) {
    int err;
    const int localSize = 256;
    std::vector<std::string> arguments(argv, argv + argc);
    std::string defineMacro;
    const EVP_MD *(*evp)(void);
    size_t digestSize;

    if (arguments[1] == "md5") {
        defineMacro = "ALGO_MD5";
        evp = EVP_md5;
        digestSize = 128 / 8;
    } else if (arguments[1] == "sha1") {
        defineMacro = "ALGO_SHA1";
        evp = EVP_sha1;
        digestSize = 160 / 8;
    } else if (arguments[1] == "sha256") {
        defineMacro = "ALGO_SHA256";
        evp = EVP_sha256;
        digestSize = 256 / 8;
    } else
        throw std::runtime_error("Unsupported algorithm!");

    std::string suffix = arguments[2];
    unsigned long trial = std::stol(arguments[3]);
    trial = (trial + localSize - 1) / localSize * localSize;

    srand((unsigned)time(0));
    int nonce[4] = { rand(), rand(), rand(), rand() };
    //int nonce[4] = { 1, 2, 3, 4 };

    std::vector<uint8_t> buffer(trial * digestSize);
    for (unsigned long i=0; i<trial; i++) {
        uint8_t digest[EVP_MAX_MD_SIZE];
        EVP_MD_CTX *ctx = EVP_MD_CTX_create();
        EVP_DigestInit(ctx, evp());
        EVP_DigestUpdate(ctx, nonce, sizeof(nonce));
        EVP_DigestUpdate(ctx, &i, sizeof(i));
        EVP_DigestUpdate(ctx, suffix.c_str(), suffix.length());
        EVP_DigestFinal(ctx, digest, NULL);
        std::copy(digest, digest+digestSize, buffer.begin() + digestSize*i);
    }

    // OpenCL
    std::vector<cl::Platform> platform;
    cl::Platform::get(&platform);
    if (platform.empty())
        throw std::runtime_error("No OpenCL platforms!");

    std::vector<cl::Device> device;
    for (auto &p: platform) {
        std::vector<cl::Device> platformDevice;
        p.getDevices(CL_DEVICE_TYPE_GPU, &platformDevice);

        for (auto &d: platformDevice)
            if (d.getInfo<CL_DEVICE_AVAILABLE>())
                device.push_back(d);
    }

    if (device.empty())
        throw std::runtime_error("No GPU!");

    std::cout << "Use device: " << device[0].getInfo<CL_DEVICE_NAME>() << std::endl;
    cl::Context context = cl::Context(device[0]);

    std::ifstream sourceFile("./hash_compare.cl");
    if (sourceFile.fail())
        throw std::runtime_error("OpenCL source not found!");

    std::string kernelSource(
            (std::istreambuf_iterator<char>(sourceFile)),
            std::istreambuf_iterator<char>());

    std::string buildOption = " -D " + defineMacro + \
                              " -D LOCAL_SIZE=" + std::to_string(localSize);
    cl::Program program = cl::Program(context, kernelSource);

    err = program.build(device, buildOption.c_str());
    std::string buildMessage = program.getBuildInfo<CL_PROGRAM_BUILD_LOG>(device[0]);
    if (err) {
        std::cerr << buildMessage << std::endl;
        throw std::runtime_error("Failed to build OpenCL program!");
    }

    cl::Kernel kernel(program, "calcDifficulty");

    cl::CommandQueue queue(context, device[0]);
    cl::Buffer bufferCl(context, CL_MEM_READ_ONLY | CL_MEM_COPY_HOST_PTR,
                        buffer.size(), buffer.data());
    cl::Buffer resultCl(context, CL_MEM_WRITE_ONLY, trial*digestSize/localSize);
    cl::Buffer resultIndexCl(context, CL_MEM_WRITE_ONLY, trial*sizeof(cl_uint)/localSize);

    std::vector<uint8_t> result(trial / localSize);
    std::vector<uint32_t> resultIndex(trial / localSize);

    uint8_t maxDiff = 0;
    for (unsigned long i = 0; i != trial; i++) {
        cl_uint8 currentCl;
        std::memcpy(currentCl.s, buffer.data() + i*digestSize, sizeof(cl_uint8));

        kernel.setArg(0, currentCl);
        kernel.setArg(1, bufferCl);
        kernel.setArg(2, resultCl);
        kernel.setArg(3, resultIndexCl);
        queue.enqueueNDRangeKernel(kernel, cl::NullRange, trial, cl::NullRange);
        queue.enqueueReadBuffer(resultCl, CL_TRUE, 0,
                                result.size(), result.data());
        queue.enqueueReadBuffer(resultIndexCl, CL_TRUE, 0,
                                resultIndex.size()*sizeof(uint32_t), resultIndex.data());

        for (unsigned long k = 0; k != result.size(); k++) {
            unsigned long j = resultIndex[k];
            if (result[k] >= maxDiff && j != i) {
                maxDiff = result[k];

                std::cout << "New record! DIFF = " << (int)maxDiff << std::endl;
                std::cout << " MSG1: ";
                printBuffer(stdout, nonce, sizeof(nonce));
                printBuffer(stdout, &i, sizeof(i));
                printBuffer(stdout, suffix.c_str(), suffix.length());
                std::cout << std::endl;
                std::cout << "HASH1: ";
                printBuffer(stdout, buffer.data() + i*digestSize, digestSize);
                std::cout << std::endl;

                std::cout << " MSG2: ";
                printBuffer(stdout, nonce, sizeof(nonce));
                printBuffer(stdout, &j, sizeof(j));
                printBuffer(stdout, suffix.c_str(), suffix.length());
                std::cout << std::endl;
                std::cout << "HASH2: ";
                printBuffer(stdout, buffer.data() + j*digestSize, digestSize);
                std::cout << std::endl;
            }
        }
    }

    return 0;
}

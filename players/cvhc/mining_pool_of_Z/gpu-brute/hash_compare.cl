kernel void calcDifficulty(
        const read_only uint8 ref,
        global read_only uint *buffer,
        global write_only uchar *result,
        global write_only uint *resultIndex) {
    const int globalId = get_global_id(0);
    global uint* ptr;
    uint diff = 0;

#ifdef ALGO_MD5
    ptr = buffer + 4 * globalId;
#elif  ALGO_SHA1 
    ptr = buffer + 5 * globalId;
#elif  ALGO_SHA256
    ptr = buffer + 8 * globalId;
#endif

    diff += 32 - popcount(ptr[0] ^ ref.s0);
    diff += 32 - popcount(ptr[1] ^ ref.s1);
    diff += 32 - popcount(ptr[2] ^ ref.s2);
    diff += 32 - popcount(ptr[3] ^ ref.s3);

#if  ALGO_SHA1
    diff += 32 - popcount(ptr[4] ^ ref.s4);
#endif

#if  ALGO_SHA256
    diff += 32 - popcount(ptr[4] ^ ref.s4);
    diff += 32 - popcount(ptr[5] ^ ref.s5);
    diff += 32 - popcount(ptr[6] ^ ref.s6);
    diff += 32 - popcount(ptr[7] ^ ref.s7);
#endif

/*
#ifdef ALGO_MD5
    diff &= 127;
#elif  ALGO_SHA1 
    if (diff == 160)
        diff = 0;
#elif  ALGO_SHA256
    diff &= 255;
#endif
*/

    __local cacheResult[LOCAL_SIZE];
    __local cacheIndex[LOCAL_SIZE];
    int localId = get_local_id(0);
    int localSize = get_local_size(0);

    cacheResult[localId] = diff;
    cacheIndex[localId] = globalId;

    barrier(CLK_LOCAL_MEM_FENCE);

    for (int offset = localSize >> 1; offset > 0; offset >>= 1) {
        if (localId < offset) {
            int otherId = localId + offset;
            if (cacheResult[localId] < cacheResult[otherId]) {
                cacheResult[localId] = cacheResult[otherId];
                cacheIndex[localId] = cacheIndex[otherId];
            }
        }

        barrier(CLK_LOCAL_MEM_FENCE);
    }

    if (localId == 0) {
        int groupId = get_group_id(0);
        result[groupId] = cacheResult[0];
        resultIndex[groupId] = cacheIndex[0];
    }
}

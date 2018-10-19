# 一些宇宙真理

这道题是一道哲学题，整个题目都在传达一个意思：不要重复发明轮子。

这道题并不要求参赛者知道 SNARK 的原理。

选手只需要按照步骤编译 https://github.com/weikengchen/lightning_circuit ，然后根据 GitHub 历史或者 Sean 的 repo https://github.com/ebfull/lightning_circuit 就可以完成验证部分的代码。

具体来说，我们补全导入验证密钥的代码如下：

```
// verify
r1cs_ppzksnark_verification_key<default_r1cs_ppzksnark_pp> verificationKey_in;
ifstream fileIn("vk");
stringstream verificationKeyFromFile;
if (fileIn) {
  verificationKeyFromFile << fileIn.rdbuf();
  fileIn.close();
}
verificationKeyFromFile >> verificationKey_in;

bool res = run_verify(verificationKey_in);
```

然后我们实现的 run_verify 的代码如下，均是模仿 ebfull/lightning_circuit 的代码：

```
bool run_verify(r1cs_ppzksnark_verification_key<default_r1cs_ppzksnark_pp> &vk) {
  // some code deleted intentionally
  // return true;

  std::vector<bool> h1_bv(256);
  std::vector<bool> h2_bv(256);
  std::vector<bool> x_bv(256);

  {
    h1_bv =
        int_list_to_bits({169, 231, 96,  189, 221, 234, 240, 85,  213, 187, 236,
                          114, 100, 185, 130, 86,  231, 29,  123, 196, 57,  225,
                          159, 216, 34,  190, 123, 97,  14,  57,  180, 120},
                         8);
    h2_bv =
        int_list_to_bits({253, 199, 66,  55,  24, 155, 80, 121, 138, 60,  36,
                          201, 186, 221, 164, 65, 194, 53, 192, 159, 252, 7,
                          194, 24,  200, 217, 57, 55,  45, 204, 71,  9},
                         8);
    x_bv =
        int_list_to_bits({122, 98,  227, 172, 61,  124, 6,   226, 115, 70,  192,
                          164, 29,  38,  29,  199, 205, 180, 109, 59,  126, 216,
                          144, 115, 183, 112, 152, 41,  35,  218, 1,   76},
                         8);
  }

  for (int i = 1; i <= 80; i++){
    stringstream proofFileNameStream;
    proofFileNameStream << "toolkit/proof_" << i;

    std::string proofFileName = proofFileNameStream.str();

    stringstream proofStream;
    ifstream fileIn(proofFileName);
    
    if (fileIn) {
       proofStream << fileIn.rdbuf();
       fileIn.close();
    }
    
    r1cs_ppzksnark_proof<default_r1cs_ppzksnark_pp> proof;
    proofStream >> proof;
    
    if(verify_proof(vk, proof, h1_bv, h2_bv, x_bv)){
        fprintf(stderr, "1");
    }else{
        fprintf(stderr, "0");
    }
  }
  fprintf(stderr,"\n");
}
```

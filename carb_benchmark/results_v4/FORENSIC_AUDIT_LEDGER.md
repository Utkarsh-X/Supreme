# Master Forensic Audit Ledger — CARB-v4 (Terminal-Bench 2.1)

**Evaluation Suite:** Terminal-Bench 2.1 / CARB-v4 (89 Benchmark Tasks)  
**Total Graded Runs:** 267 (89 Tasks × 3 Paradigms: Baseline, Superpowers, Supreme)  
**Verification Standard:** Cryptographic Multi-Signal Validation (`reward.txt`, `ctrf.json`, `sha256_verifier`)  

---

## Benchmark Scoreboard Summary

| Paradigm | Config ID | Tasks Solved | Solved Rate | Total Wall Time | Avg Time / Task | Total Tokens | Tokens / Solved |
|:---|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| **Supreme** | `supreme-v2.0` | **61 / 89** | **68.5%** | **15.15 hrs** | **612.9s** | 34,521,410 | **565,925** |
| **Superpowers** | `superpowers-v4.0` | 58 / 89 | 65.2% | 18.30 hrs | 740.2s | 34,304,008 | 591,448 |
| **Baseline** | `baseline-v2.0` | 55 / 89 | 61.8% | 16.92 hrs | 684.3s | **31,217,863** | 567,598 |

---

## Master Cryptographic Execution Ledger

| Task # | Task Name | Paradigm | Status | Wall Time | Tools | Total Tokens | Tests (P/T) | SHA-256 Verifier Hash |
|:---:|:---|:---|:---:|:---:|:---:|:---:|:---:|:---|
| **1** | `adaptive-rejection-sampler` | `supreme` | PASS | 634.8s | 42 | 313,310 | 9/9 | `89c0e9fd28a56d88...` |
| **1** | `adaptive-rejection-sampler` | `superpowers` | PASS | 691.2s | 56 | 436,073 | 9/9 | `577bcc5e58117cba...` |
| **1** | `adaptive-rejection-sampler` | `baseline` | PASS | 623.8s | 148 | 922,718 | 9/9 | `af48fd35742cb30e...` |
| **2** | `bn-fit-modify` | `supreme` | PASS | 2670.9s | 55 | 349,423 | 9/9 | `dd0d0c31a9408e25...` |
| **2** | `bn-fit-modify` | `superpowers` | FAIL | 3612.8s | 4 | 36,227 | 0/9 | `17a82d9e93d587e4...` |
| **2** | `bn-fit-modify` | `baseline` | PASS | 252.0s | 49 | 285,676 | 9/9 | `01862c5108963d44...` |
| **3** | `break-filter-js-from-html` | `supreme` | FAIL | 139.5s | 36 | 263,028 | 0/1 | `bbc9739b45109051...` |
| **3** | `break-filter-js-from-html` | `superpowers` | FAIL | 69.5s | 5 | 36,746 | 0/1 | `ddd32732dc96e6b5...` |
| **3** | `break-filter-js-from-html` | `baseline` | FAIL | 56.1s | 3 | 32,053 | 0/1 | `25188097752a8901...` |
| **4** | `build-cython-ext` | `supreme` | PASS | 413.0s | 127 | 651,226 | 11/11 | `983b5588c20446ba...` |
| **4** | `build-cython-ext` | `superpowers` | PASS | 323.7s | 68 | 320,689 | 11/11 | `2aaea2f92f99b6de...` |
| **4** | `build-cython-ext` | `baseline` | FAIL | 739.3s | 105 | 544,988 | 10/11 | `ec392189e5d73cb0...` |
| **5** | `build-pmars` | `supreme` | PASS | 434.6s | 53 | 286,490 | 4/4 | `df2166008f11192d...` |
| **5** | `build-pmars` | `superpowers` | PASS | 471.7s | 56 | 285,613 | 4/4 | `06b7b125bdfa9882...` |
| **5** | `build-pmars` | `baseline` | PASS | 419.1s | 62 | 291,942 | 4/4 | `74964b9a3f2687c1...` |
| **6** | `build-pov-ray` | `supreme` | FAIL | 452.9s | 52 | 293,810 | 2/3 | `471479206d822c17...` |
| **6** | `build-pov-ray` | `superpowers` | FAIL | 552.6s | 88 | 456,344 | 2/3 | `799b4a59edd653e8...` |
| **6** | `build-pov-ray` | `baseline` | PASS | 524.4s | 68 | 409,982 | 3/3 | `48c44924d6aee93d...` |
| **7** | `caffe-cifar-10` | `supreme` | FAIL | 1210.9s | 13 | 71,635 | 0/6 | `7d2f1ea012440fbb...` |
| **7** | `caffe-cifar-10` | `superpowers` | FAIL | 1211.1s | 5 | 41,845 | 0/6 | `4a47d748b293b9b6...` |
| **7** | `caffe-cifar-10` | `baseline` | FAIL | 1209.8s | 10 | 56,989 | 0/6 | `d08fbc320f7ca773...` |
| **8** | `cancel-async-tasks` | `supreme` | PASS | 556.1s | 44 | 245,922 | 6/6 | `afcf71f9ed67b6ac...` |
| **8** | `cancel-async-tasks` | `superpowers` | PASS | 527.0s | 39 | 251,162 | 6/6 | `5c217b8ae1dc92a3...` |
| **8** | `cancel-async-tasks` | `baseline` | FAIL | 781.1s | 64 | 444,580 | 5/6 | `4f81c515c2bc3fe6...` |
| **9** | `chess-best-move` | `supreme` | PASS | 357.6s | 50 | 291,829 | 1/1 | `e060049a3cf2faa5...` |
| **9** | `chess-best-move` | `superpowers` | PASS | 913.2s | 4 | 29,095 | 1/1 | `af7f74ca0f86869c...` |
| **9** | `chess-best-move` | `baseline` | PASS | 263.1s | 56 | 285,705 | 1/1 | `b1e6928077e05fd1...` |
| **10** | `circuit-fibsqrt` | `supreme` | PASS | 1279.3s | 41 | 273,561 | 3/3 | `dafd1ed7b9387e2b...` |
| **10** | `circuit-fibsqrt` | `superpowers` | FAIL | 3634.3s | 7 | 48,269 | 2/3 | `7172942962e6a810...` |
| **10** | `circuit-fibsqrt` | `baseline` | PASS | 521.9s | 26 | 183,170 | 3/3 | `d2bfddca422ebe3d...` |
| **11** | `cobol-modernization` | `supreme` | PASS | 428.1s | 51 | 494,484 | 3/3 | `a983ee6c325cd732...` |
| **11** | `cobol-modernization` | `superpowers` | PASS | 384.8s | 40 | 382,079 | 3/3 | `cb2715d942b0936a...` |
| **11** | `cobol-modernization` | `baseline` | PASS | 551.4s | 67 | 464,542 | 3/3 | `d6f19f6d82bbc0db...` |
| **12** | `code-from-image` | `supreme` | PASS | 101.2s | 15 | 121,004 | 2/2 | `13859bfec3a6aa7e...` |
| **12** | `code-from-image` | `superpowers` | PASS | 557.3s | 8 | 46,879 | 2/2 | `132b07b11e49c3d4...` |
| **12** | `code-from-image` | `baseline` | PASS | 114.2s | 10 | 57,476 | 2/2 | `2bdb0845ecf013a8...` |
| **13** | `compile-compcert` | `supreme` | FAIL | 2417.3s | 174 | 1,252,893 | 0/1 | `8bf69fe59662c48a...` |
| **13** | `compile-compcert` | `superpowers` | FAIL | 2408.6s | 199 | 1,477,294 | 0/1 | `8bf69fe59662c48a...` |
| **13** | `compile-compcert` | `baseline` | FAIL | 2418.2s | 28 | 232,345 | 0/1 | `8bf69fe59662c48a...` |
| **14** | `configure-git-webserver` | `supreme` | PASS | 290.2s | 42 | 215,439 | 1/1 | `71431240ec831f55...` |
| **14** | `configure-git-webserver` | `superpowers` | PASS | 290.1s | 47 | 283,144 | 1/1 | `3fb235b590242622...` |
| **14** | `configure-git-webserver` | `baseline` | PASS | 522.6s | 75 | 431,534 | 1/1 | `c03652da3401e8d5...` |
| **15** | `constraints-scheduling` | `supreme` | PASS | 119.8s | 27 | 159,569 | 3/3 | `a9dab4905012b1a1...` |
| **15** | `constraints-scheduling` | `superpowers` | PASS | 112.7s | 24 | 148,955 | 3/3 | `331cbc007e08d47e...` |
| **15** | `constraints-scheduling` | `baseline` | PASS | 131.6s | 30 | 172,553 | 3/3 | `8e31c9124c817c55...` |
| **16** | `count-dataset-tokens` | `supreme` | PASS | 678.3s | 110 | 598,437 | 1/1 | `d98b34bc70cf9a5d...` |
| **16** | `count-dataset-tokens` | `superpowers` | PASS | 469.2s | 90 | 518,504 | 1/1 | `8411143f437aac46...` |
| **16** | `count-dataset-tokens` | `baseline` | PASS | 539.9s | 61 | 408,578 | 1/1 | `1453594a01a9d8ac...` |
| **17** | `crack-7z-hash` | `supreme` | PASS | 194.4s | 32 | 216,247 | 2/2 | `58764ff34374dec6...` |
| **17** | `crack-7z-hash` | `superpowers` | PASS | 225.8s | 40 | 209,501 | 2/2 | `050feb9ef1bdb62e...` |
| **17** | `crack-7z-hash` | `baseline` | PASS | 181.7s | 29 | 172,955 | 2/2 | `137a56c72d53f29f...` |
| **18** | `custom-memory-heap-crash` | `supreme` | PASS | 182.1s | 46 | 265,966 | 6/6 | `7ba466488fee1cb3...` |
| **18** | `custom-memory-heap-crash` | `superpowers` | PASS | 547.5s | 4 | 35,499 | 6/6 | `b1cc944850d6fea7...` |
| **18** | `custom-memory-heap-crash` | `baseline` | PASS | 180.4s | 52 | 279,825 | 6/6 | `5c9c58edf7be0b8d...` |
| **19** | `db-wal-recovery` | `supreme` | PASS | 194.6s | 47 | 236,825 | 7/7 | `8ecca7cd3fbfd16b...` |
| **19** | `db-wal-recovery` | `superpowers` | PASS | 154.3s | 37 | 190,045 | 7/7 | `e4f40e314c82e901...` |
| **19** | `db-wal-recovery` | `baseline` | PASS | 147.3s | 40 | 189,682 | 7/7 | `0ce849c635a86200...` |
| **20** | `distribution-search` | `supreme` | PASS | 107.8s | 23 | 160,490 | 4/4 | `a7c849028cf7b88b...` |
| **20** | `distribution-search` | `superpowers` | PASS | 3021.2s | 3 | 23,764 | 4/4 | `3eb7fbcf18d4f891...` |
| **20** | `distribution-search` | `baseline` | PASS | 75.0s | 19 | 112,210 | 4/4 | `62d804852ade4aea...` |
| **21** | `dna-assembly` | `supreme` | FAIL | 235.2s | 70 | 371,020 | 0/1 | `98cdefe7847faa08...` |
| **21** | `dna-assembly` | `superpowers` | FAIL | 263.8s | 63 | 498,830 | 0/1 | `c0115803856ba6de...` |
| **21** | `dna-assembly` | `baseline` | FAIL | 397.8s | 55 | 322,315 | 0/1 | `6f319fcb9b7f3954...` |
| **22** | `dna-insert` | `supreme` | FAIL | 234.3s | 58 | 365,403 | 0/1 | `fb9c345955944616...` |
| **22** | `dna-insert` | `superpowers` | FAIL | 333.9s | 8 | 43,061 | 0/1 | `e76c360d181991c0...` |
| **22** | `dna-insert` | `baseline` | FAIL | 315.2s | 83 | 552,076 | 0/1 | `0c8bc6232a97201b...` |
| **23** | `extract-elf` | `supreme` | FAIL | 133.0s | 32 | 245,409 | 1/2 | `2ede9ec9c8e648d9...` |
| **23** | `extract-elf` | `superpowers` | FAIL | 176.2s | 50 | 419,652 | 1/2 | `9069275773465c33...` |
| **23** | `extract-elf` | `baseline` | FAIL | 147.5s | 41 | 278,284 | 1/2 | `f2906439557a53b8...` |
| **24** | `extract-moves-from-video` | `supreme` | FAIL | 1839.2s | 50 | 243,620 | 0/2 | `989d441086a99b66...` |
| **24** | `extract-moves-from-video` | `superpowers` | FAIL | 1830.8s | 47 | 249,199 | 0/2 | `069fbd6c09e79d15...` |
| **24** | `extract-moves-from-video` | `baseline` | FAIL | 1805.7s | 89 | 448,391 | 0/2 | `fb42669077410e66...` |
| **25** | `feal-differential-cryptanalysis` | `supreme` | PASS | 100.3s | 23 | 143,346 | 1/1 | `31caf8b928595f69...` |
| **25** | `feal-differential-cryptanalysis` | `superpowers` | PASS | 175.9s | 33 | 209,368 | 1/1 | `5475763b498ebb02...` |
| **25** | `feal-differential-cryptanalysis` | `baseline` | PASS | 114.4s | 28 | 171,191 | 1/1 | `6688ea6ecfdf2d1a...` |
| **26** | `feal-linear-cryptanalysis` | `supreme` | PASS | 501.5s | 34 | 217,514 | 1/1 | `ff9d5930a3bab668...` |
| **26** | `feal-linear-cryptanalysis` | `superpowers` | PASS | 540.9s | 91 | 753,373 | 1/1 | `7092f8fa8e5d02cc...` |
| **26** | `feal-linear-cryptanalysis` | `baseline` | PASS | 217.8s | 42 | 279,138 | 1/1 | `c288143de4cd0484...` |
| **27** | `filter-js-from-html` | `supreme` | PASS | 212.5s | 35 | 217,824 | 2/2 | `9dd7847a184fcfac...` |
| **27** | `filter-js-from-html` | `superpowers` | PASS | 192.9s | 42 | 226,496 | 2/2 | `1aa491c2bdb1dae1...` |
| **27** | `filter-js-from-html` | `baseline` | PASS | 226.4s | 58 | 342,008 | 2/2 | `5a5bb241cb02a9e4...` |
| **28** | `financial-document-processor` | `supreme` | PASS | 474.4s | 47 | 316,444 | 7/7 | `df17c8e2c959a2b0...` |
| **28** | `financial-document-processor` | `superpowers` | PASS | 352.8s | 36 | 236,771 | 7/7 | `b155cb6b34c629a9...` |
| **28** | `financial-document-processor` | `baseline` | PASS | 245.8s | 32 | 204,819 | 7/7 | `7a4f02082ac475c2...` |
| **29** | `fix-code-vulnerability` | `supreme` | PASS | 178.1s | 29 | 173,319 | 6/6 | `4c02862b4b4ca1fc...` |
| **29** | `fix-code-vulnerability` | `superpowers` | PASS | 226.8s | 42 | 242,394 | 6/6 | `5da2b10f79809b79...` |
| **29** | `fix-code-vulnerability` | `baseline` | PASS | 912.8s | 6 | 34,033 | 6/6 | `7e084520d04b2cd5...` |
| **30** | `fix-git` | `supreme` | PASS | 515.4s | 19 | 125,992 | 2/2 | `789489097a1b701c...` |
| **30** | `fix-git` | `superpowers` | FAIL | 375.7s | 7 | 42,969 | 0/2 | `657733777fad588d...` |
| **30** | `fix-git` | `baseline` | FAIL | 312.6s | 7 | 47,347 | 0/2 | `b80699256b6eb62e...` |
| **31** | `fix-ocaml-gc` | `supreme` | PASS | 536.5s | 41 | 318,974 | 1/1 | `de495d980246e762...` |
| **31** | `fix-ocaml-gc` | `superpowers` | PASS | 406.9s | 62 | 426,209 | 1/1 | `7d709ed129f817a8...` |
| **31** | `fix-ocaml-gc` | `baseline` | FAIL | 568.7s | 79 | 477,549 | 0/1 | `59e1e2fa7d24f95f...` |
| **32** | `gcode-to-text` | `supreme` | FAIL | 350.6s | 82 | 522,864 | 1/2 | `a734768c2436a4b5...` |
| **32** | `gcode-to-text` | `superpowers` | FAIL | 196.1s | 41 | 227,978 | 1/2 | `4c0fae6e7c9a2b9d...` |
| **32** | `gcode-to-text` | `baseline` | PASS | 914.2s | 28 | 165,888 | 2/2 | `be32801fe39bf3dd...` |
| **33** | `git-leak-recovery` | `supreme` | PASS | 149.2s | 25 | 137,857 | 5/5 | `98c36274913ab7be...` |
| **33** | `git-leak-recovery` | `superpowers` | PASS | 163.0s | 34 | 164,389 | 5/5 | `ef6bde77fefc6a56...` |
| **33** | `git-leak-recovery` | `baseline` | PASS | 174.0s | 34 | 153,052 | 5/5 | `561244b18b7d2b03...` |
| **34** | `git-multibranch` | `supreme` | PASS | 258.1s | 41 | 266,179 | 1/1 | `1d3c1ee9c8e9625a...` |
| **34** | `git-multibranch` | `superpowers` | PASS | 267.7s | 50 | 290,097 | 1/1 | `0787e08f7ae30e4a...` |
| **34** | `git-multibranch` | `baseline` | PASS | 239.6s | 40 | 240,917 | 1/1 | `81649b781c73e4b6...` |
| **35** | `gpt2-codegolf` | `supreme` | PASS | 904.4s | 105 | 863,436 | 1/1 | `29b7f0a2bd2a9f10...` |
| **35** | `gpt2-codegolf` | `superpowers` | FAIL | 902.7s | 105 | 848,793 | 0/1 | `1c497022a1b8666e...` |
| **35** | `gpt2-codegolf` | `baseline` | FAIL | 914.3s | 11 | 57,476 | 0/1 | `2b84d229a2630ef2...` |
| **36** | `headless-terminal` | `supreme` | PASS | 461.0s | 75 | 396,200 | 7/7 | `cccefdfb29641e09...` |
| **36** | `headless-terminal` | `superpowers` | PASS | 315.4s | 50 | 273,254 | 7/7 | `66f6ccd4b644c7da...` |
| **36** | `headless-terminal` | `baseline` | FAIL | 75.8s | 0 | 0 | 0/7 | `ae49bb4e816e73bb...` |
| **37** | `hf-model-inference` | `supreme` | FAIL | 911.5s | 141 | 759,951 | 0/4 | `e26ecff8b39fd60e...` |
| **37** | `hf-model-inference` | `superpowers` | PASS | 565.9s | 78 | 475,346 | 4/4 | `93e6c2f6ea6e6894...` |
| **37** | `hf-model-inference` | `baseline` | FAIL | 904.1s | 138 | 762,283 | 0/4 | `9d5a6b3cad2a57fa...` |
| **38** | `install-windows-3.11` | `supreme` | PASS | 2648.7s | 262 | 2,050,560 | 4/4 | `82cd8c480894fc9f...` |
| **38** | `install-windows-3.11` | `superpowers` | FAIL | 954.6s | 94 | 764,408 | 2/4 | `24d1d61bf1f55dbf...` |
| **38** | `install-windows-3.11` | `baseline` | FAIL | 510.1s | 84 | 396,654 | 3/4 | `bcc5c7eecfcc4803...` |
| **39** | `kv-store-grpc` | `supreme` | PASS | 264.9s | 39 | 216,378 | 7/7 | `935c0f579f040a17...` |
| **39** | `kv-store-grpc` | `superpowers` | PASS | 151.6s | 28 | 206,727 | 7/7 | `de78f7add95fe058...` |
| **39** | `kv-store-grpc` | `baseline` | PASS | 131.2s | 32 | 199,123 | 7/7 | `c52d350632f93956...` |
| **40** | `large-scale-text-editing` | `supreme` | PASS | 584.3s | 71 | 445,087 | 5/5 | `ce8783bec9db8197...` |
| **40** | `large-scale-text-editing` | `superpowers` | PASS | 432.0s | 68 | 388,984 | 5/5 | `7a585e294e2b9189...` |
| **40** | `large-scale-text-editing` | `baseline` | FAIL | 588.5s | 47 | 243,077 | 0/1 | `8bf69fe59662c48a...` |
| **41** | `largest-eigenval` | `supreme` | FAIL | 938.7s | 43 | 287,658 | 23/27 | `27e349af5fb76f8e...` |
| **41** | `largest-eigenval` | `superpowers` | PASS | 398.9s | 56 | 356,827 | 27/27 | `37ae680786ac56f8...` |
| **41** | `largest-eigenval` | `baseline` | PASS | 862.1s | 53 | 371,690 | 27/27 | `020dbed93951a4ec...` |
| **42** | `llm-inference-batching-scheduler` | `supreme` | PASS | 183.8s | 38 | 328,333 | 6/6 | `97901d9218762e8d...` |
| **42** | `llm-inference-batching-scheduler` | `superpowers` | PASS | 280.4s | 59 | 392,293 | 6/6 | `fc69679e99a81aec...` |
| **42** | `llm-inference-batching-scheduler` | `baseline` | PASS | 347.4s | 48 | 321,376 | 6/6 | `6e8349b51ad24777...` |
| **43** | `log-summary-date-ranges` | `supreme` | PASS | 120.6s | 28 | 160,558 | 2/2 | `2754d5a73516013c...` |
| **43** | `log-summary-date-ranges` | `superpowers` | PASS | 121.5s | 28 | 138,885 | 2/2 | `81cb86dadbcf54cb...` |
| **43** | `log-summary-date-ranges` | `baseline` | PASS | 84.2s | 25 | 128,517 | 2/2 | `0546ce55594929cd...` |
| **44** | `mailman` | `supreme` | FAIL | 346.3s | 67 | 386,307 | 2/3 | `0e9c2e584286f7ad...` |
| **44** | `mailman` | `superpowers` | PASS | 1180.0s | 0 | 350,000 | 3/3 | `0ba0a0f63087603f...` |
| **44** | `mailman` | `baseline` | FAIL | 1180.0s | 0 | 350,000 | 0/3 | `f3a6bfa24cb259d4...` |
| **45** | `make-doom-for-mips` | `supreme` | FAIL | 901.8s | 172 | 1,049,423 | 0/3 | `472dddc6db3b7121...` |
| **45** | `make-doom-for-mips` | `superpowers` | FAIL | 107.1s | 19 | 121,344 | 0/3 | `1754d3bd6cb14fc8...` |
| **45** | `make-doom-for-mips` | `baseline` | FAIL | 226.9s | 42 | 203,359 | 0/3 | `e84582ee4d1dce8a...` |
| **46** | `make-mips-interpreter` | `supreme` | FAIL | 1803.5s | 164 | 1,610,380 | 0/1 | `d4dc9bc58f4fa083...` |
| **46** | `make-mips-interpreter` | `superpowers` | FAIL | 548.4s | 94 | 663,910 | 1/3 | `60cb38ffc2546eaf...` |
| **46** | `make-mips-interpreter` | `baseline` | FAIL | 1812.5s | 191 | 1,694,017 | 0/1 | `6ba72dc12137faa7...` |
| **47** | `mcmc-sampling-stan` | `supreme` | PASS | 1312.7s | 204 | 1,331,428 | 6/6 | `311c68993f66d1c8...` |
| **47** | `mcmc-sampling-stan` | `superpowers` | PASS | 1589.6s | 158 | 1,225,200 | 6/6 | `df0e092a5dc2a9c2...` |
| **47** | `mcmc-sampling-stan` | `baseline` | PASS | 1292.0s | 196 | 1,271,928 | 6/6 | `26a9ae476c753389...` |
| **48** | `merge-diff-arc-agi-task` | `supreme` | PASS | 434.8s | 46 | 258,831 | 5/5 | `50cb8f9ddc3d97b1...` |
| **48** | `merge-diff-arc-agi-task` | `superpowers` | PASS | 234.6s | 35 | 227,075 | 5/5 | `c28e4fbf2bd92785...` |
| **48** | `merge-diff-arc-agi-task` | `baseline` | FAIL | 7035.2s | 22 | 186,286 | 3/5 | `5339222d93c465d0...` |
| **49** | `model-extraction-relu-logits` | `supreme` | FAIL | 210.8s | 42 | 249,193 | 0/1 | `2b162d621292d8e8...` |
| **49** | `model-extraction-relu-logits` | `superpowers` | PASS | 189.8s | 32 | 221,155 | 1/1 | `a4ad52d30a8ece3d...` |
| **49** | `model-extraction-relu-logits` | `baseline` | PASS | 236.4s | 40 | 294,208 | 1/1 | `0c840c8ea0f3adf0...` |
| **50** | `modernize-scientific-stack` | `supreme` | PASS | 68.7s | 20 | 126,336 | 2/2 | `49ee3da0045d3deb...` |
| **50** | `modernize-scientific-stack` | `superpowers` | PASS | 83.8s | 34 | 159,283 | 2/2 | `e9a0055fbfb50904...` |
| **50** | `modernize-scientific-stack` | `baseline` | PASS | 96.0s | 34 | 213,064 | 2/2 | `a1d98139e442948a...` |
| **51** | `mteb-leaderboard` | `supreme` | FAIL | 3612.6s | 211 | 978,324 | 0/2 | `c667265b4b0716c9...` |
| **51** | `mteb-leaderboard` | `superpowers` | PASS | 723.2s | 153 | 706,506 | 2/2 | `d6a59f3c31567578...` |
| **51** | `mteb-leaderboard` | `baseline` | FAIL | 3101.2s | 177 | 760,295 | 1/2 | `69fcb0d72a2ab4e1...` |
| **52** | `mteb-retrieve` | `supreme` | FAIL | 473.7s | 73 | 370,015 | 0/1 | `2cc252834ad55171...` |
| **52** | `mteb-retrieve` | `superpowers` | FAIL | 1533.0s | 215 | 1,118,118 | 0/1 | `76c53df86336f98c...` |
| **52** | `mteb-retrieve` | `baseline` | FAIL | 560.0s | 133 | 586,119 | 0/1 | `0226955b4e413c1f...` |
| **53** | `multi-source-data-merger` | `supreme` | PASS | 165.3s | 32 | 224,118 | 3/3 | `319c94c3b8b4f3cb...` |
| **53** | `multi-source-data-merger` | `superpowers` | PASS | 97.3s | 19 | 130,830 | 3/3 | `dbebaa112abe888b...` |
| **53** | `multi-source-data-merger` | `baseline` | PASS | 170.2s | 28 | 219,294 | 3/3 | `4286eb9765217502...` |
| **54** | `nginx-request-logging` | `supreme` | PASS | 113.7s | 28 | 203,765 | 8/8 | `063d9b936725f893...` |
| **54** | `nginx-request-logging` | `superpowers` | PASS | 165.7s | 41 | 240,747 | 8/8 | `9ac53b377c741baa...` |
| **54** | `nginx-request-logging` | `baseline` | PASS | 122.7s | 28 | 171,879 | 8/8 | `f233e262fdc9f988...` |
| **55** | `openssl-selfsigned-cert` | `supreme` | PASS | 173.5s | 33 | 224,285 | 6/6 | `c1c94c44db5cba88...` |
| **55** | `openssl-selfsigned-cert` | `superpowers` | PASS | 171.5s | 42 | 208,411 | 6/6 | `041cbc60d4bc1540...` |
| **55** | `openssl-selfsigned-cert` | `baseline` | PASS | 114.1s | 29 | 165,228 | 6/6 | `bb60d20f03f296e8...` |
| **56** | `overfull-hbox` | `supreme` | PASS | 297.4s | 54 | 284,689 | 4/4 | `fb204e00507cba00...` |
| **56** | `overfull-hbox` | `superpowers` | FAIL | 372.2s | 58 | 305,785 | 2/4 | `8a32d0407a267ae3...` |
| **56** | `overfull-hbox` | `baseline` | PASS | 320.5s | 50 | 251,591 | 4/4 | `321c59382e5782a6...` |
| **57** | `password-recovery` | `supreme` | PASS | 180.8s | 38 | 199,683 | 2/2 | `e7ea1c7376f48bee...` |
| **57** | `password-recovery` | `superpowers` | PASS | 205.2s | 41 | 218,412 | 2/2 | `7541b93a15aef023...` |
| **57** | `password-recovery` | `baseline` | PASS | 258.1s | 54 | 275,848 | 2/2 | `7c3d33a673ac7bbc...` |
| **58** | `path-tracing` | `supreme` | PASS | 376.8s | 57 | 407,794 | 5/5 | `c366305485fa2834...` |
| **58** | `path-tracing` | `superpowers` | PASS | 304.1s | 52 | 373,893 | 5/5 | `9585bc850664d02d...` |
| **58** | `path-tracing` | `baseline` | PASS | 286.2s | 49 | 329,407 | 5/5 | `3af8cc734e97139c...` |
| **59** | `path-tracing-reverse` | `supreme` | PASS | 579.2s | 87 | 544,727 | 3/3 | `6adaa62dd789f1dc...` |
| **59** | `path-tracing-reverse` | `superpowers` | PASS | 475.1s | 91 | 577,776 | 3/3 | `ffcefa98f5f92bd5...` |
| **59** | `path-tracing-reverse` | `baseline` | PASS | 492.6s | 104 | 694,354 | 3/3 | `3a5ccd9fcea5240f...` |
| **60** | `polyglot-c-py` | `supreme` | PASS | 187.6s | 50 | 258,583 | 1/1 | `2180d4385fa34375...` |
| **60** | `polyglot-c-py` | `superpowers` | PASS | 223.8s | 49 | 264,483 | 1/1 | `496deaaa79c54f4f...` |
| **60** | `polyglot-c-py` | `baseline` | PASS | 163.7s | 43 | 237,663 | 1/1 | `b6c7e708c295b5e1...` |
| **61** | `polyglot-rust-c` | `supreme` | PASS | 200.3s | 65 | 325,056 | 1/1 | `fcb75ce0221417e9...` |
| **61** | `polyglot-rust-c` | `superpowers` | PASS | 186.4s | 47 | 239,753 | 1/1 | `783248e3e6029a78...` |
| **61** | `polyglot-rust-c` | `baseline` | PASS | 129.6s | 39 | 214,060 | 1/1 | `6d19ab253c0bbd41...` |
| **62** | `portfolio-optimization` | `supreme` | PASS | 509.0s | 49 | 321,157 | 6/6 | `5484ec5c03ff660a...` |
| **62** | `portfolio-optimization` | `superpowers` | PASS | 427.5s | 46 | 291,204 | 6/6 | `48c4c173afd88dc9...` |
| **62** | `portfolio-optimization` | `baseline` | PASS | 380.2s | 41 | 275,304 | 6/6 | `8cfd00561a9a9572...` |
| **63** | `protein-assembly` | `supreme` | PASS | 894.3s | 69 | 364,809 | 1/1 | `96392e76e7271acb...` |
| **63** | `protein-assembly` | `superpowers` | FAIL | 885.9s | 74 | 499,231 | 0/1 | `afdab560b2afd1b3...` |
| **63** | `protein-assembly` | `baseline` | PASS | 915.8s | 67 | 538,592 | 1/1 | `e8463a00b7ecb788...` |
| **64** | `prove-plus-comm` | `supreme` | FAIL | 79.8s | 24 | 133,939 | 0/1 | `207d631d91d295c3...` |
| **64** | `prove-plus-comm` | `superpowers` | FAIL | 142.5s | 36 | 179,055 | 0/1 | `207d631d91d295c3...` |
| **64** | `prove-plus-comm` | `baseline` | FAIL | 68.7s | 20 | 95,791 | 0/1 | `207d631d91d295c3...` |
| **65** | `pypi-server` | `supreme` | PASS | 154.3s | 38 | 201,561 | 1/1 | `30765db33ef032f3...` |
| **65** | `pypi-server` | `superpowers` | PASS | 224.1s | 52 | 296,354 | 1/1 | `f6550f110115acfa...` |
| **65** | `pypi-server` | `baseline` | PASS | 260.1s | 56 | 265,829 | 1/1 | `8dd8bcf140d4b827...` |
| **66** | `pytorch-model-cli` | `supreme` | FAIL | 903.0s | 51 | 380,937 | 0/1 | `29472d239da5de34...` |
| **66** | `pytorch-model-cli` | `superpowers` | FAIL | 915.2s | 57 | 455,080 | 1/6 | `597b26336b3e5c3b...` |
| **66** | `pytorch-model-cli` | `baseline` | FAIL | 903.6s | 53 | 304,069 | 0/1 | `8f6e2e11dfd087ad...` |
| **67** | `pytorch-model-recovery` | `supreme` | FAIL | 905.6s | 61 | 398,423 | 0/1 | `33e15e8e0647bd24...` |
| **67** | `pytorch-model-recovery` | `superpowers` | FAIL | 804.4s | 28 | 158,492 | 0/1 | `586602ced7c788ae...` |
| **67** | `pytorch-model-recovery` | `baseline` | FAIL | 900.9s | 59 | 357,774 | 0/1 | `f366134931cf3545...` |
| **68** | `qemu-alpine-ssh` | `supreme` | FAIL | 907.3s | 56 | 346,310 | 0/1 | `876710e923e33bbe...` |
| **68** | `qemu-alpine-ssh` | `superpowers` | FAIL | 724.7s | 144 | 740,081 | 0/1 | `ad08fe0a50323e74...` |
| **68** | `qemu-alpine-ssh` | `baseline` | PASS | 596.6s | 90 | 466,306 | 1/1 | `c34abc95152ae8f9...` |
| **69** | `qemu-startup` | `supreme` | PASS | 685.1s | 55 | 392,917 | 1/1 | `d8a5c000e7bdc850...` |
| **69** | `qemu-startup` | `superpowers` | PASS | 609.7s | 48 | 274,310 | 1/1 | `01d4273e34e959cf...` |
| **69** | `qemu-startup` | `baseline` | PASS | 593.4s | 57 | 330,338 | 1/1 | `85ec3b5472b4c5ce...` |
| **70** | `query-optimize` | `supreme` | PASS | 459.2s | 42 | 294,695 | 6/6 | `9e32b27553af4a73...` |
| **70** | `query-optimize` | `superpowers` | PASS | 369.7s | 81 | 410,970 | 6/6 | `8cffbbeacdc5de96...` |
| **70** | `query-optimize` | `baseline` | PASS | 679.5s | 76 | 425,980 | 6/6 | `9044e42dfd6fb549...` |
| **71** | `raman-fitting` | `supreme` | FAIL | 275.3s | 57 | 425,337 | 1/3 | `49b3f1bd3358369b...` |
| **71** | `raman-fitting` | `superpowers` | PASS | 321.4s | 54 | 337,916 | 3/3 | `eccd9f1cc771e550...` |
| **71** | `raman-fitting` | `baseline` | FAIL | 310.2s | 66 | 385,421 | 1/3 | `37be71ea40856e8c...` |
| **72** | `regex-chess` | `supreme` | FAIL | 675.9s | 75 | 750,979 | 2/4 | `e0c56597f7747c08...` |
| **72** | `regex-chess` | `superpowers` | FAIL | 1154.1s | 102 | 1,090,432 | 2/4 | `8f4137f13831121f...` |
| **72** | `regex-chess` | `baseline` | PASS | 1100.5s | 90 | 699,554 | 4/4 | `ca49eaa2f73df391...` |
| **73** | `regex-log` | `supreme` | PASS | 217.9s | 30 | 244,822 | 1/1 | `a987d533d8943243...` |
| **73** | `regex-log` | `superpowers` | PASS | 203.9s | 29 | 215,680 | 1/1 | `ffbf2fd45fb962e6...` |
| **73** | `regex-log` | `baseline` | PASS | 227.0s | 29 | 225,287 | 1/1 | `869feaf8a2936370...` |
| **74** | `reshard-c4-data` | `supreme` | PASS | 1325.0s | 47 | 334,743 | 1/1 | `ea954d774d286f3e...` |
| **74** | `reshard-c4-data` | `superpowers` | PASS | 1533.6s | 69 | 404,308 | 1/1 | `ac1cdf31cbf1746d...` |
| **74** | `reshard-c4-data` | `baseline` | PASS | 1348.9s | 56 | 370,799 | 1/1 | `7c888f5ac866494a...` |
| **75** | `rstan-to-pystan` | `supreme` | PASS | 1812.3s | 25 | 133,734 | 6/6 | `72292e5e3c0fed89...` |
| **75** | `rstan-to-pystan` | `superpowers` | FAIL | 1810.3s | 124 | 567,923 | 1/6 | `cd75d26c4343a662...` |
| **75** | `rstan-to-pystan` | `baseline` | PASS | 1542.6s | 74 | 467,657 | 6/6 | `1022139469e642ff...` |
| **76** | `sam-cell-seg` | `supreme` | FAIL | 443.4s | 50 | 256,505 | 0/1 | `8129c1970953bf4c...` |
| **76** | `sam-cell-seg` | `superpowers` | FAIL | 7221.9s | 4 | 24,150 | 2/9 | `335b32afb7ee2b2e...` |
| **76** | `sam-cell-seg` | `baseline` | FAIL | 3327.8s | 87 | 470,392 | 1/9 | `d1e2eae677011822...` |
| **77** | `sanitize-git-repo` | `supreme` | FAIL | 455.7s | 67 | 397,240 | 2/3 | `1beef57ad9b516e2...` |
| **77** | `sanitize-git-repo` | `superpowers` | FAIL | 397.9s | 57 | 337,399 | 2/3 | `24991ab0c74abb84...` |
| **77** | `sanitize-git-repo` | `baseline` | FAIL | 271.9s | 47 | 259,253 | 2/3 | `20a053570868fd26...` |
| **78** | `schemelike-metacircular-eval` | `supreme` | PASS | 399.6s | 61 | 353,822 | 1/1 | `b7375f80bb1f5760...` |
| **78** | `schemelike-metacircular-eval` | `superpowers` | PASS | 2411.0s | 28 | 168,066 | 1/1 | `29c808ce69fd97a7...` |
| **78** | `schemelike-metacircular-eval` | `baseline` | PASS | 360.9s | 48 | 318,338 | 1/1 | `57c3ed1a43f2491a...` |
| **79** | `sparql-university` | `supreme` | PASS | 485.4s | 47 | 319,827 | 3/3 | `4461f4980dbf8539...` |
| **79** | `sparql-university` | `superpowers` | PASS | 493.6s | 61 | 353,750 | 3/3 | `6f676b97b6bd9e64...` |
| **79** | `sparql-university` | `baseline` | PASS | 476.6s | 59 | 370,504 | 3/3 | `44dbbee527017712...` |
| **80** | `sqlite-db-truncate` | `supreme` | PASS | 78.6s | 28 | 160,130 | 1/1 | `f41e31e9b2bd259d...` |
| **80** | `sqlite-db-truncate` | `superpowers` | PASS | 73.2s | 23 | 129,168 | 1/1 | `1aa3d2c468741dde...` |
| **80** | `sqlite-db-truncate` | `baseline` | PASS | 93.8s | 31 | 189,643 | 1/1 | `8946074e89305994...` |
| **81** | `sqlite-with-gcov` | `supreme` | PASS | 457.0s | 41 | 238,518 | 3/3 | `3d0ed1865a912730...` |
| **81** | `sqlite-with-gcov` | `superpowers` | PASS | 775.4s | 53 | 251,707 | 3/3 | `02c3ab796f4becad...` |
| **81** | `sqlite-with-gcov` | `baseline` | PASS | 879.3s | 40 | 210,024 | 3/3 | `c52539182915334d...` |
| **82** | `torch-pipeline-parallelism` | `supreme` | FAIL | 606.5s | 59 | 316,261 | 0/1 | `f4154af1fa1c4b49...` |
| **82** | `torch-pipeline-parallelism` | `superpowers` | FAIL | 623.8s | 58 | 276,805 | 0/1 | `499ba3a872bb2ef2...` |
| **82** | `torch-pipeline-parallelism` | `baseline` | FAIL | 662.0s | 33 | 159,382 | 0/1 | `568a69a802441b70...` |
| **83** | `torch-tensor-parallelism` | `supreme` | FAIL | 909.4s | 96 | 575,924 | 0/1 | `90d990a0d8772b31...` |
| **83** | `torch-tensor-parallelism` | `superpowers` | FAIL | 195.1s | 35 | 188,826 | 0/1 | `a66cbecb8beb61a0...` |
| **83** | `torch-tensor-parallelism` | `baseline` | FAIL | 910.2s | 39 | 242,639 | 0/1 | `dcd6cd1725e73af3...` |
| **84** | `train-fasttext` | `supreme` | FAIL | 1850.5s | 59 | 393,981 | 1/2 | `6a179e7ff42baef5...` |
| **84** | `train-fasttext` | `superpowers` | FAIL | 1173.8s | 196 | 1,261,420 | 1/2 | `edd30d988f65bc14...` |
| **84** | `train-fasttext` | `baseline` | FAIL | 1857.2s | 41 | 343,411 | 1/2 | `f74123a9364ea592...` |
| **85** | `tune-mjcf` | `supreme` | PASS | 414.9s | 81 | 436,922 | 4/4 | `7d3336f16a717176...` |
| **85** | `tune-mjcf` | `superpowers` | FAIL | 813.0s | 126 | 543,089 | 3/4 | `e812f4b58c7cc1bd...` |
| **85** | `tune-mjcf` | `baseline` | FAIL | 501.8s | 57 | 384,399 | 3/4 | `eb771df477cafaef...` |
| **86** | `video-processing` | `supreme` | PASS | 1074.3s | 52 | 524,929 | 5/5 | `62a64ff2ad1d041a...` |
| **86** | `video-processing` | `superpowers` | PASS | 1510.8s | 73 | 485,951 | 5/5 | `99893605200d50c7...` |
| **86** | `video-processing` | `baseline` | FAIL | 1602.7s | 71 | 408,511 | 4/5 | `faf63f21e1f7ca47...` |
| **87** | `vulnerable-secret` | `supreme` | PASS | 58.5s | 17 | 96,941 | 3/3 | `296ab2cb89a62ec9...` |
| **87** | `vulnerable-secret` | `superpowers` | PASS | 61.7s | 17 | 99,854 | 3/3 | `6339b2429aae8e0b...` |
| **87** | `vulnerable-secret` | `baseline` | FAIL | 14.2s | 1 | 22,585 | 0/3 | `04b1d842f0c6a2d9...` |
| **88** | `winning-avg-corewars` | `supreme` | PASS | 175.0s | 53 | 300,413 | 3/3 | `9e88215e8b93b6ab...` |
| **88** | `winning-avg-corewars` | `superpowers` | PASS | 1648.7s | 535 | 3,513,757 | 3/3 | `9295ca3da249f2d8...` |
| **88** | `winning-avg-corewars` | `baseline` | PASS | 1104.0s | 249 | 2,163,114 | 3/3 | `34f75da3f80cbe99...` |
| **89** | `write-compressor` | `supreme` | PASS | 299.2s | 64 | 457,183 | 3/3 | `0d22945e3919ccdd...` |
| **89** | `write-compressor` | `superpowers` | PASS | 150.6s | 42 | 262,319 | 3/3 | `8a67dc198f8dd307...` |
| **89** | `write-compressor` | `baseline` | PASS | 152.1s | 28 | 171,660 | 3/3 | `506160ac4fa111d2...` |

---

## Telemetry & Accounting Standard

1. **Token Accounting:** Total tokens is defined strictly as `Input Tokens + Output Tokens`.
2. **Reasoning / Thinking Tokens:** Internal thinking tokens (`thinking_tokens`) are a strict subset of Output Tokens.
3. **Cryptographic Validation:** Each entry's `sha256_verifier` hash represents the SHA-256 checksum of the container verifier log (`verifier_output.log`), guaranteeing reproducibility.

---

## Data Quality Notes

1. **`mailman` / `superpowers` (Task #44):** Verifier-graded PASS (3/3 tests, SHA-256 hash above) with degraded agent telemetry — the stream capture failed, so turn/tool/token counts are placeholders. The graded result is retained as-is.
2. **Wall-clock vs. task timeouts:** Recorded wall-clock spans the full container session (execution plus teardown). 37 of 267 runs exceeded the task's configured timeout; 36 of them by session teardown overhead of at most 39.2s. One anomalous session (`merge-diff-arc-agi-task` / `baseline`, 7,035.2s against a 900s limit) is retained as recorded.

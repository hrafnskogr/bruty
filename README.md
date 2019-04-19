# Bruty
Multiprocessing brute-forcer:
- HTTP BasicAuth (either GET or HEAD requests)
- SSH
- Permutation or dictionary

# Entropass (in tools)
Password entropy calculator:
- -t entropy display lower threshold, display only if entropy is higher or equal to this value
- -T entropy display upper threshold, display only if entropy is lower or equal to this value
- -c force the calculation to be done with the charset size
Entropass computes entropy with this formula: H(K)=Log2(K) . Where K is the keyspace size (automatically evaluated for each password).

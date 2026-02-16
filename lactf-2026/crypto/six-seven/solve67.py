import binascii
from Crypto.Util.number import long_to_bytes
n=2544225952939476681572793849456251319180909025627219708553288156674004505461529613572349541891887744582823162109585161030940602561698239240104101593826114563622584908090238278353434124301380223666717451976038446647302021032588236446075231590087016828307751382706296522913142892636304569083947767827846376040096661343734859538035818919983128478316191793700101712703284177517718165182991166661951036120641
c=2476488768936196344690057028187380112438971881808177849767894612812950616942728919332517539016456583129493407366020760509953286294471460377162578189084866559783049649546344662064639073009763280720739438640923530319341742670022751301952481688394291734140907242056932309336775735348185824664792454344245166007335913302420315924734886191147992217621531442629899400972317850823992376963950324486134042453605
e = 65537

def solve():
    # p and q end in 7
    candidates = [(7, 7)]
    
    # We need to find 256 digits
    for i in range(1, 256):
        new_candidates = []
        mod = 10**(i + 1)
        target = n % mod
        
        for p_val, q_val in candidates:
            # Test all combinations of next digits
            for p_digit in [6, 7]:
                for q_digit in [6, 7]:
                    p_next = p_digit * (10**i) + p_val
                    q_next = q_digit * (10**i) + q_val
                    
                    if (p_next * q_next) % mod == target:
                        new_candidates.append((p_next, q_next))
        
        candidates = new_candidates
        # Optimization: If we have multiple branches, just keep going. 
        # Usually, only 1 or 2 branches survive.
    
    return candidates

all_pairs = solve()
print(f"[+] Found {len(all_pairs)} potential candidate pairs.")

for i, (p_test, q_test) in enumerate(all_pairs):
    # Verification 1: Do they multiply to n?
    if p_test * q_test == n:
        print(f"[!] Verification successful for pair {i}!")
        
        # Verification 2: Are they prime? (Optional but good)
        # from Crypto.Util.number import isPrime
        # if not isPrime(p_test): continue

        phi = (p_test - 1) * (q_test - 1)
        d = pow(e, -1, phi)
        m = pow(c, d, n)
        
        decrypted_bytes = long_to_bytes(m)
        if b"lactf{" in decrypted_bytes:
            print(f"SUCCESS! Flag: {decrypted_bytes.decode()}")
            break
        else:
            print(f"Pair {i} multiplied correctly but resulted in garbage. Still searching...")

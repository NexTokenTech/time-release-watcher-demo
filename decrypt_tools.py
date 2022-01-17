import sys

sys.path.append("../Time-Capsule-Watcher/Time-Release-Blockchain")
from crypto.elgamal import PublicKey, PrivateKey
from crypto.elgamal_util import *
import crypto.elgamal as elgamal
from mining.pollard_rho_solution import *


# decrpyt release block relation tx's message
def decrypt_msg_solution(pubkey: str, solution_str: str, chiper: str):
    pubkey_str_list = pubkey.split(", ")
    # print(strlist)
    p = int(pubkey_str_list[2], 16)
    g = int(pubkey_str_list[0], 16)
    h = int(pubkey_str_list[1], 16)
    bit_length = int(pubkey_str_list[3])
    pub_key = PublicKey(p, g, h, bit_length)

    solution = PRSolution.from_str(solution_str.replace(" ", ""))
    solution.pubkey = pub_key

    private_key = solution.generate_private_key()
    print("Privatekey:{} {} {} {}".format(private_key.p, private_key.g, private_key.x, private_key.bit_length))

    y = mod_exp(pub_key.g, private_key.x, pub_key.p)
    # x = pollard_rho(pub_key.g, pub_key.h, pub_key.p, private_key.x)
    print("if the h is equal to pubkey.h,private key is right;now h is:{}".format(y))

    plain = elgamal.decrypt(private_key, chiper)
    return plain

"""
{ blockHash: '0x0515b2216fa8012618c330bff363d7a49876f4b0f05752b17b01597b5527a604',
  blockNumber: 3015063,
  from: '0x6b477781b0e68031109f21887e6b5afeaaeb002b',
  gas: 21000,
  gasPrice: BigNumber { s: 1, e: 9, c: [ 1000000000 ] },
  hash: '0xd79fc80e7b787802602f3317b7fe67765c14a7d40c3e0dcb266e63657f881396',
  input: '0x',  nonce: 0,
  r: '0x69a726edfb4b802cbf267d5fd1dabcea39d3d7b4bf62b9eeaeba387606167166',
  s: '0x7724cedeb923f374bef4e05c97426a918123cc4fec7b07903839f12517e1b3c8',
  to: '0x92b28647ae1f3264661f72fb2eb9625a89d88a31',
  transactionIndex: 9,
  v: '0x29',
  value: BigNumber { s: 1, e: 18, c: [ 12300 ] } }
> web3.eth.getTransaction("0x061bf0b4b5fdb64ac475795e9bc5a3978f985919ce6747ce2cfbbcaccaf51009")
{ blockHash: '0xe23306ce25e2e0329ed148f17e16b3b566b2b42cb86bf4ece5b41a0fee30a497',
  blockNumber: 3015068,
  from: '0x6b477781b0e68031109f21887e6b5afeaaeb002b',
  gas: 21000,
  gasPrice: BigNumber { s: 1, e: 9, c: [ 1000000000 ] },
  hash: '0x061bf0b4b5fdb64ac475795e9bc5a3978f985919ce6747ce2cfbbcaccaf51009',
  input: '0x',  nonce: 1,
  r: '0x69a726edfb4b802cbf267d5fd1dabcea39d3d7b4bf62b9eeaeba387606167166',
  s: '0x2bbd9c2a6285c2b43e728b17bda36a81653dd5f4612a2e0aefdb48043c5108de',
  to: '0x92b28647ae1f3264661f72fb2eb9625a89d88a31',
  transactionIndex: 17,
  v: '0x29',
  value: BigNumber { s: 1, e: 18, c: [ 18112, 66580600000000 ] } }
> 

"""


def derivate_privkey(p, r, s1, s2, hash1, hash2):
    z = hash1 - hash2
    s = s1 - s2
    r_inv = inverse_mod(r, p)
    s_inv = inverse_mod(s, p)
    k = (z * s_inv) % p
    d = (r_inv * (s1 * k - hash1)) % p
    return d, k

def inverse_mod( a, m ):
    """Inverse of a mod m."""
    if a < 0 or m <= a: a = a % m
    # From Ferguson and Schneier, roughly:
    c, d = a, m
    uc, vc, ud, vd = 1, 0, 0, 1
    while c != 0:
        q, c, d = divmod( d, c ) + ( c, )
        uc, vc, ud, vd = ud - q*uc, vd - q*vc, uc, vc

    # At this point, d is the GCD, and ud*a+vd*m = d.
    # If d == 1, this means that ud is a inverse.
    assert d == 1
    if ud > 0: return ud
    else: return ud + m

import ecdsa
import ethereum
import binascii

n = ecdsa.SECP256k1.order

r = int('0x69a726edfb4b802cbf267d5fd1dabcea39d3d7b4bf62b9eeaeba387606167166', 0)

r1 = r
s1 = int('0x7724cedeb923f374bef4e05c97426a918123cc4fec7b07903839f12517e1b3c8', 0)
z1 = int('0xd79fc80e7b787802602f3317b7fe67765c14a7d40c3e0dcb266e63657f881396', 0)
# z1 = int('0x350f3ee8007d817fbd7349c477507f923c4682b3e69bd1df5fbb93b39beb1e04', 0)


r2 = r
s2 = int('0x2bbd9c2a6285c2b43e728b17bda36a81653dd5f4612a2e0aefdb48043c5108de', 0)
z2 = int('0x061bf0b4b5fdb64ac475795e9bc5a3978f985919ce6747ce2cfbbcaccaf51009', 0)
# z2 = int('0x4f6a8370a435a27724bbc163419042d71b6dcbeb61c060cc6816cda93f57860c', 0)

if r1 == r2:
    print("Vulnerable")

z_options = [
    z2 - z1,
    z1 - z2,
    z1 + z2,
    - z1 - z2
]
s_options = [
    s2 - s1,
    s1 - s2,
    s1 + s2,
    - s1 - s2,
]

for z in z_options: 
    for s in s_options:
        r_inv = inverse_mod(r, n)
        s_inv = inverse_mod(s, n)
        k = (z * s_inv) % n

        pk1 = (s1 * k - z1) * inverse_mod(r1, n) % n
        pk2 = (s2 * k - z2) * inverse_mod(r2, n) % n

        if (pk1 != pk2):
            continue

        addr = ethereum.utils.privtoaddr(pk1)
        print("pk {} = addr 0x{}".format(hex(pk1), addr.hex()))


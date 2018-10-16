const ethUtils = require("ethereumjs-util");
const secp256k1 = require("secp256k1");

const hash = Buffer.from('abc467bedd1d17462fcc7942d0af7874d6f8bdefee2b299c9168a216d3ff0edb', 'hex');

const v = 0x29;
const r = Buffer.from('a5522718c0f95dde27f0827f55de836342ceda594d20458523dd71a539d52ad7', 'hex');
const s = Buffer.from('5710e64311d481764b5ae8ca691b05d14054782c7d489f3511a7abf2f5078962', 'hex');

const pubKey = ethUtils.ecrecover(
    hash,
    v,
    r,
    s,
    3,
)

const sha3 = ethUtils.keccak256(pubKey);
const address = ethUtils.pubToAddress(pubKey);

console.log("pubkey: ", pubKey.toString('hex'));
console.log("sha3  : ", sha3.toString('hex'));
console.log("addr  : ", address.toString('hex'));

// 0x92b28647ae1f3264661f72fb2eb9625a89d88a31

const pubkey = Buffer.from('03c0a51ba6b98fadbf48aecfb703f5c371eeb228f2a3e1366df7158e56bb121ce4', 'hex');
console.log("convertedKey: ", secp256k1.publicKeyConvert(pubkey, false).slice(1).toString('hex'));

// WHY NO WORK?
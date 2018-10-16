const EthereumTx = require('ethereumjs-tx')

const txParams = {
    nonce: '0x00',
    gasPrice: '0x3b9aca00',
    gasLimit: '0x15f90',
    to: '0x6b477781b0e68031109f21887e6b5afeaaeb002b',
    value: '0x00',
    data: '0x5468616e6b732c206d616e21',
    hash: '0xabc467bedd1d17462fcc7942d0af7874d6f8bdefee2b299c9168a216d3ff0edb',
    // EIP 155 chainId - mainnet: 1, ropsten: 3
    chainId: 3
}

const tx = new EthereumTx(txParams)

console.log(tx.verifySignature());
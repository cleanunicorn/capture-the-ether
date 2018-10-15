package main

import (
	"encoding/hex"
	"fmt"
	"strings"

	"github.com/ethereum/go-ethereum/common"
	"github.com/ethereum/go-ethereum/crypto"
)

func computeToContractAddr(contractHex string, nonce uint64) (string, error) {
	// Transform contractHex to Address
	contractHex = strings.TrimPrefix(contractHex, "0x")
	sBytes, err := hex.DecodeString(contractHex)
	if err != nil {
		fmt.Printf("cannot decode string: %v, to hex, err: %v\n", contractHex, err)
		return "", err
	}
	var addrHex [20]byte
	copy(addrHex[:], sBytes[:20])
	var addr common.Address = common.Address(addrHex)

	// Create contract address
	contractAddr := crypto.CreateAddress(addr, nonce)

	// Transform contract address to hex representation in string
	dst := make([]byte, 20)
	copy(dst[:], contractAddr[:20])
	contractAddrStr := hex.EncodeToString(dst)
	return contractAddrStr, nil
}

func main() {
	var i uint64

infiniteLoop:
	for {
		wallet, _ := crypto.GenerateKey()
		walletAddress := crypto.PubkeyToAddress(wallet.PublicKey).Hex()

		for i = 0; i < 10; i++ {
			if contractAddr, err := computeToContractAddr(walletAddress, i); err == nil {
				if strings.Index(contractAddr, "badc0de") != -1 {
					fmt.Printf("Found contractAddress: %v\n", contractAddr)
					fmt.Printf("PrivateKey = %v\n", hex.EncodeToString(wallet.D.Bytes()))
					fmt.Printf("Address = %v\n", walletAddress)
					fmt.Printf("Nonce = %v\n", i)
					break infiniteLoop
				}
			}
		}
	}

	// Found contractAddress: 42308e092d9f053badc0de4262140bcafffa998d
	// PrivateKey = 88df25620fdc2bc287e70d9e4b4267090d6e5c5202c70c4fc157f0117ca95529
	// Address = 0x2D68195850E8Df206c18a5a16CFafe5a548f1F9D
	// Nonce = 1
}

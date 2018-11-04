package main

import (
	"encoding/hex"
	"fmt"
	"strings"

	"crypto/ecdsa"
	"crypto/rand"

	"github.com/ethereum/go-ethereum/crypto"
)

// Address returns the address as a string
func Address(key *ecdsa.PrivateKey) string {
	return crypto.PubkeyToAddress(key.PublicKey).Hex()
}

// PrivateKey returns the private key as a string
func PrivateKey(key *ecdsa.PrivateKey) string {
	return hex.EncodeToString(key.D.Bytes())
}

func main() {
	// fmt.Println(crypto.S256())

	for {
		k, _ := ecdsa.GenerateKey(crypto.S256(), rand.Reader)
		if strings.ToLower(Address(k)) == "0x6b477781b0e68031109f21887e6b5afeaaeb002b" {
			fmt.Println(PrivateKey(k))
			break
		}
	}
}

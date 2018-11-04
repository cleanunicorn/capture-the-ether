package main

import (
	"encoding/hex"
	"fmt"

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
	for {
		k, _ := ecdsa.GenerateKey(crypto.S256(), rand.Reader)

		pubBytes := crypto.FromECDSAPub(&k.PublicKey)

		if fmt.Sprintf("%x", pubBytes[1:]) == "a96c5530f604e0a359fea09254be691ade6c5de5fb351a66d961f84c0044e1cee3890476d47ca85ace1df513235ce825b409d49cd8ba1f305ca8d580aefb74c4" {
			fmt.Println("Address: ", Address(k))
			fmt.Println("Privatekey: ", PrivateKey(k))
			break
		}
	}
}

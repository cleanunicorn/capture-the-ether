package main

import (
	"bytes"
	"crypto/ecdsa"
	"encoding/hex"
	"fmt"
	"io"
	"math/big"

	"github.com/ethereum/go-ethereum/crypto"
)

type BadRand struct {
	reader             io.Reader
	expectedTotalBytes uint
}

func NewBadRand(out int64, outputLen uint) *BadRand {
	x := big.NewInt(out)
	y := make([]byte, outputLen)
	tail := x.Bytes()

	for i, j := len(tail)-1, len(y)-1; i >= 0 && j > 0; i, j = i-1, j-1 {
		y[j] = tail[i]
	}

	return &BadRand{
		reader:             bytes.NewReader(y),
		expectedTotalBytes: outputLen,
	}
}

func (b *BadRand) Read(p []byte) (n int, err error) {
	return b.reader.Read(p)
}

// Address returns the address as a string
func Address(key *ecdsa.PrivateKey) string {
	return crypto.PubkeyToAddress(key.PublicKey).Hex()
}

// PrivateKey returns the private key as a string
func PrivateKey(key *ecdsa.PrivateKey) string {
	return hex.EncodeToString(key.D.Bytes())
}

func main() {
	var i int64
	for i = 0; true; i++ {
		br := NewBadRand(i, 40)

		k, err := ecdsa.GenerateKey(crypto.S256(), br)
		if err != nil {
			fmt.Println("Generate key error: ", err)
		}

		pubBytes := crypto.FromECDSAPub(&k.PublicKey)

		if fmt.Sprintf("%x", pubBytes[1:]) == "a96c5530f604e0a359fea09254be691ade6c5de5fb351a66d961f84c0044e1cee3890476d47ca85ace1df513235ce825b409d49cd8ba1f305ca8d580aefb74c4" {
			fmt.Println("Address: ", Address(k))
			fmt.Println("Privatekey: ", PrivateKey(k))
			break
		}

		if i%100000 == 0 {
			br := NewBadRand(i, 40)

			out := make([]byte, 40)
			n, err := io.ReadFull(br, out)
			if err != nil {
				fmt.Println("BAD READ!", err)
			}

			fmt.Printf("%v bytes read\n", n)
			fmt.Printf("%v\n", out)

			fmt.Printf("i = %d\n", i)
		}
	}
}

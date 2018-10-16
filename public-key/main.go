package main

import (
	"fmt"
	"math/big"
	"strings"
	"time"

	"github.com/ethereum/go-ethereum/crypto"
)

func func1(mustMatch string) {
	i := new(big.Int).SetInt64(0)
	one := new(big.Int).SetInt64(1)

	for {
		bs := i.Bytes()

		hash := crypto.Keccak256Hash(bs)
		address := hash.Hex()[2+64-len(mustMatch):]

		if address == mustMatch {
			fmt.Printf("%x = %v\n", bs, hash.Hex())
			break
		}

		i = i.Add(i, one)
	}
}

func func2(mustMatch string) {
	i := new(big.Int).SetInt64(0)
	one := new(big.Int).SetInt64(1)

	for {
		bs := i.Bytes()

		hash := crypto.Keccak256Hash(bs)

		if strings.HasSuffix(hash.Hex(), mustMatch) {
			fmt.Printf("%x = %v\n", bs, hash.Hex())
			break
		}

		i = i.Add(i, one)
	}
}

func func3(mustMatch string, parallel int) {
	i := new(big.Int).SetInt64(0)
	one := new(big.Int).SetInt64(1)

	stop := false

	limit := make(chan *big.Int, parallel)

	for i := 0; i < parallel; i++ {

		go func(limit <-chan *big.Int) {
			for n := range limit {
				bs := n.Bytes()

				hash := crypto.Keccak256Hash(bs)

				if strings.HasSuffix(hash.Hex(), mustMatch) {
					fmt.Printf("%x = %v\n", bs, hash.Hex())
					stop = true
				}
			}
		}(limit)
	}

	steps := 0

	for stop == false {
		if (steps % 1000000) == 0 {
			steps = 0
			fmt.Printf("%v\n", i)
		}

		limit <- new(big.Int).Set(i)
		i = i.Add(i, one)
		steps++
	}
}

func benchmark() {
	var start time.Time
	// mustMatch := "92b28647ae1f3264661f72fb2eb9625a89d88a31"
	mustMatch := "1234567"

	// Func1
	start = time.Now()
	func1(mustMatch)
	fmt.Println("func1 Time:", time.Since(start))

	// Func2
	start = time.Now()
	func2(mustMatch)
	fmt.Println("func2 Time:", time.Since(start))

	// Func3
	for p := 4; p <= 128; p += 4 {
		start = time.Now()
		func3(mustMatch, p)
		fmt.Printf("func3(%v,%v) Time:%v\n", mustMatch, p, time.Since(start))

		<-time.After(1 * time.Second)
	}
}

func main() {
	// mustMatch := "92b28647ae1f3264661f72fb2eb9625a89d88a31"
	mustMatch := "a89d88a31"
	p := 32

	start := time.Now()
	func3(mustMatch, p)
	fmt.Printf("func3(%v,%v) Time:%v\n", mustMatch, p, time.Since(start))
}

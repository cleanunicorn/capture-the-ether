pragma solidity ^0.4.21;

import "./a.sol";
import "./b.sol";

// ropsten: 0xc9AFAA0B523e50948D33AAea0525b31dB725402d

contract Factory {
    function play(address lottery) public payable {
        AlwaysWin a = (new AlwaysWin).value(msg.value)(lottery);
    }
}
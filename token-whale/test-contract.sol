pragma solidity ^0.4.21;

contract Tok {
    constructor(address _player) public {
        player = _player;
        totalSupply = 1000;
        balanceOf[player] = 1000;
    }
}
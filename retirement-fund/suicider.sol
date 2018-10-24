pragma solidity 0.4.24;

contract Suicider {
    constructor (address akrasia) public payable {
        selfdestruct(akrasia);
    }
}
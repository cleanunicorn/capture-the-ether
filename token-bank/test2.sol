pragma solidity ^0.4.24;


contract A {
    uint256 public a = 1234;

    function add(uint256 b) public {
        a += b;
    }

    function isComplete() public view returns (bool) {
        return a < 1234;
    }
}
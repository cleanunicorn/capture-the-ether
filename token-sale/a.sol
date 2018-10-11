pragma solidity 0.4.25;

contract FindOverflow {
    function returnEther(uint256 etherCount) returns (uint256) {
        return (1 ether);
    }
    
    function returnMaxBuy() returns (uint256, uint256) {
        uint256 max = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF;
        uint256 denomination = 1 ether;
        uint256 tokenOverflow = (max / denomination) + 1;
        
        uint256 mustPay = tokenOverflow * denomination;
        
        return (tokenOverflow, mustPay);
    }
}

// price: 415992086870360064 wei
// token number: 115792089237316195423570985008687907853269984665640564039458

// 1 ether = 1000000000000000000
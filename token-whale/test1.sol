pragma solidity ^0.4.21;

import "./token-whale.sol";


contract Test1 is TokenWhaleChallenge {
    function solution() public view {
        assert(balanceOf[msg.sender] < 1000000);
    }
}

// contract T is Tok {
//     function b() public view returns(uint256) {
//         return 0x1234;
//     }
// }
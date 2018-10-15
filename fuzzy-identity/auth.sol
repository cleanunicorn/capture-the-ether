pragma solidity 0.4.24;

interface FuzzyIdentityChallenge {
    function authenticate() public;
}

contract CaptureFuzzy {
    function name() external view returns (bytes32) {
        return bytes32("smarx");
    }
    
    function play(address addr) {
        FuzzyIdentityChallenge f = FuzzyIdentityChallenge(addr);
        f.authenticate();
    }    
}
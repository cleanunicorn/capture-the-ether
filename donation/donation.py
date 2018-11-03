from manticore.core.smtlib import Operators
from manticore.ethereum import ManticoreEVM, ABI

# Setup
m = ManticoreEVM()
with open('donation.sol') as f:
    source_code = f.read()

# Deploy
user_account = m.create_account(balance=10 * 10**18)
contract_account = m.solidity_create_contract(
    source_code, owner=user_account, balance=10**18)

# Two raw transactions from the attacker
hacker_account = m.create_account(balance=0)

# Deposit
# symbolic_balance = m.make_symbolic_value()
# symbolic_eth = m.make_symbolic_value()
# contract_account.donate(symbolic_balance, balance=symbolic_eth)

#
symbolic_data = m.make_symbolic_buffer(36)
m.transaction(caller=hacker_account,
              address=contract_account,
              data=symbolic_data,
              value=0)


# 
symbolic_data = m.make_symbolic_buffer(36)
m.transaction(caller=hacker_account,
              address=contract_account,
              data=symbolic_data,
              value=0)

#
symbolic_data = m.make_symbolic_buffer(36)
m.transaction(caller=hacker_account,
              address=contract_account,
              data=symbolic_data,
              value=0)

bug_found = False
for state in m.running_states:
    balance = state.platform.get_balance(contract_account.address)
    state.constrain(balance == 0)
    if state.is_feasible():
        print("[!] Bug found see {}".format(m.workspace))
        m.generate_testcase(state, 'Bug')
        bug_found = True

if not bug_found:
    print("No bugs!")

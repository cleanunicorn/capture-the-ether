#!/usr/bin/python

from manticore.ethereum import ManticoreEVM, ABI
from manticore.core.smtlib import Operators, solver

###### Initialization ######
m = ManticoreEVM()

with open('test4.sol') as f:
    source_code = f.read()

bytecode = m.compile(
    source_code,
    # contract_name="GuessTheNumberChallenge"
)

# Add hacker's address
hacker_account = m.create_account(balance=1000*10**18, address=42)
# bytecode = bytecode + bytes.fromhex("000000000000000000000000000000000000002a")

# Create one user account
# And deploy the contract
user_account = m.create_account(balance=1000*10**18)

contract_account = m.create_contract(
    init=bytecode,
    owner=user_account,
    balance=10**18
)

###### Exploration ######

symbolic_data = m.make_symbolic_buffer(36)
m.transaction(
    caller=hacker_account,
    address=contract_account,
    data=symbolic_data,
    value=10**18)

# symbolic_data = m.make_symbolic_buffer(320)
# m.transaction(
#     caller=hacker_account,
#     address=contract_account,
#     data=symbolic_data,
#     value=0)

# b2fa1c9e = isComplete()
m.transaction(
    caller=hacker_account,
    address=contract_account,
    data=bytes.fromhex("b2fa1c9e"),
    value=0)

bug_found = False
# Explore all the forks
for state in m.running_states:
    complete = state.platform.transactions[-1].return_data
    complete = ABI.deserialize("uint256", complete)

    print(complete)

    # Set constraint
    state.constrain(Operators.UGT(complete, 0))
    if state.is_feasible():
        print("Bug found! see {}".format(m.workspace))
        m.generate_testcase(state, 'Bug')
        bug_found = True

if not bug_found:
    print('No bug were found')

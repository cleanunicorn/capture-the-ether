#!/usr/bin/python

from manticore.ethereum import ManticoreEVM, ABI
from manticore.core.smtlib import Operators, solver

###### Initialization ######
m = ManticoreEVM()

with open('test2.sol') as f:
    source_code = f.read()

bytecode = m.compile(source_code, contract_name="A")

# Add hacker's address
hacker_account = m.create_account(balance=0, address=42)
bytecode = bytecode + bytes.fromhex("000000000000000000000000000000000000002a")

# Create one user account
# And deploy the contract
user_account = m.create_account(balance=1000)

contract_account = m.create_contract(
    init=bytecode,
    owner=user_account,
    balance=0)

###### Exploration ######

symbolic_data = m.make_symbolic_buffer(320)
m.transaction(
    caller=hacker_account,
    address=contract_account,
    data=symbolic_data,
    value=0)

# b2fa1c9e = isComplete()
m.transaction(
    caller=hacker_account,
    address=contract_account,
    data=bytes.fromhex("b2fa1c9e"),
    value=0)


# symbolic_data = m.make_symbolic_buffer(320)
# m.transaction(
#     caller=hacker_account,
#     address=contract_account,
#     data=symbolic_data,
#     value=0)

# contract_account.isComplete()

bug_found = False
# Explore all the forks
for state in m.running_states:

    # state.plateform.transactions returns the list of transactions
    # state.plateform.transactions[0] is the first transaction
    # state.plateform.transactions[-1] is the last transaction

    complete = state.platform.transactions[-1].return_data
    complete = ABI.deserialize("uint256", complete)

    # Set constraint
    state.constrain(Operators.UGT(complete, 0))
    if state.is_feasible():
        print("Bug found! see {}".format(m.workspace))
        m.generate_testcase(state, 'Bug')
        bug_found = True

if not bug_found:
    print('No bug were found')

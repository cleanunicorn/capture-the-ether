from manticore.ethereum import ManticoreEVM, ABI
from manticore.core.smtlib import Operators, solver

###### Initialization ######
m = ManticoreEVM()

with open('test1.sol') as f:
    source_code = f.read()

bytecode = m.compile(source_code)

# Create one user account
# And deploy the contract
user_account = m.create_account(balance=1000)
hacker_account = m.create_account(balance=0, address=42)

contract_account = m.solidity_create_contract(
    source_code,
    owner=user_account, balance=0, name="TokenBankChallenge")

###### Exploration ######

symbolic_data = m.make_symbolic_buffer(320)
m.transaction(
    caller=hacker_account,
    address=contract_account,
    data=symbolic_data,
    value=0)

symbolic_data = m.make_symbolic_buffer(320)
m.transaction(
    caller=hacker_account,
    address=contract_account,
    data=symbolic_data,
    value=0)

contract_account.isComplete()

bug_found = False
# Explore all the forks
for state in m.running_states:

    # state.plateform.transactions returns the list of transactions
    # state.plateform.transactions[0] is the first transaction
    # state.plateform.transactions[-1] is the last transaction

    complete = state.platform.transactions[-1].return_data
    complete = ABI.deserialize("bool", complete)

    # Check if it is possible to have balance_after > balance_before
    state.constrain(complete == False)
    if state.is_feasible():
        print("Bug found! see {}".format(m.workspace))
        m.generate_testcase(state, 'Bug')
        bug_found = True

if not bug_found:
    print('No bug were found')

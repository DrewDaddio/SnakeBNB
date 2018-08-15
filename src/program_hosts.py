from colorama import Fore
from infrastructure.switchlang import switch
import infrastructure.state as state
import services.data_service as svc

def run():
    print(' ****************** Welcome host **************** ')
    print()

    show_commands()

    while True:
        action = get_action()

        with switch(action) as s:
            s.case('c', create_account)
            s.case('a', log_into_account)
            s.case('l', list_cages)
            s.case('r', register_cage)
            s.case('u', update_availability)
            s.case('v', view_bookings)
            s.case('m', lambda: 'change_mode')
            s.case(['x', 'bye', 'exit', 'exit()'], exit_app)
            s.case('?', show_commands)
            s.case('', lambda: None)
            s.default(unknown_command)

        if action:
            print()

        if s.result == 'change_mode':
            return


def show_commands():
    print('What action would you like to take:')
    print('[C]reate an account')
    print('[L]ogin to your account')
    print('[R]egister a cage')
    print('[U]pdate cage availability')
    print('[V]iew your bookings')
    print('Change [M]ode (guest or host)')
    print('e[X]it app')
    print('[?] Help (this info)')
    print()


def create_account():
    print(' ****************** REGISTER **************** ')

    name = input('What is your name?')
    email = input('What is your email?').strip().lower()

    old_account = svc.find_account_by_email(email)
    if old_account:
        error_msg(f"ERROR: Account with Email {email} already exists.")
    state.active_account = svc.create_account(name, email)
    success_msg(f"Created new account with ID {state.active_account.id}.")

def log_into_account():
    print(' ****************** LOGIN **************** ')

    email = input('What is your emaio? '.strip().lower())
    account = svc.find_account_by_email(email)

    if not account:
        error_msg(f'Could not find account with email {email}.')
        return

    state.active_account = account
    success_msg('Logged in succesffully.')


def register_cage():
    print(' ****************** REGISTER CAGE **************** ')

    if not state.active_account:
        error_msg('You must login first to register a cage.')
        return

    meters = input('How many square meters is the cage? ')
    if not meters:
        error_msg('Cancelled')
        return

    meters = float(meters)
    carpeted = input('Is it carpeted [y, n]? ').lower().startswith('y')
    has_toys = input('Have snake toys [y, n]? ').lower().startswith('y')
    allow_dangerous = input('Can you host venomous snakes [y, n]? ').lower().startswith('y')
    price = float(input("How much are you charging? "))
    name = input("Give your cage a name: ")

    cage = svc.register_cage(
        state.active_account, name, allow_dangerous, has_toys, carpeted, meters, price
    )

    state.reload_account()
    success_msg(f'Register new cage with id {cage.id}.')

def list_cages(supress_header=False):
    if not supress_header:
        print(' ******************     Your cages     **************** ')

    if not state.active_account:
        error_msg('You must login first to register a cage.')
        return

    cages = svc.find_cages_for_user(state.active_account)
    print(f'You have {len(cages)} cages.')
    for c in cages:
        print(f' * {c.name} is {c.square_meters} meters.')



def update_availability():
    print(' ****************** Add available date **************** ')

    if not state.active_account:
        error_msg('You must log in first to register a cage')
        return

    list_cages(suppress_header=True)
    if not cage_number.strip():
        error_msg('Cancelled')
        print()
        return

    cage_number =input("Enter cage number: ")
    if not cage_number.strip():
        error_msg('Cancelled')
        print()
        return

    cage_number = int(cage_number)

    cages = svc.find_cages_for_user(state.active_account)
    selected_cage = cages[cage_number-1]

    success_msg("Selected cage {}".format(selected_cage.name))

    start_date = parser.parse(
        input("Enter available date [yyyy-mm-dd]: ")
    )

    days = int(input("How many days is tis block of time? "))

    svc.add_available_date(
        state.active_account,
        selected_cage,
        start_date,
        days
    )
    state.reload_account()

    success_msg(f'Date added to cage {selected_cage.name}')

def view_bookings():
    print(' ****************** Your bookings **************** ')

    # TODO: Require an account
    # TODO: Get cages, and nested bookings as flat list
    # TODO: Print details for each

    print(" -------- NOT IMPLEMENTED -------- ")


def exit_app():
    print()
    print('bye')
    raise KeyboardInterrupt()


def get_action():
    text = '> '
    if state.active_account:
        text = f'{state.active_account.name}> '

    action = input(Fore.YELLOW + text + Fore.WHITE)
    return action.strip().lower()


def unknown_command():
    print("Sorry we didn't understand that command.")


def success_msg(text):
    print(Fore.LIGHTGREEN_EX + text + Fore.WHITE)


def error_msg(text):
    print(Fore.LIGHTRED_EX + text + Fore.WHITE)
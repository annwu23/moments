from adb import DB

class Writer:
    def __init__(self):
        self.menu_title = 'Welcome to Moments{}!\nWhat would you like to do today?'
        self.account = ''
        self.menu = {
            'a':'Sign up or log in',
            'b':'Edit profile',
            'c':'Create a new moment',
            'd':'Edit moments',
            'e':'Check your stats',
            'q':'Quit'
        }
        self.menu_func = {
            'a': lambda c, s: self.login_or_enroll(c, s),
            'b': lambda c, s: self.edit_profile(c, s),
            'c': lambda c, s: self.create_moment(c, s),
            'd': lambda c, s: self.check_moment_stats(c, s),
            'e': lambda c, s: self.disable_moment(c, s),
        }
        self.divider = '='*20

    def show_menu(self, account=''):
        """show main menu"""
        print(self.divider)
        if self.account == '':
            print(self.menu_title.format(''))
        else:
            print(self.menu_title.format(', {}'.format(self.account)))
        print(self.divider)
        for fid, fname in self.menu.items():
            print('{}: {}'.format(fid, fname))
        print(self.divider)
        opt = input('>> ').lower()
        if opt in self.menu.keys():
            return opt, self.menu[opt]
        else:
            return '', 'Sorry, that\'s not an option!'

    def login_or_enroll(self, db, func_title):
        """Log in or sign up"""
        if self.account == '':
            account_input = input('Account: ')
            if db.check_if_account_enrolled(account_input, "WRITERS"):
                password_input = input('Password: ')
                if db.check_if_password_correct(account_input, "WRITERS", password_input):
                    self.account = account_input
                    print(db.get_account_info(self.account, "WRITERS"))
                else:
                    print("Incorrect password!")
            else:
                if db.insert_or_update_account(account_input, "WRITERS", 'insert'):
                    print('Account created! :) You may now log in.')
        else:
            print("You're already logged in!")

    def edit_profile(self, db, func_title):
        """Edits the writer's profile + description"""
        


with DB() as db:
    awriter = Writer()
    while True:
        func_id, func_name = awriter.show_menu()
        if func_id == 'q':
            break
        elif func_id == '':
            print(func_name)
        else:
            if awriter.account == '':
                func_id = 'a'
                print('Please sign up or log in first!')
            awriter.menu_func[func_id](db, func_name)
        print()
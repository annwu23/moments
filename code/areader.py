#areader.py

from adb import DB

class Reader:
    def __init__(self):
        self.menu_title = 'Welcome to Moments{}!\nWhat would you like to do today?'
        self.account = ''
        self.menu = {
            'a':'Sign up or log in',
            'b':'Browse',
            'c':'Search',
            'd':'Read your bookmarked moments',
            'e':'Show random moment',
            'f':'Show random writer',
            'q':'Quit',
        }
        self.menu_func = {
            'a': lambda c, s: self.login_or_enroll(c, s),
            'b': lambda c, s: self.browse(c, s),
            'c': lambda c, s: self.search(c, s),
            'd': lambda c, s: self.read_bookmarks(c, s),
            'e': lambda c, s: self.random_moment(c, s),
            'f': lambda c, s: self.random_writer(c, s),
        }
        self.divider = '='*20

    def show_menu(self, account=''):
        """ Main menu"""
        print(self.divider)
        if self.account == '':
            print(self.menu_title.format(""))
        else:
            print(self.menu_title.format(", {}".format(self.account)))
        print(self.divider)
        for fid, fname in self.menu.items():
            print('{}: {}'.format(fid, fname))
        print(self.divider)
        opt = input('Please select: ').lower()
        if opt in self.menu.keys():
            return opt, self.menu[opt]
        else:
            return '', 'No such option'
    
    def login_or_enroll(self, db, func_title):
        """Log in or sign up"""
        if self.account == '':
            account_input = input('Account: ')
            if db.check_if_account_enrolled(account_input, "READERS"):
                password_input = input('Password: ')
                if db.check_if_password_correct(account_input, "READERS", password_input):
                    self.account = account_input
                    print(db.get_account_info(self.account, "READERS"))
                else:
                    print("Incorrect password!")
            else:
                if db.insert_or_update_account(account_input, "READERS", 'insert'):
                    print('Account created! :) You may now log in.')
        else:
            print("You're already logged in!")
    
    def browse(self, db, func_title):
        browse_type = input("Browse by:\n1. Newest moments\n2. Most popular moments\n3. ")
    
    def search(self, db, func_title):
        search_type = input("Are you searching by:\n1. Title\n2. Writer\n>> ")
        if search_type == "1":
            title = input("Title: ")
            db.search_titles(title)
        elif search_type == "2":
            writer = input("Writer: ")
            if writer in db.get_all_writers():
                title_list = db.print_writer(writer)
                while True:
                    select = input("If you want to read one of these moments, just input its number. Otherwise, press enter.\n>> ")
                    if select.isnumeric():
                        if int(select) in range(1, len(title_list) + 1):
                            db.moment_menu(self.account, db.select_moment_with_attribute("TITLE", title_list[select - 1][3:]))
                            break
            else:
                print("Sorry, that writer isn't registered!")
        else:
            print("Not an option!")
    
    def read_bookmarks(self, db, func_title):
        bookmarks = db.fetch_bookmarks(self.account)
        for mark in range(len(bookmarks)):
            print("{}. \"{}\", by {}".format(mark + 1, bookmarks[mark][0], bookmarks[mark][0]))
        while True:
            select = input("If you want to read one of your bookmarks, just input its number. Otherwise, press enter.\n>> ")
            if select.isnumeric():
                if int(select) in range(1, len(bookmarks) + 1):
                    db.moment_menu(self.account, db.select_moment_with_attribute("TITLE", bookmarks[select - 1][0]))
                    break
            elif select == "":
                break

    def random_moment(self, db, func_title):
        my_id = db.random_id()
        if my_id is None:
            print("Sorry, there are currently no moments recorded. Try again later?")
            return
        print(db.print_moment(my_id))
        print("\n\n\n")
        db.moment_menu(self.account, my_id)
    
    def random_writer(self, db, func_title):
        my_writer = db.random_writer()
        if my_writer is not None:
            title_list = db.print_writer(my_writer)
            while True:
                select = input("If you want to read one of these moments, just input its number. Otherwise, press enter.\n>> ")
                if select.isnumeric():
                    if int(select) in range(1, len(title_list) + 1):
                        db.moment_menu(self.account, db.select_moment_with_attribute("TITLE", title_list[select - 1][3:]))
                        break
        else:
            print("Sorry, there are currently no writers signed up! Try again later?")
        

with DB() as db:
    areader = Reader()
    while True:
        func_id, func_name = areader.show_menu()
        if func_id == 'q':
            break
        elif func_id == '':
            print(func_name)
        else:
            if areader.account == '':
                func_id = 'a'
                print('Please sign up or log in first!')
            areader.menu_func[func_id](db, func_name)
        print()
    print("\n\nThank you for using Moments!")
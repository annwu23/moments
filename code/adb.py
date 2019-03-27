class DB:
    def __init__(self):
        self.conn = None
        self.cur = None
        self.title_side = '-'*12

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
        return False

    def open(self):
        """Turn on database connection"""
        if self.conn is None:
            import sqlite3
            self.conn = sqlite3.connect('moments.db') #dbname
            self.cur = self.conn.cursor()
        return True

    def close(self):
        """Turn off database connection"""
        if self.conn is not None:
            self.conn.close()
            self.conn = None
        return True
        
    def check_if_account_enrolled(self, arg_account, account_type):
        """Check if account is in database"""
        self.cur.execute("SELECT COUNT(*) FROM {} WHERE ACCOUNT=?".format(account_type), (arg_account,))
        if self.cur.fetchone()[0] == 1:
            return True
        else:
            return False
    
    def check_if_password_correct(self, arg_account, account_type, arg_password):
        """Check if password is correct"""
        self.cur.execute("SELECT PASSWORD FROM {} WHERE ACCOUNT=?".format(account_type), (arg_account,))
        if self.cur.fetchone()[0] == arg_password:
            return True
        else:
            return False
    
    def insert_or_update_account(self, account_id, account_type, action):
        """Add or update account"""
        data_ok = True
        full_name = input('Full name: ')
        if full_name == 'q':
            return False

        password = input('Password: ')
        if password == 'q':
            return False
        
        birth_year = input('Birth year: ')
        if birth_year.isdigit():
            birth_year = int(birth_year)
            if birth_year not in range(1918, 2006):
                data_ok = False
        else:
            data_ok = False

        # data is fine, go ahead
        if data_ok:
            if action == 'insert':
                    self.cur.execute("INSERT INTO {} VALUES (?, ?, ?, ?)".format(account_type), 
                        (account_id, full_name, password, birth_year))
            elif action == 'update':
                self.cur.execute("UPDATE {} SET NAME=?, PASSWORD=?, BIRTHYEAR=? WHERE ACCOUNT=?".format(account_type), 
                    (full_name, password, birth_year, account_id))
            self.conn.commit()
            return True
        else:
            return False
    
    def get_account_info(self, account, account_type):
        """Print account information"""
        account_info = "Account: {}\n".format(account)
        self.cur.execute("SELECT NAME FROM {} WHERE ACCOUNT=?".format(account_type), (account,))
        account_info += "Name: {}\n".format(self.cur.fetchone()[0])
        self.cur.execute("SELECT BIRTHYEAR FROM {} WHERE ACCOUNT=?".format(account_type), (account,))
        account_info += "Birthyear: {}".format(self.cur.fetchone()[0])
        return account_info
    
    def get_all_titles(self):
        """Returns list of titles in table of moments"""
        self.cur.execute("SELECT TITLE FROM MOMENTS")
        return self.cur.fetchall()

    def get_all_writers(self):
        """Returns list of writers in table of moments"""
        self.cur.execute("SELECT ACCOUNT FROM WRITERS")
        return self.cur.fetchall()

    def print_moment(self, num):
        """Print the moment out."""
        self.cur.execute("SELECT * FROM MOMENTS WHERE ID=?", (num,))
        moment = self.cur.fetchone()
        return ' '.join(("\n\n\nTITLE:", moment[1] + "\n\nBY:", moment[2] + "\n\n\n" + moment[3] + "\n\n\n" + "APPLAUSE:", str(moment[5])))
    
    def moment_menu(self, account, num):
        """Display options after reading moment"""
        while True:
            select = input("Would you like to:\n1. Leave applause\n2. Bookmark\n3. Leave")
            if select == "1":
                self.cur.execute("SELECT APPLAUSE FROM MOMENTS WHERE ID=?", (num,))
                app_num = self.cur.fetchone()[0]
                self.cur.execute("SELECT COUNT(*) FROM APPLAUSE WHERE ACCOUNT=? AND ID=?", (account, num))
                if self.cur.fetchone()[0] == 0:
                    self.cur.execute("UPDATE MOMENTS SET APPLAUSE=? WHERE ID=?", (app_num + 1, num))
                    self.cur.execute("INSERT INTO APPLAUSE VALUES (?, ?)", (account, num))
                    print("Thanks for applauding! :)")
                else:
                    self.cur.execute("UPDATE MOMENTS SET APPLAUSE=? WHERE ID=?", (app_num - 1, num))
                    self.cur.execute("DELETE FROM APPLAUSE WHERE ACCOUNT=? AND ID=?", (account, num))
                    print("Aw, you decided it wasn't so great after all? Maybe next time. :)")
                self.conn.commit()
                break
            elif select == "2":
                print(self.bookmark_moment(account, num))
                break
            elif select == "3":
                break
        return

    def search_titles(self, title):
        self.cur.execute("SELECT * FROM MOMENTS WHERE TITLE LIKE '%{}%'".format(title))
        titles = self.cur.fetchall()
        if titles == []:
            print("Sorry, no works with similar titles found!")
            return
        for i in range(len(titles) // 5 + 1):
            title_list = titles[(i * 5):(i * 5 + 5)]
            for i, title in enumerate(title_list):
                print("{}. {}".format(i + 1, title))
            select = input("To select a story to read, put in its ID.\nIf you're not interested in any of these moments, simply press enter.\n>> ")
            if select in range(i * 5, i * 5 + 5):
                print(print_moment(select))
                break

    def print_writer(self, account):
        self.cur.execute("SELECT ACCOUNT, NAME, BIRTHYEAR FROM WRITERS WHERE ACCOUNT=?", (account,))
        writer_list = self.cur.fetchone()[0]
        self.cur.execute("SELECT TITLE FROM MOMENTS WHERE ACCOUNT=?", (account,))
        title_list = self.cur.fetchall()
        print("Account: %s\nName: %s\nBirth year: %s" % writer_list)
        print("\nMoments written:")
        titles = ["{}. {}\n".format((i + 1), title_list[i][0]) for i in range(len(title_list))]
        for t in titles:
            print(t)
        return titles
    
    def select_moment_with_attribute(self, att_type, att):
        self.cur.execute("SELECT ID FROM MOMENTS WHERE {}=?".format(att_type), (att,))
        num = self.cur.fetchone()
        self.print_moment(num[0])
        return num[0]
        
    def bookmark_moment(self, account, num):
        self.cur.execute("INSERT INTO BOOKMARKS VALUES (?, ?)", (account, num))
        self.conn.commit()
        return "This moment was successfully bookmarked!"

    def random_id(self):
        import random
        self.cur.execute("SELECT COUNT(*) FROM MOMENTS")
        length = self.cur.fetchone()[0]
        if length != 0:
            return random.randint(1, length)
        else:
            return None
        
    def random_writer(self):
        import random
        self.cur.execute("SELECT ACCOUNT FROM WRITERS")
        writer_list = self.cur.fetchall()
        if writer_list != []:
            ran_writer = random.choice(writer_list)[0]
            return ran_writer
        return None

    def fetch_bookmarks(self, account):
        self.cur.execute("SELECT ID FROM BOOKMARKS WHERE ACCOUNT=?", (account,))
        mark_list = self.cur.fetchall()
        bookmarks = []
        for mark in range(len(mark_list)):
            self.cur.execute("SELECT TITLE, ACCOUNT FROM MOMENTS WHERE ID=?", (mark_list[mark][0],))
            bookmarks.append(self.cur.fetchone())
        return bookmarks

    def edit_profile(self, account):
        self.cur.execute("SELECT PROFILE FROM BOOKMARKS WHERE ACCOUNT=?", (account,))
        profile = self.cur.fetchone()[0]
        if profile == '':
            new_text = input("Your profile is empty!\n Why don't you introduce yourself?\n>>")
        else:
            print("Current profile:\n" + profile)
            new_text = input("Do you want to change this? (Y/N)\n>>")
            self.cur.execute("UPDATE WRITERS SET PROFILE=? WHERE ACCOUNT=?", (new_text, account))



'''
possible edits for v 2.0:
    - add draft func and editing for published moments
    - add edit profile hints
'''

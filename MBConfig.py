import re, sqlite3, sys
from sqlite3 import Error

class Config:
    def __init__(self):
        self.filename = 'mushbot.db'
        self.options = dict()

    def _createOptions(self, c, columns, firsttime=True):
        create_options_table = """ CREATE TABLE IF NOT EXISTS options (
                                    id integer PRIMARY KEY,
                                    MUSH_USERNAME varchar(50) NOT NULL,
                                    MUSH_PASSWORD varchar(50) NOT NULL,
                                    MUSH_SERVER varchar(50) NOT NULL,
                                    MUSH_PORT integer NOT NULL,
                                    MUSH_OWNER varchar(50) NOT NULL,
                                    CONNECT_ATTEMPTS integer DEFAULT 10,
                                    VERBOSE boolean DEFAULT False,
                                    LOG_PREFIX varchar(50),
                                    LOG_SERVER varchar(50),
                                    LOG_USERNAME varchar(50),
                                    LOG_PASSWORD varchar(50),
                                    LOG_CWD varchar(255),
                                    LOG_URL varchar(255)
        );"""
        c.execute(create_options_table)
        if firsttime == True:
            print("----FIRST-TIME SETUP----")
        else:
            print("----MODIFYING OPTIONS----")
        mush_user = input("What is the bot's MUSH username? (This should be created in advance.) ").strip()
        mush_password = input("What is the bot's MUSH password? ").strip()
        mush_server = input("What is the URL or IP address of the MUSH server? ").strip()
        mush_port = input("What is the port of the MUSH server? ").strip()
        mush_owner = input("What is the MUSH username of the user who owns this bot? ").strip()
        connect_attempts = input("How many times should the bot try to connect before giving up? (Default: 10) ").strip()
        connect_attempts = 10 if connect_attempts == "" else int(connect_attempts)
        verbose = input("Should the bot echo its output to this screen (in addition to the MUSH)? (y/N) ").strip()
        verbose = True if "y" in verbose.lower() else False
        use_logging = input("When you ask the bot to log its input, do you want it to upload the logs to a different server? (y/N) ").strip()
        use_logging = True if "y" in use_logging.lower() else False
        log_prefix = ""
        log_server = ""
        log_username = ""
        log_password = ""
        log_cwd = ""
        log_url = ""
        if use_logging:
            log_prefix = input("What prefix should be used for the log filenames? ").strip()
            log_server = input("What is the URL or IP address of the server where the logs will be stored? ").strip()
            log_username = input("What is the username for that server? ").strip()
            log_password = input("What is the password for that server? ").strip()
            log_cwd = input("In what directory should the bot upload its logs?\n(This can be relative or absolute; leave off the trailing slash) ")
            log_url = input("What URL should be used to access the final log from the web? (Leave off the filename.) ")
        print("\nOkay, I have everything I need. Saving your options...")
        insert_options_row = "INSERT INTO options ({}) values (?,?,?,?,?,?,?,?,?,?,?,?,?)".format(columns)
        insert_options = (mush_user, mush_password, mush_server, mush_port, mush_owner, connect_attempts, verbose, log_prefix, log_server, log_username, log_password, log_cwd, log_url)
        c.execute(insert_options_row, insert_options)

    def getConfig(self, modify=False):
        columns = "MUSH_USERNAME,MUSH_PASSWORD,MUSH_SERVER,MUSH_PORT,MUSH_OWNER,CONNECT_ATTEMPTS,VERBOSE,LOG_PREFIX,LOG_SERVER,LOG_USERNAME,LOG_PASSWORD,LOG_CWD,LOG_URL"
        if modify == True:
            try:
                conn = sqlite3.connect(self.filename)
                c = conn.cursor()
                self._createOptions(c,columns,False)
                conn.commit()
                c.execute("select * from options")
                row = c.fetchone()
                col_list = columns.split(',')
                for i in range(len(col_list)):
                    options[col_list[i]] = row[i+1]
                self.options = options
                conn.close()
            except Error as e:
                print("Encountered a fatal error: {}".format(e))
                print("Terminating...")
                conn.close()
                sys.exit(0)
        if self.options == {}:
            options = dict()
            currentheader = ""
            try:
                conn = sqlite3.connect(self.filename)
                c = conn.cursor()
                c.execute("select * from options")
                row = c.fetchone()
                if row == None:
                    print("Didn't find any options, so it's time for...")
                    self._createOptions(c, columns)
                    conn.commit()
                    c.execute("select * from options")
                    row = c.fetchone()
                conn.close()
            except Error as e:
                if str(e) == "no such table: options":
                    try:
                        print("Didn't find the options table, so it's time for...")
                        self._createOptions(c, columns)
                        conn.commit()
                        c.execute("SELECT * FROM options")
                        row = c.fetchone()
                    except Error as e:
                        print("Encountered a fatal error: {}".format(str(e)))
                        print("Terminating...")
                        conn.close()
                        sys.exit(0)
                else:
                    print("Encountered a fatal error: {}".format(str(e)))
                    print("Terminating...")
                    conn.close()
                    sys.exit(0)
            col_list = columns.split(',')
            for i in range(len(col_list)):
                options[col_list[i]] = row[i+1]

            self.options = options
        return self.options

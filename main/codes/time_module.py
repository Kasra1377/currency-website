import datetime

class TimeModule():
    now = datetime.datetime.now()
    yesterday = now - datetime.timedelta(1)

    # Extract date
    today = datetime.datetime.strftime(now ,"%Y-%m-%d")    # -> 2015-05-26
    yesterday = datetime.datetime.strftime(yesterday ,"%Y-%m-%d")    # -> 2015-05-25

    def __init__(self):
        pass
    
    def current_time(self):
        self.current = datetime.datetime.strftime(self.now ,"%H:%M:%S")    # -> 12:05:32
        return self.current

    def today_date(self):
        self.today = datetime.datetime.strftime(self.now ,"%Y-%m-%d")    # -> 2015-05-26
        return self.today
    
    def yesterday_date(self):
        self.yesterday = self.now - datetime.timedelta(1)
        self.yesterday = datetime.datetime.strftime(self.yesterday ,"%Y-%m-%d")    # -> 2015-05-25
        return self.yesterday

if __name__ =="__main__":
    tm = TimeModule()
    print("current_time : ", tm.current_time())
    print("today_date : ", tm.today_date())
    print("yesterday_date : ", tm.yesterday_date())
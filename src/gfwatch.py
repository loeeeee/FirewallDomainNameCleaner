import os
import re
import time
import settings

from termcolor import colored

class GFWatch:
    def __init__(self,
                 data_dir: str,
                 ) -> None:
        """
        Make the GFWatch a usable object
        """
        self.censored_url = [set() for i in range(9)]
        self.iterate_order = [
            self._rule_0,
            self._rule_3,
            self._rule_4,
            self._rule_6,
            self._rule_8,
            self._rule_2,
        ]
        self._load_GFWatch(data_dir)

    def isCensored(self, URL: str) -> bool:
        flag = False
        for rule in self.iterate_order:
            # Skip rule 1, 5, 7, because they are covered in more general rules
            flag = rule(URL)
            if flag:
                return flag
        return flag
            
    def _load_GFWatch(self, working_dir: str) -> None:
        # Load file
        latest_folder = self._find_latest_folder(working_dir)
        file_dir = os.path.join(working_dir, latest_folder)
        file_dir = os.path.join(file_dir, "domain.rules")
        with open(file_dir, "r", buffering=4096, encoding="utf-8") as base_file:
            # Read file line by line
            while line := base_file.readline():
                parsed_line = line.split("|")
                tested_url, rules, base_url = parsed_line[0], parsed_line[1], parsed_line[2]
                parsed_rules = rules[1:-1].split(",")
                for rule in parsed_rules:
                    rule = int(rule)
                    if rule in [1, 5, 7]:
                        # Skip rule 1, 5, 7, because they are covered in more general rules
                        pass
                    self.censored_url[rule].add(base_url)
        return

    def _find_latest_folder(self, 
                           parent_dir: str
                           ) -> str:
        """
        Find the latest folder based on its name
        """
        folders = [f for f in os.listdir(parent_dir) if os.path.isdir(os.path.join(parent_dir, f))]
        
        latest_folder = ""
        latest_date = None
        
        for folder in folders:
            try:
                date = folder[:8]  # Assuming the first 8 characters represent the date in YYYYMMDD format
                year = int(date[:4])
                month = int(date[4:6])
                day = int(date[6:8])
                folder_date = year, month, day

                if latest_date is None or folder_date > latest_date:
                    latest_date = folder_date
                    latest_folder = folder
            except ValueError:
                continue
        
        return latest_folder
    
    def _rule_0(self, URL: str) -> bool:
        if URL in self.censored_url[0]:
            return True
        return False
    
    def _rule_2(self, URL: str) -> bool:
        pattern = r'^' + re.escape(URL) + r'\w+$'
        matches = [domain for domain in self.censored_url[3] if re.match(pattern, domain)]
        if len(matches) != 0:
             return True
        return False

    def _rule_3(self, URL: str) -> bool:
        pattern = r'^\w+\.' + re.escape(URL) + '$'
        matches = [domain for domain in self.censored_url[3] if re.match(pattern, domain)]
        if len(matches) != 0:
             return True
        return False
    
    def _rule_4(self, URL: str) -> bool:
        pattern = r'^\w+' + re.escape(URL) + '$'
        matches = [domain for domain in self.censored_url[3] if re.match(pattern, domain)]
        if len(matches) != 0:
             return True
        return False
    
    def _rule_6(self, URL: str) -> bool:
        pattern = r'^\w+\.' + re.escape(URL) + r'\w+$'
        matches = [domain for domain in self.censored_url[3] if re.match(pattern, domain)]
        if len(matches) != 0:
             return True
        return False
    
    def _rule_8(self, URL: str) -> bool:
        pattern = r'^\w+' + re.escape(URL) + r'\w+$'
        matches = [domain for domain in self.censored_url[3] if re.match(pattern, domain)]
        if len(matches) != 0:
             return True
        return False
    
def test() -> None:
    # Loading
    print(colored("Start loading GFWatch."))
    start_time = time.time()
    watch = GFWatch(settings.DATA_DIR)
    finish_time = time.time()
    print(colored(f"Finish loading the GFWatch, taking {round(finish_time - start_time, 3)}s", "cyan"))

    # Uncensored
    uncensored_urls = [
        "www.baidu.com",
        "www.zhihu.com",
        "www.example.com",
        "www.bilibili.com",
    ]

    start_time = time.time()
    for url in uncensored_urls:
        try:
            assert watch.isCensored(url) == False
            print(f"Passing assert {url} for uncensored url.")
        except AssertionError:
            print(colored(f"Assertion error with uncensored url, \n{url}", "red"))
    finish_time = time.time()
    print(colored(f"Finish asserting uncensored_url, taking {round(finish_time - start_time, 3)}s", "cyan"))

    # Rule 0
    rule_0_urls = [
        "pornhub.com",
        "google.com.hk",
        "google.com.tr",
        "google.com.gh",
        "youtube.com",
        "president.gov.tw",
        "bbc.co.uk",
        "nicovideo.jp",
        "nqu.edu.tw",
        "www.bitznet.app",
        "g.alexyang.me",
        "paimeng.cloud"
    ]
    for url in rule_0_urls:
        try:
            assert watch.isCensored(url) == True
            print(f"Passing assert {url} for strict match censoring.")
        except AssertionError:
            print(colored(f"Assertion error with rule 0 on url, \n{url}", "red"))
    
    # Rule 2
    rule_2_urls = [
        "servebeer.comwegdsfasdf",
        "redirectme.netsadfasdf",
        "selfip.netasdfagbh",
        "coinfield.coms",
    ]
    for url in rule_2_urls:
        try:
            assert watch.isCensored(url) == True
            print(f"Passing assert {url} for rule 2.")
        except AssertionError:
            print(colored(f"Assertion error with rule 2 on url, \n{url}", "red"))

    # Rule 3
    rule_3_urls = [
        "adsfewradsf.pixnet.net",
        "g.goo.ne.jp",
        "ov.google.cv",
        "pzocxvkpo.pan.in2s.net",
    ]
    for url in rule_2_urls:
        try:
            assert watch.isCensored(url) == True
            print(f"Passing assert {url} for rule 3.")
        except AssertionError:
            print(colored(f"Assertion error with rule 3 on url, \n{url}", "red"))

if __name__ == "__main__":
    print(colored("Start GFWatch testing...", "green"))
    test()
    print(colored("Finish GFWatch testing...", "green"))
else:
    pass
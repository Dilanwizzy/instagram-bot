from selenium import webdriver
from time import sleep
from info import user_email, user_password

executable_path = '/home/dev/chromedriver'
url = "https://www.instagram.com/"
cookies_url = "~/.config/chromium/Default/"

class InstagramBlockBot:

    def __init__(self, url, cookies_url, executable_path):
        self.url = url
        self.cookies_url = cookies_url
        self.executable_path = executable_path
        self.post_number = 0
        self.block_count = 0
        #look for sentences to block
        self.comments_to_block = ["no ad", "i accept", "i post", "will accept", 'P O S T E D', 'just posted',
                                    'leaked photo', 'leaked pic', 'i posted', 'who else high', 'check me out',
                                    'check em out', 'fastest acceptor', 'world record', 'follow if', 'dank meme',
                                  'fight page', 'fights page', 'im public', 'i am public', 'my bio', 'follow me',
                                  'i bet $', 'i bet £', 'post meme',
                                  'i bet you' 'dankest meme', 'post fight', 'follow my', 'check my page out',
                                  'leaked celeb', 'i legit posted', 'has the best meme', 'post great meme',
                                  'do not read my name', 'do not read my bio', 'in my profile', 'i recreate meme',
                                  'posts meme', 'literally posted', 'th follower', 'follows me', 'i steal meme',
                                  'grow a meme page']

        #can remove if not using cookies_url
        self.webOptions = webdriver.ChromeOptions()
        self.webOptions.add_argument("--user-data-dir=" + self.cookies_url)

        #can remove options= if not using cookies_url
        self.driver = webdriver.Chrome(options=self.webOptions, executable_path=self.executable_path)
        self.driver.get(self.url)
        self.driver.implicitly_wait(1)

        if len(self.driver.find_elements_by_xpath('//*[@id="react-root"]/section/main/article/div[2]/div[2]/div/p')) > 0:
            self.login()
        else:
            self.get_post()

    def login(self):
        self.driver.find_element_by_name("username").send_keys(user_email)
        self.driver.find_element_by_name("password").send_keys(user_password)
        self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[2]/div[1]/div/form/div[4]').click()
        self.driver.implicitly_wait(2)
        self.driver.find_element_by_xpath("//button[contains(text(), 'Not Now')]").click()
        self.get_post()

    def scroll(self, scroll_value):
        self.driver.execute_script('window.scrollTo(0, window.scrollY + ' + str(scroll_value) + ')')

    #Gets all post and loops through them opening them on a new tab
    def get_post(self):
        self.scroll(3500)
        sleep(0.5)

        index = 0
        numberOfPost = 0

        posts = self.driver.find_elements_by_xpath('//*[@id="react-root"]/section/main/section/div/div[2]/div/article')

        while True:
            self.driver.switch_to.window(self.driver.window_handles[0])
            self.close_tabs()
            if index == 7:
                self.scroll(6500)
                sleep(2)
                posts = self.driver.find_elements_by_xpath('//*[@id="react-root"]/section/main/section/div/div[2]/div/article')
                index = 0
                numberOfPost += 8
                if numberOfPost >= 100:
                    self.driver.close()
                    break
            if len(posts[index].find_elements_by_class_name('_8Rm4L')) > 0:
                post_comment_url = posts[index].find_element_by_class_name('_8Rm4L').get_attribute('href')
                self.driver.execute_script('window.open("' + post_comment_url + '")')
                self.post_number += 1
                sleep(1)
                self.current_post()
                sleep(2)
            else:
                print("ok")

            index += 1

    def current_post(self):
        self.driver.switch_to.window(self.driver.window_handles[1])
        clicks = 0
        #loads the comment. Each click will load 12 comments. You can decide how many comments the program to look at
        #Does not look at replies
        while True:
            if len(self.driver.find_elements_by_xpath('//*[@id="react-root"]/section/main/div/div[1]/article/div[2]/div[1]/ul/li/div/button')) > 0:
                self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div[1]/article/div[2]/div[1]/ul/li/div/button').click()
                sleep(1)
                clicks += 1
                if clicks == 7:
                    break
            else:
                break
        get_all_comments = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div[1]/article/div[2]/div[1]').find_elements_by_class_name("Mr508")
        print('Post Number: ' + str(self.post_number) + ' number of comments: ' + str(len(get_all_comments)))
        for comments in get_all_comments:
            get_comment = comments.find_element_by_css_selector('span').text
            self.compare_comment(get_comment.lower(), comments)

        self.driver.execute_script('window.close()')

    #compare the words in our list to the user's comment
    def compare_comment(self, comment, comment_css_selector):
        for words in self.comments_to_block:
            if words.lower() in comment:
                block_user_url = comment_css_selector.find_element_by_class_name('_2dbep').get_attribute('href')
                self.driver.execute_script('window.open("' + block_user_url + '")')
                sleep(1)
                self.block_user()
                self.driver.switch_to.window(self.driver.window_handles[1])


    def block_user(self):
        self.block_count = 0
        blocked_second = False
        self.driver.switch_to.window(self.driver.window_handles[2])

        def isBlocked(window_handle):
            self.driver.switch_to.window(self.driver.window_handles[window_handle])
            no_user_to_block = False
            followers = ''
            following = ''

            #Check if user has been blocked already
            if len(self.driver.find_elements_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a')) > 0:
                followers = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a').find_element_by_css_selector('span').text
                following = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[3]/a').find_element_by_css_selector('span').text
            elif len(self.driver.find_elements_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/span')) > 0:
                followers = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/span').find_element_by_css_selector('span').text
                following = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[3]/span').find_element_by_css_selector('span').text
            else:
                no_user_to_block = True

            if followers == '0' and following == '0':
                self.driver.execute_script('window.close()')
            elif no_user_to_block:
                self.driver.execute_script('window.close()')
            else:
                block(window_handle)

        def block(window_handle):
            self.driver.switch_to.window(self.driver.window_handles[window_handle])
            self.driver.find_element_by_class_name('wpO6b').click()
            self.driver.implicitly_wait(1)
            self.driver.find_element_by_xpath('/html/body/div[4]/div/div/div/button[1]').click()
            self.driver.implicitly_wait(1)
            self.driver.find_element_by_xpath('/html/body/div[4]/div/div/div[2]/button[1]').click()
            sleep(1)
            #Instagram may of not confirmed that the user was blocked.
            #Program will attempt to block them 10 times otherwise it will give up and print out the username
            if len(self.driver.find_elements_by_xpath('/html/body/div[2]/div/div/div/p')) > 0:
                self.driver.execute_script('window.close()')
            elif self.block_count >= 10:
                if len(self.driver.find_elements_by_xpath('//*[@id="react-root"]/section/main/div/header/section/div[1]/h2')) > 0:
                    print('Could not block ' + self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/div[1]/h2').text)
                    self.driver.execute_script('window.close()')
                elif len(self.driver.find_elements_by_xpath('//*[@id="react-root"]/section/main/div/header/section/div[1]/h1')) > 0:
                    print('Could not block ' + self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/div[1]/h1').text)
                    self.driver.execute_script('window.close()')
                else:
                    print('Failed to block a user')
            else:
                self.driver.find_element_by_xpath('/html/body/div[4]/div/div/div[2]/button').click()
                sleep(1)
                self.block_count += 1
                isBlocked(window_handle)

        try:
            if len(self.driver.find_elements_by_xpath('//*[@id="react-root"]/section/main/div/header/section/div[2]/span/a[1]')) > 0:
                second_account_url = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/div[2]/span/a[1]').get_attribute('href')
                self.driver.execute_script('window.open("' + second_account_url + '")')
                sleep(1)
                isBlocked(3)
                blocked_second = True
            else:
                isBlocked(2)

            if blocked_second:
                isBlocked(2)
        except:
            if len(self.driver.find_elements_by_xpath('//*[@id="react-root"]/section/main/div/header/section/div[1]/h2')) > 0:
                print('Could not block ' + self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/div[1]/h2').text)
                self.driver.execute_script('window.close()')
            elif len(self.driver.find_elements_by_xpath('//*[@id="react-root"]/section/main/div/header/section/div[1]/h1')) > 0:
                print('Could not block ' + self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/div[1]/h1').text)
                self.driver.execute_script('window.close()')
            else:
                print('could not block the user')

    #close tabs if something goes wrong
    def close_tabs(self):
        index = len(self.driver.window_handles)
        if index > 4:
            print("Something caused the program to get out of synced")
            print("Closing all tabs except posts")
            for x in range(index-1, 0, -1):
                print("closing tab: " + str(x+1))
                self.driver.switch_to.window(self.driver.window_handles[x])
                self.driver.execute_script('window.close()')

mybot = InstagramBlockBot(url, cookies_url, executable_path)


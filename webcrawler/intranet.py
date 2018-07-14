from selenium import webdriver
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, UnexpectedAlertPresentException
from bs4 import BeautifulSoup

def parsed_subject(id, pw):
    
    # webdriver 정보
    driver = webdriver.Chrome("/Users/k352ex/Downloads/Chromedriver")
    driver.implicitly_wait(3)

    # 웹정보서비스 로그인 URL
    driver.get("http://intra.wku.ac.kr/SWupis/V005/login.jsp") 

    # 로그인을 위한 id, pw 정보
    driver.find_element_by_name('userid').send_keys(id)
    driver.find_element_by_name('passwd').send_keys(pw)

    # 로그인 버튼 클릭
    driver.find_element_by_xpath(
        "//*[@id = 'f_login']/fieldset/dl/dd[3]/input").click()

    # 접속 후 Alert 창 확인
    try:
        WebDriverWait(driver, 1).until(EC.alert_is_present(), "test")
        alert = driver.switch_to_alert()
        alert.accept()
        print("alert accepted")
    except TimeoutException:
        print("no alert")

    # 로그인 실패
    if driver.current_url[:54] == "http://intra.wku.ac.kr/SWupis/V005/login.jsp?error_msg": 
        return False



    ### 사용자 정보 크롤링 
    ### 이름, 학번, 이미지, 학년, 소속, 이수학기, 전공
    
    driver.get('http://intra.wku.ac.kr/SWupis/V005/Service/Stud/Resume/resume.jsp?sm=3')

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    
    user_name = soup.select('body > table:nth-of-type(1) > tbody > tr > td:nth-of-type(3) > form > table > tbody > tr:nth-of-type(1) > td:nth-of-type(4)')
    user_number = soup.select('body > table:nth-of-type(1) > tbody > tr > td:nth-of-type(3) > form > table > tbody > tr:nth-of-type(1) > td:nth-of-type(2)')
    user_image = soup.select('body > table:nth-of-type(1) > tbody > tr > td:nth-of-type(1) > table > tbody > tr > td > img')
    user_grade = soup.select('body > table:nth-of-type(1) > tbody > tr > td:nth-of-type(3) > form > table > tbody > tr:nth-of-type(3) > td:nth-of-type(2)')
    user_college = soup.select('body > table:nth-of-type(1) > tbody > tr > td:nth-of-type(3) > form > table > tbody > tr:nth-of-type(4) > td:nth-of-type(2)')
    user_completed_semester = soup.select('body > table:nth-of-type(1) > tbody > tr > td:nth-of-type(3) > form > table > tbody > tr:nth-of-type(3) > td:nth-of-type(4)')
    user_major = soup.select('body > table:nth-of-type(1) > tbody > tr > td:nth-of-type(3) > form > table > tbody > tr:nth-of-type(4) > td:nth-of-type(4)')

    user_name = user_name[0].text
    user_number = user_number[0].text
    user_image = user_image[0]['src']
    user_grade = user_grade[0].text
    user_college = user_college[0].text
    user_completed_semester = user_completed_semester[0].text
    user_major = user_major[0].text

    # 사용자 정보 : 이름, 학번, 이미지경로, 학년, 단과대학명, 이수학기, 전공
    user_info = [user_name, user_number, user_image, user_grade, user_college, user_completed_semester, user_major]


    ### 장학 이력 정보 크롤링
    ### 년도, 학기, 장학명, 장학입학금, 장학수업료, 계

    driver.get('http://intra.wku.ac.kr/SWupis/V005/Service/Stud/Search/scholarResume.jsp?sm=3')

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    scholar_ship = []

    year = soup.select('body > table:nth-of-type(2) > tbody > tr > td:nth-of-type(1)')
    semester = soup.select('body > table:nth-of-type(2) > tbody > tr > td:nth-of-type(2)')
    scholar_name = soup.select('body > table:nth-of-type(2) > tbody > tr > td:nth-of-type(3)')
    scholar_money1 = soup.select('body > table:nth-of-type(2) > tbody > tr > td:nth-of-type(4)')
    scholar_money2 = soup.select('body > table:nth-of-type(2) > tbody > tr > td:nth-of-type(5)')
    scholar_total = soup.select('body > table:nth-of-type(2) > tbody > tr > td:nth-of-type(6)')

    for t_year, t_semester, t_scholar_name, t_scholar_money1, t_scholar_money2, t_scholar_total in zip(year, semester, scholar_name, scholar_money1, scholar_money2, scholar_total):
        scholar_ship.append([
            t_year.text,
            t_semester.text,
            t_scholar_name.text,
            t_scholar_money1.text,
            t_scholar_money2.text,
            t_scholar_total.text
        ])        

    print(scholar_ship)

    # 전체 성적 리스트 주소

    driver.get(
        "http://intra.wku.ac.kr/SWupis/V005/Service/Stud/Score/scoreAll.jsp?sm=3")

    # 페이지 로드 대기
    driver.implicitly_wait(3)


    try:
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
    except selenium.common.exceptions.UnexpectedAlertPresentException:
        pass
  
    driver.implicitly_wait(3)
    
    select_year = soup.select(
        'body > table > tbody > tr > td:nth-of-type(6) > a')

    year_list = []

    for item in select_year:
        year_list.append(item)

    # 데이터를 담을 전체 리스트
    information = []
    subject = {}
    sum_of_grade_point = 0

    for x in year_list:
        driver.get("http://intra.wku.ac.kr" + x['href'])
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        # 이수구분
        subject_kind = soup.select(
            'body > table:nth-of-type(2) > tbody > tr > td:nth-of-type(1)')
        # 과목명
        subject_list = soup.select(
            'body > table:nth-of-type(2) > tbody > tr > td:nth-of-type(3)')
        # 학점
        subject_grade_point = soup.select(
            'body > table:nth-of-type(2) > tbody > tr > td:nth-of-type(4)')
        # 점수
        subject_grade = soup.select(
            'body > table:nth-of-type(2) > tbody > tr > td:nth-of-type(6)')

        for kind, title, point, grade in zip(subject_kind, subject_list, subject_grade_point, subject_grade):
            subject[title.text] = [kind.text, point.text, grade.text]
            sum_of_grade_point += float(point.text)


    information.append(subject)
    information.append({'sum_of_grade_point' : sum_of_grade_point})
    information.append(user_info)
    information.append(scholar_ship)

    driver.close()
    
    return information

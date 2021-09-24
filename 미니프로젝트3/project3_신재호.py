from os import replace
from bs4 import BeautifulSoup
import requests
from lxml.html import fromstring, tostring
import urllib.request as req
import pandas as pd

class crawling:
    def __init__(self):
        
        self.news_section={"사회":'society',
        '정치':'politics',
        '경제':'economic',
        '국제':'foreign',
        '문화':'culture',
        '연예':'entertain',
        '스포츠':'sports',
        'IT':'digital'}

        #데이터 크롤링 할 베이스 url
        self.daum_url="https://news.daum.net/breakingnews"
        #최종 출력할 엑셀 파일 위치
        self.out_excel_dir='./output.xlsx'
        #데이터 저장할 판다스 데이터프레임
        self.news_data=pd.DataFrame({'category':[],'news_script':[],'news_link':[]})

    def readNewsScript(self,category):
        '''
        category의 실시간 뉴스 수집하는 함수
        input: category (news_section 키에 속하는 string)
        '''
        try:
            print(category+" 크롤링 뉴스 수집 ")
            daum_url="https://news.daum.net/breakingnews"
            section = self.news_section[category]

            URL=daum_url+'/'+section+'/'
            
            print("url :", URL)

            #주소에 requests
            response = requests.get(URL)
            #http 정보 수집
            root = fromstring(response.content)
            soup= BeautifulSoup(tostring(root),'html.parser')

            #뉴스 해당하는 부분 css select 
            link_url = soup.select("ul.list_news2 > li > a ")
            link_text = soup.select("ul.list_news2 > li > a > img")

            for i in enumerate(link_url):

                #뉴스 내용과 url 수집
                news_script =link_text[i[0]]['alt']
                news_url= i[1]['href']
                
                #판다스 데이터 프레임에 저장
                self.news_data=self.news_data.append({
                                    'category':category,
                                    'news_script':news_script,
                                    'news_link':news_url
                                    },ignore_index=True)
        except Exception as e:
            print("뉴스 수집이 실패하였습니다.")
            print(e)

    def toExcel(self,out_excel_dir='./output.xlsx'):
        try:
            self.news_data.to_excel(out_excel_dir)
            print(out_excel_dir+"파일이 생성 되었습니다.")
        except Exception as e:
            print("파일이 생성되지 않았습니다.")
            print(e)


    def getNewsData(self):
        return self.news_data
    
    def getSection(self):
        return self.news_section


if __name__ =="__main__":

    #객체 생성
    cw = crawling()
    
    # 뉴스 섹션 정보 확인
    section=cw.getSection()

    #각 섹션별 뉴스 수집
    for key in section:
        cw.readNewsScript(key)

    #수집된 정보 확인
    print(cw.getNewsData())

    #파일로 출력
    cw.toExcel('./outdata.xlsx')

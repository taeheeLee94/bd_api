import requests
from urllib.parse import urlparse
import pandas as pd

# import geopandas

error_code = 0

while True:
    try:
        print("input address: ", end="")
        address = input()
        # print("address = ", address)
        # address = "경기도 용인시 처인구 모현읍 외대로 81"
        url = "https://dapi.kakao.com/v2/local/search/address.json?query=" + address
        result = requests.get(urlparse(url).geturl(),
                              headers={"Authorization": "KakaoAK 3c53094cf92240765e2a2b0acd32bce4"})
        json_obj = result.json()

        list = []
        for document in json_obj['documents']:
            val = [document['road_address']['building_name'], document['address']['b_code'], document['address_name'],
                   document['y'], document['x']]
            list.append(val)

        df = pd.DataFrame(list, columns=['building_name', 'b_code', 'address_name', 'lat', 'lon'])
        textInput = df['b_code'][0]

        # print(df)
        mt = document['address']['mountain_yn']

        if mt == 'Y':
            mt = 1
        else:
            mt = 0

        bun = document['address']['main_address_no']
        ji = document['address']['sub_address_no']

        for i in range(0, 4):
            if len(bun) == 4:
                break
            else:
                bun = '0' + bun

        for i in range(0, 4):
            if len(ji) == 4:
                break
            else:
                ji = '0' + ji

        # print(bun, ji)

        import requests, bs4
        import pandas as pd
        from lxml import html
        from urllib.request import Request, urlopen
        from urllib.parse import urlencode, quote_plus, unquote

        import xml.etree.ElementTree as ET
        from xml.etree.ElementTree import parse

        decode_key = 'qxYCqkstCZ8XGIddZD07gVxLSNV8Ivpcp4QNatFfp4nS3lmhVB4kg1F4+PoFnHGjlKViFlvHtKGzNpcR4WIHbw=='
        url = 'http://apis.data.go.kr/1613000/BldRgstService_v2/getBrFlrOulnInfo'
        queryParams = ('?' +
                       urlencode({quote_plus('ServiceKey'): decode_key,
                                  quote_plus('sigunguCd'): textInput[:5],
                                  quote_plus('bjdongCd'): textInput[5:],
                                  quote_plus('platGbCd'): mt,
                                  quote_plus('bun'): bun,
                                  quote_plus('ji'): ji,
                                  #                           quote_plus('startDate') : '',
                                  #                           quote_plus('endDate') : '',
                                  quote_plus('numOfRows'): '1000',
                                  #                           quote_plus('pageNo') : '10'
                                  }))

        request = Request(url + queryParams)

        request.get_method = lambda: 'GET'
        response_body = urlopen(request).read()
        response_body = response_body.decode('utf-8')

        xmlobj = bs4.BeautifulSoup(response_body, 'lxml-xml')
        rows = xmlobj.findAll('item')

        # print("rows = ", rows)

        columns = rows[0].find_all()
        # print(columns)

        rowList = []
        nameList = []
        columnList = []

        rowsLen = len(rows)

        import time

        timestr = time.strftime("%Y-%m-%d %H%M%S")

        for i in range(0, rowsLen):
            columns = rows[i].find_all()

            columnsLen = len(columns)
            for j in range(0, columnsLen):
                if i == 0:
                    nameList.append(columns[j].name)

                eachColumn = columns[j].text
                columnList.append(eachColumn)

            rowList.append(columnList)
            columnList = []

        # result = pd.DataFrame(rowList, columns=nameList)
        nameList[0] = "면적"
        nameList[1] = "면적제외여부"
        nameList[2] = "법정동코드"
        nameList[3] = "건물명"
        nameList[4] = "블록"
        nameList[5] = "번(지)"
        nameList[6] = "생성일자"
        nameList[7] = "동명칭"
        nameList[8] = "기타용도"
        nameList[9] = "기타구조"
        nameList[10] = "층구분코드"
        nameList[11] = "층구분코드명"
        nameList[12] = "층번호"
        nameList[13] = "층번호명"
        nameList[14] = "(번)지"
        nameList[15] = "로트"
        nameList[16] = "주부속구분코드"
        nameList[17] = "주부속구분코드명"
        nameList[18] = "주용도코드"
        nameList[19] = "주용도코드명"
        nameList[20] = "관리건축물대장PK"
        nameList[21] = "새주소법정동코드"
        nameList[22] = "새주소본번"
        nameList[23] = "새주소도로코드"
        nameList[24] = "새주소부번"
        nameList[25] = "새주소지상지하코드"
        nameList[26] = "도로명대지위치"
        nameList[27] = "대지구분코드"
        nameList[28] = "대지위치"
        nameList[29] = "순번"
        nameList[30] = "시군구코드"
        nameList[31] = "특수지명"
        nameList[32] = "구조코드"
        nameList[33] = "구조코드명"

        result = pd.DataFrame(rowList, columns=nameList)

        in_name = (
            "면적제외여부", "법정동코드", "블록", "번(지)", "생성일자", "층구분코드", "(번)지", "로트",
            "주부속구분코드", "주용도코드", "관리건축물대장PK", "새주소법정동코드", "새주소본번",
            "새주소도로코드", "새주소부번", "새주소지상지하코드", "대지구분코드", "시군구코드",
            "특수지명", "구조코드"
        )

        for i in range(len(in_name)):
            del result[in_name[i]]

        result.to_excel(excel_writer=timestr + ' sub ' + address + '.xlsx')

        url = 'http://apis.data.go.kr/1613000/BldRgstService_v2/getBrTitleInfo'
        queryParams = ('?' +
                       urlencode({quote_plus('ServiceKey'): decode_key,
                                  quote_plus('sigunguCd'): textInput[:5],
                                  quote_plus('bjdongCd'): textInput[5:],
                                  quote_plus('platGbCd'): mt,
                                  quote_plus('bun'): bun,
                                  quote_plus('ji'): ji,
                                  #                           quote_plus('startDate') : '',
                                  #                           quote_plus('endDate') : '',
                                  quote_plus('numOfRows'): '1000',
                                  #                           quote_plus('pageNo') : '10'
                                  }))

        request = Request(url + queryParams)
        request.get_method = lambda: 'GET'
        response_body = urlopen(request).read()
        response_body = response_body.decode('utf-8')

        xmlobj = bs4.BeautifulSoup(response_body, 'lxml-xml')
        rows = xmlobj.findAll('item')
        columns = rows[0].find_all()

        rowList = []
        nameList = []
        columnList = []

        rowsLen = len(rows)
        for i in range(0, rowsLen):
            columns = rows[i].find_all()

            columnsLen = len(columns)
            for j in range(0, columnsLen):
                if i == 0:
                    nameList.append(columns[j].name)

                eachColumn = columns[j].text
                columnList.append(eachColumn)

            rowList.append(columnList)
            columnList = []

        result = pd.DataFrame(rowList, columns=nameList)

        in_name = (
            "bcRat", "bjdongCd", "block", "bun",
            "bylotCnt", "crtnDay", "dongNm", "emgenUseElvtCnt",
            "engrEpi", "engrGrade", "engrRat", "fmlyCnt", "gnBldCert",
            "gnBldGrade", "heit", "indrAutoArea", "indrAutoUtcnt",
            "indrMechArea", "indrMechUtcnt", "itgBldCert", "itgBldGrade", "ji", "lot",
            "mainAtchGbCd", "mainAtchGbCdNm", "mainPurpsCd", "mgmBldrgstPk", "naBjdongCd",
            "naRoadCd", "naUgrndCd", "oudrAutoArea", "oudrAutoUtcnt", "oudrMechArea",
            "oudrMechUtcnt", "platGbCd", "pmsnoGbCd", "pmsnoGbCdNm", "pmsnoKikCd",
            "pmsnoKikCdNm", "pmsnoYear", "regstrGbCd", "regstrKindCd", "regstrKindCdNm",
            "rideUseElvtCnt", "rnum", "roofCd", "sigunguCd", "splotNm", "stcnsDay",
            "strctCd", "totDongTotArea", "vlRat", "vlRatEstmTotArea", "hhldCnt", "hoCnt",
            "naMainBun", "pmsDay", "naSubBun"
        )

        for i in range(len(in_name)):
            del result[in_name[i]]

        result.columns = ["건축면적(㎡)", "부속건축물면적(㎡)", "부속건축물수", "건물명", "기타용도",
                          "기타지붕", "기타구조", "지상층수", "주용도코드명", "도로명대지위치", "대지면적(㎡)",
                          "대지위치", "대장구분코드명", "지붕코드명", "구조코드명", "연면적(㎡)", "지하층수", "사용승인일"]

        result.to_excel(excel_writer=timestr + ' main ' + address + '.xlsx')

        print("출력 완료")

    except:
        if error_code == 99:
            print("정확한 주소를 입력해주세요.")
        elif error_code == 100:
            print("error")
        elif error_code == 101:
            print("에러")
        elif error_code == 102:
            print("why")
        else:
            print("건축물대장이 조회되지않습니다.")
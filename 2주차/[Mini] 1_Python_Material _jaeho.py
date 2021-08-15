# -*- coding: utf-8 -*-
import sqlite3
import os
PRODUCT_FILE_NAME = './PRODUCT.db'
ORDER_FILE_NAME='./ORDER.db'


def db_print(FILE_NAME):
    #DB 전체 출력을 위한 함수
    conn = sqlite3.connect(FILE_NAME)
    cur = conn.cursor()
    cur.execute("SELECT * FROM Product")
    rows = cur.fetchall()
    print(f'{"@CODE":15s}{"@NAME":15s}{"@PRICE":15s}{"@COUNT":15s}{"@COMMENT":15s}')

    for row in rows:
        #db 데이터를 db 리스트에 객체로 넣음
        print(f'{str(row[0]):15s}{row[1]:15s}{str(row[2]):15s}{str(row[3]):15s}{row[4]:15s}')
    conn.close()



def order(order_code,order_amount):
    '''
    주문 하기 위한 함수
    code : 구매 원하는 상품 코드
    amount: 구매 원하는 갯수
    '''
    #주문 요청한 데이터 정보 수집해옴
    conn = sqlite3.connect(PRODUCT_FILE_NAME)
    curr=conn.cursor()
    curr.execute(f"SELECT ID, NAME, PRICE, COUNT, COMMENT FROM Product WHERE ID={order_code};")
    product_data = curr.fetchone()
    conn.close()
    
    #상품 코드가 있으면
    if product_data!=None:
        id=product_data[0]
        name=product_data[1]
        price=product_data[2]
        amount=product_data[3]
        comment=product_data[4]

        #상품 구입 가능한 물량인지
        if amount>=order_amount: 
            #Order DB에 추가
            conn = sqlite3.connect(ORDER_FILE_NAME)
            curr=conn.cursor()
            curr.execute(f"INSERT INTO Product VALUES ({id},'{name}',{price},{order_amount},'{comment}')")
            conn.commit()
            conn.close()

            #상품 목록에서 수량 업데이트
            conn = sqlite3.connect(PRODUCT_FILE_NAME)
            curr=conn.cursor()
            curr.execute("UPDATE product SET count = ? WHERE id = ?", (amount-order_amount, id))
            conn.commit()
            conn.close()
            return 
        else:
            print("\n@@오류 :구입 수량이 부족 합니다.")
            return

    print("\n@@오류 : 입력하신 상품코드에 해당하는 상품이 없습니다.")
    return


#메인 함수
if __name__== "__main__":
    while True:
        #1. 상품 목록 DB 없을때 세팅
        if not os.path.exists(PRODUCT_FILE_NAME):
            conn = sqlite3.connect(PRODUCT_FILE_NAME)
            conn.execute('CREATE TABLE Product(ID,NAME,PRICE,COUNT,COMMENT)')
            conn.executemany("INSERT INTO Product VALUES (?, ?, ?, ?, ?)",
                [(1001, 'Pen',1000, 10, 'RED PEN'),
                (2001, 'Note',500, 3, 'Yellow Note'),
                (3001, 'Book',10000, 10, 'Comic book'),
                (4001, 'ruler',2000, 7, '30 cm ruler'),
                ])
            conn.commit()
            conn.close()
        
        #2. 주문 목록 DB 없을때 생성
        if not os.path.exists(ORDER_FILE_NAME):
            conn = sqlite3.connect(ORDER_FILE_NAME)
            conn.execute('CREATE TABLE Product(ID,NAME,PRICE,COUNT,COMMENT)')
            conn.commit()
            conn.close()

        #3. 상품 목록을 표시
        print("\n@@@@@@@상품 목록@@@@@@@")
        db_print(PRODUCT_FILE_NAME) 

        #4. 상품 번호와 주문 수량을 입력받는 코드
        order_code=int(input("\n구매하실 상품의 번호를 입력해주세요: "))
        order_amount=int(input("\n구매할 수량을 입력해주세요: "))

        #5. 주문 하기 
        order(order_code,order_amount)
        
        #6. 현재까지 주문 내역을 출력하는 코드
        print("현재까지 구매한 내역 보기")

        #7. ORDER 데이터 불러와서 출력하기
        db_print(ORDER_FILE_NAME)
        #8. 결과 출력하기
        buy_again=int(input("\n@추가 구입 - 1    @종료 - 그외\n"))
        if buy_again!=1:
            break
        os.system('cls')

















##################클래스 사용 하였을때 ############################


# # -*- coding: utf-8 -*-
# import sqlite3
# import os
# PRODUCT_FILE_NAME = './PRODUCT.db'
# ORDER_FILE_NAME='./ORDER.db'



# class PRODUCT:
#     '''
#     물건 저장하는 객체
#     id: 상품 코드
#     name: 상품명
#     price : 상품가격
#     count : 상품 갯수
#     comment : 상품 설명
#     '''

#     def __init__(self,id_number, name, price, count, comment):
#         self.id_number=id_number
#         self.name=name
#         self.price= price
#         self.count=count
#         self.comment=comment

#     def product_print(self):
#         #print(f'ID:{self.id_number}, 상품명:{self.name}, 금액:{self.price}, 갯수:{self.count}, 설명:{self.comment}')
#         print(f'{str(self.id_number):15s}{self.name:15s}{str(self.price):15s}{str(self.count):15s}{self.comment:15s}')
    
#     def get_data(self):
#         return self.id_number, self.name, self.price, self.count, self.comment

# def get_product_data(FILE_NAME):
#     #DB 전체 출력을 위한 함수
#     db_list=[]
#     conn = sqlite3.connect(FILE_NAME)
#     cur = conn.cursor()
#     cur.execute("SELECT * FROM Product")
#     rows = cur.fetchall()
#     for row in rows:
#         #db 데이터를 db 리스트에 객체로 넣음
#         product=PRODUCT(row[0],row[1],row[2],row[3],row[4])
#         db_list.append(product)
#     conn.close()

#     return db_list

# def order(product_list,order_code,order_amount):
#     '''
#     주문 하기 위한 함수
#     product_list :물건 목록
#     code : 구매 원하는 상품 코드
#     amount: 구매 원하는 갯수
#     '''
#     order_check=0
#     for product in product_list:
#         id,name,price,amount,comment=product.get_data()
#         #상품 코드가 있으면1001
#         if id ==order_code: 
#             #상품 구입 가능한 물량인지
#             if amount>=order_amount: 
#                 order_check=1 # 구입 표기

#                 #Order DB에 추가
#                 conn = sqlite3.connect(ORDER_FILE_NAME)
#                 curr=conn.cursor()
#                 curr.execute(f"INSERT INTO Product VALUES ({id},'{name}',{price},{order_amount},'{comment}')")
#                 conn.commit()
#                 conn.close()

#                 #상품 목록에서 수량 업데이트
#                 conn = sqlite3.connect(PRODUCT_FILE_NAME)
#                 curr=conn.cursor()
#                 curr.execute("UPDATE product SET count = ? WHERE id = ?", (amount-order_amount, id))
#                 conn.commit()
#                 conn.close()
#                 return 

#             else:
#                 print("\n@@오류 :구입 수량이 부족 합니다.")
#                 return

#     print("\n@@오류 : 입력하신 상품코드에 해당하는 상품이 없습니다.")
#     return


# #메인 함수
# if __name__== "__main__":
#     while True:
#         #1. 상품 목록 DB 없을때 세팅
#         if not os.path.exists(PRODUCT_FILE_NAME):
#             conn = sqlite3.connect(PRODUCT_FILE_NAME)
#             conn.execute('CREATE TABLE Product(ID,NAME,PRICE,COUNT,COMMENT)')
#             conn.executemany("INSERT INTO Product VALUES (?, ?, ?, ?, ?)",
#                 [(1001, 'Pen',1000, 10, 'RED PEN'),
#                 (2001, 'Note',500, 3, 'Yellow Note'),
#                 (3001, 'Book',10000, 10, 'Comic book'),
#                 (4001, 'ruler',2000, 7, '30 cm ruler'),
#                 ])
#             conn.commit()
#             conn.close()
        
#         #2. 주문 목록 DB 없을때 생성
#         if not os.path.exists(ORDER_FILE_NAME):
#             conn = sqlite3.connect(ORDER_FILE_NAME)
#             conn.execute('CREATE TABLE Product(ID,NAME,PRICE,COUNT,COMMENT)')
#             conn.commit()
#             conn.close()

#         #3. 상품 데이터 불러오기
#         db_list=get_product_data(PRODUCT_FILE_NAME) 

#         ##4. 상품 목록을 표시
#         print("\n@@@@@@@상품 목록@@@@@@@")
#         print(f'{"@CODE":15s}{"@NAME":15s}{"@PRICE":15s}{"@COUNT":15s}{"@COMMENT":15s}')
#         for product in db_list:
#             product.product_print()
        
#         ##5. 상품 번호와 주문 수량을 입력받는 코드
#         order_code=int(input("\n구매하실 상품의 번호를 입력해주세요: "))
#         order_amount=int(input("\n구매할 수량을 입력해주세요: "))

#         #6. 주문 하기 
#         order(db_list,order_code,order_amount)



#         ##7. 현재까지 주문 내역을 출력하는 코드
#         print('')
#         print("현재까지 구매한 내역 보기")

#         #8. ORDER 데이터 불러와서 출력하기
#         print(f'{"@CODE":15s}{"@NAME":15s}{"@PRICE":15s}{"@COUNT":15s}{"@COMMENT":15s}')
#         order_list=get_product_data(ORDER_FILE_NAME)
#         for product in order_list:
#             product.product_print()

#         buy_again=int(input("\n@추가 구입 - 1    @종료 - 그외\n"))
#         if buy_again!=1:
#             break
#         os.system('cls')




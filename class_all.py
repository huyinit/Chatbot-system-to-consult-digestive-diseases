import re

import mysql.connector
import json
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="huyinit",
    database="chtdttt"
)


class ConvertData:
    """
    Truy vấn và xử lý dữ liệu
    """
    def __init__(self):
        self.resultbenh = []
        self.resulttrieutrung = []
        self.resultfc = []
        self.resultbc = []
        self.resulttt = []

    def convertbenh(self):
        """
        Lấy dữ liệu bảng bệnh
        """
        dbbenh = mydb.cursor()
        dbbenh.execute("SELECT * FROM chtdttt.benh;")
        benh = dbbenh.fetchall()
        dirbenh = {}
        for i in benh:
            dirbenh['idbenh'] = i[0]
            dirbenh['tenBenh'] = i[1]
            dirbenh["nguyennhan"] = i[2]
            dirbenh['loikhuyen'] = i[3]
            self.resultbenh.append(dirbenh)
            dirbenh = {}

    def converttrieuchung(self):
        """
        Lấy dữ liệu từ bảng trieuchung
        """
        dbtrieuchung = mydb.cursor()
        dbtrieuchung.execute("SELECT * FROM chtdttt.trieuchung;")
        trieuchung = dbtrieuchung.fetchall()
        dirtrieuchung = {}
        # resulttrieuchung=[]
        for i in trieuchung:
            dirtrieuchung['idtrieuchung'] = i[0]
            dirtrieuchung['noidung'] = i[1]
            self.resulttrieutrung.append(dirtrieuchung)
            dirtrieuchung = {}

    def getfc(self):
        """
        Nhóm các bệnh cùng 1 triệu chứng
        """
        dbfc = mydb.cursor()
        dbfc.execute(
            "select idsuydien, luat.idluat, idtrieuchung, idbenh, trangthai from suydien, luat where suydien.idluat=luat.idluat and trangThai='1'")
        fc = dbfc.fetchall()
        s = []
        d = []
        for i in range(len(fc)):
            s.append(fc[i][2])
            d.append(fc[i][3])

        tt = s[0]
        benh = []
        dicfc = {}
        for i in range(len(s)):
            if s[i] == tt:
                benh.append(d[i])
            else:
                dicfc['trieuchung'] = tt
                dicfc['benh'] = benh
                tt = s[i]
                self.resultfc.append(dicfc)
                benh = []
                benh.append(d[i])
                dicfc = {}

    def getbc(self):
        """
        Nhóm các triệu chứng cùng 1 bệnh
        """
        dbbc = mydb.cursor()
        dbbc.execute("select idsuydien, luat.idluat, idtrieuchung, idbenh, trangthai from suydien, luat where suydien.idluat=luat.idluat and trangThai='0' order by idbenh")
        fc = dbbc.fetchall()
        rule = []
        s = []
        d = []
        for i in range(len(fc)):
            rule.append(fc[i][1])
            s.append(fc[i][2])
            d.append(fc[i][3])
        # print(rule)
        vtrule = rule[0]
        tt = []
        benh = None
        # result=[]
        dicbc = {}
        for i in range(len(rule)):
            if rule[i] == vtrule:
                tt.append(s[i])
                benh = d[i]
            else:
                dicbc['rule'] = vtrule
                dicbc['benh'] = benh
                dicbc['trieuchung'] = tt
                vtrule = rule[i]
                self.resultbc.append(dicbc)
                benh = d[i]
                tt = []
                tt.append(s[i])
                dicbc = {}

    def groupbc(self):
        """
        
        """
        p = []
        vt = self.resultbc[0]['benh']
        temp = []
        for i in self.resultbc:
            t = []
            t.append(i['benh'])
            for j in i['trieuchung']:
                t.append(j)
            temp.append(t)
        return temp

    def groupfc(self):
        res = []
        for i in self.resultfc:
            for j in range(len(i['benh'])):
                res.append([i['benh'][j], i['trieuchung']])
        return res

    def gettrieuchung(self):
        """
        Nhóm tất cả triệu chứng trong 1 bệnh
        """
        dbtrieuchung=mydb.cursor()
        dbtrieuchung.execute("SELECT * FROM chtdttt.suydien order by idbenh")
        dttt=dbtrieuchung.fetchall()
        benh=[]
        tt=[]
        rule=[]
        for i in dttt:
            benh.append(i[3])
            tt.append(i[2])
            rule.append(i[1])
        vtbenh=benh[0]
        lstt=[]
        dirtt={}
        
        for i in range(len(benh)):
            if benh[i]==vtbenh:
                lstt.append(tt[i])
            else:
                dirtt[vtbenh]=sorted(set(lstt))
                lstt=[]
                vtbenh=benh[i]
                lstt.append(tt[i])
        dirtt[vtbenh]=sorted(set(lstt))
        self.resulttt=dirtt
        return self.resulttt
    
    def get_benh_by_id(self, id_benh):
        """
        Tìm bệnh dựa trên id
        """
        for i in self.resultbenh:
            if i["idbenh"] == id_benh:
                return i
        return 0

    def get_trieuchung_by_id(self, id_trieuchung):
        for i in self.resulttrieutrung:
            if i["idtrieuchung"] == id_trieuchung:
                return i
        return 0

    

class Validate:
    def __init__(self) -> None:
        pass

    def validate_input_number_form(self,value):
        while (1):
            valueGetRidOfSpace = ''.join(value.split(' '))
            check = valueGetRidOfSpace.isnumeric()
            if (check):
                return valueGetRidOfSpace
            else:
                print("-->Chatbot: Vui lòng nhập 1 số dương")
                value = input()

    def validate_phonenumber(self,value):
        while (1):
            valueGetRidOfSpace = ''.join(value.split(' '))
            check = valueGetRidOfSpace.isnumeric()
            if (check):
                return valueGetRidOfSpace
            else:
                print("-->Chatbot: Vui lòng nhập 1 số điện thoại đúng định dạng")
                value = input()


    def validate_email(self, email):
        while (1):
            regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

            if (re.fullmatch(regex, email)):
                # print("Chatbot:Tôi đã nhận được thông tin Email của bạn")
                return email

            else:
                print("-->Chatbot: Vui lòng nhập lại email")
                email = input()

    def validate_name(self, value):
        while (1):
            valueGetRidOfSpace = ''.join(value.split(' '))

            check = valueGetRidOfSpace.isalpha()
            if (check):
                # print("Tôi đã nhận được thông tin Tên của bạn")
                return value
            else:
                print("-->Chatbot: Vui lòng nhập lại tên ! ")
                value = input()

    def validate_binary_answer(self, value):
        acceptance_answer_lst = ['1', 'y', 'yes', 'co', 'có']
        decline_answer_lst = ['0', 'n', 'no', 'khong', 'không']
        value = value+''
        while (1):
            if (value) in acceptance_answer_lst:
                return True
            elif value in decline_answer_lst:
                return False
            else:
                print(
                    "-->Chatbot: Câu trả lời không hợp lệ. Vui lòng nhập lại câu trả lời")
                value = input()


class Person:
    def __init__(self, name, phoneNumber, email):
        self.name = name
        self.phoneNumber = phoneNumber
        self.email = email

    def __str__(self):
        return f"{self.name} - {self.phoneNumber} - {self.email}"


class TreeForFC(object):
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right


class Symptom:
    def __init__(self, code, detail):
        self.code = code
        self.detail = detail


def printTree(node, level=0):
    if node != None:
        printTree(node.left, level + 1)
        print(' ' * 10 * level + '-> ' + str(node.value))
        printTree(node.right, level + 1)
        

def searchindexrule(rule,goal):
    """
    Tìm vị trí các rule có bệnh là goal
    """
    index=[]
    for r in range(len(rule)):
        if rule[r][0]==goal:
            index.append(r)
    return index
def get_s_in_d(answer,goal,rule,d,flag):
    """
    Lấy các triệu chứng theo sự suy diễn để giảm thiểu câu hỏi
    và  đánh dấu các luật đã được duyệt qua để bỏ qua những luật có cùng cùng câu hỏi vào
    """
    result=[]
    index=[]
    if flag==1:
        for i in range(len(rule)):
            if (rule[i][0]==goal) and (answer in rule[i]) and (i in d):
                for j in rule[i]:
                    if j[0]=='S':
                        result.append(j)
                        # result=set()
    else:
        for i in range(len(rule)):
            if (rule[i][0]==goal) and (answer in rule[i]): index.append(i)
            if (rule[i][0]==goal) and (answer not in rule[i]) and (i in d):
                for j in rule[i]:
                    if j[0]=='S':
                        result.append(j)        

    return sorted(set(result)),index


'''
db = ConvertData()
db.convertbenh()  # bang benh
db.converttrieuchung()  # bang trieu chung
db.getfc()
db.getbc()
luat_lui = db.groupbc()
luat_tien = db.groupfc()
print(db.resultbenh)

'''
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
import mysql
import mysql.connector
sem_key="Second Semester ( 2nd Sem)"
num=int(sem_key.split(" ")[3][0])
def con_csv(tn):
    z=0
    while 1:
        try:
            trn=dr.find_element_by_xpath("/html/body/div[1]/div[3]/div[2]/div[3]/ul/li[2]/div[4]/ul/li[" +str(1 +z)+"]/a")
            trn_t=trn.text
            print(trn_t)
            if(tn.lower()==trn_t.lower()):
                print("if con. true")
                break
        except:
            print("can't find the table to convert in csv format")
            return
        z+=1
    trn.click()
    dr.find_element_by_xpath("/html/body/div[2]/div[2]/div/ul/li[5]/a").click()
    WebDriverWait(dr,10).until(ec.presence_of_element_located((By.XPATH,"/html/body/div[4]/form/div[1]/ul/li[2]/input")))
    dr.find_element_by_xpath("/html/body/div[4]/form/div[1]/ul/li[2]/input").click()
    dr.find_element_by_xpath("/html/body/div[4]/form/div[2]/select").send_keys("CSV")
    dr.execute_script("window.scrollTo(0, 200)")
    z=0
    while 1:
        try:
            tl=dr.find_element_by_xpath("/html/body/div[4]/form/div[3]/div/table/tbody/tr["+ str(z+1)+"]/td[1]/input")
        except:
            break
        if(tl.get_attribute("value").lower()!=tn.lower()):
            tl.click()
        z+=1
    el=dr.find_element_by_xpath("/html/body/div[4]/form/div[7]/input")
    #dr.execute_script("arguments[0].ScrollIntoView;",tl)
    dr.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    dl=dr.find_element_by_xpath("/html/body/div[4]/form/div[6]/div[2]/div/ul/li[7]/input")
    dl.click()
    el.click()
    z+=1
    
    
mydb=mysql.connector.connect(host="localhost",user="root",passwd="",database="batch2k18")
tn=input("Enter Table Name : ")
cursor=mydb.cursor()
try:
    c="create table `"+ tn +"` "
    k="(Roll_No BIGINT(50),Name Varchar(50),"
    for i in range(0,num):
        k=k+"sem"+str(i+1)+"cgpa float ," 
    k=k+'ygpa float '
    #sql=sql+k+") values "
    c=c+k+",primary key (Roll_No))"
    cursor.execute(c)
    print("Given table not present new table Created")
except mysql.connector.errors.ProgrammingError:
    print("Table Already Present")
    while 1:
        ch=input("Wnt to Concatenate Data(CD) or Refresh Table(RT): (CD/RT) ")
        if ch=='CD' or ch=='cd':
            break
        elif ch=='RT' or ch=='rt':
            cursor.execute("drop table "+tn)
            cursor.execute(c)
            break
        else:
            print("Invalid input....lets try this again") 
roll_s=int(input("Enter the Upper limit of Roll number : "))
roll_e=int(input("Enter the Lower limit of Roll number(inclusive) : "))
dr=webdriver.Chrome("d:\chromedriver")
sql="insert into `"+tn+"` (Roll_No,Name, "
for i in range(0,num):
    sql=sql+"sem"+str(i+1)+"cgpa ,"
sql=sql+"ygpa ) values"
ar=[]
for i in range(roll_s,roll_e+1):
    c=dr.get("https://makaut1.ucanapply.com/smartexam/public/result-details")
    try:
        roll=dr.find_element_by_name("ROLLNO")
        roll.send_keys(str(i))
        sem=dr.find_element_by_name("SEMCODE")
        sem.send_keys(sem_key)
        sub=dr.find_element_by_xpath("/html/body/div[2]/div/div[2]/div[1]/div/div/form/div[2]/div[1]/button")
        sub.click()
        name=dr.find_element_by_xpath("/html/body/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[2]/div/table[2]/tbody/tr[2]/td[1]/strong/span")
        cgpa=dr.find_element_by_xpath("/html/body/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[2]/div/table[6]/tbody/tr[1]/td[1]/strong")
        z=0
        cgpa=[]
        while 1:
            try:
                tl=dr.find_element_by_xpath("/html/body/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[2]/div/table[6]/tbody/tr["+str(z+1)+"]/td/strong")
                li=list(tl.text.split("      "))      
            except:
                break
            if(li[0]=="YGPA"):
                cgpa.append(float(li[1]))
                break
            else:
                cgpa.append(float(li[1].split(":")[1]))                
            z+=1
    except:
        print("Can't Find Data for :",i)
        continue
    val=[i,name.text]
    val=val+cgpa
    val=tuple(val)
    try :
        cursor.execute(sql + str(val))
    except mysql.connector.errors.IntegrityError:
        continue
    else :
        ar.append(val)
mydb.commit()
dr.get("http://localhost/phpmyadmin/ ")
dr.find_element_by_xpath('/html/body/div[1]/div[3]/div[2]/div[3]/ul/li[2]/a').click()
'''/html/body/div[1]/div[3]/div[2]/div[3]/ul/li[2]/div[4]/ul/li[1]/a
/html/body/div[1]/div[3]/div[2]/div[3]/ul/li[2]/div[4]/ul/li[3]/a'''
while 1:
    ch=input("Wnt to convert the sql file to csv format(y/n): ")
    if ch=='y' or ch=='Y':
        con_csv(tn)
        break
    elif ch=='n' or ch=='n':
        break
    else:
        print("Invalid input....lets try this again") 


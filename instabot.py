from time import sleep
from selenium import webdriver
import getpass 
import csv

#Inputs from User
print("Username:", end="")
username = str(input())
print("password:", end="")
pas = getpass.getpass()
print("Username of Person whose Photo you want to access:", end="")
spy = str(input())
print("Image Number(from Recent): ", end="")
postno = int(input())
print("What would you like to do? \n1. Like Photo  \n2. Comment on Photo \n3. Read All Comments \n4. Like all Comments \nYou can enter multiple Choices using space between them")
choice = list(map(int, (input().strip().split()))) #Array of selected Actions

if len(choice)>4 or len(choice)<0 or max(choice)>4 or min(choice)<0:
	print("Invalid Selection")
	exit() 

#If User wants to comment, take comment as well as input
if 2 in choice:
	print("What you would like to Comment: ", end="")
	comm = str(input())

#If User wants to fetch comments, take User's choice to take commennts in csv
if 3 in choice:
	print("Would you like to get Comments in excel document:(Y/N) ", end="")
	excel = str(input())

browser = webdriver.Firefox(executable_path=r'C:\Users\HP\AppData\Local\Programs\Python\Python38-32\Lib\site-packages\selenium\webdriver\firefox\geckodriver.exe')
browser.get('https://www.instagram.com/')
sleep(2)

name = browser.find_element_by_xpath('/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div[2]/div/label/input')
name.send_keys(username)

password = browser.find_element_by_xpath('/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div[3]/div/label/input')
password.send_keys(pas)

#Login Attempt
sleep(2)
try:
	signin = browser.find_element_by_xpath('/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div[4]/button') 
	signin.click()
except:
	print("Invalid username or password")
	exit()
sleep(5)

try:
	browser.get('https://www.instagram.com/'+spy)
except:
	print('Invalid Username')
	exit()
  
row = postno//3
row = row + 1
column = postno%3
if column == 0:
    column = 3

sleep(5)

#Opening Post
try:
	im = '/html/body/div[1]/section/main/div/div[3]/article/div[1]/div/div['+str(r)+']/div['+str(c)+']/a/div/div[2]'
	img = browser.find_element_by_xpath(im)
except:
	print('Login Failed or Private Account')
	exit()

img.click()
sleep(3)

#liking post
if 1 in choice:
	sleep(2)
	like = browser.find_element_by_xpath('/html/body/div[4]/div[2]/div/article/div[2]/section[1]/span[1]/button')
	like.click()
sleep(1)

#Commenting on Post
if 2 in choice:
	try:
		browser.find_element_by_xpath('/html/body/div[4]/div[2]/div/article/div[2]/section[1]/span[2]/button').click()
		comment_box = browser.find_element_by_xpath('/html/body/div[4]/div[2]/div/article/div[2]/section[3]/div/form/textarea')
		comment_box.send_keys(str(comm))
		sleep(1)
		browser.find_element_by_xpath('/html/body/div[4]/div[2]/div/article/div[2]/section[3]/div/form/button').click()
	except:
		print('Error in Commenting')
sleep(1)

#Fetching comments
if 3 in choice:
	if excel == 'Y':
		CName = []
		CD = []
	i = 1
	print("\n-----------Comments--------------\n")
	while True:
		try:
			cb = '/html/body/div[4]/div[2]/div/article/div[2]/div[1]/ul/ul['+str(i)+']/div/li/div/div[1]/div[2]/h3/div/a'
			cn = browser.find_element_by_xpath(cb)
			print(cn.text, end=" - ")
			CName.append(cn.text)
			y = '/html/body/div[4]/div[2]/div/article/div[2]/div[1]/ul/ul['+str(i)+']/div/li/div/div[1]/div[2]/span'
			c = browser.find_element_by_xpath(y)
			print(c.text)
			CD.append(c.text)	
			i += 1
			sleep(0.5)
			try:
				browser.find_element_by_xpath('/html/body/div[4]/div[2]/div/article/div[2]/div[1]/ul/li/div/button').click()
			except:
				pass
		except Exception as e:
			break
      
#Adding comments in excel
	if excel == 'Y':
		file = open('Comments.csv', 'w', encoding="utf-8", newline='')
		writer = csv.writer(file)
		writer.writerow(['User','Comment'])
		for i in range(len(CD)):
			writer.writerow([str(CName[i]),str(CD[i])])
		print('\nDone! File Created With name Comments.csv')
		file.close()
sleep(1)

#Liking all comments
if 4 in choice:
	for j in range(1,i-1):	
		x = '/html/body/div[4]/div[2]/div/article/div[2]/div[1]/ul/ul['+str(j)+']/div/li/div/span/div/button'
		likec = browser.find_element_by_xpath(x)
		likec.click()
		sleep(0.5)
		try:
			browser.find_element_by_xpath('/html/body/div[4]/div[2]/div/article/div[2]/div[1]/ul/li/div/button').click()
		except:
			pass

print('Thanks For Using')

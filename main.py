#cities in canada
import platform
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import os
from bs4 import BeautifulSoup
import time
import timeit
from datetime import date,time
import time

df=pd.read_csv('canadacities.csv')
df=df[['city','province_name']]
# df.head()

def main():
    for q in range(0,len(df['city'])):
        
        # inputs
        # location
        states = df['city'][q]+' '+df['province_name'][q]
        occupation = 'Spa'
        limit=300
        # url to scrape
        url = f"https://www.google.com/maps/search/{occupation}+in+{states}"

        start = timeit.default_timer()
        print(f'Start Time: {start}')

        print('URL(Data Source): ',end='')
        print(url)

        #create a dictionary of the data structure
        data = {'Name': [], 'Data': [],
                'Occupation': [], 'Location': []}

        chromedriver = "chromedriver"
        os.environ["webdriver.chrome.driver"] = chromedriver
        driver = webdriver.Chrome(chromedriver)
        driver2 = webdriver.Chrome(chromedriver)
        driver.get(url)
        items = []
        last_height = driver.execute_script("return document.body.scrollHeight")
        # print('last_height '+str(last_height))
        element = driver.find_element(
            by=By.XPATH, value='/html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]')
        item_target_count = limit
        timer = 5
        print('Occupation: ',end='')
        print(occupation)
        print('Location: ',end='')
        print(states)

        # this loop scrools down and loads more data
        print('Scrolling: ',end=' ')
        #scroller

        #this scrolls for data point 
        for k in range(0, limit):
            per=int((k/limit)*100)
            print(f'->> {per}%',end=' ')
            driver.execute_script(
                "arguments[0].scrollTop = arguments[1]", element, item_target_count)
            item_target_count += 100
            time.sleep(timer/5)



        #scrapper
        # this function the scrape data
        def scrapper():
            time.sleep(timer/5)
            print('')
            print(f'number of {occupation} found')
            limit=len(driver.find_elements(By.CLASS_NAME, 'hfpxzc'))
            print(limit)
            print('--------')
            print('Scrapping')
            print('--------')
            for i in range(0, limit):
                # print(i)
                per=int((i/limit)*100)
                print(f'->> {per}%',end=' ')
                # move into the section/business card
                try:
                    soupy1 = BeautifulSoup(driver.page_source, 'html.parser')
                    data_link=soupy1.find_all("a", {"class": "hfpxzc"})[i]
                    # print('href')
                    # print(data_link['href'])
                    driver2.get(data_link['href'])
                    driver.find_elements(By.CLASS_NAME, 'hfpxzc')[i].click()
                except Exception as e:
                    print('An error occured 1: ',end='')
                    print(e,end=' ')
                    continue

                # wait for 5 sec --allow data load
                time.sleep(timer)

                # get the data
                soupy = BeautifulSoup(driver2.page_source, 'html.parser')
                name = soupy.find("h1", {"class": "DUwDvf fontHeadlineLarge"})
                # data2=data.find_all("div", {"class": "m6QErb"})
                address = soupy.find(
                    "div", {"class": "RcCsl fVHpi w4vB1d NOE9ve M0S7ae AG25L"})
                phone = soupy.find_all(
                    "div", {"class": "RcCsl fVHpi w4vB1d NOE9ve M0S7ae AG25L"})
                # for j in range(0,len(phone)):
                #     print(phone[j].text)
                if name != None:
                    try:

                        # print('Name: '+name.text)
                        # print('Address: '+address.text)
                        # print('Phone: '+phone[2].text)

                        # # phone=soupy.find_all("div", {"class": "W4Efsd"})[i]
                        # # print(len(phone))
                        # # print(phone.text)

                        # print('-------------')
                        data['Name'].append(name.text)
                        # data['Address'].append(address.text)
                        Suppose_phone_data=[]
                        
                        for j in range(0,len(phone)):
                            
                            Suppose_phone_data.append(phone[j].text)
                            
                        data['Data'].append(",".join(Suppose_phone_data))
                        # data['Phone Number'].append(phone[2].text)
                    except Exception as e:
                        # try:
                        #     data['Name'].append('')
                        #     data['Address'].append(address.text)
                        # except Exception as e:
                        #     try:
                        #         data['Address'].append('')
                        #         data['Phone Number'].append(phone[2].text)
                        #     except Exception as e:
                        #         data['Phone Number'].append('')
                        #         continue
                                
                    # except Exception as e:
                        print('An error occured2: ',end='')
                        print(e,end=' ')
                        continue
                else:
                    try:
                        # print('Name: '+name)
                        # print('Address: '+address)
                        # print('Phone: '+phone[2].text)

                        # # phone=soupy.find_all("div", {"class": "W4Efsd"})[i]
                        # # print(len(phone))
                        # # print(phone.text)

                        # print('-------------')
                        data['Name'].append(name)
                        # data['Address'].append(address)
                        Suppose_phone_data=[]
                        
                        for j in range(0,len(phone)):
                            
                            Suppose_phone_data.append(phone[j].text)
                            
                        data['Data'].append(",".join(Suppose_phone_data))
                        # data['Phone Number'].append(phone[2])
                    # except Exception as e:
                    #     try:
                    #         data['Name'].append('')
                    #         data['Address'].append(address)
                    #     except Exception as e:
                    #         try:
                    #             data['Address'].append('')
                    #             data['Phone Number'].append(phone[2])
                    #         except Exception as e:
                    #             data['Phone Number'].append('')
                    #             continue
                                
                    except Exception as e:
                        print('An error occured3: ',end='')
                        print(e,end=' ')
                        continue

                data['Occupation'].append(occupation)
                data['Location'].append(states)

        scrapper()

        #export
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)

        today = date.today()
        # export
        print('')
        print('-----')
        print('Exporting...')
        try:
            df_export = pd.DataFrame(data)
            if platform.system() != "Darwin":
                df_export.to_csv(r"data/{name}-betacleaning.csv".format(name=f'{occupation}-{states}-{today}-{(current_time).replace(":","-")}'))
            else:
                df_export.to_csv(f"./data/{occupation}-{states}-{today}-{current_time}-betacleaning.csv")
            print('-----')
            print('Done Exporting')
            print('-----')
            print('Preview')
            # df.head()


        except Exception as e:
            print('-----')
            print('Error Exporting: ',end=' ')
            print(e,end=' ')
            return 'done'
        try:
                
            #cleaning
            def stage2(row):  
                data=row['Data']
                data=data.split(',')
                #print(data)
                data1=[]
                for i in range(0,len(data)):
                    
                    data3=list(data[i].replace(' ',''))
                    #print(data[i])
                    #print(data3)
                    if data3[0] == '+':
                        #print(data[i])
                        return data[i]

                return ''

            def stage3(row):  
                data=row['Data']
                data=data.split(',')
                #print(data)
                data1=[]
                for i in range(0,len(data)):
                    
                    data3=list(data[i].replace(' ',''))
                    #print(data[i])
                    #print(data3)
                    if data3[0] == '+':
                        #print(data[0:i-1])
                        return ",".join(data[0:i-1])

                return ''


            df_export['Phone'] = df_export.apply(lambda row: stage2(row), axis=1)
            df_export['Address'] = df_export.apply(lambda row: stage3(row), axis=1)
            df_export=df_export[['Name','Occupation','Location','Phone','Address']]
            if platform.system() != "Darwin":
                df_export.to_csv(r"data/{name}-betacleaning.csv".format(name=f'{occupation}-{states}-{today}-{(current_time).replace(":","-")}'))
            else:
                df_export.to_csv(f"./data/{occupation}-{states}-{today}-{current_time}-betacleaning.csv")
            stop = timeit.default_timer()
            print('Time taken: ', stop - start) 
        except Exception as e:
            print('-----')
            print('Error Exporting: ',end=' ')
            print(e,end=' ')
            return 'done'

    return 'done'

main()
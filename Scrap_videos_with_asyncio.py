from catch_Error import  FailedRequest
import asyncio
import aiohttp
import socket
import socks
import re
import json
from aiosocks.connector import ProxyConnector
import logging
import os
from bs4 import BeautifulSoup
import aiofiles
import aiohttp.connector
conn = ProxyConnector(remote_resolve=True)
headers = {
      'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36',
      'Connection':'Keep-Alive',
      'Accept-Language':'zh-CN,zh;q=0.8',
      'Accept-Encoding':'gzip,deflate,sdch',
      'Accept':'*/*',
      'Accept-Charset':'GBK,utf-8;q=0.7,*;q=0.3',
      'Cache-Control':'max-age=0'
      }
socks.setdefaultproxy(proxy_type=socks.PROXY_TYPE_SOCKS5, addr="127.0.0.1", port=9150)
socket.socket = socks.socksocket
payload = {'.....': '.....', '......': '......'}
import aiohttp.connector
import requests
import datetime
baseUrl = 'url'
endUrl = '.html'
file_name = str(datetime.datetime.now().strftime("%y-%m-%d-%H-%M")) + ".txt"
with requests.Session() as s:
    response = s.post("url", data=payload, headers=headers)
    print("Begin")
    async def get_Pages():
        url = 'url'
        login_data = {'.......': '......', '.....': '......'}
        s.post(url, data=login_data)
        dictionary = {}
        num_retries = 10
        url_b = ""
        for x in range(0, num_retries):
            try:
                for page_num in range(1, 2):
                    lst = []
                    url_z = baseUrl + str(page_num) + endUrl
                    response = s.get(url_z)
                    int_error = response.status_code
                    if int_error == 200:
                        soup = BeautifulSoup(response.text, "html.parser")
                        for Actor_page in soup.find_all(class_='scenes'):
                            for Actor_page_url in Actor_page.find_all('a'):
                                url_b = (Actor_page_url['href'])
                                lst.append(Actor_page_url['href'])
                            dictionary.update({page_num: lst})
                    else:
                        raise Exception
            except Exception:
                await FailedRequest.try_to_Reconnect(session=s, url=url_b,
                                                     message=FailedRequest.message,
                                                     raised=FailedRequest.raised)
            else:
                print("Got all pages")
                break
        with open("data_pages.txt", 'w') as outfile:
            json.dump(dictionary, outfile, sort_keys=True, indent=4,
                      ensure_ascii=False)
        return  dictionary



    async def get_video_Page():
        print("works")
        with open('data_pages.txt') as json_file:
            data = json.load(json_file)
        video_url = ""
        num_retries = 10
        list_video = []
        for x in range(0, num_retries):
            try:
                response = data
                for key, value  in response.items():
                    for page in value:
                        if s.get(page).status_code == 200:
                            response_get = s.get(page)
                            int_error = response_get.status_code
                            if int_error == 200:
                                soup = BeautifulSoup(response_get.text, "html.parser")
                                for a in soup.find_all(class_='desktop_title'):
                                    video_url =  a['href']
                                links = list(set(pager['href'] for pager in soup.find_all(class_='desktop_title')))
                                list_video.extend(links)
                            else:
                                raise Exception
            except Exception:
                print(video_url)
                await FailedRequest.try_to_Reconnect(session=s, url=video_url,
                                                     message=FailedRequest.message,
                                                     raised=FailedRequest.raised)
            else:
                print("Got all pages")
                break

        with open("data_videos.txt", 'w') as outfile:
            json.dump(list_video, outfile, sort_keys=True, indent=4,
                      ensure_ascii=False)
        return list_video


    async def pak_Video(url, session, semaphore, headers):
        async with semaphore:
            num_retries = 4
            Foldername = "video" + os.sep + os.path.basename(url)
            logging.info('downloading %s', Foldername)
            for x in range(0, num_retries):
                try:
                    await asyncio.sleep(120)
                    future = loop.run_in_executor(None, s.get, url)
                    response = await  future
                    int_error = response.status_code
                    if int_error == 200:
                        print(int_error, "video", os.path.basename(url))
                        soup = BeautifulSoup(response.text, "html.parser")
                        video_link = soup.find("video").get("src")
                        print(video_link)
                        async with session.get(video_link, timeout=None) as r:
                            if not os.path.exists(Foldername):
                                os.makedirs(Foldername)
                            if not os.path.exists(Foldername + os.sep + os.path.basename(url.replace('.html', '.mp4'))):
                                async with  aiofiles.open(Foldername + os.sep + os.path.basename(url.replace('.html', '.mp4')),
                                                          mode='wb') as f:
                                    while True:  # save file
                                        chunk = await r.content.read(1024)
                                        if not chunk:
                                            break
                                        await f.write(chunk)
                            else:
                                logging.info('Already existing %s',
                                             Foldername + os.sep + os.path.basename(url.replace('.html', '.mp4')))
                    else:
                        print("cant download")
                        raise Exception

                except Exception:
                    await FailedRequest.try_to_Reconnect(session=s, url=url,
                                                         message=FailedRequest.message,
                                                         raised=FailedRequest.raised)
                    break
                else:
                    break



    async def get_Images(url, session, semaphore, headers):
        async with semaphore:
            num_retries = 10
            Foldername = "video" + os.sep + os.path.basename(url)
            for x in range(0, num_retries):
                try:
                    future = loop.run_in_executor(None, s.get, url)
                    response = await  future
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.text, "html.parser")
                        foto_link = soup.find("video").get("poster")
                        async with session.get(foto_link, timeout=10) as r:
                                if not os.path.exists(Foldername):
                                    os.makedirs(Foldername)
                                if not os.path.exists(Foldername + os.sep + os.path.basename(url.replace('.html', '.png'))):
                                    async with  aiofiles.open(Foldername + os.sep + os.path.basename(url.replace('.html', '.png')), mode='wb') as f:
                                        while True: # save file
                                            logging.info('downloading %s', Foldername)
                                            chunk = await r.content.read(1024)
                                            if not chunk:
                                                break

                                            await f.write(chunk)
                                        print("done")
                                else:
                                    logging.info('Already existing %s', Foldername + os.sep + os.path.basename(url.replace('.html', '.png')))
                                    pass
                    else:
                        print("cant Download")
                        raise Exception
                except Exception:
                    await FailedRequest.try_to_Reconnect(session=s, url=url,
                                                         message=FailedRequest.message,
                                                         raised=FailedRequest.raised)
                    break
                else:
                    break

    async def get_Title(url, session, semaphore, headers):
        async with semaphore:
            num_retries = 10
            Foldername = "video" + os.sep + os.path.basename(url)
            for x in range(0, num_retries):
                try:
                    await asyncio.sleep(60)
                    future = loop.run_in_executor(None, s.get, url)
                    response = await  future
                    int_error = response.status_code
                    if int_error == 200:
                        soup = BeautifulSoup(response.text, "html.parser")
                        data = soup.find('div', attrs={'class': 'header icon1 mobile_video_title'})
                        videostar = data.text
                        if not os.path.exists(Foldername):
                            os.makedirs(Foldername)
                        if not os.path.exists(Foldername + os.sep + "titel.txt"):
                            async with  aiofiles.open(Foldername + os.sep + "titel.txt", mode='w') as f:
                                logging.info('downloading %s', Foldername)
                                await f.write(videostar)
                        else:
                            logging.info('Already existing %s',
                                         Foldername + os.sep + "titel.txt")
                            pass

                    else:
                        print("cant Download")
                        raise Exception
                except Exception:
                    await FailedRequest.try_to_Reconnect(session=s, url=url,
                                                     message=FailedRequest.message,
                                                     raised=FailedRequest.raised)
                    break
                else:
                    break


    async def get_Description(url, session, semaphore, headers):
        async with semaphore:
            num_retries = 10
            Foldername = "video" + os.sep + os.path.basename(url)
            for x in range(0, num_retries):
                try:
                    await asyncio.sleep(45)
                    future = loop.run_in_executor(None, s.get, url)
                    response = await  future
                    int_error = response.status_code
                    if int_error == 200:
                        soup = BeautifulSoup(response.text, "html.parser")
                        data = soup.find('div', attrs={'class': 'video_Description'})
                        description = data.text
                        description = str( description.strip())
                        description = re.sub("Read more...", "",  description)
                        if not os.path.exists(Foldername):
                            os.makedirs(Foldername)
                        if not os.path.exists(Foldername + os.sep + " description.txt"):
                            async with  aiofiles.open(Foldername + os.sep + " description.txt", mode='w') as f:
                                logging.info('Downloading %s', Foldername)
                                await f.write(descriptie)
                        else:
                            logging.info('already existing %s',
                                         Foldername + os.sep + " description.txt")
                            pass
                    else:
                        print("cant Download")
                        raise Exception
                except Exception:
                    await FailedRequest.try_to_Reconnect(session=s, url=url,
                                                         message=FailedRequest.message,
                                                         raised=FailedRequest.raised)
                    break
                else:
                    break



    async def get_Lastname(url, session, semaphore, headers):
        async with semaphore:
            num_retries = 10
            Foldername = "video" + os.sep + os.path.basename(url)
            for x in range(0, num_retries):
                try:
                    await asyncio.sleep(25)
                    future = loop.run_in_executor(None, s.get, url)
                    response = await  future
                    int_error = response.status_code
                    if int_error == 200:
                        soup = BeautifulSoup(response.text, "html.parser")
                        for a in soup.find_all('p', attrs={'class': 'names top mobile_video_title'}):
                            for acteurs in a.findAll('a'):
                                acteurnamen = acteurs.text
                                if not os.path.exists(Foldername):
                                    os.makedirs(Foldername)
                                if not os.path.exists(Foldername + os.sep + "acteurs.txt"):
                                    async with  aiofiles.open(Foldername + os.sep + "acteurs.txt", mode='w') as f:
                                        logging.info('downloading %s', Foldername)
                                        await f.write(acteurnamen + "\r\n")
                                else:
                                    logging.info('Bestaat all %s',
                                                 Foldername + os.sep + "acteurs.txt")
                                    pass

                    else:
                        print("cant download")
                        raise Exception
                except Exception:
                    await FailedRequest.try_to_Reconnect(session=s, url=url,
                                                         message=FailedRequest.message,
                                                         raised=FailedRequest.raised)
                    break
                else:
                    break



    async def main(loop):
            async with aiohttp.ClientSession(loop=loop, headers=headers) as session:
                logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')
                semaphore = asyncio.Semaphore(4)
                #tasks2 = [get_pornstar_video_Page()]
                await get_pornstar_Pages()
                #await asyncio.wait_for(get_pornstar_Pages(), timeout=None)
                asyncio.sleep(50)
                await get_pornstar_video_Page()
                with open('data_videos.txt') as  json_file:
                    data =  json.load(json_file)
                tasks1 = [pak_Video(url, session, semaphore, headers) for url in data]
                tasks2 = [pak_Fotos(url, session, semaphore, headers) for url in data]
                tasks3 = [pak_Titel(url, session, semaphore, headers) for url in data]
                tasks4 = [pak_Descriptie(url, session, semaphore, headers) for url in data]
                tasks5 = [pak_Acteurnamen(url, session, semaphore, headers) for url in data]
                await asyncio.gather(*tasks1, *tasks2, *tasks3, *tasks4, *tasks5)

    if __name__ == '__main__':
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main(loop))

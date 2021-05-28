import os
import requests
from config import headers
from functools import partial
import concurrent.futures
import time
import copy


def scrape(ci, folderPath, downloadList, urls):
    os.path.split(urls)
    fileName = urls.split('/')[-1][0:-3]
    saveName = os.path.join(folderPath, fileName + ".mp4")
    if os.path.exists(saveName):
        # 跳過已下載
        print('當前目標: {0} 已下載, 故跳過...剩餘 {1} 個'.format(
            urls.split('/')[-1], len(downloadList)))
    else:
        response = requests.get(urls, headers=headers, timeout=10)
        content_ts = response.content
        if ci:
            content_ts = ci.decrypt(content_ts)  # 解碼
        with open(saveName, 'ab') as f:
            f.write(content_ts)
            # 輸出進度
            print('\r當前下載: {0} , 剩餘 {1} 個'.format(
                urls.split('/')[-1], len(downloadList)), end='', flush=True)

    downloadList.remove(urls)


def prepareCrawl(ci, folderPath, tsList):
    downloadList = copy.deepcopy(tsList)
    # 開始時間
    start_time = time.time()
    print('開始下載 ' + str(len(downloadList)) + ' 個檔案..', end='')
    print('預計等待時間: {0:.2f} 分鐘 視影片長度與網路速度而定)'.format(len(downloadList) / 150))

    # 開始爬取
    startCrawl(ci, folderPath, downloadList)

    end_time = time.time()
    print('花費 {0:.2f} 分鐘 爬取完成 !'.format((end_time - start_time) / 60))


def startCrawl(ci, folderPath, downloadList):
    # 同時建立及啟用 20 個執行緒
    while(downloadList != []):
        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            executor.map(partial(scrape, ci, folderPath,
                                 downloadList), downloadList)

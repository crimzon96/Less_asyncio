import socket
import socks
import asyncio
import logging

from aiosocks.connector import ProxyConnector
import aiohttp.connector
import  urllib3
import http
from http import client
import requests
conn = ProxyConnector(remote_resolve=True)
import time
socks.setdefaultproxy(proxy_type=socks.PROXY_TYPE_SOCKS5, addr="127.0.0.1", port=9150)
socket.socket = socks.socksocket
user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
headers = {'User-Agent': user_agent}
with requests.Session() as s:
    response = s.post("url", data=payload, headers=headers)

    HTTP_STATUS_CODES_TO_RETRY =  [404, 400, 500, 502, 503, 504]
    class FailedRequest(BaseException):
        code = 0
        message = ''
        url = ''
        raised = ''

        def __init__(self, *, raised='', message='', code='', url=''):
            self.raised         = raised
            self.message        = message
            self.code           = code
            self.url            = url

            super().__init__("code:{c} url={u} message={m} raised={r} ".format(
                c=self.code, u=self.url, m=self.message, r=self.raised))

        async def try_to_Reconnect(session, url, message,
                      interval     = 1.5,
                      read_timeout = 12.4,
                      **kwargs):
            backoff_interval = interval
            raised_exc = None
            attempt = 15

            for x in range(0, attempt):
                if raised_exc:
                    logging.error('caught "%s", remaining tries %s '
                                  'sleeping %.2fsecs', raised_exc,
                                  attempt, backoff_interval)
                try:
                    with aiohttp.Timeout(timeout=read_timeout):
                        with s.get(url, data=payload, headers=headers) as response:
                            if response.status_code != 200:
                                try:
                                    s.post("url", data=payload, headers=headers)
                                    s.get("url", headers=headers)
                                    raise Exception
                                except Exception as exc:
                                    logging.error(
                                        'failed to decode response code:%s url:%s '
                                        'error:%s response:%s',
                                        response.status_code, url, exc,
                                        response.reason
                                    )
                                    raise aiohttp.ServerDisconnectedError
                            elif response.status_code == 404:
                                print("http_status_code_error")
                                logging.error(
                                    'received invalid response code:%s url:%s error:%s'
                                    ' response:%s', response.status_code, url, '',
                                    response.reason
                                )
                                s.post("url", data=payload, headers=headers)
                                s.get("url", headers=headers)
                                raise aiohttp.ServerDisconnectedError
                            elif response.status_code == 200:
                                logging.info(
                                    'received valid response code:%s url:%s No error:%s'
                                    ' response:%s', response.status_code, url, '',
                                    response.reason
                                )
                                break
                            elif None:
                                print("Got None")
                                s.post("url", data=payload, headers=headers)
                                s.get("url", headers=headers)
                                raise Exception
                            else:
                                print("break code ")
                                break

                except(aiohttp.ServerDisconnectedError,
                       UnboundLocalError,
                       aiohttp.client_exceptions.ServerDisconnectedError,
                       urllib3.exceptions.MaxRetryError,
                       urllib3.exceptions.NewConnectionError,
                       http.client.RemoteDisconnected,
                       urllib3.exceptions.ProtocolError,
                       requests.exceptions.ConnectionError,
                       requests.exceptions.HTTPError,
                       ConnectionError,
                       Exception,
                       AttributeError,
                       BaseException

                       ) as exc:
                    try:
                        s.post("url", data=payload, headers=headers)
                        s.get("url", headers=headers)
                        code = exc.code
                        message = ""
                        pass
                    except AttributeError:
                        code = ''
                        message= 'Got a error'
                    raised_exc = FailedRequest(code=code, message=message, url=url,
                                               raised=exc.__class__.__name__)
                    s.post("url", data=payload, headers=headers)
                    s.get("url", headers=headers)

                else:
                    raised_exc = None
                    break

                attempt -= 1

            if raised_exc:
                raise raised_exc


failed = FailedRequest
failed.raised = "raised"
failed.message = "this is working"
failed.url = ''
""""test"""
# loop = asyncio.get_event_loop()
# loop.run_until_complete(failed.try_to_Reconnect(url="http://google.com/404", message=failed.message,session=s))

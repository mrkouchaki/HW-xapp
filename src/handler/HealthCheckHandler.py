#       Copyright (c) 2020 Samsung Electronics Co., Ltd. All Rights Reserved.
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#          http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
# ==================================================================================

import json
from ricxappframe.xapp_frame import RMRXapp
from ..utils.constants import Constants
from ._BaseHandler import _BaseHandler
# from ..manager import SdlAlarmManager


class HealthCheckHandler(_BaseHandler):
    print('///////enter class HealthCheckHandler(_BaseHandler)///////')

    def __init__(self, rmr_xapp: RMRXapp, msgtype):
        print('//////enter def init in HealthCheckHandler/////')
        print('rmr_xapp=', rmr_xapp)
        print('msgtype=', msgtype)
        super().__init__(rmr_xapp, msgtype)
        # self.sdl_alarm_mgr = SdlAlarmManager()

    def request_handler(self, rmr_xapp, summary, sbuf):
        print('//////enter def request_handler in HealthCheckHandler/////')
        print('sbuf=', sbuf)
        print('summary=', summary)
        ok = self._rmr_xapp.healthcheck()
        print('ok = self._rmr_xapp.healthcheck()=', ok)
        # self.sdl_alarm_mgr.checkSdl()
        if ok:
            print('////enter if/////')
            payload = b"OK\n"
            print('payload = b OK\n=', payload)
        else:
            print('/////enter else//////')
            payload = b"ERROR [RMR or SDL is unhealthy]\n"
            print('payload = b ERROR [RMR or SDL is unhealthy]\n=', payload)
            print('Constants.RIC_HEALTH_CHECK_RESP=', Constants.RIC_HEALTH_CHECK_RESP)
        self._rmr_xapp.rmr_rts(sbuf, new_payload=payload, new_mtype=Constants.RIC_HEALTH_CHECK_RESP)
        self._rmr_xapp.rmr_free(sbuf)

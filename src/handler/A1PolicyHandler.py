# ==================================================================================
#
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
from ricxappframe.xapp_frame import RMRXapp, rmr
from ..utils.constants import Constants
from ._BaseHandler import _BaseHandler


class A1PolicyHandler(_BaseHandler):
    print('/////////enter A1PolicyHandler class in A1PolicyHandler/////')

    def __init__(self, rmr_xapp: RMRXapp, msgtype):
        print('/////////enter def init in A1PolicyHandler/////')
        super().__init__(rmr_xapp, msgtype)

    def request_handler(self, rmr_xapp, summary, sbuf):
        print('/////////enter def request_handler in A1PolicyHandler/////')
        self._rmr_xapp.rmr_free(sbuf)
        print('self._rmr_xapp= _rmr_xapp.rmr_free(sbuf)=', self._rmr_xapp)
        try:
            print('/////enter try in request_handler////)
            req = json.loads(summary[rmr.RMR_MS_PAYLOAD])  # input should be a json encoded as bytes
            print('req = json.loads(summary[rmr.RMR_MS_PAYLOAD])input should be a json encoded as bytes=', req)
            self.logger.debug("A1PolicyHandler.resp_handler:: Handler processing request")
            print('self.logger.debug(A1PolicyHandler.resp_handler:: Handler processing request)=', self.logger())
        except (json.decoder.JSONDecodeError, KeyError):
            print('///////enter except/////')
            print('json.decoder.JSONDecodeError=', json.decoder.JSONDecodeError)
            self.logger.error("A1PolicyManager.resp_handler:: Handler failed to parse request")
            print('self.logger.error(A1PolicyManager.resp_handler:: Handler failed to parse request)=', self.logger())
            return

        if self.verifyPolicy(req):
            print('self.verifyPolicy(req)=', self.verifyPolicy(req))
            print('//////enter if self.verifyPolicy(req) ///////')
            self.logger.info("A1PolicyHandler.resp_handler:: Handler processed request: {}".format(req))
            print('self.logger.info(A1PolicyHandler.resp_handler:: Handler processed request: .format(req))=', self.logger())
        else:
            print('/////////enter else////////')      
            self.logger.error("A1PolicyHandler.resp_handler:: Request verification failed: {}".format(req))
            print('self.logger.error(A1PolicyHandler.resp_handler:: Request verification failed:.format(req))=', self.logger())
            return
        self.logger.debug("A1PolicyHandler.resp_handler:: Request verification success: {}".format(req))
        print('self.logger after try & if=', self.logger())

        resp = self.buildPolicyResp(req)
        print('resp = self.buildPolicyResp(req)=', resp)
        print('json.dumps(resp).encode()=', json.dumps(resp).encode())
        print('Constants.A1_POLICY_RESP=', Constants.A1_POLICY_RESP)
        self._rmr_xapp.rmr_send(json.dumps(resp).encode(), Constants.A1_POLICY_RESP)
        print('self._rmr_xapp(.rmr_send)=', self._rmr_xapp)
        self.logger.info("A1PolicyHandler.resp_handler:: Response sent: {}".format(resp))
        print('self.logger.info("A1PolicyHandler.resp_handler:: Response sent: {}".format(resp))=', self.logger())
        print('self.logger.info("A1PolicyHandler.resp_handler:: Response sent: {}".format(resp))=', self.logger.info())
        print('self.logger.info("A1PolicyHandler.resp_handler:: Response sent: {}".format(resp))=', self.logger)

    def verifyPolicy(self, req: dict):
        print('////////enter def verifyPolicy(self, req: dict): in A1PolicyHandler/////)
        print('req: dict)=', req)
        for i in ["policy_type_id", "operation", "policy_instance_id"]:
            print('i=', i)
            if i not in req:
                print(' i not in req: and should return False')
                return False
        print(' i in req: and should return True')
        return True

    def buildPolicyResp(self, req: dict):
        print('////////enter def def buildPolicyResp(self, req: dict): in A1PolicyHandler/////)
        print('req: dict)=', req)
        req["handler_id"] = self._rmr_xapp.config["xapp_name"]
        print('req[handler_id]= = self._rmr_xapp.config[xapp_name]=', req["handler_id"])
        del req["operation"]
        print('req after del req[operation]=', req)
        req["status"] = "OK"
        print('req after req[status] = OK=', req)
        return req

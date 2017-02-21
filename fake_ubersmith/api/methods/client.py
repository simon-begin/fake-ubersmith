# Copyright 2017 Internap.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from fake_ubersmith.api.base import Base
from fake_ubersmith.api.ubersmith import FakeUbersmithError
from fake_ubersmith.api.utils.helpers import record
from fake_ubersmith.api.utils.response import response


class Client(Base):
    def __init__(self):
        super().__init__()

        self.records = {}

        self.credit_cards = []
        self.countries = {}
        self.clients = []
        self.credit_card_response = 1
        self.credit_card_delete_response = True

    def hook_to(self, entity):
        entity.register_endpoints(
            ubersmith_method='client.cc_add',
            function=self.client_cc_add
        )
        entity.register_endpoints(
            ubersmith_method='client.cc_update',
            function=self.client_cc_update
        )
        entity.register_endpoints(
            ubersmith_method='client.cc_info',
            function=self.client_cc_info
        )
        entity.register_endpoints(
            ubersmith_method='client.cc_delete',
            function=self.client_cc_delete
        )
        entity.register_endpoints(
            ubersmith_method='client.get',
            function=self.client_get
        )
        entity.register_endpoints(
            ubersmith_method='client.add',
            function=self.client_add
        )

    def client_add(self, form_data):
        client_id = len(self.clients)

        form_data["clientid"] = client_id
        self.clients.append(form_data)

        return response(data=str(client_id))

    def client_get(self, form_data):
        client_id = form_data["client_id"]
        client = next(
            (
                client for client in self.clients
                if client["clientid"] == client_id
            ),
            None
        )
        if client is not None:
            return response(data=client)
        else:
            return response(
                error_code=1,
                message="Client ID '{}' not found.".format(client_id)
            )

    @record(method='client.cc_add')
    def client_cc_add(self, form_data):
        if isinstance(self.credit_card_response, FakeUbersmithError):
            return response(
               error_code=self.credit_card_response.code,
               message=self.credit_card_response.message
            )
        return response(data=self.credit_card_response)

    @record(method='client.cc_update')
    def client_cc_update(self, form_data):
        if isinstance(self.credit_card_response, FakeUbersmithError):
            return response(
               error_code=self.credit_card_response.code,
               message=self.credit_card_response.message
            )
        return response(data=True)

    def client_cc_info(self, form_data):
        # This call returns no error if providing parameters, only an empty list
        if "billing_info_id" in form_data:
            return response(
                data={
                    cc["billing_info_id"]: cc for cc in self.credit_cards
                    if cc["billing_info_id"] == form_data["billing_info_id"]
                }
            )
        elif "client_id" in form_data:
            return response(
                data={
                    cc["billing_info_id"]: cc for cc in self.credit_cards
                    if cc["clientid"] == form_data["client_id"]
                }
            )
        else:
            return response(
                error_code=1,
                message="request failed: client_id parameter not supplied"
            )

    @record(method='client.cc_delete')
    def client_cc_delete(self, form_data):
        if isinstance(self.credit_card_delete_response, FakeUbersmithError):
            return response(
                error_code=self.credit_card_delete_response.code,
                message=self.credit_card_delete_response.message
            )
        return response(data=True)
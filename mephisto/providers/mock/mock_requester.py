#!/usr/bin/env python3

# Copyright (c) Facebook, Inc. and its affiliates.
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

from mephisto.data_model.requester import Requester
from mephisto.providers.mock.provider_type import PROVIDER_TYPE

from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from mephisto.data_model.database import MephistoDB
    from mephisto.data_model.task import TaskRun

MOCK_BUDGET = 100000.0


class MockRequester(Requester):
    """
    High level class representing a requester on some kind of crowd provider. Sets some default
    initializations, but mostly should be extended by the specific requesters for crowd providers
    with whatever implementation details are required to get those to work.
    """

    def __init__(self, db: "MephistoDB", db_id: str):
        super().__init__(db, db_id)
        # TODO any additional init as is necessary once
        # a mock DB exists

    def register_credentials(self) -> None:
        """Mock requesters don't actually register credentials"""
        pass

    def get_available_budget(self) -> float:
        """MockRequesters have $100000 to spend"""
        return MOCK_BUDGET

    @staticmethod
    def new(db: "MephistoDB", requester_name: str) -> "Requester":
        return MockRequester._register_requester(db, requester_name, PROVIDER_TYPE)

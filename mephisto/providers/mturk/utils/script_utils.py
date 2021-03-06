#!/usr/bin/env python3

# Copyright (c) Facebook, Inc. and its affiliates.
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

from typing import List, Optional, TYPE_CHECKING

from mephisto.providers.mturk.mturk_utils import give_worker_qualification
from mephisto.data_model.requester import Requester

if TYPE_CHECKING:
    from mephisto.data_model.database import MephistoDB

def direct_soft_block_mturk_workers(
    db: "MephistoDB",
    worker_list: List[str],
    soft_block_qual_name: str,
    requester_name: Optional[str] = None,
):
    """
    Directly assign the soft blocking MTurk qualification that Mephisto 
    associates with soft_block_qual_name to all of the MTurk worker ids 
    in worker_list. If requester_name is not provided, it will use the 
    most recently registered mturk requester in the database.
    """
    reqs = db.find_requesters(requester_name=requester_name, provider_type="mturk")
    requester = reqs[-1]

    mturk_qual_details = requester.datastore.get_qualification_mapping(
        soft_block_qual_name
    )
    if mturk_qual_details is not None:
        # Overrule the requester, as this qualification already exists
        requester = Requester(db, mturk_qual_details["requester_id"])
        qualification_id = mturk_qual_details["mturk_qualification_id"]
    else:
        qualification_id = requester._create_new_mturk_qualification(
            soft_block_qual_name
        )

    mturk_client = requester._get_client(requester._requester_name)
    for idx, worker_id in enumerate(worker_list):
        if idx % 50 == 0:
            print(f'Blocked {idx + 1} workers so far.')
        try:
            give_worker_qualification(mturk_client, worker_id, qualification_id, value=1)
        except Exception as e:
            print(f'Failed to give worker with ID: \"{worker_id}\" qualification with error: {e}. Skipping.')

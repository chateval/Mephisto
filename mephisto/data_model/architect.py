#!/usr/bin/env python3

# Copyright (c) Facebook, Inc. and its affiliates.
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

from abc import ABC, abstractmethod
from typing import Dict, List, Any, TYPE_CHECKING, Callable

if TYPE_CHECKING:
    from mephisto.server.channels.channel import Channel
    from mephsito.data_model.packet import Packet
    from mephisto.data_model.task import TaskRun
    from mephisto.data_model.database import MephistoDB
    from argparse import _ArgumentGroup as ArgumentGroup


class Architect(ABC):
    """
    Provides methods for setting up a server somewhere and deploying tasks
    onto that server.
    """

    ARCHITECT_TYPE: str

    def __init__(
        self,
        db: "MephistoDB",
        opts: Dict[str, Any],
        task_run: "TaskRun",
        build_dir_root: str,
    ):
        """
        Initialize this architect with whatever options are provided given
        add_args_to_group. Parse whatever additional options may be required
        for the specific task_run.

        Also set up any required database/memory into the MephistoDB so that
        this data can be stored long-term.
        """
        raise NotImplementedError()

    @classmethod
    def assert_task_args(cls, args: Dict[str, Any]):
        """
        Assert that the provided arguments are valid. Should 
        fail if a task launched with these arguments would
        not work. 

        This should include throwing an exception if the architect
        needs login details or something similar given the 
        arguments passed in.
        """
        return

    def get_channels(
        self,
        on_channel_open: Callable[[str], None],
        on_catastrophic_disconnect: Callable[[str], None],
        on_message: Callable[[str, "Packet"], None],
    ) -> List["Channel"]:
        """
        Return a list of all relevant channels that the Supervisor will
        need to register to in order to function
        """
        raise NotImplementedError()

    def download_file(self, filename: str, save_dir: str) -> None:
        """
        Save the file that is noted as stored on the server to 
        the desired save location.
        """
        raise NotImplementedError()

    @classmethod
    def add_args_to_group(cls, group: "ArgumentGroup") -> None:
        """
        Defines options that are potentially usable for this server location,
        and adds them to the given argparser group. The group's 'description'
        attribute should be used to put any general help for these options.

        If the description field is left empty, the argument group is ignored
        """
        # group.description = 'For `Architect`, you can supply...'
        # group.add_argument('--server-option', help='Lets you customize')
        return

    def prepare(self) -> str:
        """
        Produce the server files that will be deployed to the server
        """
        raise NotImplementedError()

    def deploy(self) -> str:
        """
        Launch the server, and push the task files to the server. Return
        the server URL
        """
        raise NotImplementedError()

    def cleanup(self) -> None:
        """
        Remove any files that were used for the deployment process that
        no longer need to be kept track of now that the task has
        been launched.
        """
        raise NotImplementedError()

    def shutdown(self) -> None:
        """
        Shut down the server launched by this Surveyor, as stored
        in the db.
        """
        raise NotImplementedError()

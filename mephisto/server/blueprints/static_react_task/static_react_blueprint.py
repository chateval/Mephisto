#!/usr/bin/env python3

# Copyright (c) Facebook, Inc. and its affiliates.
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

from mephisto.data_model.assignment import InitializationData
from mephisto.server.blueprints.abstract.static_task.static_blueprint import (
    StaticBlueprint,
)
from mephisto.server.blueprints.static_react_task.static_react_task_builder import (
    StaticReactTaskBuilder,
)
from mephisto.core.registry import register_mephisto_abstraction

import os
import time
import csv

from typing import ClassVar, List, Type, Any, Dict, Iterable, TYPE_CHECKING

if TYPE_CHECKING:
    from mephisto.data_model.task import TaskRun
    from mephisto.data_model.blueprint import AgentState, TaskRunner, TaskBuilder
    from mephisto.data_model.assignment import Assignment
    from argparse import _ArgumentGroup as ArgumentGroup

BLUEPRINT_TYPE = "static_react_task"


@register_mephisto_abstraction()
class StaticReactBlueprint(StaticBlueprint):
    """Blueprint for a task that runs off of a built react javascript bundle"""

    TaskBuilderClass: ClassVar[Type["TaskBuilder"]] = StaticReactTaskBuilder
    BLUEPRINT_TYPE = BLUEPRINT_TYPE

    def __init__(self, task_run: "TaskRun", opts: Any):
        super().__init__(task_run, opts)
        self.js_bundle = os.path.expanduser(opts["task_source"])
        if not os.path.exists(self.js_bundle):
            raise FileNotFoundError(
                f"Specified bundle file {self.js_bundle} was not found from {os.getcwd()}"
            )

    @classmethod
    def assert_task_args(cls, opts: Any) -> None:
        """Ensure that static requirements are fulfilled, and source file exists"""
        super().assert_task_args(opts)

        found_task_source = opts.get("task_source")
        assert (
            found_task_source is not None
        ), "Must provide a path to a javascript bundle in `task_source`"
        found_task_path = os.path.expanduser(found_task_source)
        assert os.path.exists(
            found_task_path
        ), f"Provided task source {found_task_path} does not exist."

    @classmethod
    def add_args_to_group(cls, group: "ArgumentGroup") -> None:
        """
        Adds required options for StaticReactBlueprints.

        task_source points to the file intending to be deployed for this task
        data_csv has the data to be deployed for this task.
        """
        super().add_args_to_group(group)

        group.description = """
            StaticReactBlueprint: Tasks launched from static blueprints need 
            a prebuilt javascript bundle containing the task. We suggest building 
            with our provided useMephistoTask hook.
        """
        group.add_argument(
            "--task-source",
            dest="task_source",
            help="Path to file containing javascript bundle for the task",
            required=True,
        )
        return

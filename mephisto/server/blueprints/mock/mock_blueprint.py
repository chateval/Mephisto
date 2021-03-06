#!/usr/bin/env python3

# Copyright (c) Facebook, Inc. and its affiliates.
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

from mephisto.data_model.blueprint import Blueprint, OnboardingRequired
from mephisto.data_model.assignment import InitializationData
from mephisto.core.argparse_parser import str2bool
from mephisto.server.blueprints.mock.mock_agent_state import MockAgentState
from mephisto.server.blueprints.mock.mock_task_runner import MockTaskRunner
from mephisto.server.blueprints.mock.mock_task_builder import MockTaskBuilder
from mephisto.core.registry import register_mephisto_abstraction

import os
import time

from typing import ClassVar, List, Type, Any, Dict, Iterable, TYPE_CHECKING

if TYPE_CHECKING:
    from mephsito.data_model.agent import OnboardingAgent
    from mephisto.data_model.task import TaskRun
    from mephisto.data_model.blueprint import AgentState, TaskRunner, TaskBuilder
    from mephisto.data_model.assignment import Assignment
    from mephisto.data_model.worker import Worker
    from argparse import _ArgumentGroup as ArgumentGroup

BLUEPRINT_TYPE = "mock"


@register_mephisto_abstraction()
class MockBlueprint(Blueprint, OnboardingRequired):
    """Mock of a task type, for use in testing"""

    AgentStateClass: ClassVar[Type["AgentState"]] = MockAgentState
    OnboardingAgentStateClass: ClassVar[Type["AgentState"]] = MockAgentState
    TaskBuilderClass: ClassVar[Type["TaskBuilder"]] = MockTaskBuilder
    TaskRunnerClass: ClassVar[Type["TaskRunner"]] = MockTaskRunner
    supported_architects: ClassVar[List[str]] = ["mock"]
    BLUEPRINT_TYPE = BLUEPRINT_TYPE

    def __init__(self, task_run: "TaskRun", opts: Dict[str, Any]):
        super().__init__(task_run, opts)
        self.init_onboarding_config(task_run, opts)

    @classmethod
    def add_args_to_group(cls, group: "ArgumentGroup") -> None:
        """
        MockBlueprints specify a count of assignments, as there 
        is no real data being sent
        """
        super().add_args_to_group(group)
        OnboardingRequired.add_args_to_group(group)
        group.description = "MockBlueprint arguments"
        group.add_argument(
            "--num-assignments",
            dest="num_assignments",
            help="Number of assignments to launch",
            type=int,
            required=True,
        )
        group.add_argument(
            "--use-onboarding",
            dest="use_onboarding",
            help="Whether onboarding should be required",
            type=str2bool,
            default=False,
        )
        return

    def get_initialization_data(self) -> Iterable[InitializationData]:
        """
        Return the number of empty assignments specified in --num-assignments
        """
        return [
            MockTaskRunner.get_mock_assignment_data()
            for i in range(self.opts["num_assignments"])
        ]

    # TODO(OWN) this should probably be part of the TaskRunner, which is actually privy to the task
    def validate_onboarding(
        self, worker: "Worker", onboarding_agent: "OnboardingAgent"
    ) -> bool:
        """
        Onboarding validation for MockBlueprints just returns the 'should_pass' field
        """
        return onboarding_agent.state.get_data()["should_pass"]

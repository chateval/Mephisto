import os
import time
import shlex
from mephisto.core.local_database import LocalMephistoDB
from mephisto.core.operator import Operator

USE_LOCAL = 0
NO_SANDBOX = 1
if not NO_SANDBOX:
    os.environ["SKIP_LOCALE_REQUIREMENT"]="TRUE"

db = LocalMephistoDB()

#db.new_requester("NoahTurkProject.1024@gmail.com_sandbox", "mturk_sandbox")
#db.new_requester("NoahTurkProject.1024@gmail.com_mock", "mock")
#db.new_requester("NoahTurkProject.1024@gmail.com", "mturk")
#Mock never completes properly - you can't test seeing worker id

operator = Operator(db)
provider_type = "mock" if USE_LOCAL else ("mturk" if NO_SANDBOX else "mturk_sandbox")
requester = db.find_requesters(provider_type=provider_type)[-1]
requester.register()
requester_name = requester.requester_name
architect_type = "local" if USE_LOCAL else "heroku"
assert USE_LOCAL or NO_SANDBOX or requester_name.endswith('_sandbox'), "Should use a sandbox for testing"

#frame height greater than 650
#task timeout 18000=5 hours
#The argument string goes through shlex.split twice, hence the quoting.
ARG_STRING = (
    "--blueprint-type static "
    f"--architect-type {architect_type} "
    f"--requester-name {requester_name} "
    '--task-title "\\"Fruit video task (best done on mobile phone)\\"" '
    '--task-description "\\"Take a video of an orange from all sides.\\"" '
    "--task-reward 1.5 "
    "--task-tags static,task,testing "
    '--data-csv "data.csv" '
    '--assignment-duration-seconds 18000 ' # max time for a worker to complete.
    '--task-source "merged.out.html" '
    #'--allow-mobile required '
    '--extra-source-dir payload '
    #'--html-source "task.html" '
    f"--units-per-assignment 10 "    
)

try:
    operator.parse_and_launch_run(shlex.split(ARG_STRING))
    print("task run supposedly launched?")
    print(operator.get_running_task_runs())
    while len(operator.get_running_task_runs()) > 0:
        print(f'Operator running {operator.get_running_task_runs()}')
        time.sleep(10)
except Exception as e:
    import traceback
    traceback.print_exc()
except (KeyboardInterrupt, SystemExit) as e:
    pass
finally:
    operator.shutdown()

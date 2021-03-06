from parsl.providers import LocalProvider
from parsl.channels import LocalChannel

from parsl.config import Config
from parsl.executors import HighThroughputExecutor

h_config = Config(
    executors=[
        HighThroughputExecutor(
            label="htex_local",
            cores_per_worker=1,
            provider=LocalProvider(
                channel=LocalChannel(),
                init_blocks=1,
                max_blocks=1,
            ),
        )
    ],
    initialize_logging=False
)

from parsl.executors.threads import ThreadPoolExecutor

t_config = Config(executors=[ThreadPoolExecutor()],
                initialize_logging=False
)

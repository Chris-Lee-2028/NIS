from typing import Type
import os
import json
import torch
import pprint
import random
from tensorboard_logger import Logger as TbLogger
import warnings

from options import get_options, Option
from problems.problem_pdp import PDP
from problems.problem_nvrp import NVRP
from problems.problem_nvta import NVTA
from agent.agent import Agent
from agent.ppo import PPO


def load_agent(name: str) -> Type[Agent]:
    agent = {
        'ppo': PPO,
    }.get(name, None)
    assert agent is not None, "Currently unsupported agent: {}!".format(name)
    return agent


def load_problem(name: str) -> Type[PDP]:
    d = {
        'nvrp': NVRP,
        'nvta': NVTA,
    }
    problem = d.get(name, None)
    assert problem is not None, "Currently unsupported problem: {}!".format(name)
    return problem


def run(opts: Option) -> None:
    # Pretty print the run args
    pprint.pprint(vars(opts))

    # Set the random seed to initialize neural networks
    torch.manual_seed(opts.seed)
    random.seed(opts.seed)

    # Optionally configure tensorboard
    tb_logger = None
    if not opts.no_tb and not opts.distributed:
        tb_logger = TbLogger(
            os.path.join(
                opts.log_dir,
                "{}_{}".format(opts.problem, opts.graph_size),
                opts.run_name,
            )
        )
    if not opts.no_saving and not os.path.exists(opts.save_dir):
        os.makedirs(opts.save_dir)

    # Save arguments so exact configuration can always be found
    if not opts.no_saving:
        with open(os.path.join(opts.save_dir, "args.json"), 'w') as f:
            json.dump(vars(opts), f, indent=True)

    # Set the device
    opts.device = torch.device("cuda" if opts.use_cuda else "cpu")

    # Figure out what's the problem
    problem = load_problem(opts.problem)(
        size=opts.graph_size,
        init_val_method=opts.init_val_method,
        check_feasible=opts.use_assert,
    )

    # Figure out the RL algorithm
    agent = load_agent(opts.RL_agent)(problem.name, problem.size, opts)

    # Load data from load_path
    assert (
        opts.load_path is None or opts.resume is None
    ), "Only one of load path and resume can be given"
    load_path = opts.load_path if opts.load_path is not None else opts.resume

    # Do validation only
    if opts.eval_only:
        # Load the validation datasets
        agent.start_inference(
            problem, opts.val_dataset, tb_logger, load_path, zoom=opts.zoom
        )

    else:
        if opts.resume:
            epoch_resume = int(
                os.path.splitext(os.path.split(opts.resume)[-1])[0].split("-")[1]
            )
            print("Resuming after {}".format(epoch_resume))
            agent.opts.epoch_start = epoch_resume + 1

        # Start the actual training loop
        agent.start_training(problem, opts.val_dataset, tb_logger, load_path)


if __name__ == "__main__":
    warnings.filterwarnings("ignore")

    os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False

    run(get_options())

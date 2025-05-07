# Neural Integrated Search

## Dependencies

* Python>=3.8
* PyTorch>=1.7
* tensorboard_logger
* tqdm

## Usage

### Training

#### NVRP examples

21 nodes:

```bash
python run.py --problem nvrp --graph_size 20 --shared_critic
```

51 nodes:

```bash
python run.py --problem nvrp --graph_size 50 --shared_critic
```

101 nodes:

```bash
python run.py --problem nvrp --graph_size 100 --shared_critic
```

#### NVTA examples

21 nodes:

```bash
python run.py --problem nvta --graph_size 20 --shared_critic
```

51 nodes:

```bash
python run.py --problem nvta --graph_size 50 --shared_critic
```

101 nodes:

```bash
python run.py --problem nvta --graph_size 100 --shared_critic
```

#### Examples

For inference 2,000 NVTA instances with 100 nodes and no data augment (NIS):

```bash
python run.py --eval_only --no_saving --no_tb --problem nvta --graph_size 100 --val_m 1 --val_dataset './datasets/pdp_100.pkl' --load_path './pre-trained/nis/pdtspl_100/epoch-198.pt' --val_size 2000 --val_batch_size 2000 --T_max 3000 --shared_critic
```

For inference 2,000 NVTA instances with 100 nodes using the augments (NIS-A):

```bash
python run.py --eval_only --no_saving --no_tb --problem nvta --graph_size 100 --val_m 50 --val_dataset './NIS-datasets/pdp_100.pkl' --load_path './NIS-pretrained-model/nis/nvta_100/epoch-198.pt' --val_size 2000 --val_batch_size 200 --T_max 3000 --shared_critic
```

Run ```python run.py -h``` for detailed help on the meaning of each argument.

## Acknowledgements

We appreciate the code and framework that have provided assistance to this repository.

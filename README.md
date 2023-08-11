# articProtocol

The `articProtocol` is a Python script designed to perform various bioinformatics tasks. Specifically, it handles base calling, barcoding, and applying the ARTIC protocol for Oxford Nanopore sequencing data related to SARS-CoV-2.

## 🚀 Features

- **Base Calling** using Guppy
- **Barcoding** with Guppy
- Implementation of the **ARTIC protocol** using `artic minion`
- **Depth Analysis**
- **Email Notifications** upon process completion

## 📋 Dependencies

- Guppy (For basecalling)
- ARTIC toolkit
- pandas
- Python standard libraries: os, subprocess, argparse, shutil
- Python 3.x

## 🔧 Installation

1. **Clone this repository:**
    ```bash
    git clone [URL of this repository]
    ```

2. **Navigate to the repository:**
    ```bash
    cd [repository name]
    ```

3. **Ensure you have all the required dependencies installed.**

## 🎯 Usage

```bash
python articProtocol.py -r RUN_NAME -f FAST5 -m MIN -x MAX -a ACCURACY [-g NUM_CALLERS] [-k GPU_RUNNERS_PER_DEVICE] [-i CHUNKS_PER_RUNNER] [-j NUMGPUS] [-e EMAIL]
```
### Parameters:

- `-r, --run_name`: Name of the project.
- `-f, --fast5`: Full path to the directory containing the fast5 files.
- `-m, --min`: Minimum amplicon length.
- `-x, --max`: Maximum amplicon length.
- `-a, --accuracy`: Execute Guppy basecaller in high or fast mode (values: 'fast', 'high').
- `-g, --num_callers`: (Optional) Number of parallel basecallers. Default = 8.
- `-k, --gpu_runners_per_device`: (Optional) Tag to maximize GPU usage. Default = 64.
- `-i, --chunks_per_runner`: (Optional) Maximum chunks per run. Default = 256.
- `-j, --numGpus`: (Optional) Number of GPUs. Default = 1.
- `-e, --email`: (Optional) Notify by email upon completion. Values: "Si" or "No". Default = "No".


## Output Notes:

1. `my_consensus_genomes.fasta`: This is a concatenated file of all consensus genome sequences.
2. `depth.csv`: A file detailing sequencing depth.

After completion, an email notification can be sent (if chosen) containing relevant details and attachments.

## Contact:

For any questions or issues with the code, feel free to reach out:

**Twitter**: [@El_Dryosa](https://twitter.com/El_Dryosa)  
**Email**: [example@email.com](mailto:juvenal.yosa@gmail.com)


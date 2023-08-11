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


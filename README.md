# Strategies of Code-switching in Human-Machine Dialogs

This repository contains the implementation and analysis code for the experiments described in our paper:

> **Strategies of Code-switching in Human-Machine Dialogs**
> [arXiv:2508.07325](https://arxiv.org/abs/2508.07325)

## Overview

Our project implements a **Map-Task chatbot** used to study code-switching in human–machine interactions.
It features a **client–server architecture**:

* **Client:** A React-based web application providing the interactive map-task interface for participants.
* **Server:** A Python Flask application implementing the chatbot agent logic and handling communication with the client.

In addition, the repository includes an **`analysis/`** directory containing scripts and notebooks for **post-processing and analyzing collected data** from our experiments.

## Paper Link

📄 [Read the full paper on arXiv](https://arxiv.org/abs/2508.07325)

If you use this code in your work, please cite our paper:

```bibtex
@misc{geckt2025strategiescodeswitchinghumanmachinedialogs,
      title={Strategies of Code-switching in Human-Machine Dialogs}, 
      author={Dean Geckt and Melinda Fricke and Shuly Wintner},
      year={2025},
      eprint={2508.07325},
      archivePrefix={arXiv},
      primaryClass={cs.CL},
      url={https://arxiv.org/abs/2508.07325}, 
}
```

## Directory Structure

```
.
├── client/        # React web application for the Map-Task interface
├── server/        # Python Flask application implementing the chatbot
├── analysis/      # Data post-processing and analysis scripts
└── README.md
```

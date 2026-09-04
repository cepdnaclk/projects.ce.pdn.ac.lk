---
layout: project_page_dept
title: PeraMorphIQ
caption: ""
nav_order: 3
permalink: /peramorphiq/
gh_page: "projects/department_projects/peramorphiq.md"
thumb_image: "/assets/images/peramorphiq-thumb.png"

repositories:
  - https://github.com/PeraMorphIQ/PeraMorphIQ-SRAM-Compiler
  - https://github.com/PeraMorphIQ/PeraMorphIQ-Web
  - https://github.com/cepdnaclk/e16-4yp-neuromorphic-architecture
  - https://github.com/cepdnaclk/e17-4yp-Neuromorphic-NoC-Architecture-for-SNNs
  - https://github.com/cepdnaclk/e18-4yp-Neuromorphic-NoC-Architecture-for-SNNs

publications:
  - https://doi.org/10.1016/j.sysarc.2026.103869
  - https://doi.org/10.48550/arXiv.2603.11939
  - https://doi.org/10.1109/ICIIS58898.2023.10253607

projects:
  - https://projects.ce.pdn.ac.lk/4yp/e16/neuromorphic-architecture/
  - https://projects.ce.pdn.ac.lk/4yp/e17/Neuromorphic-NoC-Architecture-for-SNNs/
  - https://projects.ce.pdn.ac.lk/4yp/e18/Neuromorphic-NoC-Architecture-for-SNNs/
  - https://projects.ce.pdn.ac.lk/4yp/e20/On-Chip-Online-Learning-For-Neuromorphic-Hardware/

links:
  - { title: "Project Website", url: "https://peramorphiq.ce.pdn.ac.lk/" }
  - { title: "GitHub Organization", url: "https://github.com/PeraMorphIQ" }
  - { title: "Research Projects", url: "https://peramorphiq.ce.pdn.ac.lk/projects.html" }
  - { title: "Publications", url: "https://peramorphiq.ce.pdn.ac.lk/publications.html" }
  - { title: "LinkedIn", url: "https://www.linkedin.com/company/peramorphiq/" }
---

**Brain-inspired hardware for energy-efficient intelligence at the edge.**

_PeraMorphIQ_ is a neuromorphic computing research group at the _Department of Computer Engineering_, University of Peradeniya, and is part of [ESCAL](https://escal.ce.pdn.ac.lk/){:target="\_blank"} (Embedded Systems and Computer Architecture Laboratory) under [PeraCom](https://www.ce.pdn.ac.lk/){:target="\_blank"}. The group designs neuromorphic architectures for spiking neural networks, from accelerator microarchitecture and RISC-V System-on-Chip integration through to FPGA prototypes and silicon analysis.

Our work runs end to end, from simulation frameworks and algorithmic exploration through FPGA prototypes to ASIC implementation. We build configurable neuromorphic accelerators with on-chip learning, memory and power optimisation, and real-time processing suited to embedded deployment. By bridging neuroscience, machine learning and embedded systems, we aim at computing platforms that borrow the adaptability and energy efficiency of biological neural systems, and are small enough to actually deploy.

### Research areas

Four connected threads, from the neuron model up to a deployable system-on-chip.

- **Neuromorphic accelerators** - Configurable accelerator microarchitectures for spiking networks, designed for the small-scale regime where embedded and edge workloads actually sit.
- **Spiking neural networks & on-chip learning** - Hardware-realisable learning rules and the weight-update paths that let a deployed device adapt without a round trip to a host machine.
- **RISC-V SoC & Network-on-Chip** - Custom ISA extensions, network interfaces and 2D-mesh interconnect that turn a general-purpose open ISA into a spiking-network substrate.
- **Edge AI hardware** - Memory organisation, power optimisation and FPGA-to-ASIC paths that bring real-time inference within the energy budget of an edge device.

### Featured projects

- [**SNAP-V: A RISC-V SoC with Configurable Neuromorphic Acceleration for Small-Scale Spiking Neural Networks**](https://peramorphiq.ce.pdn.ac.lk/project.html?id=snap-v-accelerator){:target="\_blank"} (E19 Final Year Project, 2024-present) - A RISC-V neuromorphic SoC with two accelerator variants, Cerebra-S (bus-based) and Cerebra-H (NoC-based), optimised for small-scale SNN inference at 1.05 pJ per synaptic operation.
- [**On-Chip Offline Neuromorphic Computing**](https://peramorphiq.ce.pdn.ac.lk/project.html?id=on-chip-offline-learning){:target="\_blank"} (E20 Final Year Project, 2025-present) - A custom RISC-V CPU with a six-instruction ISA extension for on-chip spiking neural network backpropagation training, running without any host PC.
- [**On-Chip Online Learning for Neuromorphic Hardware**](https://peramorphiq.ce.pdn.ac.lk/project.html?id=on-chip-online-learning){:target="\_blank"} (E20 Final Year Project, 2025-present) - Learning rules implemented directly in neuromorphic hardware, so a deployed device can adapt online without a round trip to a host machine.
- [**PeraMorphIQ SRAM Compiler**](https://github.com/PeraMorphIQ/PeraMorphIQ-SRAM-Compiler){:target="\_blank"} (Open-source tool, 2026-present) - A streamlined, automated workflow for generating custom SRAM macros, built on the OpenRAM framework and released publicly for the open-source hardware community.

### Selected publications

- **Neuromorphic architectures for edge-oriented spiking neural networks: A review** <br />
  Kanishka Gunawardana, Sanka Peeris, Kavishka Rambukwella, Roshan Ragel, Isuru Nawinne <br />
  _Journal of Systems Architecture_, 177, 103869 (2026) | Open access (CC BY 4.0) <br />
  doi: [10.1016/j.sysarc.2026.103869](https://doi.org/10.1016/j.sysarc.2026.103869){:target="\_blank"}
- **SNAP-V: A RISC-V SoC with Configurable Neuromorphic Acceleration for Small-Scale Spiking Neural Networks** <br />
  Kanishka Gunawardana, Sanka Peeris, Kavishka Rambukwella, Thamish Wanduragala, Saadia Jameel, Roshan Ragel, Isuru Nawinne <br />
  _arXiv_ preprint (2026) | Open access <br />
  doi: [10.48550/arXiv.2603.11939](https://doi.org/10.48550/arXiv.2603.11939){:target="\_blank"}
- **RV32IMF Five-Stage Pipeline Implementation with Interrupt and Random Number Generation Units** <br />
  Dinindu Thilakarathna, Heshan Dissanayake, Roshan Ragel, Isuru Dasanayake, Mahanama Wickramasinghe <br />
  _2023 IEEE 17th International Conference on Industrial and Information Systems (ICIIS)_ (2023) <br />
  doi: [10.1109/ICIIS58898.2023.10253607](https://doi.org/10.1109/ICIIS58898.2023.10253607){:target="\_blank"}

### Work with us

We supervise final-year and graduate projects, and we welcome collaboration with research groups and industry partners working on neuromorphic and edge AI hardware.

Our code, tools and hardware releases are published through the [PeraMorphIQ GitHub organisation](https://github.com/PeraMorphIQ){:target="\_blank"}.

For the details, feel free to contact [Dr. Isuru Nawinne](https://people.ce.pdn.ac.lk/staff/academic/isuru-nawinne/){:target="\_blank"} and/or [Prof. Roshan Ragel](https://people.ce.pdn.ac.lk/staff/academic/roshan-ragel/){:target="\_blank"}, or write to [peramorphiq@eng.pdn.ac.lk](mailto:peramorphiq@eng.pdn.ac.lk).

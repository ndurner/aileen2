# Aileen 2.0 - AI Office Agent
Welcome to Aileen 2.0! Aileen is an AI office agent designed to assist with specific tasks, currently focused on summarizing legislative proceedings broadcast by Germany's parliamentary TV. Leveraging recent advances in transformer technology, Aileen can navigate and adapt to changes in web environments autonomously, providing personalized summaries via email to authorized users.

Please note that Aileen 2.0 is specialized for this single use-case and is not yet a general-purpose AI assistant. We are continuously working on expanding her capabilities and look forward to future developments.

# Prerequisites
- Nvidia CUDA and Pytorch set up
    - e.g. AWS AMI "Deep Learning OSS Nvidia Driver AMI GPU PyTorch 2.2 (Ubuntu 20.04)"
        * activate environment with "conda activate pytorch"
    - Tested using Nvidia T4 GPU (AWS instance type: g4dn.xlarge)
- Chrome installed (for Selenium)
    1. wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
    2. sudo apt install ./google-chrome-stable_current_amd64.deb

# Installation

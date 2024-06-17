# Aileen 2.0 - AI Office Agent
Welcome to Aileen 2.0! Aileen is an AI office agent designed to assist with specific tasks, currently focused on summarizing legislative proceedings broadcast by Germany's parliamentary TV. Leveraging recent advances in transformer technology, Aileen can navigate and adapt to changes in web environments autonomously, providing personalized summaries via email to authorized users.

Please note that Aileen 2.0 is specialized for this single use-case and is not (yet?) a general-purpose AI assistant.

> Aileen 2 was created for 'NVIDIA and LangChain #GenerativeAI Agents Developer Contest'. Treat it as a technology preview.

# Features and special techniques
* Vision: can "look" at websites through PaliGemma and EasyOCR CRAFT-CDNN
* Small Language Model support
* Function-calling implemented through Python syntax (not JSON, as commonly used)

# Prerequisites
- Ubuntu GNU/Linux, Python 3
- [Nvidia NGC API key](https://docs.nvidia.com/ai-enterprise/deployment-guide-spark-rapids-accelerator/0.1.0/appendix-ngc.html)
- Nvidia CUDA and PyTorch set up. Tested variants:
    - Option 1: Amazon Web Services:
        * AMI: "Deep Learning OSS Nvidia Driver AMI GPU PyTorch 2.3 (Ubuntu 20.04)"
            * activate environment with "conda activate pytorch"
        * Instance type: g4dn.xlarge
            * (provides Nvidia T4)
            * 100 GB root volume
            * optionally: Security Group settings that will allow inbound HTTP for Twilio SMS Webhook
    - Option 2: Vast.ai:
        * Instance type: 1x RTX A5000
        * Template: Nvcr.io/Nvidia/Pytorch
        * Disk: 60 GB
        * Launch mode: "Run interactive shell server, SSH"
        * (cli command:)
> vastai create instance x --image nvcr.io/nvidia/pytorch:23.10-py3 --env '-e DATA_DIRECTORY=/workspace/' --disk 60.12945594969661 --ssh --direct

- Chrome installed (for Selenium)
    * wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
    * sudo apt install ./google-chrome-stable_current_amd64.deb
- Internet connection for Installation below

# Installation
0. (ensure that your PyTorch enabled venv is enabled)
    * with the AWS Deep Learning AMI:
        * conda init
        * conda activate pytorch
    * with the Nvidia PyTorch container:
        * sudo apt install python3.10-venv
        * python3 -m venv venv
        * source venv/bin/activate
1. download this repository:
    * git clone --depth 1 https://github.com/ndurner/aileen2
2. install dependencies:
    * cd aileen2; pip install -U -r requirements.txt
3. install the transformer models
    1. option 1: if you have a direct link to PaliGemma MIX 448:
        1. at the console:
            * python3 ./setup_resources.py --vlm-model-url "https://..."
    2. option 2: install using Hugging Face:
        1. log in to HuggingFace, request access to the [MIX checkpoint](https://huggingface.co/google/paligemma-3b-mix-448)
        2. at the console:
            * huggingface-cli login 
            * huggingface-cli download "google/paligemma-3b-mix-448"
        3. install the rest:
            * python3 ./setup_resources.py
4. integrations are mocked-up by default, to switch: in config.json set:
    * implementations/agent_lm: lm_ngc
    * implementations/vlm: vlm_hf
    * implementations/ocr: ocr_easyocr
5. create a file named ".env" in this folder:
    * touch .env
6. set Nvidia API key
    1. Option 1: in .env:
        * NVIDIA_API_KEY=nvapi-...
    2. Option 2: in config.json:
        * key "nvidia_api_key"
7. optionally, if Aileen shall be reachable via SMS text messages ("Cloud office" option):
    1. [create a Twilio account](https://www.twilio.com/try-twilio), get a Twilio phone number, retrieve Auth Token
    2. add Twilio Auth Token:
        1. Option 1: to .env:
            * TWILIO_AUTH_TOKEN=...
        2. Option 2: to config.json:
            * key "twilio_auth_token"
    3. in config.json, under "server", verify that the Webhook necessary to receive notifications on can be established at "host" and "port"
    4. in the Twilio management console (Phone Numbers -> Active Numbers -> (Number) -> "Configure" tab -> scroll down to "Messaging Configuration"), establish an HTTP POST Webhook: as "http://(host):(port)/sms", e.g.:
        * http://ec2-54-226-207-14.compute-1.amazonaws.com:5000/sms
8. optionally, if Aileen shall send results by E-Mail:
    1. set up [Amazon Simple Email Service](https://aws.amazon.com/de/ses/)
    2. if in a sandboxed account, be sure to register any recepients under Identities
    3. for the IAM user, role "AmazonSESFullAccess" can be used
    4. add AWS Access Key and Secret Access Key to .env:
        * AWS_ACCESS_KEY_ID=A...
        * AWS_SECRET_ACCESS_KEY=B...
9. add user profile(s) to config.json: key "users":
```
    "users": {
        "+18005550100": {
            "profile": "Software Engineer",
            "email": "ndurner@example.invalid"
        }
```
The key (+1800... in this example) is the user’s phone number, the "profile" therein their profile text (used for the personalized summary) and recipient E-Mail address.

# Advanced Configuration
When the mockups have been switched for real implementations (see Installing above), the Language Models Llama3-8B-Instruct (for the Agent) and Gemma-7B (for summarization) are used by default. This can be changed in config.json to models offered through the Nvidia NGC Model Catalog. Not all models are supported, though. A list of supported models can be found in lm.py ("get_ctx_len_for_model"). For each model, the Tokenizer needs to be accessible. For gated models, this can be achieved by obtaining access via Hugging Face (and setting HF_TOKEN in .env) or establishing a publicly accessible copy in lm.py ("get_tokenizer_for_model").

# Running
0. (use TRANSFORMERS_OFFLINE=1 if a gated model (like PaliGemma) is to be used without Hugging Face access), e.g.:
    * export TRANSFORMERS_OFFLINE=1
1. Option 1: on local device:
    * python3 ./main.py --task "Summarize https://dbtg.tv/cvid/7611506"
2. Option 2: on server ("cloud office"):
    * python3 ./server.py

# Anticipated questions
## SessionNotCreatedException
Error message:
> selenium.common.exceptions.SessionNotCreatedException: Message: session not created: Chrome failed to start: exited normally.
  (session not created: DevToolsActivePort file doesn't exist)
  (The process started from chrome location /home/ubuntu/.cache/selenium/chrome/linux64/126.0.6478.61/chrome is no longer running, so ChromeDriver is assuming that Chrome has crashed.)

Remedy: check that Chrome is installed and Selenium is set up (see Prerequisites above)

## Access to model is restricted
Error message:
> Access to model google/paligemma-3b-mix-448 is restricted. You must be authenticated to access it.

Remedy: after PaliGemma has been downloaded to the Hugging Face cache (either through a direct download/setup-resources.py or huggingface-cli, see above),
both main.py and server.py can be run after the TRANSFORMERS_OFFLINE environment variable has been set, e.g. in the file .env:
> TRANSFORMERS_OFFLINE=1

If setup-resources.py had failed previously after a successful direct-download of PaliGemma, you can re-run
setup-resources.py using the already downloaded tar instead of the direct-download URL:
> python3 ./setup_resources.py --vlm-model-url /tmp/paligemma.tar

## module 'cv2.dnn' has no attribute 'DictValue'
Error message:
> AttributeError: module 'cv2.dnn' has no attribute 'DictValue'

Set up a fresh venv. Assuming the Nvidia PyTorch container:
> apt install python3.10-venv
python3 -m venv venv
source venv/bin/activate

Then, repeat installation procedure as above.

# Acknowledgments
The PaliGemma parser in paligemma/ was taken from Big-Vision repository, where it was released under Apache-2.0 license.

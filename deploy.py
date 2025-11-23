import os
import contextlib
import inspect
import sys
import modal
from modal import Image, App, asgi_app
from fastapi import FastAPI
from mcp.server.fastmcp import FastMCP
import requests
import time
import io
import zipfile
import json
from fastapi.responses import StreamingResponse
import asyncio
from fastapi import FastAPI, Request, HTTPException, Depends
from claude_agent_sdk import ClaudeAgentOptions, ClaudeSDKClient


app = modal.App(name="transilience-prod-claude-laptop")

IGNORED_DIRS = {'.git', '__pycache__', 'node_modules', '.venv', '.pytest_cache', '.mypy_cache'}
IGNORED_EXTENSIONS = {'.pyc', '.pyo', '.pyd', '.so', '.dylib', '.DS_Store'}


#HOME = "/tmp/securitygpt/custom_skills/vuln_researcher/"
HOME = "/tmp/securitygpt/custom_skills/aws_compliance_collector_min/"
HOME = "/tmp/securitygpt/custom_skills/aws_access_reviewer/"
HOME = "/tmp/workfolder/playwright-min/"

base_user_prompt = """ 


- upload the following reports to S3:
    - reports of each of the agents, in separate files, each file should be a markdown file.
    - any other files you created, upload all of them to S3.
        Use curl to upload the file to S3: example:

    ```bash 
    curl -X POST https://transilience--s3-file-upload-fastapi-app-dev.modal.run/upload \
    -F "file=@/tmp/report.md"
    ```
""" 

task_prompt = """
- create detailed todo tasks as and check off as you are executing them.  upload the todo task markdownfile to s3 as well.
""" 
s3_upload_prompt = """
- upload the following reports to S3:
    - reports of each of the agents, in separate files, each file should be a markdown file.
    - any other files you created, upload all of them to S3.
    - Install any tools that you do not have to accomplish the task.
""" 

compliance_prompt = """
get configurations of database and compute services in all regions and their compliance information for the services and upload the report to S3, 
"""
incident_response_prompt = """
get guard duty alerts from AWS Guard Duty, conduct root cause analysis and upload the report to S3, 
""" 
cost_optimizer_prompt = """
get cost optimization root cause analysis from AWS Cost Explorer and upload the report to S3, 
""" 
vuln_researcher_prompt = """
get vulnerability research report for CVE-2025-11371 and upload the all the reports to S3
""" 


base_system_prompt = f"""
- you would be given a task and your goal is to accomplish the task in the bestest way and most efficient way possible.
- the instructions would be given to you in the CLAUDE.md file
- your skills are specified in .claude/skills/ directory 
- additional agents, if any needed, would be given to you in the .claude/agents/ directory.
**Rules**
 - always think about how to accomplish the task in the bestest way possible with the minimal number of steps
- think about how to group the results to make it easier to understand and report on.
- you must not hallucinate or make up any information, you must only use the information provided to you or what you got from executing the tools
- Install any tools that you do not have to accomplish the task.

CRITICAL RULES:
Your HOME directory is {HOME}, you must not attempt to access files from outside your HOME directory.

    """

memory_prompt = """
IMPORTANT: ALWAYS VIEW YOUR MEMORY DIRECTORY BEFORE DOING ANYTHING ELSE.
MEMORY PROTOCOL:
1. Use the `view` command of your `memory` tool to check for earlier progress.
2. ... (work on the task) ...
    - As you make progress, record status / progress / thoughts etc in your memory.
- ASSUME INTERRUPTION: Your context window might be reset at any moment, so you risk losing any progress that is not recorded in your memory directory.
"""
incident_response_system_prompt = """
get guard duty alerts from AWS Guard Duty, conduct root cause analysis and upload the report to S3, 
""" 


slack_prompt = """
    - you must send all the reports you generated and files you created to Slack in threads. Use environment variable SLACK_TOKEN for the token.

"""


user_prompt = base_user_prompt + compliance_prompt + s3_upload_prompt  + slack_prompt 

system_prompt = base_system_prompt 

# Set HOME directory to the target directory
os.environ["HOME"] = HOME
    
# Build the Modal image with all required dependencies
image = (
    modal.Image.from_registry("ubuntu:20.04", add_python="3.11")
    .run_commands(
        "export DEBIAN_FRONTEND=noninteractive",
        "ln -fs /usr/share/zoneinfo/UTC /etc/localtime",
        "apt-get update && apt-get install -y tzdata",
        "dpkg-reconfigure --frontend noninteractive tzdata",
    )
    .run_commands(
        "apt-get update && apt-get upgrade -y",
        "apt-get install -y --no-install-recommends \
        curl \
        git \
        python3 \
        python3-pip \
        sudo \
        software-properties-common \
        ca-certificates"
    )
    .run_commands("curl -fsSL https://deb.nodesource.com/setup_lts.x | bash - && \
                   apt-get install -y nodejs")
    .run_commands("npm install -g @anthropic-ai/claude-code")
    .pip_install("anyio", "loguru", "claude-code-sdk", "anthropic")
    .run_commands("pip install pydantic fastapi --upgrade")
    .run_commands("pip install --upgrade modal")
    .pip_install(
        "anyio", "loguru", "pandas", "requests", "asyncio", "claude_agent_sdk", "aiohttp", "dnspython"
    )
    .add_local_dir(
        "/Users/venkat/workfolder/",
        remote_path="/tmp/workfolder/", 
        ignore=lambda p: (
            any(part in IGNORED_DIRS for part in p.parts) or
            any(p.name.endswith(ext) for ext in IGNORED_EXTENSIONS)
        )
    )
)

# Modal secrets
tr_aws_secrets = [modal.Secret.from_name("tr_aws_secret", environment_name="main")]
llm_secrets = [modal.Secret.from_name("llm-secrets", environment_name="main")]
aws_secrets = [modal.Secret.from_name("my-aws-secret", environment_name="main")]
all_secrets = tr_aws_secrets + llm_secrets + aws_secrets


async def run_test():
    import subprocess
    import sys

    print(
        subprocess.check_output(
            [
                "claude",
                "--output-format",
                "stream-json",
                "--verbose",
                "--max-turns",
                "1",
                "--print",
                "say hi!",
            ]
        ).decode(),
        file=sys.stderr,
    )
    
    
@app.function(image=image, secrets=all_secrets, timeout=6000)
async def get_prompts(HOME: str, type: str, customer_name: str):
    print(HOME, type, customer_name)
    

    base_system_prompt = f"""
        - you would be given a task and your goal is to accomplish the task in the bestest way and most efficient way possible.
        - the instructions would be given to you in the SKILL.md file, any other instructions would be given to you in .md files in the same directory as the SKILL.md file.
        - additional scripts, if any needed, would be given to you in the scripts/ directory.
        - additional agents, if any needed, would be given to you in the .claude/agents/ directory.
        **Rules**
        - always think about how to accomplish the task in the bestest way possible with the minimal number of steps
        - think about how to group the results to make it easier to understand and report on.
        - you must not hallucinate or make up any information, you must only use the information provided to you or what you got from executing the tools
        - Install any tools that you do not have to accomplish the task.

        CRITICAL RULES:
        1. NO MEMORY - Do not check previous work
        2. NO VERIFICATION - Do not read what you wrote
        3. NO CONTEXT - Each action is independent
        4. ONE TASK - Complete your single task and stop
        5. Your HOME directory is {HOME}, you must not attempt to access files from outside your HOME directory.

        """

    memory_prompt = """
        IMPORTANT: ALWAYS VIEW YOUR MEMORY DIRECTORY BEFORE DOING ANYTHING ELSE.
        MEMORY PROTOCOL:
        1. Use the `view` command of your `memory` tool to check for earlier progress.
        2. ... (work on the task) ...
            - As you make progress, record status / progress / thoughts etc in your memory.
        - ASSUME INTERRUPTION: Your context window might be reset at any moment, so you risk losing any progress that is not recorded in your memory directory.
        """
    incident_response_prompt = f"""
    your task :
    get guard duty alerts from AWS Guard Duty for {customer_name}, conduct root cause analysis and upload the report to S3, 
    """ 

    compliance_prompt = f"""
    your task :
    get configurations of database and compute services for {customer_name} in all regions and their compliance information for the services and upload the report to S3, 
    """

    slack_prompt = f"""
        - you must send all the reports you generated and files you created to Slack in threads. Use environment variable SLACK_TOKEN for the token.
        slack_channel = 'transilience-{customer_name}-secops'
    """

    reviewer_prompt = f"""
    your task :
    send hello text of customer {customer_name} to slack in a thread.
    """

    user_prompt = base_user_prompt + reviewer_prompt + s3_upload_prompt  + slack_prompt  + reviewer_prompt

    system_prompt = base_system_prompt + reviewer_prompt

    
    if type == "test":
        return base_user_prompt, base_system_prompt
    elif type == "aws_compliance_collector_min":
        return base_user_prompt + compliance_prompt + s3_upload_prompt  + slack_prompt, system_prompt  
    elif type == "vuln_researcher":
        return base_user_prompt + vuln_researcher_prompt + s3_upload_prompt  + slack_prompt , system_prompt  
    elif type == "cost_optimizer":
        return base_user_prompt + cost_optimizer_prompt + s3_upload_prompt  + slack_prompt , system_prompt  
    elif type == "aws_incident_analyzer":
        return base_user_prompt + incident_response_prompt + s3_upload_prompt  + slack_prompt , system_prompt  
    elif type == "aws_access_reviewer":
        return base_user_prompt + reviewer_prompt + s3_upload_prompt  + slack_prompt , system_prompt  
    
    

    
import asyncio
import aiohttp
from pathlib import Path
from typing import Any, Dict
from claude_agent_sdk import tool, create_sdk_mcp_server, ClaudeSDKClient, ClaudeAgentOptions

SERVICE_URL = "https://transilience--s3-file-upload-fastapi-app-dev.modal.run/upload"

# Define the S3 upload tool using the @tool decorator
@tool("upload_to_s3", "Upload a file to S3 bucket via the Modal endpoint", {"file_path": str, "service_url": str})
async def upload_to_s3(args: dict[str, Any]) -> dict[str, Any]:
    """
    Upload a file to S3 via the Modal endpoint.
    
    Args:
        args: Dictionary containing:
            - file_path: Path to the file to upload
            - service_url: URL of the upload service (optional, defaults to SERVICE_URL)
    
    Returns:
        Dict with upload result
    """
    file_path = args.get("file_path")
    service_url = args.get("service_url", SERVICE_URL)
    
    path = Path(file_path)
    
    if not path.exists():
        error_msg = f"File not found: {file_path}"
        return {
            "content": [{
                "type": "text",
                "text": f"❌ Error: {error_msg}"
            }],
            "success": False,
            "error": error_msg
        }
    
    try:
        status_msg = f"Uploading {path.name}..."
        
        # Use aiohttp for async file upload
        async with aiohttp.ClientSession() as session:
            with open(path, 'rb') as f:
                form_data = aiohttp.FormData()
                form_data.add_field('file', f, filename=path.name)
                
                async with session.post(service_url, data=form_data) as response:
                    if response.status == 200:
                        result = await response.json()
                        s3_key = result.get('s3_key')
                        file_size = path.stat().st_size
                        
                        success_msg = (
                            f"✓ File uploaded successfully!\n"
                            f"Filename: {path.name}\n"
                            f"S3 Key: {s3_key}\n"
                            f"Size: {file_size} bytes"
                        )
                        
                        return {
                            "content": [{
                                "type": "text",
                                "text": success_msg
                            }],
                            "success": True,
                            "s3_key": s3_key,
                            "filename": path.name,
                            "size": file_size,
                            "error": None
                        }
                    else:
                        error_text = await response.text()
                        error_msg = f"HTTP {response.status}: {error_text}"
                        return {
                            "content": [{
                                "type": "text",
                                "text": f"❌ Upload failed: {error_msg}"
                            }],
                            "success": False,
                            "error": error_msg
                        }
    
    except Exception as e:
        error_msg = str(e)
        return {
            "content": [{
                "type": "text",
                "text": f"❌ Error during upload: {error_msg}"
            }],
            "success": False,
            "error": error_msg
        }


# Create an SDK MCP server with the custom tool
s3_server = create_sdk_mcp_server(
    name="s3-upload-tools",
    version="1.0.0",
    tools=[upload_to_s3]
)
  
@app.function(image=image, secrets=all_secrets, timeout=6000)
async def run_claude_agent(type: str, customer_name: str):
    import os, sys
    
    sys.path.append('/tmp/')
    # ANTHROPIC_API_KEY should be set via environment variable or Modal secrets
    # os.environ["ANTHROPIC_API_KEY"] = "your-anthropic-api-key-here"

    HOME = "/tmp/workfolder/playwright-min/" 
    # List .claude directory structure
    import subprocess
    claude_dir = os.path.join(HOME, ".claude")
    if os.path.exists(claude_dir):
        print(f"\n=== Listing .claude directory structure ===")
        result = subprocess.run(
            ["ls", "-alR", claude_dir],
            capture_output=True,
            text=True
        )
        print(result.stdout)
        if result.stderr:
            print(f"stderr: {result.stderr}")
    else:
        print(f"\n.claude directory does not exist at {claude_dir}")

    sys.exit
    #user_prompt, system_prompt =  get_prompts.remote(HOME, type, customer_name)
    user_prompt = "use your skillks and collect stock news on apple "
    system_prompt = base_system_prompt +  "\n you are a helpful assistant that helps with company stock research"
    print (f"system_prompt\n {system_prompt}")    
    print (f"user_prompt\n {user_prompt}"    )
    
    # Change to the working directory
    os.chdir(HOME)
    
    # Ensure /tmp has proper permissions
    os.chmod("/tmp", 0o777)
    
    # Create .claude/memory directory
    claude_memory_dir = os.path.join(HOME, ".claude", "memory")
    os.makedirs(claude_memory_dir, exist_ok=True)
    
    print("in run_claude_agent_test .........................")
    print(f"HOME directory: {os.environ['HOME']}")
    print(f"Current working directory: {os.getcwd()}")
    print(f"Running as UID: {os.getuid()}")
    
    options = ClaudeAgentOptions(
        system_prompt=system_prompt,
        permission_mode='acceptEdits',
        cwd=HOME,
        model="claude-haiku-4-5",
        max_thinking_tokens=1024,
        allowed_tools=[
            #"WebSearch",
            #"WebFetch",
            "Write",
            "Read",
            "Bash",
            #"memory",
            "Glob",
            "Grep",
            #"mcp__s3-upload-tools__upload_to_s3"
        ],
        #max_turns=10,
        #mcp_servers={"s3-upload-tools": s3_server}
    )

    print("before ClaudeSDKClient initialization .........................")
    async with ClaudeSDKClient(options=options) as client:
        await client.query(prompt=user_prompt)
        async for message in client.receive_response():
            print('\n\n message: \n\n')
            print(message)  

@app.function(image=image, secrets=all_secrets, timeout=600)
async def run_claude_test(task: str, customer_name: str):
    print("Running in parent process, should work")
    await run_claude_agent.remote(task, customer_name)
    
    
@app.local_entrypoint()
def local_entrypoint():
    #run_claude_test.remote()
    type = "aws_incident_analyzer"
    type = "aws_access_reviewer"
    customer_name = "finmont"
    run_claude_agent.remote(type, customer_name)
    

custom_domains = [
    "clauderoot.transilienceapp.com",
    "clauderoot.transilienceapp.com"
] if os.environ.get('MODAL_PROFILE') == 'transilience' else [
    "clauderoot.transilienceapi.com",
    "clauderoot.transilienceapi.com"
]

web_app = FastAPI()

@web_app.get("/")
async def root():
    return {"message": "Claude Root Agent API"}

@web_app.post("/run")
async def run_agent(request: Request):
    data = await request.json()
    #type = data.get("type", "aws_compliance_collector_min")
    #type = data.get("type", "aws_incident_analyzer")
    #customer_name = data.get("customer_name", "korr")
    
    # Trigger the agent asynchronously
    #run_claude_agent.spawn(type, customer_name)
    
    #return {"status": "started", "type": type, "customer_name": customer_name}

@app.function(image=image, secrets=all_secrets)
@asgi_app(custom_domains=custom_domains)
def clauderoot_transilience_app_com():
    return web_app

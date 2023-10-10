import aiohttp
import logging
import subprocess
from typing import Any
from ..dependencies.service_models import HttpResponse

async def get_request(session: aiohttp.ClientSession, url: str,
                      **kwargs: Any) -> HttpResponse:
    try:
        async with session.get(url=url, **kwargs, ssl=False) as response:
            status_code = response.status
            headers = response.headers
            response_content_type = headers.get('Content-Type')
            
            if 'json' in response_content_type:
                response_data = await response.json()
            else:
                response_data = await response.text()
            return HttpResponse(headers=headers, status_code=status_code, response_data=response_data)
    except aiohttp.ClientError as e:
        return {"error": f"Error getting data from {url}: {e}"}
    

async def post_request(session: aiohttp.ClientSession, 
                       url: str, 
                       auth: aiohttp.BasicAuth, 
                       data: dict,
                       logging: logging):
    headers = {
        'Content-Type': 'application/json'
    }
    
    try:
        async with session.post(url=url,
                                data=data,
                                headers=headers,
                                auth=auth, 
                                ssl=False) as response:
            response_content_type = response.content_type
            status_code = response.status
            
            if 'json' in response_content_type:
                response_data = await response.json()
            else:
                response_data = await response.text()
            logging.info(f"status={response.status}, message={response_data}")
            return HttpResponse(headers=headers, status_code=status_code, response_data=response_data)
        
    except aiohttp.ClientError as e:
        return {"error": f"Error posting data to {url}: {e}"}

def execute_shell(script: str):
    script_command = [script]
    # Run the shell script
    try:
        # Run the script and capture the output and error streams
        completed_process = subprocess.run(script_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Check if the process completed successfully
        if completed_process.returncode == 0:
            print("Script executed successfully.")
            print("Output:")
            print(completed_process.stdout)
        else:
            print(f"Script failed with return code {completed_process.returncode}.")
            print("Error:")
            print(completed_process.stderr)
    except FileNotFoundError:
        print("The script file was not found.")
        raise Exception("The script file was not found.")
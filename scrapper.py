import pip_system_certs.wrapt_requests
import os
import ssl
import time
import requests
from bs4 import BeautifulSoup
import csv
import json
from rich.console import Console
from rich.progress import track
from rich.panel import Panel
import warnings
import contextlib

# Base URL of the site
BASE_URL = "https://e-crub.gunb.gov.pl"
INTER_REQUEST_DELAY_MILISECONDS = 100
CERTFILE = os.path.join(os.path.dirname(__file__), "Certum Trusted Network CA.crt")
CERTFILE = False

console = Console()

from urllib3.exceptions import InsecureRequestWarning

old_merge_environment_settings = requests.Session.merge_environment_settings

@contextlib.contextmanager
def no_ssl_verification():
    opened_adapters = set()

    def merge_environment_settings(self, url, proxies, stream, verify, cert):
        # Verification happens only once per connection so we need to close
        # all the opened adapters once we're done. Otherwise, the effects of
        # verify=False persist beyond the end of this context manager.
        opened_adapters.add(self.get_adapter(url))

        settings = old_merge_environment_settings(self, url, proxies, stream, verify, cert)
        settings['verify'] = False

        return settings

    requests.Session.merge_environment_settings = merge_environment_settings

    try:
        with warnings.catch_warnings():
            warnings.simplefilter('ignore', InsecureRequestWarning)
            yield
    finally:
        requests.Session.merge_environment_settings = old_merge_environment_settings

        for adapter in opened_adapters:
            try:
                adapter.close()
            except:
                pass


def fetch_initial():
    global CERTFILE
    """
    Sends a request simulating the form submission with the given voivodeship.
    
    Adjust the URL endpoint and payload parameters as needed.
    """
    # Replace '/search' with the correct endpoint for the form
    search_url = f"{BASE_URL}"
    
    session = requests.Session()
    try:
        # Depending on the form, you might need GET or POST
        response = session.get(search_url, verify=CERTFILE)
        response.raise_for_status()
    except Exception as err:
        console.print(f"[red]Error fetching the main page: {err}[/red]")
        raise
    return response.text, session

def get_professional_cards(filter_voivodeship_id=1, page_size=20, page_number=2, stats_total="count", master_session=requests.Session()):
    global CERTFILE
    """
    Fetches professional cards from the API with controllable query parameters.

    Parameters:
        filter_voivodeship_id (int): The ID of the voivodeship to filter by.
        page_size (int): Number of records per page.
        page_number (int): Which page to retrieve.
        stats_total (str): The type of stats total to include (e.g., "count").

    Returns:
        dict: The JSON response from the API.
    """
    # Base URL for the API endpoint
    url = "https://e-crub.gunb.gov.pl/api/public/professional_cards"
    
    # Define the GET parameters. The keys include square brackets which will be automatically encoded.
    params = {
        "filter[voivodeship_id]": filter_voivodeship_id,
        "page[size]": page_size,
        "page[number]": page_number,
        "stats[total]": stats_total
    }
    
    # Define headers matching the raw request.
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7",
        # "Connection": "keep-alive",
        # "If-None-Match": 'W/"1ffaab6bda437ca328d6cb548c7cf716"',
        "Referer": "https://e-crub.gunb.gov.pl/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/131.0.0.0 Safari/537.36",
        "sec-ch-ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"'
    }
    
    # Define cookies from the raw request.
    cookies = {
        "_clck": "gfkis7|2|fta|0|1866",
        "_ga": "GA1.1.1215205328.1739112774",
        "_clsk": "7adpx9|1739113377407|2|1|r.clarity.ms/collect",
        "_ga_9ZWKM3TKHL": "GS1.1.1739112773.1.1.1739113507.0.0.0",
        "_ga_PCJR826VDS": "GS1.1.1739112773.1.1.1739113507.0.0.0",
        "startquestion-session": '{"expirationDate":1739117636661,"data":{"pageTime":775,"numberOfVisitedPages":1}}'
    }
    
    # Create a session and make the GET request.
    with master_session as session:
        # ensure the session existing cookies override the above predefined cookie set
        cookies.update(session.cookies)
        # wait before making the request
        time.sleep(INTER_REQUEST_DELAY_MILISECONDS / 1000)
        response = session.get(url, params=params, headers=headers, cookies=cookies, verify=CERTFILE)
        # Raise an error for bad responses (e.g. 4xx or 5xx status codes)
        response.raise_for_status()
        # Return the response as JSON
        try:
            gjson = response.json()
            return gjson
        except json.JSONDecodeError as err:
            console.print(f"[red]Error decoding JSON: {err}[/red]")
            console.print(Panel(response.text, title="Response Text"))
            return None
    
def flatten_record(rec):
    """
    Extract fields from one record and return a flat dictionary.
    Adjust the keys and processing as needed.
    """

    # first validate the record, to ensure it's not empty or bogus - if it is missing
    # id or type or decision name we can't proceed and should return None
    if not rec.get('id') or not rec.get('type') or not rec.get('attributes', {}).get('decision', {}).get('names'):
        return None
    
    flattened = {}
    flattened['id'] = rec.get('id', '')
    flattened['type'] = rec.get('type', '')
    
    # Attributes level
    attributes = rec.get('attributes', {})
    flattened['email_address'] = attributes.get('email_address', '')
    flattened['phone_number'] = attributes.get('phone_number', '')
    flattened['postal_address'] = attributes.get('postal_address', '')
    
    # personal_details nested object
    personal = attributes.get('personal_details', {})
    flattened['professional_title'] = personal.get('professional_title', '')
    flattened['academic_degree'] = personal.get('academic_degree', '')
    flattened['primary_voivodeship'] = personal.get('primary_voivodeship', '')
    memberships = personal.get('memberships', [])
    # Join memberships into a single string (you can choose any separator)
    flattened['memberships'] = '; '.join(memberships) if memberships else ''
    
    # decision nested object
    decision = attributes.get('decision', {})
    flattened['decision_names'] = decision.get('names', '')
    flattened['decision_number'] = decision.get('decision_number', '')
    flattened['permission_number'] = decision.get('permission_number', '')
    
    # specialities is an array – here we assume one or more specialties per record.
    # You can decide to either extract only the first one or join multiple.
    specialities = attributes.get('specialities', [])
    if specialities:
        spec_list = []
        for s in specialities:
            # Create a composite string for each speciality. Adjust as needed.
            spec_str = f"speciality: {s.get('speciality', '')}, discipline: {s.get('discipline', '')}, extent: {s.get('extent', '')}"
            spec_list.append(spec_str)
        flattened['specialities'] = " | ".join(spec_list)
    else:
        flattened['specialities'] = ''
    
    # If there is any additional nested data (for example, address details in contact_data), process it similarly.
    # In the sample, contact_data.address is an empty dict.
    # if address in contact_data is not empty, flatten all fields (regardless of names) to a single string, otherwise set it to an empty string
    contact_data = attributes.get('contact_data', {})
    if contact_data.get('address'):
        address = contact_data.get('address')
        address_str = ', '.join([f"{k}: {v}" for k, v in address.items()])
        flattened['contact_data_address'] = address_str
    else:
        flattened['contact_data_address'] = ''

    return flattened

def get_if_already_fetched(voivodeship_code, page_number, file_folder_name):
    """
    Check if the response for the given voivodeship and page number has already been fetched.
    Validate that the file exists and is a parseable JSON.
    """
    filename = f"{file_folder_name}/response_voiv{voivodeship_code}_page{page_number}.json"
    if not os.path.exists(filename):
        return False
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)   # Try to parse the JSON
    except Exception as e:
        console.print(f"[red]Error reading the file {filename}: {e}[/red]")
        return False

def response_storage(jsondata, voivodeship_code, page_number, file_folder_name):
    """
    Store the JSON response to a file.
    """
    # Create a folder if it doesn't exist
    if not os.path.exists(file_folder_name):
        os.makedirs(file_folder_name)
    
    # Define the filename based on the voivodeship and page number
    filename = f"{file_folder_name}/response_voiv{voivodeship_code}_page{page_number}.json"
    
    # Write the JSON data to the file
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(jsondata, f, ensure_ascii=False, indent=4)
    
    console.print(f"[bold]Response saved to {filename}[/bold]")

def get_response_from_file_or_fetch(voivodeship_code, page_number, page_size, stats_total, master_session, file_folder_name):
    """
    Get the response from a file if it has already been fetched, otherwise fetch it.
    """
    response = get_if_already_fetched(voivodeship_code, page_number, file_folder_name)
    if response:
        console.print(f"[bold]Response for voivodeship {voivodeship_code}, page {page_number} already fetched[/bold]")
    else:
        response = get_professional_cards(filter_voivodeship_id=voivodeship_code, page_number=page_number, page_size=page_size, stats_total=stats_total, master_session=master_session)
        if response:
            response_storage(response, voivodeship_code, page_number, file_folder_name)

    # check a sample record to see if it's valid
    if response and response.get('data'):
        sample_record = response['data'][0]
        if not flatten_record(sample_record):
            console.print(f"[red]Invalid record for voivodeship {voivodeship_code}, page {page_number}[/red]")
            raise ValueError("Invalid record")
        
    return response

def main():
    # codes 1 to 16
    voivodeship_codes = range(1, 17)
    page_size = 20
    
    # construct current folder name from current year and week number
    year, week, _ = time.strftime("%Y %U %a").split()
    file_folder_name = f"responses_{year}_week{week}"
    
    console.print("[bold green]Starting crawl...[/bold green]")

    with no_ssl_verification():
        try:
            list_html, session = fetch_initial()
        except Exception:
            return
        
        responses = []
        success = True

        for voivodeship_code in voivodeship_codes:
            console.print(f"[bold]Processing voivodeship code: {voivodeship_code}[/bold]")
            page = 1
            initial_call = get_response_from_file_or_fetch(voivodeship_code =voivodeship_code, page_size=page_size, page_number=page, stats_total="count", master_session=session, file_folder_name=file_folder_name)
            total_count = initial_call["meta"]["stats"]["total"]["count"]
            number_of_pages = total_count // page_size + 1
            responses.append(initial_call)
            if number_of_pages > 1:
                for page in track(range(2, number_of_pages + 1), description=f"Processing voivodeship {voivodeship_code}, {number_of_pages} pages...", console=console):
                    data = get_response_from_file_or_fetch(voivodeship_code =voivodeship_code, page_size=page_size, page_number=page, stats_total="", master_session=session, file_folder_name=file_folder_name)
                    if data is None:
                        console.print(f"[red]Error fetching page {page} for voivodeship code {voivodeship_code}[/red], stopping.")
                        success = False
                        break
                    # Process the data here
                    responses.append(data)

    if not success:
        console.print("[red]Crawl failed. Exiting.[/red]")
        return
    
    # Prepare CSV output.
    # Initially, we set a basic set of fieldnames; these may be updated dynamically.
    output_filename = f"{file_folder_name}/results.csv"
    
    # Collect all flattened records
    all_records = []
    for resp in track(responses, description="Flattening records...", console=console):
        for rec in resp.get('data', []):
            flat = flatten_record(rec)
            if flat:
                all_records.append(flat)
            else:
                console.print(f"[red]Invalid record: {rec}[/red]")
                raise ValueError("Invalid record")

    # Write the flattened data to a CSV file.
    # Excel generally handles CSV files encoded with UTF-8 with a BOM.
    if all_records:
        fieldnames = list(all_records[0].keys())
        with open(output_filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
            # write the separator information as sep=; to ensure Excel opens the file correctly
            sep = ";"
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, restval="---", quoting=csv.QUOTE_ALL, delimiter=sep)
            writer.writeheader()
            writer.writerows(all_records)
            
    console.print(f"[bold green]Crawl completed. Results saved to {output_filename}[/bold green]")

if __name__ == "__main__":
    main()

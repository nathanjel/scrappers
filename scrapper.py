import requests
from bs4 import BeautifulSoup
import csv
import json
import certifi
from rich.console import Console
from rich.progress import track

# Base URL of the site
BASE_URL = "https://e-crub.gunb.gov.pl"

console = Console()
# certificate
certdata = certifi.where()
certdata = False

# log certificate data
console.print(f"Using certificate: {certdata}")

# example response

# {
#     "data": [
#         {
#             "id": "833",
#             "type": "professional_cards",
#             "attributes": {
#                 "email_address": null,
#                 "phone_number": null,
#                 "postal_address": null,
#                 "personal_details": {
#                     "professional_title": "inżynier",
#                     "academic_degree": "brak",
#                     "primary_voivodeship": "Dolnośląskie",
#                     "memberships": []
#                 },
#                 "decision": {
#                     "names": "Władysław Henryk Alejski",
#                     "decision_number": "25/96/Lw",
#                     "permission_number": null
#                 },
#                 "contact_data": {
#                     "address": {}
#                 },
#                 "specialities": [
#                     {
#                         "speciality": "instalacyjna w zakresie sieci, instalacji i urządzeń elektrycznych i elektroenergetycznych",
#                         "discipline": "projektowanie i kierowanie robotami budowlanymi",
#                         "extent": "bez ograniczeń"
#                     }
#                 ]
#             }
#         },
#         {
#             "id": "834",
#             "type": "professional_cards",
#             "attributes": {
#                 "email_address": null,
#                 "phone_number": null,
#                 "postal_address": null,
#                 "personal_details": {
#                     "professional_title": "inżynier",
#                     "academic_degree": "brak",
#                     "primary_voivodeship": "Dolnośląskie",
#                     "memberships": []
#                 },
#                 "decision": {
#                     "names": "Ryszard Artur Biernacki",
#                     "decision_number": "26/96/Lw",
#                     "permission_number": null
#                 },
#                 "contact_data": {
#                     "address": {}
#                 },
#                 "specialities": [
#                     {
#                         "speciality": "instalacyjna w zakresie sieci, instalacji i urządzeń elektrycznych i elektroenergetycznych",
#                         "discipline": "projektowanie i kierowanie robotami budowlanymi",
#                         "extent": "bez ograniczeń"
#                     }
#                 ]
#             }
#         },
#         {
#             "id": "835",
#             "type": "professional_cards",
#             "attributes": {
#                 "email_address": null,
#                 "phone_number": null,
#                 "postal_address": null,
#                 "personal_details": {
#                     "professional_title": "technik",
#                     "academic_degree": "brak",
#                     "primary_voivodeship": "Dolnośląskie",
#                     "memberships": []
#                 },
#                 "decision": {
#                     "names": "Kazimierz Antoni Chomicz",
#                     "decision_number": "27/96/Lw",
#                     "permission_number": null
#                 },
#                 "contact_data": {
#                     "address": {}
#                 },
#                 "specialities": [
#                     {
#                         "speciality": "instalacyjna w zakresie sieci, instalacji i urządzeń elektrycznych i elektroenergetycznych",
#                         "discipline": "kierowanie robotami budowlanymi",
#                         "extent": "ograniczone"
#                     }
#                 ]
#             }
#         },
#         {
#             "id": "836",
#             "type": "professional_cards",
#             "attributes": {
#                 "email_address": null,
#                 "phone_number": null,
#                 "postal_address": null,
#                 "personal_details": {
#                     "professional_title": "inżynier",
#                     "academic_degree": "brak",
#                     "primary_voivodeship": "Dolnośląskie",
#                     "memberships": []
#                 },
#                 "decision": {
#                     "names": "Jan Szynal",
#                     "decision_number": "30/96/Lw",
#                     "permission_number": null
#                 },
#                 "contact_data": {
#                     "address": {}
#                 },
#                 "specialities": [
#                     {
#                         "speciality": "instalacyjna w zakresie sieci, instalacji i urządzeń elektrycznych i elektroenergetycznych",
#                         "discipline": "projektowanie i kierowanie robotami budowlanymi",
#                         "extent": "bez ograniczeń"
#                     }
#                 ]
#             }
#         },
#         {
#             "id": "837",
#             "type": "professional_cards",
#             "attributes": {
#                 "email_address": null,
#                 "phone_number": null,
#                 "postal_address": null,
#                 "personal_details": {
#                     "professional_title": "magister inżynier",
#                     "academic_degree": "brak",
#                     "primary_voivodeship": "Dolnośląskie",
#                     "memberships": [
#                         "Dolnośląska Okręgowa Izba Inżynierów Budownictwa"
#                     ]
#                 },
#                 "decision": {
#                     "names": "Henryk Żmurko",
#                     "decision_number": "31/96/Lw",
#                     "permission_number": null
#                 },
#                 "contact_data": {
#                     "address": {}
#                 },
#                 "specialities": [
#                     {
#                         "speciality": "instalacyjna w zakresie sieci, instalacji i urządzeń elektrycznych i elektroenergetycznych",
#                         "discipline": "kierowanie robotami budowlanymi",
#                         "extent": "bez ograniczeń"
#                     }
#                 ]
#             }
#         },
#         {
#             "id": "921",
#             "type": "professional_cards",
#             "attributes": {
#                 "email_address": null,
#                 "phone_number": null,
#                 "postal_address": null,
#                 "personal_details": {
#                     "professional_title": "magister inżynier",
#                     "academic_degree": "brak",
#                     "primary_voivodeship": "Dolnośląskie",
#                     "memberships": [
#                         "Dolnośląska Okręgowa Izba Inżynierów Budownictwa"
#                     ]
#                 },
#                 "decision": {
#                     "names": "Grażyna Danuta Kasendra",
#                     "decision_number": "1/96",
#                     "permission_number": null
#                 },
#                 "contact_data": {
#                     "address": {}
#                 },
#                 "specialities": [
#                     {
#                         "speciality": "instalacyjna w zakresie sieci, instalacji i urządzeń wodociągowych i kanalizacyjnych, cieplnych, wentylacyjnych i gazowych",
#                         "discipline": "projektowanie",
#                         "extent": "bez ograniczeń"
#                     }
#                 ]
#             }
#         },
#         {
#             "id": "922",
#             "type": "professional_cards",
#             "attributes": {
#                 "email_address": null,
#                 "phone_number": null,
#                 "postal_address": null,
#                 "personal_details": {
#                     "professional_title": "inżynier",
#                     "academic_degree": "brak",
#                     "primary_voivodeship": "Dolnośląskie",
#                     "memberships": []
#                 },
#                 "decision": {
#                     "names": "Anna Bożena Matyja Gazda",
#                     "decision_number": "2/96",
#                     "permission_number": null
#                 },
#                 "contact_data": {
#                     "address": {}
#                 },
#                 "specialities": [
#                     {
#                         "speciality": "instalacyjna w zakresie sieci, instalacji i urządzeń wodociągowych i kanalizacyjnych, cieplnych, wentylacyjnych i gazowych",
#                         "discipline": "projektowanie",
#                         "extent": "ograniczone"
#                     }
#                 ]
#             }
#         },
#         {
#             "id": "923",
#             "type": "professional_cards",
#             "attributes": {
#                 "email_address": null,
#                 "phone_number": null,
#                 "postal_address": null,
#                 "personal_details": {
#                     "professional_title": "magister inżynier architekt",
#                     "academic_degree": "brak",
#                     "primary_voivodeship": "Dolnośląskie",
#                     "memberships": [
#                         "Dolnośląska Okręgowa Izba Architektów RP"
#                     ]
#                 },
#                 "decision": {
#                     "names": "Jacek Tomasz Świtoń",
#                     "decision_number": "3/96",
#                     "permission_number": null
#                 },
#                 "contact_data": {
#                     "address": {}
#                 },
#                 "specialities": [
#                     {
#                         "speciality": "architektoniczna",
#                         "discipline": "projektowanie",
#                         "extent": "bez ograniczeń"
#                     }
#                 ]
#             }
#         },
#         {
#             "id": "925",
#             "type": "professional_cards",
#             "attributes": {
#                 "email_address": null,
#                 "phone_number": null,
#                 "postal_address": null,
#                 "personal_details": {
#                     "professional_title": "technik",
#                     "academic_degree": "brak",
#                     "primary_voivodeship": "Dolnośląskie",
#                     "memberships": []
#                 },
#                 "decision": {
#                     "names": "Józef Franciszek Ślączka",
#                     "decision_number": "5/96",
#                     "permission_number": null
#                 },
#                 "contact_data": {
#                     "address": {}
#                 },
#                 "specialities": [
#                     {
#                         "speciality": "instalacyjna w zakresie sieci, instalacji i urządzeń elektrycznych i elektroenergetycznych",
#                         "discipline": "kierowanie robotami budowlanymi",
#                         "extent": "ograniczone"
#                     }
#                 ]
#             }
#         },
#         {
#             "id": "926",
#             "type": "professional_cards",
#             "attributes": {
#                 "email_address": null,
#                 "phone_number": null,
#                 "postal_address": null,
#                 "personal_details": {
#                     "professional_title": "technik",
#                     "academic_degree": "brak",
#                     "primary_voivodeship": "Dolnośląskie",
#                     "memberships": [
#                         "Dolnośląska Okręgowa Izba Inżynierów Budownictwa"
#                     ]
#                 },
#                 "decision": {
#                     "names": "Krzysztof Zbigniew Wajda",
#                     "decision_number": "6/96",
#                     "permission_number": null
#                 },
#                 "contact_data": {
#                     "address": {}
#                 },
#                 "specialities": [
#                     {
#                         "speciality": "instalacyjna w zakresie sieci, instalacji i urządzeń elektrycznych i elektroenergetycznych",
#                         "discipline": "kierowanie robotami budowlanymi",
#                         "extent": "ograniczone"
#                     }
#                 ]
#             }
#         },
#         {
#             "id": "927",
#             "type": "professional_cards",
#             "attributes": {
#                 "email_address": null,
#                 "phone_number": null,
#                 "postal_address": null,
#                 "personal_details": {
#                     "professional_title": "magister inżynier",
#                     "academic_degree": "brak",
#                     "primary_voivodeship": "Dolnośląskie",
#                     "memberships": [
#                         "Dolnośląska Okręgowa Izba Inżynierów Budownictwa"
#                     ]
#                 },
#                 "decision": {
#                     "names": "Arkadiusz Hurko",
#                     "decision_number": "7/96",
#                     "permission_number": null
#                 },
#                 "contact_data": {
#                     "address": {}
#                 },
#                 "specialities": [
#                     {
#                         "speciality": "instalacyjna w zakresie sieci, instalacji i urządzeń wodociągowych i kanalizacyjnych, cieplnych, wentylacyjnych i gazowych",
#                         "discipline": "kierowanie robotami budowlanymi",
#                         "extent": "bez ograniczeń"
#                     }
#                 ]
#             }
#         },
#         {
#             "id": "928",
#             "type": "professional_cards",
#             "attributes": {
#                 "email_address": null,
#                 "phone_number": null,
#                 "postal_address": null,
#                 "personal_details": {
#                     "professional_title": "magister inżynier",
#                     "academic_degree": "brak",
#                     "primary_voivodeship": "Dolnośląskie",
#                     "memberships": []
#                 },
#                 "decision": {
#                     "names": "Adam Roman Jaskuła",
#                     "decision_number": "8/96",
#                     "permission_number": null
#                 },
#                 "contact_data": {
#                     "address": {}
#                 },
#                 "specialities": [
#                     {
#                         "speciality": "instalacyjna w zakresie sieci, instalacji i urządzeń wodociągowych i kanalizacyjnych, cieplnych, wentylacyjnych i gazowych",
#                         "discipline": "kierowanie robotami budowlanymi",
#                         "extent": "bez ograniczeń"
#                     }
#                 ]
#             }
#         },
#         {
#             "id": "929",
#             "type": "professional_cards",
#             "attributes": {
#                 "email_address": null,
#                 "phone_number": null,
#                 "postal_address": null,
#                 "personal_details": {
#                     "professional_title": "magister inżynier",
#                     "academic_degree": "brak",
#                     "primary_voivodeship": "Dolnośląskie",
#                     "memberships": [
#                         "Dolnośląska Okręgowa Izba Inżynierów Budownictwa"
#                     ]
#                 },
#                 "decision": {
#                     "names": "Wojciech Narcyz Tarka",
#                     "decision_number": "9/96",
#                     "permission_number": null
#                 },
#                 "contact_data": {
#                     "address": {}
#                 },
#                 "specialities": [
#                     {
#                         "speciality": "instalacyjna w zakresie sieci, instalacji i urządzeń wodociągowych i kanalizacyjnych, cieplnych, wentylacyjnych i gazowych",
#                         "discipline": "kierowanie robotami budowlanymi",
#                         "extent": "bez ograniczeń"
#                     }
#                 ]
#             }
#         },
#         {
#             "id": "930",
#             "type": "professional_cards",
#             "attributes": {
#                 "email_address": null,
#                 "phone_number": null,
#                 "postal_address": null,
#                 "personal_details": {
#                     "professional_title": "magister inżynier",
#                     "academic_degree": "brak",
#                     "primary_voivodeship": "Dolnośląskie",
#                     "memberships": [
#                         "Dolnośląska Okręgowa Izba Inżynierów Budownictwa"
#                     ]
#                 },
#                 "decision": {
#                     "names": "Adam Piotr Gierczak",
#                     "decision_number": "11/96",
#                     "permission_number": null
#                 },
#                 "contact_data": {
#                     "address": {}
#                 },
#                 "specialities": [
#                     {
#                         "speciality": "konstrukcyjno-budowlana",
#                         "discipline": "kierowanie robotami budowlanymi",
#                         "extent": "bez ograniczeń"
#                     }
#                 ]
#             }
#         },
#         {
#             "id": "931",
#             "type": "professional_cards",
#             "attributes": {
#                 "email_address": null,
#                 "phone_number": null,
#                 "postal_address": null,
#                 "personal_details": {
#                     "professional_title": "magister inżynier",
#                     "academic_degree": "brak",
#                     "primary_voivodeship": "Dolnośląskie",
#                     "memberships": [
#                         "Dolnośląska Okręgowa Izba Inżynierów Budownictwa"
#                     ]
#                 },
#                 "decision": {
#                     "names": "Adam Piotr Gierczak",
#                     "decision_number": "189/98/UW",
#                     "permission_number": null
#                 },
#                 "contact_data": {
#                     "address": {}
#                 },
#                 "specialities": [
#                     {
#                         "speciality": "konstrukcyjno-budowlana",
#                         "discipline": "projektowanie",
#                         "extent": "bez ograniczeń"
#                     }
#                 ]
#             }
#         },
#         {
#             "id": "932",
#             "type": "professional_cards",
#             "attributes": {
#                 "email_address": null,
#                 "phone_number": null,
#                 "postal_address": null,
#                 "personal_details": {
#                     "professional_title": "magister inżynier",
#                     "academic_degree": "brak",
#                     "primary_voivodeship": "Dolnośląskie",
#                     "memberships": [
#                         "Dolnośląska Okręgowa Izba Inżynierów Budownictwa"
#                     ]
#                 },
#                 "decision": {
#                     "names": "Adam Piotr Gierczak",
#                     "decision_number": "191/00/DUW",
#                     "permission_number": null
#                 },
#                 "contact_data": {
#                     "address": {}
#                 },
#                 "specialities": [
#                     {
#                         "speciality": "architektoniczna",
#                         "discipline": "projektowanie",
#                         "extent": "ograniczone"
#                     }
#                 ]
#             }
#         },
#         {
#             "id": "934",
#             "type": "professional_cards",
#             "attributes": {
#                 "email_address": null,
#                 "phone_number": null,
#                 "postal_address": null,
#                 "personal_details": {
#                     "professional_title": "inżynier",
#                     "academic_degree": "brak",
#                     "primary_voivodeship": "Dolnośląskie",
#                     "memberships": []
#                 },
#                 "decision": {
#                     "names": "Aleksander Wyderkowski",
#                     "decision_number": "114/00/DUW",
#                     "permission_number": null
#                 },
#                 "contact_data": {
#                     "address": {}
#                 },
#                 "specialities": [
#                     {
#                         "speciality": "instalacyjna w zakresie sieci, instalacji i urządzeń elektrycznych i elektroenergetycznych",
#                         "discipline": "projektowanie i kierowanie robotami budowlanymi",
#                         "extent": "bez ograniczeń"
#                     }
#                 ]
#             }
#         },
#         {
#             "id": "960",
#             "type": "professional_cards",
#             "attributes": {
#                 "email_address": null,
#                 "phone_number": null,
#                 "postal_address": null,
#                 "personal_details": {
#                     "professional_title": "technik",
#                     "academic_degree": "brak",
#                     "primary_voivodeship": "Dolnośląskie",
#                     "memberships": [
#                         "Dolnośląska Okręgowa Izba Inżynierów Budownictwa"
#                     ]
#                 },
#                 "decision": {
#                     "names": "Bolesław Michaluk",
#                     "decision_number": "6/96",
#                     "permission_number": null
#                 },
#                 "contact_data": {
#                     "address": {}
#                 },
#                 "specialities": [
#                     {
#                         "speciality": "instalacyjna w zakresie sieci, instalacji i urządzeń wodociągowych i kanalizacyjnych, cieplnych, wentylacyjnych i gazowych",
#                         "discipline": "kierowanie robotami budowlanymi",
#                         "extent": "ograniczone"
#                     }
#                 ]
#             }
#         },
#         {
#             "id": "961",
#             "type": "professional_cards",
#             "attributes": {
#                 "email_address": null,
#                 "phone_number": null,
#                 "postal_address": null,
#                 "personal_details": {
#                     "professional_title": "magister inżynier",
#                     "academic_degree": "brak",
#                     "primary_voivodeship": "Dolnośląskie",
#                     "memberships": [
#                         "Dolnośląska Okręgowa Izba Inżynierów Budownictwa"
#                     ]
#                 },
#                 "decision": {
#                     "names": "Dariusz Sidorczyk",
#                     "decision_number": "5/96",
#                     "permission_number": null
#                 },
#                 "contact_data": {
#                     "address": {}
#                 },
#                 "specialities": [
#                     {
#                         "speciality": "instalacyjna w zakresie sieci, instalacji i urządzeń wodociągowych i kanalizacyjnych, cieplnych, wentylacyjnych i gazowych",
#                         "discipline": "kierowanie robotami budowlanymi",
#                         "extent": "bez ograniczeń"
#                     }
#                 ]
#             }
#         },
#         {
#             "id": "962",
#             "type": "professional_cards",
#             "attributes": {
#                 "email_address": null,
#                 "phone_number": null,
#                 "postal_address": null,
#                 "personal_details": {
#                     "professional_title": "technik",
#                     "academic_degree": "brak",
#                     "primary_voivodeship": "Dolnośląskie",
#                     "memberships": [
#                         "Dolnośląska Okręgowa Izba Inżynierów Budownictwa"
#                     ]
#                 },
#                 "decision": {
#                     "names": "Bogusław Gil",
#                     "decision_number": "3/96",
#                     "permission_number": null
#                 },
#                 "contact_data": {
#                     "address": {}
#                 },
#                 "specialities": [
#                     {
#                         "speciality": "konstrukcyjno-budowlana",
#                         "discipline": "kierowanie robotami budowlanymi",
#                         "extent": "ograniczone"
#                     }
#                 ]
#             }
#         }
#     ],
#     "meta": {
#         "stats": {
#             "total": {
#                 "count": 12268
#             }
#         }
#     }
# }

def fetch_initial():
    """
    Sends a request simulating the form submission with the given voivodeship.
    
    Adjust the URL endpoint and payload parameters as needed.
    """
    # Replace '/search' with the correct endpoint for the form
    search_url = f"{BASE_URL}"
    
    session = requests.Session()
    try:
        # Depending on the form, you might need GET or POST
        response = session.get(search_url, timeout=10, verify=certdata)
        response.raise_for_status()
    except requests.RequestException as err:
        console.print(f"[red]Error fetching the main page: {err}[/red]")
        raise
    return response.text, session

def get_professional_cards(filter_voivodeship_id=1, page_size=20, page_number=2, stats_total="count", master_session=requests.Session()):
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
        "Connection": "keep-alive",
        "If-None-Match": 'W/"1ffaab6bda437ca328d6cb548c7cf716"',
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
        response = session.get(url, params=params, headers=headers, cookies=cookies, verify=certdata)
        # Raise an error for bad responses (e.g. 4xx or 5xx status codes)
        response.raise_for_status()
        # Return the response as JSON
        return response.json()
    
def flatten_record(rec):
    """
    Extract fields from one record and return a flat dictionary.
    Adjust the keys and processing as needed.
    """
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
    return flattened

def main():
    # codes 1 to 16
    voivodeship_codes = range(1, 17)
    page_size = 20

    console.print("[bold green]Starting crawl...[/bold green]")
    
    try:
        list_html, session = fetch_initial()
    except Exception:
        return
    
    responses = []

    for voivodeship_code in voivodeship_codes:
        console.print(f"[bold]Processing voivodeship code: {voivodeship_code}[/bold]")
        page = 1
        initial_call = get_professional_cards(filter_voivodeship_id=voivodeship_code, page_size=page_size, page_number=page, stats_total="count", master_session=session)
        total_count = initial_call["meta"]["stats"]["total"]["count"]
        number_of_pages = total_count // page_size + 1
        responses.append(initial_call)
        if number_of_pages > 1:
            for page in track(range(2, number_of_pages + 1), description="Processing pages..."):
                data = get_professional_cards(filter_voivodeship_id=voivodeship_code, page_size=page_size, page_number=page, stats_total="count", master_session=session)
                if data is None:
                    continue
                # Process the data here
                responses.append(data)

    # Prepare CSV output.
    # Initially, we set a basic set of fieldnames; these may be updated dynamically.
    output_filename = "results.csv"
    
    # Collect all flattened records
    all_records = []
    for resp in responses:
        for rec in resp.get('data', []):
            flat = flatten_record(rec)
            all_records.append(flat)

    # Write the flattened data to a CSV file.
    # Excel generally handles CSV files encoded with UTF-8 with a BOM.
    if all_records:
        fieldnames = list(all_records[0].keys())
        with open(output_filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(all_records)
            
    console.print(f"[bold green]Crawl completed. Results saved to {output_filename}[/bold green]")

if __name__ == "__main__":
    main()

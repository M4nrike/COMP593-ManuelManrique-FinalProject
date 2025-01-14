'''
Library for interacting with NASA's Astronomy Picture of the Day API.
'''
import requests
import hashlib
import re
import os

NASA_API_URL = 'https://api.nasa.gov/planetary/apod/'
#https://apod.nasa.gov/apod/image/2408/perseid_iss_4256.jpg
#https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY

script_dir = os.path.dirname(os.path.abspath(__file__))
image_cache_dir = os.path.join(script_dir, 'images')

parameters = {
      "api_key": "3L2Opq58DSqlyMQcb1Q9yoFh8vILAbXFehb0pqnK"
}

apod_info_dict = {
    "Title", 
    "copyright",
    "explanation",
    "date",
    "path",
    "imagehash",
    "media_type"
}       

def main():
    # TODO: Add code to test the functions in this module
    nasa_info = get_apod_info('2024-05-18')
    #v_title="  El cosmos, #G32, -127 +Universo "
    #v_titleClean =cleanTitle(v_title)   
    #print(f"Quedo: {v_titleClean}")
    get_apod_image_url(apod_info_dict)
    return

def cleanTitle(v_title):
    # {REQ-18, part 1}
    v_aux=v_title.strip()           # Leading and trailing spaces are removed
    v_aux2=v_aux.replace(' ', '_')  # Inner spaces are replaced by '_'
    # Use a regular expression, obtein lettters, numbers and '_'
    v_titleaux = re.findall(r'[a-zA-Z_0-9]+', v_aux2)   
    v_Title=""
    for titles in v_titleaux:
        v_Title += titles

    print (f"v_aux:{v_aux}  v_aux2:{v_aux2} v_titleaux: {v_titleaux} v_Title:{v_Title}")
    return(v_Title)
    

def get_apod_info(apod_date):
    """Gets information from the NASA API for the Astronomy 
    Picture of the Day (APOD) from a specified date.

    Args:
        apod_date (date): APOD date (Can also be a string formatted as YYYY-MM-DD)

    Returns:
        dict: Dictionary of APOD info, if successful. None if unsuccessful
    """
    # TODO: Complete the function body
    # Hint: The APOD API uses query string parameters: https://requests.readthedocs.io/en/latest/user/quickstart/#passing-parameters-in-urls
    # Hint: Set the 'thumbs' parameter to True so the info returned for video APODs will include URL of the video thumbnail image 
    return


def get_apod_image_url(apod_info_dict):
    """Gets the URL of the APOD image from the dictionary of APOD information.

    If the APOD is an image, gets the URL of the high definition image.
    If the APOD is a video, gets the URL of the video thumbnail.

    Args:
        apod_info_dict (dict): Dictionary of APOD info from API

    Returns:
        str: APOD image URL
    """
    # TODO: Complete the function body
    # Hint: The APOD info dictionary includes a key named 'media_type' that indicates whether the APOD is an image or video
    v_date="2023-10-27"
    #url = NASA_API_URL + v_date
    url = NASA_API_URL 
    resp_msg = requests.get(url, params=parameters)
    # print (resp_msg.url)
    #Check if request was successful
    if resp_msg.status_code == requests.codes.ok:
           results = resp_msg.json()
           print(f"Getting {results['date']} APOD information from NASA ... success")
           print(f"APOD title: {results['title']}")
           print(f"APOD URL: {results['url']}")
           tit_aux =cleanTitle(results['title'])
           url2 = results["url"]
           # Check if is an image
           print(results["media_type"])
           file_content = resp_msg.content
           if results["media_type"] == "image":
               titaux= tit_aux + ".jpg"
               rutacache= image_cache_dir + "\\" + titaux
               print (f"rutaCache= {rutacache}")
               print (f"title:{titaux}")
               print (f"Downloading from image from \n {url2} ...success")
               image_hash = hashlib.sha256(file_content).hexdigest()
               print(f"APOD SHA-256: {image_hash}")
               with open(rutacache, "wb") as f:
                   f.write(requests.get(url2).content)
           else:
               # Extract binay content from response message body
               file_content = resp_msg.content
               image_hash = hashlib.sha256(file_content).hexdigest()
               print("SE TIENE EL HAS256 DEL VIDEO") 
               print(f"APOD SHA-256: {image_hash}")
               print (url2)
    else:
        print("File not retreived")
        
    return (results)

if __name__ == '__main__':
    main()
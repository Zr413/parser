# Import the required modules
import requests
import bs4
import argparse
import sys

# Define a function to parse the HTML content and display it without tags
def parse_html(html):
    # Create a BeautifulSoup object to parse the HTML content
    soup = bs4.BeautifulSoup(html, "html.parser")
    # Get the text of the HTML content without tags
    text = soup.get_text(strip=True)
    # Return the text
    return text

# Define a function to parse the js content and display it without tags
def parse_js(html):
    # Create a BeautifulSoup object to parse the HTML content
    soup = bs4.BeautifulSoup(html, "html.parser")
    # Find all the script elements that contain js code
    scripts = soup.find_all("script", type="text/javascript")
    # Create an empty list to store the js texts
    js_texts = []
    # Loop through each script element
    for script in scripts:
        # Get the text of the script element without tags
        text = script.get_text(strip=True)
        # Add the text to the js texts list
        js_texts.append(text)
    # Return the js texts list
    return js_texts

# Define a function to find the tags that allow to make a GET request and display them with their attributes
def find_get_tags(html):
    # Create a BeautifulSoup object to parse the HTML content
    soup = bs4.BeautifulSoup(html, "html.parser")
    # Find all the a and form elements that have a href or action attribute with a GET method
    elements = soup.find_all(lambda tag: (tag.name == "a" and tag.has_attr("href")) or (tag.name == "form" and tag.has_attr("action") and tag.get("method").lower() == "get"))
    # Create an empty list to store the tags
    get_tags = []
    # Loop through each element
    for element in elements:
        # Get the tag name and attributes of the element as a string
        tag = str(element)
        # Add the tag to the get tags list
        get_tags.append(tag)
    # Return the get tags list
    return get_tags

# Define a function to find the tags that allow to make a POST request and display them with their attributes
def find_post_tags(html):
    # Create a BeautifulSoup object to parse the HTML content
    soup = bs4.BeautifulSoup(html, "html.parser")
    # Find all the form elements that have an action attribute with a POST method
    elements = soup.find_all("form", action=True, method=lambda m: m.lower() == "post")
    # Create an empty list to store the tags
    post_tags = []
    # Loop through each element
    for element in elements:
        # Get the tag name and attributes of the element as a string
        tag = str(element)
        # Add the tag to the post tags list
        post_tags.append(tag)
    # Return the post tags list
    return post_tags

# Define a function to search for text or tags on the HTML pages of the web site and display them without tags
def search_info(html, info):
    # Create a BeautifulSoup object to parse the HTML content
    soup = bs4.BeautifulSoup(html, "html.parser")

    # Check if info starts with < and ends with >, indicating that it is a tag name
    if info.startswith("<") and info.endswith(">"):
        # Remove the < and > from info
        info = info[1:-1]
        # Find all the elements that match the tag name
        elements = soup.find_all(info)
    else:
        # Find all the elements that contain the information to search
        # Use 'string' instead of 'text'
        elements = soup.find_all(string=lambda t: info.lower() in t.lower())

    # Create an empty list to store the texts or tags
    texts_or_tags = []
    
    # Loop through each element
    for element in elements:
        # Get the text of the element without tags or keep it as a tag if it is a tag name search 
        if info.startswith("<") and info.endswith(">"):
            text_or_tag = str(element)
        else:
            text_or_tag = element.get_text(strip=True)
        # Add the text or tag to the texts or tags list 
        texts_or_tags.append(text_or_tag)

    # Return the texts or tags list 
    return texts_or_tags

# Define a function to save a list of items to a file 
def save_to_file(items, file_name):
    with open(file_name, "w") as file:
        # Write each item in the list to a new line in the file 
        for item in items:
            file.write(item + "\n")

# Define a function to display a list of items 
def display_items(items):
    # Loop through each item in the list 
    for item in items:
        # Print the item 
        print(item)

# Define the command-line arguments
parser = argparse.ArgumentParser(description="A web site parser that can search for information and analyze HTML or js text")
parser.add_argument("-u", "--url", help="The web site URL to parse", required=True)
parser.add_argument("-html", "--html", help="Parse the HTML content of the web site", action="store_true")
parser.add_argument("-js", "--js", help="Parse the js content of the web site", action="store_true")
parser.add_argument("-get", "--get", help="Find the tags that allow to make a GET request on the web site", action="store_true")
parser.add_argument("-post", "--post", help="Find the tags that allow to make a POST request on the web site", action="store_true")
parser.add_argument("-t", "--text", help="Search for text or tags on the HTML pages of the web site")

# Parse the command-line arguments
args = parser.parse_args()

# Check if at least one of -html, -js, -get, -post, or -t is specified
if not (args.html or args.js or args.get or args.post or args.text):
    # Raise an exception and display the help message
    parser.error("You must specify at least one of -html, -js, -get, -post, or -t")

# Get the web site URL from the arguments
web_site = args.url

# Send a GET request to the web site and get the HTML content
response = requests.get(web_site)
html = response.text

# Create an empty list to store the output
output = []

# If -html is specified, call the parse_html function and display the result
if args.html:
    # Call the parse_html function and get the result
    html_text = parse_html(html)
    # Add the result to the output list
    output.append(html_text)
    # Display a message indicating that the HTML content is parsed
    print("The HTML content of the web site is parsed and displayed without tags")

# If -js is specified, call the parse_js function and display the result
if args.js:
    # Call the parse_js function and get the result
    js_texts = parse_js(html)
    # Add the result to the output list
    output.extend(js_texts)
    # Display a message indicating that the js content is parsed
    print("The js content of the web site is parsed and displayed without tags")

# If -get is specified, call the find_get_tags function and display the result
if args.get:
    # Call the find_get_tags function and get the result
    get_tags = find_get_tags(html)
    # Add the result to the output list
    output.extend(get_tags)
    # Display a message indicating that GET tags are found
    print("The tags that allow to make a GET request on the web site are found and displayed with their attributes")

# If -post is specified, call the find_post_tags function and display the result
if args.post:
    # Call the find_post_tags function and get the result
    post_tags = find_post_tags(html)
    # Add the result to the output list
    output.extend(post_tags)
    # Display a message indicating that POST tags are found
    print("The tags that allow to make a POST request on the web site are found and displayed with their attributes")

# If -t is specified, call the search_info function and display the result
if args.text:
    # Get the information to search from the argument
    info = args.text

    # Call the search_info function and get the result 
    texts_or_tags = search_info(html, info)

    # Add the result to the output list 
    output.extend(texts_or_tags)

    # Display a message indicating that information is found 
    print(f"The information {info} is found on HTML pages of web site and displayed without tags")

# Save the output to a file
file_name = "output.txt"
save_to_file(output, file_name)

# Print a message indicating that output is saved to a file 
print(f"The output is saved to {file_name}")

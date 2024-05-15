import json
import re

def clean_addresses(key, addresses):
    rawaddresses = []
    for address in addresses:
        rawaddress = re.sub('[\W_]+', '', address) #Remvoing all non alphanumeric characters
        rawaddresses.append(rawaddress.lower())
        #print(rawaddress,":", address)

    result = rawaddresses.copy()
    # Iterate through the list of strings.
    for s1 in rawaddresses:
        for s2 in rawaddresses:
            #print(s1,":", s2)
            # Skip comparing a string with itself.
            if s1 == s2:
                continue

            # Check if s1 is a substring of s2.
            if s1 in s2 and s1 in result:
                del addresses[result.index(s1)]
                # If s1 is a substring of s2 and is still in the result list, remove it.
                result.remove(s1)
    
    if len(addresses) == 2:
        strippedAddressList =[]
        for address in addresses:
            strippedAddress = re.sub('[\W_]+', '', address) #Remvoing all non alphanumeric characters
            strippedAddressList.append(strippedAddress.lower())

        if strippedAddressList[0] in strippedAddressList[1]:
            del addresses[0]
        elif strippedAddressList[1] in strippedAddressList[0]:
            del addresses[1]


    return addresses

def contains_special_characters(address):
    # Define a regular expression pattern that matches any character
    # other than alphabets, numbers, commas, apostrophes, and spaces.
    pattern = r'[^a-zA-Z0-9, \' ]'
    
    # Use re.search to find any match of the pattern in the string.
    return bool(re.search(pattern, address))

def filter_addresses(addressList):
    # Use a list comprehension to filter out strings that contain special characters.
    filtered_strings = [s for s in addressList if not contains_special_characters(s)]
    return filtered_strings

def extrating_postcodes_with_100_characters(json_file,company_number,column_name):

    extractedPostcodes =[]

    # Load the JSON data from the file
    with open(json_file, 'r') as file:
        data = json.load(file)

    # Define the regex pattern
    pattern = r'\b([A-Z][A-HJ-Y]?[0-9][A-Z0-9]? ?[0-9][A-Z]{2}|GIR ?0A{2})\b'

    # Create a dictionary to store 100 characters containing the postcode
    characters_with_postcode = {}

    #  Iterate through the data and scan the specified column for matches
    for item in data:
        if column_name or company_number in item:
            websiteTxt = item[column_name]
            companyNumber = item[company_number]
        
            # Find all matching postcodes in the text
            extractedPostcodes = re.findall(pattern, websiteTxt)

            # Find the unique postcodes
            # uniquePostcodes = list(set(extractedPostcodes))
            # companyNumberPostcodesDict[companyNumber] = uniquePostcodes

            # Iterate through the extracted postcodes
            for postcode in extractedPostcodes:
                # Find the index of each occurrence of the postcode
                for match in re.finditer(postcode, websiteTxt):
                    # Get the starting and ending index of the 100-character snippet
                    start_index = max(0, match.start() - 100)
                    end_index = match.end()
                
                    # Extract the 100 characters containing the postcode
                    snippet = websiteTxt[start_index:end_index]
                
                    # Store the snippet in the characters_with_postcode dictionary
                    if postcode not in characters_with_postcode:
                        characters_with_postcode[postcode] = []
                    characters_with_postcode[postcode].append(snippet)

    # Save to dictonary
    postcodeAddressDict = {postcode: snippets for postcode, snippets in characters_with_postcode.items()}
    # for key, value in postcodeAddressDict.items():
    #     print(f'{key}: {value}')

    return postcodeAddressDict

def main():
    json_file = 'data/database.json'

    # Specify the name of the column containing the data
    column_name = 'COLUMN_NAME'
    company_number = 'company_number'

    postcode_100_character_dict = extrating_postcodes_with_100_characters(json_file,company_number,column_name)

    final = {}
    addressList = []
    tempList = []
    for key, value in postcode_100_character_dict.items():
        addressList.clear()
        tempList.clear()
        #list_1 = postcode_100_character_dict[key]
        for content in value:
            # print(content)
            extractedAddress = ''
            splitcontent = content.split()
            # print(splitcontent)
            for words in reversed(splitcontent):
                if words[0].isupper() or words[0].isdigit():
                    extractedAddress = words +" "+ extractedAddress
                else: 
                    # print(key,':',extractedAddress)
                
                    strippedAddress = re.sub('[\W_]+', '', extractedAddress) #Remvoing all non alphanumeric characters

                    if strippedAddress not in tempList:
                        tempList.append(strippedAddress)
                        unicodedAddress = bytes(extractedAddress, 'utf-8').decode('unicode_escape') #applying unicodes
                        addressList.append(unicodedAddress.rstrip()) #Removing all space
                    break
        #print(addressList)

        filteredaddresses = filter_addresses(addressList) # Remove unnecessary addresses
        cleanedaddresses = clean_addresses(key, filteredaddresses.copy()) # Remove substrings
        
        final[key] = cleanedaddresses

    for key, value in final.items():
        print(f'{key}: {value}')
            

if __name__ == "__main__":
    main()

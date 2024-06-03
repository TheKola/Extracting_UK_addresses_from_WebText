## README: UK Address Extraction from Website Text

### Overview
This project demonstrates a method for extracting UK addresses from textual content on company websites, specifically focusing on the text around postcode areas. Developed while working at The Data City, the project focuses on analyzing patterns in address formats to facilitate address extraction based on regex and text analysis.

### Project Structure and Logic
1. **Database to JSON Conversion**: The process starts by converting data from an SQLite database into a JSON file. This file maps company numbers to corresponding website text in JSON format, effectively creating a nested JSON structure.

2. **Address Extraction Process**:
   - **Postcode Identification**: Using regex, the script identifies all UK postcodes in the website text.
   - **Context Extraction**: For each identified postcode, the script extracts 100 characters preceding it. This chunk is likely to contain the address.
   - **Address Isolation**: From the extracted context, the script isolates potential address segments by capturing sequences starting with uppercase letters or digits (commonly how addresses are formatted).
   - **Refinement**: Further refinement includes removing non-alphanumeric characters and unnecessary substrings to distill the addresses to their most probable and relevant forms.

3. **Subprocesses**:
   - **Removing Substrings**: A function identifies and removes substrings from potential address candidates to avoid redundancy.
   - **Removing Unnecessary Addresses**: Another function filters out any strings with special characters or patterns that do not match typical address formats.

### Database Structure
The primary database used in this project contains several tables, but the focus is on scrapped contents. This table includes columns such as Company Number and Website scrapped content, where the website content is stored in a JSON format.

### Code Explanation
- The Python script consists of multiple blocks handling different parts of the process:
   - Database interaction and data extraction to JSON.
   - Regex-based postcode extraction from the JSON data.
   - Extracting surrounding text based on postcode occurrences.
   - Cleaning and refining extracted addresses to remove redundancies and non-address content.

### Usage
- Clone the repository to your local machine:
```shell
git clone https://github.com/TheKola/Extracting_UK_addresses_from_WebText.git
```
- Ensure that the SQLite database file is correctly formatted and accessible from the data folder.
```shell
# pip install virtualenv
virtualenv [virtual_env_name]
[virtual_env_name]/Scripts/activate   

```
- Run the Python script in an environment that supports Python and the necessary libraries (`sqlite3`, `json`, `re`).
```shell
pip install --no-cache -r requirements.txt
```
- Creating the required json file
```shell
python src/database.py
```
- Extracting addresses
```shell
python src/main.py
```

- Examine the output for the extracted data and in the terminal/console for debug prints of the process.
- The final output is storded in a python dictonary as postcode and full address pair.

### Conclusion
This project provides a structured approach to extracting UK addresses from textual data on company websites. It demonstrates the power of regex and simple text manipulation techniques in data extraction tasks, particularly useful in data analytics and machine learning preprocessing steps.

## Contributing
Contributions are welcome! Please read the [contributing guidelines](CONTRIBUTING.md) for more details.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

### Acknowledgements
This project was developed at The Data City, and it leverages common data manipulation libraries in Python to provide a robust solution for address extraction from unstructured text sources.

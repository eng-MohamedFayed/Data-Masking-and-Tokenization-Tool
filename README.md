# Data Masking and Tokenization Tool

This Python tool provides a framework for anonymizing and pseudonymizing sensitive datasets by masking or transforming personal information. By enabling various masking techniques like pseudonymization, tokenization, redaction, and random data generation, this tool ensures data privacy, particularly for datasets containing sensitive information such as personal identifiers, financial details, and contact information.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Use Cases](#use-cases)
- [How It Works](#how-it-works)
  - [Code Structure](#code-structure)
  - [Options and Masking Techniques](#options-and-masking-techniques)
- [License](#license)

---

## Overview
The primary goal of data masking is to protect sensitive information by transforming it into a format that cannot be used to identify individuals. Data masking is essential in:
- Testing environments
- Data sharing for analytics
- Training ML models without revealing confidential data
This tool facilitates the choice of masking techniques on a per-field basis, allowing for customized anonymization strategies.

## Features
- **Pseudonymization:** Replaces sensitive data with generic, unique identifiers.
- **Tokenization:** Hashes data with SHA-256 and adds salt for irreversible transformation.
- **Redaction:** Hides all but a configurable number of characters.
- **Faker-generated Masking:** Generates realistic fake data using [Faker](https://faker.readthedocs.io/).
- **Custom Masking Options:** For each field, choose masking type (pseudonymize, tokenize, redact, etc.) and data type (phone, email, address, etc.).
  
## Installation
### Dependencies
Ensure you have Python 3.x installed and install the necessary libraries:
```bash
pip install Faker
```

### Getting the Repository
Clone this repository to your local machine using Git:
```bash
git clone https://github.com/eng-MohamedFayed/Data-Masking-and-Tokenization-Tool.git
cd data-masking-tool
```

### File Structure
The main script, `data_masking_tool.py`, is the only file required to run the tool.

## Usage
Run the tool by executing:
```bash
python data_masking_tool.py
```

The tool will prompt you to define the fields you wish to include in your dataset and the masking options for each. You’ll be able to interactively:
1. Add entries to the dataset.
2. Mask individual or all entries.
3. View, modify, or delete dataset entries.
4. Export original and masked datasets as JSON files.

## Use Cases
This tool is ideal for professionals in:
- **Cybersecurity and Privacy Compliance:** Ensuring sensitive data is not shared in its original form.
- **Software Testing:** Using masked data to test applications in non-production environments.
- **Data Science and Machine Learning:** Masking data fields to preserve privacy while using anonymized data for analysis and model training.

---

## How It Works
### Code Structure
The main components of this tool are:
- **Data Entry and Management:** Users can add, delete, modify, and view entries in the dataset.
- **Masking Options:** Each field can be assigned a masking method (pseudonymize, tokenize, redact, or mask).
- **Data Export:** Original and masked datasets can be saved to separate JSON files for further use.

### Options and Masking Techniques
The following choices are provided for each field:
- **None:** No masking applied.
- **Pseudonymize:** Generates unique identifiers for each entry.
- **Tokenize:** Applies SHA-256 hashing with a salt for irreversibility.
- **Redact:** Shows only the last few characters while masking the rest.
- **Mask (using Faker):** Generates random but realistic-looking fake data based on the field type.

#### Example Field Options:
When choosing to mask data with Faker, specify the data type. Options include:
  - `phone`: Generates a realistic phone number.
  - `email`: Generates a realistic email address.
  - `address`: Generates a random address.
  - `credit card`: Generates a random credit card number.
  - `date`: Generates a random date.
  - `generic`: Generates random text.

### Detailed Walkthrough
1. **Pseudonymize** - Each field marked with this option is replaced with a generic identifier based on the field name.
2. **Tokenize** - SHA-256 hashing combined with a unique salt ensures that the tokenized data cannot be reverted to its original form.
3. **Redact** - Only the last few characters of each field are shown, while the rest are replaced with asterisks.
4. **Mask** - The `Faker` library provides context-appropriate fake data.

---

## License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

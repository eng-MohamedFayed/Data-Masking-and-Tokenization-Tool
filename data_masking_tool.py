import hashlib
import json
import os
from faker import Faker

# Initialize Faker
faker = Faker()

# Function to pseudonymize names
def pseudonymize(field, index):
    return f"{field}_{index}"

# Function to tokenize data (simple MD5 hashing)
def tokenize_data(data):
    salt = os.urandom(32)
    return hashlib.sha256(data.encode() + salt).hexdigest(),salt

# Function to redact data (show only last 4 digits)
def redact_data(data, num_visible=4):
    if num_visible >= len(data):
        return data
    return '*' * (len(data) - num_visible) + data[(len(data) - num_visible):len(data)]

# Function to mask phone number using Faker
def mask_phone():
    return faker.phone_number()

# Function to mask email using Faker
def mask_email():
    return faker.email()

# Function to mask address using Faker
def mask_address():
    return faker.address()

# Function to mask credit card number using Faker
def mask_credit_card():
    return faker.credit_card_number()

# Function to mask generic text
def mask_generic():
    return faker.text(max_nb_chars=20)

# Function to mask date
def mask_date():
    return faker.date()

# Dataset dictionary
dataset = {}
masked_dataset = {}
field_masking_options = {}
masking_data_type = {}
ID_salt = {}

#for masking all entries
def mask_all_entries():
    for entry_id, entry in dataset.items():
        if entry_id not in masked_dataset:
            masked_entry = apply_mask(entry_id, entry, field_masking_options)
            masked_dataset[entry_id] = masked_entry
    print("All entries have been masked.")
# Helper function to display the menu
def display_menu():
    print("\nOptions:")
    print("1 - Add data to dataset")
    print("2 - Delete a specific entry")
    print("3 - View entries")
    print("4 - Modify any part of a specific entry")
    print("5 - Mask a specific entry")
    print("6 - Mask all entries")
    print("7 - Output original data to text file")
    print("8 - Output masked data to text file")
    print("9 - Quit")

# Function to save dataset to a text file
def save_to_file(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

# Function to apply the mask based on user input
def apply_mask(entry_id, entry, masking_options):
    masked_entry = {}
    for field, value in entry.items():
        if masking_options[field][0] == 'pseudonymize':
            masked_entry[field] = pseudonymize(field, entry_id)  # Pseudonymize
        elif masking_options[field][0] == 'tokenize':
            masked_entry[field],salt = tokenize_data(value)
            ID_salt[entry_id] = salt
        elif masking_options[field][0] == 'redact':
            masked_entry[field] = redact_data(value, masking_options[field][1])
        elif masking_options[field][0] == 'mask':
            # Masking logic based on data type
            data_type = masking_data_type[field]
            if data_type == 'phone':
                masked_entry[field] = mask_phone()
            elif data_type == 'email':
                masked_entry[field] = mask_email()
            elif data_type == 'address':
                masked_entry[field] = mask_address()
            elif data_type == 'credit card':
                masked_entry[field] = mask_credit_card()
            elif data_type == 'date':
                masked_entry[field] = mask_date()
            else:
                masked_entry[field] = mask_generic()  # Generic masking for unknown types
        else:
            masked_entry[field] = value  # No masking
    return masked_entry

# Main function to run the program
def main():
    global dataset, masked_dataset, field_masking_options, masking_data_type, ID_salt
    
    try:
        dataset_name = input("Enter the dataset name (e.g., patients, customers): ").strip()
        if not dataset_name:
            raise ValueError("Dataset name cannot be empty.")
        
        # Get the fields from the user
        fields = input("Enter the fields you want to include (comma-separated, e.g., name, SSN, email, etc.): ").split(',')
        fields = [field.strip().lower() for field in fields if field.strip()]
        if not fields:
            raise ValueError("Fields cannot be empty.")
        
        print("""Choose masking option for each field:
        0 - none (do nothing)
        1 - pseudonymize (replace with a generic name)
        2 - tokenize (hash the data)
        3 - redact (show only last 4 digits unless specified otherwise)
        4 - mask (use Faker to generate fake data)""")
        
        # Ask for masking options for each field
        for field in fields:
            while True:
                try:
                    option = input(f"{field}: ").strip()
                    if option not in ['0', '1', '2', '3', '4']:
                        raise ValueError("Invalid option. Please choose from 0, 1, 2, 3, or 4.")
                    break
                except ValueError as e:
                    print(e)
            
            option = {"0": "none", "1": "pseudonymize", "2": "tokenize", "3": "redact", "4": "mask"}[option]
            
            if option == "mask":
                while True:
                    try:
                        data_type = input(f"What type of data is {field}? (phone, email, address, credit card, date, or other): ").strip().lower()
                        if data_type not in ['phone', 'email', 'address', 'credit card', 'other']:
                            raise ValueError("Invalid data type. Please choose from phone, email, address, credit card, date, or other.")
                        masking_data_type[field] = data_type
                        break
                    except ValueError as e:
                        print(e)
            
            if option == "redact":
                while True:
                    try:
                        num_visible = int(input("How many visible characters do you want in your data (from the end)? ").strip())
                        if num_visible < 0:
                            raise ValueError("Number of visible characters cannot be negative.")
                        break
                    except ValueError as e:
                        print(e)
            else:
                num_visible = 0
            
            field_masking_options[field] = [option, num_visible]
        
        # Menu loop
        while True:
            display_menu()
            choice = input("Choose an option: ").strip()
            
            if choice == '1':  # Add data to dataset
                entry = {}
                for field in fields:
                    entry[field] = input(f"Enter {field}: ").strip()
                dataset[len(dataset) + 1] = entry
                print(f"Entry added to {dataset_name} dataset.")
            
            elif choice == '2':  # Delete a specific entry
                try:
                    entry_id = int(input("Enter the entry ID to delete: ").strip())
                    if entry_id in dataset:
                        del dataset[entry_id]
                        print(f"Entry {entry_id} deleted.")
                    else:
                        print("Entry not found.")
                except ValueError:
                    print("Invalid entry ID. Please enter a valid number.")
            
            elif choice == '3':  # View entries
                print("\nOriginal Data:")
                print(json.dumps(dataset, indent=4))
            
            elif choice == '4':  # Modify an entry
                try:
                    entry_id = int(input("Enter the entry ID to modify: ").strip())
                    if entry_id in dataset:
                        field_to_modify = input(f"Which field do you want to modify? ({', '.join(fields)}): ").strip().lower()
                        if field_to_modify in fields:
                            new_value = input(f"Enter the new value for {field_to_modify}: ").strip()
                            dataset[entry_id][field_to_modify] = new_value
                            print(f"Entry {entry_id} updated.")
                            del masked_dataset[entry_id]
                        else:
                            print(f"{field_to_modify} is not a valid field.")
                    else:
                        print("Entry not found.")
                except ValueError:
                    print("Invalid entry ID. Please enter a valid number.")
            
            elif choice == '5':  # Mask a specific entry
                try:
                    entry_id = int(input("Enter the entry ID to mask: ").strip())
                    if entry_id in dataset:
                        if entry_id not in masked_dataset:
                            masked_dataset[entry_id] = apply_mask(entry_id, dataset[entry_id], field_masking_options)
                            print(f"Masked entry {entry_id}:")
                            print(json.dumps(masked_dataset[entry_id], indent=4))
                        else:
                            print(f"Entry {entry_id} is already masked.")
                            print(json.dumps(masked_dataset[entry_id], indent=4))
                    else:
                        print("Entry not found.")
                except ValueError:
                    print("Invalid entry ID. Please enter a valid number.")
            
            elif choice == '6':  # Mask all entries
                mask_all_entries()
                print(json.dumps(masked_dataset, indent=4))
            
            elif choice == '7':  # Output original data to text file
                save_to_file(dataset, f"{dataset_name}_original.txt")
                print(f"Original data saved to {dataset_name}_original.txt")
            
            elif choice == '8':  # Mask all data and output masked data to text file
                mask_all_entries()
                save_to_file(masked_dataset, f"{dataset_name}_masked.txt")
                print(f"Masked data saved to {dataset_name}_masked.txt")
            elif choice == '9':  # Quit
                print("Exiting...")
                break
            
            else:
                print("Invalid choice. Please select a valid option.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

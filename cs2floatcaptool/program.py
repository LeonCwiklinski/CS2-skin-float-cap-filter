import json

def load_json(file_path):
    """Load the JSON file with skin data."""
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print("JSON file not found.")
        return None
    except json.JSONDecodeError:
        print("Error decoding JSON.")
        return None

def filter_skins(skins_data, low_cap, high_cap, tier):
    """Filter skins based on float caps and rarity tier."""
    results = set()  # Use a set to avoid duplicates
    for skin_name, skin_info in skins_data.items():
        # Check if "float-caps" exists and is a valid list with two numeric values
        float_caps = skin_info.get("float-caps")
        if not (isinstance(float_caps, list) and len(float_caps) == 2 and all(isinstance(f, (int, float)) for f in float_caps)):
            continue

        min_float, max_float = float_caps
        skin_tier = skin_info["rarity"].lower()

        # Check if skin meets the criteria and ensure float caps match exactly
        if (skin_tier == tier.lower() and 
            (low_cap == min_float and high_cap == max_float) and
            "★" not in skin_name):  # Exclude skins with the ★ symbol
            # Extract the base name of the skin (without condition info)
            base_skin_name = skin_info["name"]
            results.add(base_skin_name)  # Add base skin name to results

    return list(results)  # Convert the set back to a list for returning

def main():
    # Load the JSON data
    data = load_json("data2.json")
    if data is None:
        return

    # Get user input
    try:
        low_cap = float(input("Enter the low float cap: "))
        high_cap = float(input("Enter the high float cap: "))
        tier = input("Enter the skin tier (e.g., Restricted): ")
    except ValueError:
        print("Invalid input. Please enter numbers for float caps.")
        return

    # Filter and display results
    matched_skins = filter_skins(data, low_cap, high_cap, tier)

    if matched_skins:
        print("Matching skins:")
        for skin in matched_skins:
            print(skin)
    else:
        print("No skins found with the specified criteria.")

if __name__ == "__main__":
    main()

input("Press Enter to exit...")
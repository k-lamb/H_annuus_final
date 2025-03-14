import pandas as pd # type: ignore

wd = "/global/scratch/users/kericlamb/Hannuus_moments3/data"

# Read the file and trim to relevant section
with open("%s/easySFS_output.txt" % wd, "r") as file:
    lines = file.readlines()

# Extract sections starting from "Wild" and "TV"
wild_index = lines.index("Wild\n")
tv_index = lines.index("TV\n")

wild_data = lines[wild_index + 1 : tv_index]  # Data after "Wild"
tv_data = lines[tv_index + 1 :]  # Data after "TV"

# Function to parse data
def parse_data(data_lines, label):
    # Combine all lines into one string and split by tabs
    raw_data = "".join(data_lines).split("\t")
    # Extract numbers within parentheses
    parsed_data = [tuple(map(int, item.strip("()").split(", "))) for item in raw_data if item.strip()]
    # Create DataFrame and add label
    df = pd.DataFrame(parsed_data, columns=["Projection", "Segregating Sites"])
    df["Population"] = label
    return df

# Process Wild and TV data
wild_df = parse_data(wild_data, "Wild")
tv_df = parse_data(tv_data, "TV")
final_df = pd.concat([wild_df, tv_df], ignore_index=True) # Combine both datasets

# Save to CSV or print
final_df.to_csv("%s/easySFS_output_processed.csv" % wd, index=False)

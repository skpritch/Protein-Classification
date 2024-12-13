import os
import requests
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed

def fetch_pdb_ids(uniprot_id):
    url = f'https://www.ebi.ac.uk/pdbe/api/mappings/best_structures/{uniprot_id}'
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get(uniprot_id, [])
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch PDB IDs for UniProt ID {uniprot_id}: {e}")
        return []

def fetch_pdb_metadata(pdb_id):
    url = f'https://data.rcsb.org/rest/v1/core/entry/{pdb_id}'
    try:
        response = requests.get(url, timeout=20)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch metadata for PDB ID {pdb_id}: {e}")
        return None

def select_best_pdb(pdb_entries):
    method_priority = {
        'X-RAY DIFFRACTION': 4,
        'ELECTRON MICROSCOPY': 3,
        'SOLUTION NMR': 1,
    }

    best_pdb = None
    highest_score = -1

    for entry in pdb_entries:
        pdb_id = entry['pdb_id'].lower()
        metadata = fetch_pdb_metadata(pdb_id)
        if not metadata:
            continue

        # Get experimental method
        methods = metadata.get('exptl', [])
        method = methods[0]['method'].upper() if methods else 'UNKNOWN'
        method_score = method_priority.get(method, 0)

        # Get popularity (citation count)
        citation_count = metadata.get('rcsb_accession_info', {}).get('rcsb_citation_count', 0)

        # Get completeness (polymer coverage)
        polymer_coverage = metadata.get('rcsb_entry_info', {}).get('polymer_coverage', 0)

        # Calculate total score
        total_score = method_score * 1000 + citation_count * 10 + polymer_coverage

        if total_score > highest_score:
            highest_score = total_score
            best_pdb = pdb_id

    return best_pdb

def download_pdb(pdb_id, output_dir, downloaded_pdbs):
    pdb_id = pdb_id.lower()
    if pdb_id in downloaded_pdbs:
        # PDB file has already been downloaded; skip without printing
        return
    url = f'https://files.rcsb.org/download/{pdb_id}.pdb'
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        file_path = os.path.join(output_dir, f'{pdb_id}.pdb')
        with open(file_path, 'w') as f:
            f.write(response.text)
        downloaded_pdbs.add(pdb_id)
        print(f'Downloaded {pdb_id}')
    except requests.exceptions.RequestException as e:
        print(f"Failed to download {pdb_id}: {e}")

def process_protein(uniprot_id, downloaded_pdbs):
    pdb_entries = fetch_pdb_ids(uniprot_id)
    if not pdb_entries:
        return uniprot_id, None

    if len(pdb_entries) == 1:
        best_pdb = pdb_entries[0]['pdb_id'].lower()
    else:
        best_pdb = select_best_pdb(pdb_entries)

    if best_pdb:
        return uniprot_id, best_pdb
    else:
        return uniprot_id, None

def main():
    # Load the combined metadata file
    input_csv = '/Users/simonpritchard/Documents/Academics/Junior_Year/ML_Tutorial/Protein_Project/Data/Metadata/combined_metadata.csv'
    df = pd.read_csv(input_csv, dtype=str)

    # Directory to save PDB files
    pdb_output_dir = '/Users/simonpritchard/Documents/Academics/Junior_Year/ML_Tutorial/Protein_Project/Data/pdb_files'
    os.makedirs(pdb_output_dir, exist_ok=True)

    # Initialize the set of downloaded PDB IDs with existing files
    downloaded_pdbs = set()
    for file_name in os.listdir(pdb_output_dir):
        if file_name.endswith('.pdb'):
            pdb_id = os.path.splitext(file_name)[0].lower()
            downloaded_pdbs.add(pdb_id)

    # Dictionary to store UniProt ID to PDB mapping
    pdb_mapping = {}

    # Use ThreadPoolExecutor for parallel processing
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_uniprot = {executor.submit(process_protein, uniprot_id, downloaded_pdbs): uniprot_id for uniprot_id in df['Entry'].unique()}

        for future in as_completed(future_to_uniprot):
            uniprot_id = future_to_uniprot[future]
            try:
                uniprot_id, best_pdb = future.result()
                pdb_mapping[uniprot_id] = best_pdb
                if best_pdb:
                    download_pdb(best_pdb, pdb_output_dir, downloaded_pdbs)
                else:
                    print(f"No suitable PDB found for UniProt ID {uniprot_id}")
            except Exception as e:
                print(f"Error processing UniProt ID {uniprot_id}: {e}")

    # Add the selected PDB IDs to the dataframe
    df['Selected_PDB'] = df['Entry'].map(pdb_mapping)
    # Save the updated dataframe
    df.to_csv(input_csv, index=False)
    print('Updated combined_metadata.csv with selected PDB IDs.')

if __name__ == '__main__':
    main()
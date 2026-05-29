"""
Parse NSS 77th Round metadata and guide data extraction for Pune district
"""

import xml.etree.ElementTree as ET
from pathlib import Path

def parse_nss_metadata(xml_file):
    """Parse DDI/XML metadata file"""

    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Define namespace
    ns = {'ddi': 'http://www.icpsr.umich.edu/DDI'}

    # Extract key information
    metadata = {
        'survey_title': None,
        'survey_id': None,
        'period': 'January 2019 - December 2019',
        'round': '77th Round',
        'abstract': None,
        'geography': None,
        'variables': []
    }

    # Extract title
    title_elem = root.find('.//ddi:titl', ns)
    if title_elem is not None:
        metadata['survey_title'] = title_elem.text

    # Extract ID
    id_elem = root.find('.//ddi:IDNo', ns)
    if id_elem is not None:
        metadata['survey_id'] = id_elem.text

    # Extract abstract
    abstract_elem = root.find('.//ddi:abstract', ns)
    if abstract_elem is not None:
        metadata['abstract'] = abstract_elem.text.strip()

    # Extract geography
    geog_elem = root.find('.//ddi:geogCover', ns)
    if geog_elem is not None:
        metadata['geography'] = geog_elem.text.strip()

    return metadata

def print_metadata_summary(metadata):
    """Print summary of survey metadata"""
    print("\n" + "="*70)
    print("NSS SURVEY METADATA SUMMARY")
    print("="*70)
    print(f"Title: {metadata['survey_title']}")
    print(f"Survey ID: {metadata['survey_id']}")
    print(f"Period: {metadata['period']}")
    print(f"Round: {metadata['round']}")
    print(f"\nGeography: {metadata['geography']}")
    print(f"\nAbstract:\n{metadata['abstract']}")
    print("="*70)

def print_download_instructions():
    """Print instructions for downloading actual data"""
    print("\n" + "="*70)
    print("NEXT STEP: DOWNLOAD ACTUAL DATA FILES")
    print("="*70)
    print("\n1. Go back to NADA portal: https://microdata.gov.in/")
    print("\n2. Navigate to the NSS 77th Round survey page")
    print("\n3. Look for 'Data Files' or 'Download' section")
    print("\n4. Available formats typically include:")
    print("   - CSV (comma-separated values) - BEST for Python/pandas")
    print("   - XLSX (Excel format)")
    print("   - DTA (Stata format)")
    print("   - SPSS SAV format")
    print("\n5. Download the data files and place in: data/raw/")
    print("\nKey variables to look for:")
    print("   - State code (Maharashtra = 27)")
    print("   - District code (Pune = 27-03)")
    print("   - Taluka/Block name (Shirur)")
    print("   - Village name (Loni Dewakar)")
    print("   - Irrigated area")
    print("   - Crop cultivated")
    print("   - Water source")
    print("   - Irrigation method")
    print("="*70)

if __name__ == "__main__":
    metadata_file = "C:\\Users\\Somdeep Kundu\\Downloads\\DDI-IND-MOSPI-NSSO-77Rnd-Sch33.1-January2019-December2019.xml"

    try:
        metadata = parse_nss_metadata(metadata_file)
        print_metadata_summary(metadata)
        print_download_instructions()
    except Exception as e:
        print(f"Error parsing metadata: {e}")
        print("\nManual download instructions:")
        print_download_instructions()

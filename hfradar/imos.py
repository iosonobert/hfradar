import xarray as xr
import requests
from bs4 import BeautifulSoup


# find year folders
def is_date_folder(a):
    try:
        int(a.text[0:-1])
        return True
    except ValueError:
        return False

def is_nc_file(a):
    return a.text.endswith('.nc')

def get_acorn_radial_file(site, year=None, month=None, day=None):
    """Get the ACORN radial file URL for a given site. Specify Year, month, day to get specific file.
    If year, month, day are None, get the latest file available."""


    if year is None:
        base = f'https://thredds.aodn.org.au/thredds/catalog/IMOS/ACORN/radial/{site}/catalog.html'
        print(f'Accessing {base}')
        html = requests.get(base).text
        soup = BeautifulSoup(html, 'html.parser')

        years = [a.text for a in soup.select('a') if is_date_folder(a)]

        year = years[-1]
    else:
        year = str(year) + '/'

    if month is None:
        latest = f'https://thredds.aodn.org.au/thredds/catalog/IMOS/ACORN/radial/{site}/{year}catalog.html'
        print(f'Accessing {latest}')
        html = requests.get(latest).text
        soup = BeautifulSoup(html, 'html.parser')

        months = [a.text for a in soup.select('a') if is_date_folder(a)]
        month = months[-1][0:-1]
    else:
        month = f'{month:02d}' + '/'

    if day is None:
        latest = f'https://thredds.aodn.org.au/thredds/catalog/IMOS/ACORN/radial/{site}/{year}{month}/catalog.html'
        print(f'Accessing {latest}')
        html = requests.get(latest).text
        soup = BeautifulSoup(html, 'html.parser')

        days = [a.text for a in soup.select('a') if is_date_folder(a)]
        day  = days[-1][0:-1]
    else:
        day = f'{day:02d}' 

    latest = f'https://thredds.aodn.org.au/thredds/catalog/IMOS/ACORN/radial/{site}/{year}{month}/{day}/catalog.html'

    print(f'Accessing {latest}')
    html = requests.get(latest).text
    soup = BeautifulSoup(html, 'html.parser')

    files = [a.text for a in soup.select('a') if is_nc_file(a)]

    latest_file_url = f'https://thredds.aodn.org.au/thredds/fileServer/IMOS/ACORN/radial/{site}/{year}{month}/{day}/{files[-1]}'
    latest_file_url = latest_file_url.replace('fileServer', 'dodsC')
    ds = xr.open_dataset(latest_file_url)
    
    return ds, latest_file_url
import re
import pandas as pd

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, *args, **kwargs):

    def extract_reward_value(text):
        pattern = r'\$([\d,]+)'
        match = re.search(pattern, str(text))  # Convert to string before searching
        if match:
            value_str = match.group(1).replace(',', '')  # Remove commas from the matched string
            return int(value_str)
        else:
            return None

    data['reward_value'] = data['reward_text'].apply(extract_reward_value)
    data['caution'] = data['caution'].str.replace('<p>', '').str.replace('</p>', '')
    data['crime_classification'] = data['url'].str.split('/').str[-2]
    data['is_armed'] = data['warning_message'].str.upper().str.contains('ARMED')
    data['is_dangerous'] = data['warning_message'].str.upper().str.contains('DANGEROUS')
    data['birth_year'] = data['dates_of_birth_used'].str.extract(r'\b(\d{4})\b').astype(float).fillna(0).astype(int)
    data['modified'] = pd.to_datetime(data['modified']).dt.strftime('%Y-%m-%d %H:%M:%S.%f')
    data['publication'] = pd.to_datetime(data['publication']).dt.strftime('%Y-%m-%d %H:%M:%S.%f')
    data['remarks'] = data['remarks'].str.replace('<p>', '').str.replace('</p>', '')
    data['id'] = data['@id'].str.split('/').str[-1]
    data['check_date'] = pd.to_datetime(data['check_datetime']).dt.strftime('%Y-%m-%d')
    data['check_datetime'] = pd.to_datetime(data['check_datetime']).dt.strftime('%Y-%m-%d %H:%M:%S.%f')


    data = data[['check_date', 'check_datetime', 'title', 'id',  'crime_classification', 'reward_value', 
                'publication', 'caution', 'sex', 'race', 'eyes', 
                'hair', 'scars_and_marks', 'nationality', 'is_armed', 'is_dangerous', 
                'modified', 'remarks']]



    return data

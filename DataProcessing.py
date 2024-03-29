import re
import string
import pandas as pd
#import nltk
#from nltk.corpus import stopwords
#nltk.download("stopwords")
import spacy
spacy.cli.download("en_core_web_sm")
nlp = spacy.load("en_core_web_sm")

#Function to fix the headers of data read in from blob storage
def fix_headers(df):
    headers = df.iloc[0]
    df = df[1:]
    df.columns = headers
    return df

#Function that performs text cleaning -- can add more actions as neccesary
def clean(text):
    #Removing URLs
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    #Removing Email addresses
    text = re.sub(r'\S*@\S*\s?', '', text)
    #Removing Numbers
    text = re.sub(r'\d+','',text)
    #Removing irregular characters
    text = re.sub(r'[^a-zA-Z]', ' ', text)
    #Removing blanked(x'ed) out info
    text = re.sub(r'xx', '', text)
    #Removing extra whitespace
    text = re.sub(r'^\s*|\s\s*', ' ', text).strip()
    return text.lower()

def remove_names(df, txt_col_name):
    doc = list(nlp.pipe(df[txt_col_name].to_numpy()))
    removed_names = []
    for i in [token.text for token in doc]:
        if i in [ent.text for ent in doc.ents if ent.label_ == 'PERSON']:
            continue
        else:
            removed_names.append(i)

#Function that combines claim notes for claims with multiple iterations
def combine_notes(str_lst):
    clm_note = ""
    for i in str_lst:
        if type(i) != float:
            clm_note = clm_note + str(i) + '. '
    return clm_note

#Applying the cleaning function to a specific column - takes dataframe & text/notes column name as input & outputs the cleaned text column
def text_cleaning(df: pd.DataFrame, txt_col_name: str):
    '''
    Cleans text column of a dataframe
        Function:
        - Removes URLs, Email Addresses, numbers, special characters, extra whitespace, and x'ed out information.
        - Returns all words in lowercase

        Parameters:
        - df --> DataFrame object
        - txt_col_name --> The name of the column that contains the text that needs to be cleaned

        Returns:
        - df[cleaned_text] --> column that contains cleaned text
            - This will automatically create a new column in your df named 'cleaned_text'
    '''
    df['cleaned_text'] = df[txt_col_name].apply(clean)
    
    return df['cleaned_text']


def replace_abbrevs(df:pd.DataFrame, text_field:str, abbreviations:dict={}):
    """
    prepare text field by stripping extra spaces, and if desired replace abbrevations

    Params:
    df: pandas data frame with text field
    text_field: column name of text field to be altered
    abbreviations: dictionary of possible abbreviations to be converted to full text, default: {}

    Returns:
    df[prepped_text] --> column that contains abbreviation replacements
    """

    if abbreviations !={}:
        abbreviations = {r'(?i)\W{} '.format(key): " " + val + " " for key, val in abbreviations.items()}
        df['prepped_text'] = df[text_field].replace(abbreviations, regex=True).str.strip()

    return df['prepped_text']

    
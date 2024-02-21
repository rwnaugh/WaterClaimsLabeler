#Function to fix the headers of data read in from blob storage
def fix_headers(df):
    headers = df.iloc[0]
    df = df[1:]
    df.columns = headers
    return df

#Function that combines claim notes for claims with multiple iterations
#Also returns the notes in lower case
def combine_notes(str_lst):
    clm_note = ""
    for i in str_lst:
        if type(i) != float:
            clm_note = clm_note + str(i) + '. '
    return clm_note.lower()

#Removing URLs
def remove_url(text):
    return re.sub(r'https?://\S+|www\.\S+', '', text)

#Removing numbers & punctuation
def remove_irr_char(text):
    return re.sub(r'[^a-zA-Z]', ' ', text)

#Removing extra whitespace
def remove_extra_whitespaces(text):
    return re.sub(r'^\s*|\s\s*', ' ', text).strip()
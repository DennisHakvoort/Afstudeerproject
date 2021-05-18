# Processor
The processor is the pure preparation part of Kitea. The processor fullfills the follwoing roles: (A exclamation mark is added to features not yet implemented)
- Fetches documents from the datasource (currently only the BBC test data, not the real confluence data)
- Converts the data into a predefined 'Document' state
- Preprocessing of the docuemnts (removing stopwords, lemmatization, removing punctuation, etc.)
- Calculates semantic distance between different documents
- Stores the documents into the database
- Stores the document distance into the database

The search component will not interact directly with the processor. The only way of sharing data between the two is through the database.
"""
DREAM Respiratory Virus Challenge 2016

Team: Germany
Members:
- Damien
- Eric
- Christoph
- Guy

Script Author: Eric J. Ma
Script Contributors and Dates:
Date: 26 July 2016

I have assumed here the following directory structure:
- DREAM
  - notebooks
  - scripts
  - data
  - tests
This script should be placed in the "scripts" directory.
"""

import pandas as pd

# Read in the expression data as a pandas dataframe.
expression_df = pd.read_csv('../data/ViralChallenge_training_EXPRESSION_RMA.tsv', sep="\t", index_col='FEATUREID').T

# Read in the clinical data as a pandas dataframe.
clinical_df = pd.read_csv('../data/ViralChallenge_training_CLINICAL.tsv', sep='\t')
clinical_df.set_index('CEL', inplace=True)  # allows us to join on this column later.
clinical_df = clinical_df[clinical_df['TIMEHOURS'] <= 24]  # filter unnecessary data.


# Split the data by study ID
clinical_split = dict()
for grp, dat in clinical_df.groupby('STUDYID'):
    print(grp)
    if grp == 'Rhinovirus Duke':  # there is a problem doing the .unstack() operation for this subset of data.
        print('->passing!')
        pass
    else:
        clinical_split[grp] = dat.join(expression_df).reset_index().sort_values(['STUDYID', 'SUBJECTID', 'SHEDDING_SC1',
                                                                                 'SYMPTOMATIC_SC2', 'LOGSYMPTSCORE_SC3',
                                                                                 'AGE', 'GENDER', 'EARLYTX', 'SHAM', 'TIMEHOURS'])
        del clinical_split[grp]['SAMPLEID']
        del clinical_split[grp]['CEL']

        clinical_split[grp] = clinical_split[grp].set_index(['STUDYID', 'SUBJECTID', 'SHEDDING_SC1',
                                                             'SYMPTOMATIC_SC2', 'LOGSYMPTSCORE_SC3',
                                                             'AGE', 'GENDER', 'EARLYTX', 'SHAM', 'TIMEHOURS'])
        clinical_split[grp] = clinical_split[grp].unstack()
        clinical_split[grp].columns = clinical_split[grp].columns.to_series().apply(pd.Series).astype(str).T.apply('_'.join)
        clinical_split[grp].to_csv('{0}.csv'.format(grp))

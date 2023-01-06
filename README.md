# GitHub Repository Visibility maintenance script

## Prerequisites
Python 3
`pip install -r requirements.txt`

## Usage: List Repository Visibility
Purpose: To list repository visibility info. <br/>
How to Use: Execute following command-line with your organization name and token (Personal Access Token). The list of repository names and visibility information is written to a csv file `repos.csv`.

- Command-line:
`python3 repo_vis.py list -o <org-name> -t <token>`
- Output:
`repos.csv`
- Output Format: `<repo_name>,<visibility>`
 ```text
 name_of_repoA,PRIVATE
 name_of_repoB,INTERNAL
 ```
- Log File:
`repo_vis.log`

## Usage: Compare Repository Visibility
Purpose: To compare repository visibility info. <br/>
How to Use: Execute following command-line with your target organization name and token (Personal Access Token). The list of repository names and visibility information is written to a csv file `repos_target.csv`. The list of repository names and visibility information will be compared with `repos.csv` and the differences are shown in 'repos_diff.csv'.

- Command-line:
`python3 repo_vis.py compare -o <org-name> -t <token>`
- Input:
`repos.csv`
- Output 1:
`repos_target.csv`
- Output Format: `<repo_name>,<visibility>`
- Output 2:
`repos_diff.csv`
- Output 2 Format: `<repo_name>,<visibility>,<is_same?>(True/False),<expected_visibility>(visiblity or NOT FOUND if not exists`
- Sample:
 ```text
 name_of_repoA,PRIVATE,True
 name_of_repoB,INTERNAL,False,PRIVATE
 name_of_repoC,INTERNAL,False,NOT FOUND
 ```
- Log File:
`repo_vis.log`

## Usage: Update Repository Visibility
Purpose: To update repository visibility info. <br/>
How to Use: Execute following command-line with your target organization name and token (Personal Access Token). Processes visibility update for repository that shows the differences in the 'repos_diff.csv'.

- Command-line:
`python3 repo_vis.py update -o <org-name> -t <token>`
- Input:
`repos_diff.csv`
- Log File:
`repo_vis.log`
- Note:
422 Client Error: visibility cannot be updated due to validation error. Most likely visibility is already updated case.

### Additional Notes
The name of the output CSV file can be changed in settings.py

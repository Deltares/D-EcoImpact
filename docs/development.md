# Development D-Eco Impact
## Workflow
### Developer:
1. Move the jira issue you want to work on from "todo" into "in progress".
(issue should be in the sprint, if not please discuss with product owner about changing the sprint scope).

1. Create a development branch from the main branch with the name "feat[issue id] {summary of the issue}" 
For example: 
> feat[DEI-123] Improve functionality A
and switch your local copy to the development branch.

3. Commit the necessary changes with a clear message on what has been changed.

1. Check if all checks have passed (green checkmark, no red cross).
 
1. Check if there are changes in the main branch. If so, merge these to the development branch and fix all possible conflicts in the code , if any. Go back to point 4 of this list.
 
1. Move issue from "in progress" to "in review" and create a pull-request with the name "feat[issue id: like DEI-123]{summary of the issue}".

### Reviewer:
1. Change issue status from "in review" to "being reviewed". This should make you the assignee.
1. Look at the development details of the issue.
1. Open the linked pull-request in GitHub.
1. Change reviewer to yourself.
1. Go to the "Files changed" tab to see the changes.
1. Add your review comments (see comment on a PR documentation).

Some things to consider:
* is the code in the right place
* is it readable
* is the code documented (all public methods and classes should have doc strings)
* are all tests and checks green
* is the code covered by tests

7. Set the status of the issue (comment, approve or request changes).
1. Change jira status to the right type

Approved -> "In Test"
Request changes -> "To do"
Comment -> "In review" (with assignee the developer).

### Tester:
1. Change issue status from "in test" to "being tested". This should make you the assignee.
 
1. (For a bug) -> Checkout the main branch and try to reproduce the issue.
 
1. Change your local checkout to the development branch (from which pull-request was created).
 
1. Test the new functionality or bug fix by running the main script from python in a clean python environment.
 
1. Add comment in the issue with the findings (ok or not because ....).
 
1. Change jira status to the right type

Test ok -> "Merge"
Not ok -> "To do"

### (If test is ok)

1. Go to pull request on GitHub.

1. Check if there will be merge conflicts (shown by GitHub) and if the development branch is up to date with the main branch.

if there are merge conflicts reported -> check with developer to resolve the merge issues.
if the branch does not have merge conflicts and is not up to date -> press the update branch button.

3. If the branch is up to date and does not have merge conflicts you can merge the pull request to the main branch.

1. Change issue status in jira from "merge" to "validate".

1. Change your local checkout to the main branch and do a few checks to see if the merge was correct.

1. If the merge was successful, change issue status in jira from "validate" to "done".

Agreements

 
Coding:
 
We use the PEP8 style guide for python development.
We use typing where possible.
We avoid using global variables.
We use encapsulation by only making the necessary imports and variables public.
 
For testing we use the pytest module.
For checking the style guide we use flake8 and pylint.
For managing external dependencies we use poetry (.toml file).
 
We prefer to use vscode for development (sharing settings using .vscode folder) usinge the following plugins:
autoDocstring
python
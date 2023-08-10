# Development D-Eco Impact
## Workflow
### Developer:
1. Move the jira issue you want to work on from "todo" into "in progress".
(issue should be in the sprint, if not please discuss with product owner about changing the sprint scope).

1. Create a development branch from the main branch with the name based on that of the issue <br /> _feat[issue id] {summary of the issue}_. For example: 
    > **_feat[DEI-123] Improve functionality A_**

    Then switch your local copy to the development branch.

3. Commit the necessary changes with clear messages on what has been done.

1. Verify if all checks have passed (a green checkmark is shown, not a red cross).

    ![checks](assets/images/1_all_checks_passed.png "Github showing that all checks have passed. If one or more checks have failed, then a red cross is shown instead.")
    Is one or more checks fail, they must be fixed before continuing.

5. Once all checks pass, control if there are any changes in the main branch. If so, merge them to the development branch and fix all possible conflicts in the code, if any, and then go back to point 4 of this list.
 
1. Move the issue from _In progress_ to _In review_ and create a pull-request with the name of the branch previously assigned:
    > _feat[issue id]{summary of the issue}_.

### Reviewer:
1. Change the status of the issue from _In review_ to _Being reviewed_. This should make you automatically the assignee.
1. Look at the development details of the issue.
![detailsIssues](assets/images/2_development_details_of_issues.png "Details of development for an issue, including the branches linked to the issue, the commits and the pull requests.")


1. Open the linked pull-request in GitHub.
1. Change the reviewer to yourself if it didn't happen before, as indicated in point 1.

    ![reviewer](assets/images/2_assign_review.png "Details of development for an issue, including the branches linked to the issue, the commits and the pull requests.")

5. Go to the _Files changed_ tab to see the modifications implemented for the issue.

    ![filesChanged](assets/images/2_files_changed.png "Files changed when solving an issue. The files on the list on the left can be selected one by one. The right panel will then show the changes in the selected file.")

6. Add your review comments (see [comment on a PR documentation](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests/commenting-on-a-pull-request) ).

    Some points to analyse during the review are:
    * is the code in the right place?
    * is it readable?
    * is the code documented (all public methods and classes should have doc strings)?
    * are all tests and checks green?
    * is the code covered by tests?
    ![codeCoverage](assets/images/2_code_coverage.png "Code coverage of each file which has been changed during a commit. Details indicating how many statements are present, how many of those are missing from being testedhow many are excluded and what the resulting code coverage is for that file. The total code coverage is shown as well.")
7. Set the status of the issue (comment, approve or request changes).
    ![statusIssue](assets/images/2_status_of_issue.png "Based on the outcome of the review process, indicate if the issue has been simply commented, approved or rejected because some changes are requested.")
1. Change the status if the issue in Jira corrspondingly:

    * Approved -> _In Test_
    * Request changes -> _To do_
    * Comment -> _In review_ (with the developer as assignee).

### Tester:
1. Change issue status from "in test" to "being tested". This should make you the assignee.
 
1. (For a bug) -> Checkout the main branch and try to reproduce the issue.
 
1. Change your local checkout to the development branch (from which pull-request was created).
 
1. Test the new functionality or bug fix by running the main script from python in a clean python environment.
 
1. Add comment in the issue with the findings (ok or not because ....).
 
1. Move the issue in Jira to the corresponding new state:
    * Test ok -> _Merge_
    * Not ok -> _To do_

### If test is succesful

1. Go to pull request on GitHub.

1. Check if there will be merge conflicts (shown by GitHub) and if the development branch is up to date with the main branch.
![mergeCOnflicts](assets/images/4_no_conflicts_can_merge.png "If there are no conflicts with the base branch, the code of the feature can be safely merged. Otherwise, the conflicts need to be solved before.")

    * If any merge conflicts are reported, then check with developer to resolve the merge issues.
    * If the branch does not have any merge conflicts and is not up to date -> press the update branch button.

3. If the branch is up to date and does not have merge conflicts you can merge the pull request to the main branch.

1. Change issue status in jira from "merge" to "validate".

1. Change your local checkout to the main branch and do a few checks to see if the merge was correct.

1. If the merge was successful, change issue status in jira from "validate" to "done".

### Agreements
 
#### Coding:

* We use the [PEP8 style guide](https://pep8.org/) for python development.
* We use [typing}(https://docs.python.org/3/library/typing.html) where possible.
* We avoid using global variables.
* We use encapsulation by only making the necessary imports and variables public.
 
* For testing we use the pytest module.
* For checking the style guide we use flake8 and pylint.
* For managing external dependencies we use poetry (.toml file).
 
* We prefer to use vscode for development (sharing settings using .vscode folder) usinge the following plugins:
    * [autoDocstring](https://marketplace.visualstudio.com/items?itemName=njpwerner.autodocstring)
    * [python](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
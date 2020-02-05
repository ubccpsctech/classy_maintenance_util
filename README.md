# classy_maintenance_util
Perform routine operations and procedures.

Features: 

- Disassociates repos for every team in a Github organization
- Setup of a Github organization (org creation, Classy default team creation, LDAP integration, some but not all org configuration)

NOTE: Tested with Github Enterprise but not Github.com

Example config.ini:

```C
[DEFAULT]
github_org = classydev
api_token = longRandomString
api_path = https://github-dev.students.cs.ubc.ca/api/v3
ignored_team_names = admin,staff,students
req_delay = 2.0
staff_ldap=cpsc999_2019W2_TAs
students_ldap=cpsc999_2019W2

[999]
github_org = cpsc999-2019w-t1
api_path = https://github.students.cs.ubc.ca/api/v3
api_token = githubAPIToken

[999-dev]
github_org = cpsc999-2019w-t1
api_token = githubAPIToken
```

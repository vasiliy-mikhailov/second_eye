# текущая деятельность
# select
#     to_char(project.pkey||'-'||issue.issuenum) as "id",
#     'https://jira.mcb.ru/browse/'||project.pkey||'-'||issue.issuenum as "url",
#     issue.summary as "name",
#     nvl(work_log.time_worked, 0) as "time_spent",
#     to_char(-1) as "system_change_request_id",
#     issue.issuestatus as "state_id"
# from
#     jira60.jiraissue issue
#     inner join jira60.project project on issue.project=project.id
#     left join (select round(sum(work_log.timeworked) / 60 / 60) time_worked, work_log.issueid issue_id from jira60.worklog work_log group by work_log.issueid) work_log on work_log.issue_id = issue.id
# where
#     issue.issueType = 12305
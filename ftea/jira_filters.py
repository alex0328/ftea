kadlubowski = {
    'all_tasks_tasks': 'project = TP AND issuetype in (Bug, Story, Task) order by created DESC',
    'all_tasks_done': 'project = TP AND issuetype in (Bug, Story, Task) AND status = Done order by created DESC',
    'all_tasks_todo': 'project = TP AND issuetype in (Bug, Story, Task) AND status = "To Do" order by created DESC',
    'all_inprogress': 'project = TP AND issuetype in (Bug, Story, Task) AND status = "In Progress" order by created DESC',
    'all_epics_epics': 'project = TP AND issuetype = Epic order by created DESC',
}

ff = {
    'all_tasks_tasks': 'project = FF order by created DESC',
    'all_tasks_done': 'project = FF AND status in (Closed, Resolved, Testing) order by created DESC',
    'all_tasks_todo': 'project = FF AND status in (Open, "To Do") order by created DESC',
    'all_tasks_hold': 'project = FF AND status in ("On Hold") order by created DESC',
    'all_inprogress': 'project = FF AND status = "In Progress" order by created DESC',
    'all_epics_epics': 'project = FF AND issuetype = Epic order by created DESC',
}
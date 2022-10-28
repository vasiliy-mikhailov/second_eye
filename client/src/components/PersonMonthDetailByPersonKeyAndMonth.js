import React, {Component} from "react";
import {gql} from '@apollo/client';
import { graphql } from '@apollo/client/react/hoc';
import Typography from '@material-ui/core/Typography';
import {Box, Link} from "@material-ui/core";
import TimeSheetsByDateIssueChart from "./TimeSheetsByDateIssueChart";
import {Link as RouterLink} from "react-router-dom";
import {DataGridPro} from "@mui/x-data-grid-pro";

const fetchPersonMonthByPersonKeyAndMonth = gql`
    query PersonMonthByPersonKeyAndMonth($personKey: String!, $month: Date!) {
        personMonthByPersonKeyAndMonth(personKey: $personKey, month: $month) {
            person {
                id
                name
            }
            
            analysisTimeSpentMonthFte
            developmentTimeSpentMonthFte
            testingTimeSpentMonthFte
            managementTimeSpentMonthFte
            incidentFixingTimeSpentMonthFte
            nonProjectActivityTimeSpentMonthFte
            timeSpentMonthFte
            
            incidents {
                id
                incident {
                    id
                    key
                    url
                    name
                    
                            
                    projectTeam {
                        id
                        name
                    }
                }
                timeSpentMonthFte          
            }
            
            systemChangeRequests {
                id
                systemChangeRequest {
                    id
                    key
                    url
                    name
                    
                    changeRequest {
                        id
                        name
                        
                        projectTeam {
                            id
                            name
                        }
                    }
                }
                managementTimeSpentMonthFte          
            }
            
            nonProjectActivities {
                id
                nonProjectActivity {
                    id
                    key
                    url
                    name
            
                }
                timeSpentMonthFte          
            }
            
            tasks {
                id
                task {
                    id
                    key
                    url
                    name
                    
                    systemChangeRequest {
                        id
                        key
                        name
                        
                        changeRequest {
                            id
                            key
                            name
                            
                            projectTeam {
                                id
                                name
                            }
                        }
                    }
                }
                timeSpentMonthFte          
            }
        }
    }
`;

class PersonMonthDetailByPersonKeyAndMonth extends Component {
    render() {
        if (this.props.data.loading) { return <div>Loading ...</div> }
        const personKey = this.props.match.params.personKey
        const month = this.props.match.params.month
        const personMonth = this.props.data.personMonthByPersonKeyAndMonth

        const personName = personMonth.person.name

        const analysisTimeSpentMonthFte = personMonth.analysisTimeSpentMonthFte
        const developmentTimeSpentMonthFte = personMonth.developmentTimeSpentMonthFte
        const testingTimeSpentMonthFte = personMonth.testingTimeSpentMonthFte
        const managementTimeSpentMonthFte = personMonth.managementTimeSpentMonthFte
        const incidentFixingTimeSpentMonthFte = personMonth.incidentFixingTimeSpentMonthFte
        const nonProjectActivityTimeSpentMonthFte = personMonth.nonProjectActivityTimeSpentMonthFte
        const timeSpentMonthFte = personMonth.timeSpentMonthFte

        const tasks = personMonth.tasks
        const incidents = personMonth.incidents
        const nonProjectActivities = personMonth.nonProjectActivities
        const systemChangeRequests = personMonth.systemChangeRequests

        const incidentsTableContents = incidents.slice()
            .filter(a => a.timeSpentMonthFte > 0)
            .sort((a, b) => ((a.timeSpentMonthFte < b.timeSpentMonthFte) ? 1 : ((a.timeSpentMonthFte > b.timeSpentMonthFte) ? -1 : 0)))
            .map(incidentTaskTimeSpent => (
                    {
                        id: incidentTaskTimeSpent.id,
                        incidentId: incidentTaskTimeSpent.incident.id,
                        incidentKey: incidentTaskTimeSpent.incident.key,
                        incidentUrl: incidentTaskTimeSpent.incident.url,
                        incidentName: incidentTaskTimeSpent.incident.name,
                        projectTeamId: incidentTaskTimeSpent.incident.projectTeam.id,
                        projectTeamName: incidentTaskTimeSpent.incident.projectTeam.name,
                        timeSpentMonthFte: incidentTaskTimeSpent.timeSpentMonthFte,
                    }
            ))

        const incidentsTableColumns = [
            {
                field: 'projectTeamName',
                headerName: 'Команда проекта',
                flex: 1,
                renderCell: (params) => (
                    <RouterLink to={ `/projectTeams/${ params.getValue(params.id, 'projectTeamId') }` }>
                        { params.getValue(params.id, 'projectTeamName') }
                    </RouterLink>
                ),
            },
            {
                field: 'incidentName',
                headerName: 'Инцидент',
                flex: 1,
                renderCell: (params) => (
                    <Link href={ params.getValue(params.id, 'incidentUrl') } target="_blank">
                        { params.getValue(params.id, 'incidentName') }
                    </Link>
                ),
            },
            {
                field: 'timeSpentMonthFte',
                headerName: 'Трудомощность, FTE',
                width: 200,
                align: 'right',
                valueFormatter: ({ value }) => value.toLocaleString(undefined, { maximumFractionDigits: 3}) ,
            },
        ];

      const systemChangeRequestsTableContents = systemChangeRequests.slice()
            .filter(a => a.managementTimeSpentMonthFte > 0)
            .sort((a, b) => ((a.managementTimeSpentMonthFte < b.managementTimeSpentMonthFte) ? 1 : ((a.managementTimeSpentMonthFte > b.managementTimeSpentMonthFte) ? -1 : 0)))
            .map(systemChangeRequestsTaskTimeSpent => (
                    {
                        id: systemChangeRequestsTaskTimeSpent.id,
                        incidentId: systemChangeRequestsTaskTimeSpent.systemChangeRequest.id,
                        incidentKey: systemChangeRequestsTaskTimeSpent.systemChangeRequest.key,
                        incidentUrl: systemChangeRequestsTaskTimeSpent.systemChangeRequest.url,
                        incidentName: systemChangeRequestsTaskTimeSpent.systemChangeRequest.name,
                        projectTeamId: systemChangeRequestsTaskTimeSpent.systemChangeRequest.changeRequest.projectTeam.id,
                        projectTeamName: systemChangeRequestsTaskTimeSpent.systemChangeRequest.changeRequest.projectTeam.name,
                        managementTimeSpentMonthFte: systemChangeRequestsTaskTimeSpent.managementTimeSpentMonthFte,
                    }
            ))

        const systemChangeRequestsTableColumns = [
            {
                field: 'projectTeamName',
                headerName: 'Команда проекта',
                flex: 1,
                renderCell: (params) => (
                    <RouterLink to={ `/projectTeams/${ params.getValue(params.id, 'projectTeamId') }` }>
                        { params.getValue(params.id, 'projectTeamName') }
                    </RouterLink>
                ),
            },
            {
                field: 'systemChangeRequestName',
                headerName: 'Заявка на доработку ПО',
                flex: 1,
                renderCell: (params) => (
                    <Link href={ params.getValue(params.id, 'incidentUrl') } target="_blank">
                        { params.getValue(params.id, 'incidentName') }
                    </Link>
                ),
            },
            {
                field: 'managementTimeSpentMonthFte',
                headerName: 'Трудомощность - управление, FTE',
                width: 200,
                align: 'right',
                valueFormatter: ({ value }) => value.toLocaleString(undefined, { maximumFractionDigits: 3}) ,
            },
        ];


        const nonProjectActivitiesTableContents = nonProjectActivities.slice()
            .filter(a => a.timeSpentMonthFte > 0)
            .sort((a, b) => ((a.timeSpentMonthFte < b.timeSpentMonthFte) ? 1 : ((a.timeSpentMonthFte > b.timeSpentMonthFte) ? -1 : 0)))
            .map(nonProjectActivityTaskTimeSpent => (
                    {
                        id: nonProjectActivityTaskTimeSpent.id,
                        nonProjectActivityId: nonProjectActivityTaskTimeSpent.nonProjectActivity.id,
                        nonProjectActivityKey: nonProjectActivityTaskTimeSpent.nonProjectActivity.key,
                        nonProjectActivityUrl: nonProjectActivityTaskTimeSpent.nonProjectActivity.url,
                        nonProjectActivityName: nonProjectActivityTaskTimeSpent.nonProjectActivity.name,
                        timeSpentMonthFte: nonProjectActivityTaskTimeSpent.timeSpentMonthFte,
                    }
            ))

        const nonProjectActivitiesTableColumns = [
            {
                field: 'nonProjectActivityName',
                headerName: 'Название',
                flex: 1,
                renderCell: (params) => (
                    <Link href={ params.getValue(params.id, 'nonProjectActivityUrl') } target="_blank">
                        { params.getValue(params.id, 'nonProjectActivityName') }
                    </Link>
                ),
            },
            {
                field: 'timeSpentMonthFte',
                headerName: 'Трудомощность, FTE',
                width: 200,
                align: 'right',
                valueFormatter: ({ value }) => value.toLocaleString(undefined, { maximumFractionDigits: 3}) ,
            },
        ];

        const tasksTableContents = tasks.slice()
            .filter(a => a.timeSpentMonthFte > 0)
            .sort((a, b) => ((a.timeSpentMonthFte < b.timeSpentMonthFte) ? 1 : ((a.timeSpentMonthFte > b.timeSpentMonthFte) ? -1 : 0)))
            .map(personTaskTimeSpent => (
                    {
                        id: personTaskTimeSpent.id,
                        taskId: personTaskTimeSpent.task.id,
                        taskKey: personTaskTimeSpent.task.key,
                        taskUrl: personTaskTimeSpent.task.url,
                        taskName: personTaskTimeSpent.task.name,
                        systemChangeRequestId: personTaskTimeSpent.task.systemChangeRequest.id,
                        systemChangeRequestKey: personTaskTimeSpent.task.systemChangeRequest.key,
                        systemChangeRequestName: personTaskTimeSpent.task.systemChangeRequest.name,
                        changeRequestId: personTaskTimeSpent.task.systemChangeRequest.changeRequest.id,
                        changeRequestKey: personTaskTimeSpent.task.systemChangeRequest.changeRequest.key,
                        changeRequestName: personTaskTimeSpent.task.systemChangeRequest.changeRequest.name,
                        projectTeamId: personTaskTimeSpent.task.systemChangeRequest.changeRequest.projectTeam.id,
                        projectTeamName: personTaskTimeSpent.task.systemChangeRequest.changeRequest.projectTeam.name,
                        timeSpentMonthFte: personTaskTimeSpent.timeSpentMonthFte,
                    }
            ))

        const tasksTableColumns = [
            {
                field: 'projectTeamName',
                headerName: 'Команда проекта',
                flex: 1,
                renderCell: (params) => (
                    <RouterLink to={ `/projectTeams/${ params.getValue(params.id, 'projectTeamId') }` }>
                        { params.getValue(params.id, 'projectTeamName') }
                    </RouterLink>
                ),
            },
            {
                field: 'changeRequestName',
                headerName: 'Заявка на доработку ПО',
                flex: 1,
                renderCell: (params) => (
                    <RouterLink to={ `/changeRequests/${ params.getValue(params.id, 'changeRequestKey') }` }>
                        { params.getValue(params.id, 'changeRequestName') }
                    </RouterLink>
                ),
            },
            {
                field: 'systemChangeRequestName',
                headerName: 'Заявка на доработку системы',
                flex: 1,
                renderCell: (params) => (
                    <RouterLink to={ `/systemChangeRequests/${ params.getValue(params.id, 'systemChangeRequestKey') }` }>
                        { params.getValue(params.id, 'systemChangeRequestName') }
                    </RouterLink>
                ),
            },
            {
                field: 'taskName',
                headerName: 'Задача',
                flex: 1,
                renderCell: (params) => (
                    <Link href={ params.getValue(params.id, 'taskUrl') } target="_blank">
                        { params.getValue(params.id, 'taskName') }
                    </Link>
                ),
            },
            {
                field: 'timeSpentMonthFte',
                headerName: 'Трудомощность, FTE',
                width: 200,
                align: 'right',
                valueFormatter: ({ value }) => value.toLocaleString(undefined, { maximumFractionDigits: 3}) ,
            },
        ];

        return (
            <Box>
                <Typography variant="body" noWrap>
                    Сотрудник { personName } <br />
                    FTE: { timeSpentMonthFte.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2}) } <br />
                    - аналитика: { analysisTimeSpentMonthFte.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2}) } <br />
                    - разработка: { developmentTimeSpentMonthFte.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2}) } <br />
                    - тестирование: { testingTimeSpentMonthFte.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2}) } <br />
                    - управление: { managementTimeSpentMonthFte.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2}) } <br />
                    - инциденты: { incidentFixingTimeSpentMonthFte.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2}) } <br />
                    - непроизводственная деятельность: { nonProjectActivityTimeSpentMonthFte.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2}) } <br />
                </Typography>

                <br />

                <Typography variant="h6" noWrap>
                   Списания на задачи
                </Typography>
                <div>
                    <DataGridPro
                        rows={ tasksTableContents }
                        columns={ tasksTableColumns }
                        autoHeight
                    />
                </div>

                <br />
                <br />

                <Typography variant="h6" noWrap>
                   Списание на управление в заявках на доработку систем
                </Typography>
                <div>
                    <DataGridPro
                        rows={ systemChangeRequestsTableContents }
                        columns={ systemChangeRequestsTableColumns }
                        autoHeight
                    />
                </div>

                <br />
                <br />

                <Typography variant="h6" noWrap>
                   Списания на инциденты
                </Typography>

                <div>
                    <DataGridPro
                        rows={ incidentsTableContents }
                        columns={ incidentsTableColumns }
                        autoHeight
                    />
                </div>

                <br />
                <br />

                <Typography variant="h6" noWrap>
                   Списания на непроизводственную (текущую) деятельность
                </Typography>

                <div>
                    <DataGridPro
                        rows={ nonProjectActivitiesTableContents }
                        columns={ nonProjectActivitiesTableColumns }
                        autoHeight
                    />
                </div>

                <br />
                <br />
            </Box>
        );
    }
}

export default graphql(fetchPersonMonthByPersonKeyAndMonth, {
    options: (props) => { return { variables: { personKey: props.match.params.personKey, month: props.match.params.month }}}
})(PersonMonthDetailByPersonKeyAndMonth);
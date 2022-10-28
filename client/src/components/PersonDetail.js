import React, {Component} from "react";
import {gql} from '@apollo/client';
import { graphql } from '@apollo/client/react/hoc';
import Typography from '@material-ui/core/Typography';
import {Box, Link} from "@material-ui/core";
import TimeSheetsByDateIssueChart from "./TimeSheetsByDateIssueChart";
import {Link as RouterLink} from "react-router-dom";
import {DataGridPro} from "@mui/x-data-grid-pro";

const fetchPersonByKey = gql`
    query PersonByKey($key: String!) {
          personByKey(key: $key) {
               id
               name
                
               analysisTimeSpentChrononFte
               developmentTimeSpentChrononFte
               testingTimeSpentChrononFte
               managementTimeSpentChrononFte
               incidentFixingTimeSpentChrononFte
               nonProjectActivityTimeSpentChrononFte
               timeSpentChrononFte
               
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
                    timeSpentChrononFte          
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
                    managementTimeSpentChrononFte          
               }
        
               nonProjectActivities {
                    id
                    nonProjectActivity {
                        id
                        key
                        url
                        name

                    }
                    timeSpentChrononFte          
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
                    timeSpentChrononFte          
               }
               chrononStartDate
               chrononEndDate
          }
    }
`;

class PersonDetail extends Component {
    render() {
        if (this.props.data.loading) { return <div>Loading ...</div> }
        const personKey = this.props.match.params.key
        const person = this.props.data.personByKey

        const personName = person.name

        const analysisTimeSpentChrononFte = person.analysisTimeSpentChrononFte
        const developmentTimeSpentChrononFte = person.developmentTimeSpentChrononFte
        const testingTimeSpentChrononFte = person.testingTimeSpentChrononFte
        const managementTimeSpentChrononFte = person.managementTimeSpentChrononFte
        const incidentFixingTimeSpentChrononFte = person.incidentFixingTimeSpentChrononFte
        const nonProjectActivityTimeSpentChrononFte = person.nonProjectActivityTimeSpentChrononFte
        const timeSpentChrononFte = person.timeSpentChrononFte

        const chrononStartDate = person.chrononStartDate
        const chrononEndDate = person.chrononEndDate

        const tasks = person.tasks
        const incidents = person.incidents
        const nonProjectActivities = person.nonProjectActivities
        const systemChangeRequests = person.systemChangeRequests

        const incidentsTableContents = incidents.slice()
            .filter(a => a.timeSpentChrononFte > 0)
            .sort((a, b) => ((a.timeSpentChrononFte < b.timeSpentChrononFte) ? 1 : ((a.timeSpentChrononFte > b.timeSpentChrononFte) ? -1 : 0)))
            .map(incidentTaskTimeSpent => (
                    {
                        id: incidentTaskTimeSpent.id,
                        incidentId: incidentTaskTimeSpent.incident.id,
                        incidentKey: incidentTaskTimeSpent.incident.key,
                        incidentUrl: incidentTaskTimeSpent.incident.url,
                        incidentName: incidentTaskTimeSpent.incident.name,
                        projectTeamId: incidentTaskTimeSpent.incident.projectTeam.id,
                        projectTeamName: incidentTaskTimeSpent.incident.projectTeam.name,
                        timeSpentChrononFte: incidentTaskTimeSpent.timeSpentChrononFte,
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
                field: 'timeSpentChrononFte',
                headerName: 'Трудомощность, FTE',
                width: 200,
                align: 'right',
                valueFormatter: ({ value }) => value.toLocaleString(undefined, { maximumFractionDigits: 3}) ,
            },
        ];

      const systemChangeRequestsTableContents = systemChangeRequests.slice()
            .filter(a => a.managementTimeSpentChrononFte > 0)
            .sort((a, b) => ((a.managementTimeSpentChrononFte < b.managementTimeSpentChrononFte) ? 1 : ((a.managementTimeSpentChrononFte > b.managementTimeSpentChrononFte) ? -1 : 0)))
            .map(systemChangeRequestsTaskTimeSpent => (
                    {
                        id: systemChangeRequestsTaskTimeSpent.id,
                        incidentId: systemChangeRequestsTaskTimeSpent.systemChangeRequest.id,
                        incidentKey: systemChangeRequestsTaskTimeSpent.systemChangeRequest.key,
                        incidentUrl: systemChangeRequestsTaskTimeSpent.systemChangeRequest.url,
                        incidentName: systemChangeRequestsTaskTimeSpent.systemChangeRequest.name,
                        projectTeamId: systemChangeRequestsTaskTimeSpent.systemChangeRequest.changeRequest.projectTeam.id,
                        projectTeamName: systemChangeRequestsTaskTimeSpent.systemChangeRequest.changeRequest.projectTeam.name,
                        managementTimeSpentChrononFte: systemChangeRequestsTaskTimeSpent.managementTimeSpentChrononFte,
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
                field: 'managementTimeSpentChrononFte',
                headerName: 'Трудомощность - управление, FTE',
                width: 200,
                align: 'right',
                valueFormatter: ({ value }) => value.toLocaleString(undefined, { maximumFractionDigits: 3}) ,
            },
        ];


        const nonProjectActivitiesTableContents = nonProjectActivities.slice()
            .filter(a => a.timeSpentChrononFte > 0)
            .sort((a, b) => ((a.timeSpentChrononFte < b.timeSpentChrononFte) ? 1 : ((a.timeSpentChrononFte > b.timeSpentChrononFte) ? -1 : 0)))
            .map(nonProjectActivityTaskTimeSpent => (
                    {
                        id: nonProjectActivityTaskTimeSpent.id,
                        nonProjectActivityId: nonProjectActivityTaskTimeSpent.nonProjectActivity.id,
                        nonProjectActivityKey: nonProjectActivityTaskTimeSpent.nonProjectActivity.key,
                        nonProjectActivityUrl: nonProjectActivityTaskTimeSpent.nonProjectActivity.url,
                        nonProjectActivityName: nonProjectActivityTaskTimeSpent.nonProjectActivity.name,
                        timeSpentChrononFte: nonProjectActivityTaskTimeSpent.timeSpentChrononFte,
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
                field: 'timeSpentChrononFte',
                headerName: 'Трудомощность, FTE',
                width: 200,
                align: 'right',
                valueFormatter: ({ value }) => value.toLocaleString(undefined, { maximumFractionDigits: 3}) ,
            },
        ];

        const tasksTableContents = tasks.slice()
            .filter(a => a.timeSpentChrononFte > 0)
            .sort((a, b) => ((a.timeSpentChrononFte < b.timeSpentChrononFte) ? 1 : ((a.timeSpentChrononFte > b.timeSpentChrononFte) ? -1 : 0)))
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
                        timeSpentChrononFte: personTaskTimeSpent.timeSpentChrononFte,
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
                field: 'timeSpentChrononFte',
                headerName: 'Трудомощность, FTE',
                width: 200,
                align: 'right',
                valueFormatter: ({ value }) => value.toLocaleString(undefined, { maximumFractionDigits: 3}) ,
            },
        ];

        return (
            <Box>
                <Typography variant="body" noWrap>
                    Сотрудник { personName } данные за период с {chrononStartDate} по {chrononEndDate} <br />
                    FTE: { timeSpentChrononFte.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2}) } <br />
                    - аналитика: { analysisTimeSpentChrononFte.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2}) } <br />
                    - разработка: { developmentTimeSpentChrononFte.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2}) } <br />
                    - тестирование: { testingTimeSpentChrononFte.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2}) } <br />
                    - управление: { managementTimeSpentChrononFte.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2}) } <br />
                    - инциденты: { incidentFixingTimeSpentChrononFte.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2}) } <br />
                    - непроизводственная деятельность: { nonProjectActivityTimeSpentChrononFte.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2}) } <br />
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

export default graphql(fetchPersonByKey, {
    options: (props) => { return { variables: { key: props.match.params.key }}}
})(PersonDetail);
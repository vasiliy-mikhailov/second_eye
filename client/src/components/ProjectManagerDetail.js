import React from "react";
import {gql, useQuery} from '@apollo/client';
import Typography from '@material-ui/core/Typography';
import {Box} from "@material-ui/core";
import {Link as RouterLink, useParams} from "react-router-dom";
import {DataGridPro, GridToolbarContainer, GridToolbarExport} from "@mui/x-data-grid-pro";

const fetchProjectManagerById = gql`
            query ProjectManagerById($id: Int) {
                projectManagerById(id: $id) {
                    id
                    
                    name
                    
                    isActive
                    
                    months {
                        id
                        month
                        timeSpentFte
                        
                        analysisTimeSpentFte
                        developmentTimeSpentFte
                        testingTimeSpentFte
                        managementTimeSpentFte
                        incidentFixingTimeSpentFte
                        nonProjectActivityTimeSpentFte
                        
                        workingDaysInMonthOccured
                    }
                    
                    projectTeams {
                        id
                        name
                        timeSpentChrononFte
                    }
                }
            }
`;

function ToolBarWithExport() {
    return (
        <GridToolbarContainer>
            <GridToolbarExport
                csvOptions={{
                    delimiter: ";",
                    utf8WithBom: true,
                }}
            />


        </GridToolbarContainer>
    );
}

function ProjectManagerDetail() {
    const {id} = useParams();
    const {loading, error, data} = useQuery(fetchProjectManagerById, {
        variables: {id: id}
    });

    if (loading) return 'Loading ...'

    if (error) return `Error! ${error.message}`

    const projectManager = data.projectManagerById
    const months = projectManager.months
    const projectTeams = projectManager.projectTeams

    const monthsTableContents = months.slice()
        .sort((a, b) => ((a.month < b.month) ? 1 : ((a.month > b.month) ? -1 : 0)))
        .map(month => (
            {
                id: month.id,
                month: month.month,
                timeSpentFte: month.timeSpentFte,
                analysisTimeSpentFte: month.analysisTimeSpentFte,
                developmentTimeSpentFte: month.developmentTimeSpentFte,
                testingTimeSpentFte: month.testingTimeSpentFte,
                managementTimeSpentFte: month.managementTimeSpentFte,
                incidentFixingTimeSpentFte: month.incidentFixingTimeSpentFte,
                nonProjectActivityTimeSpentFte: month.nonProjectActivityTimeSpentFte,
                workingDaysInMonthOccured: month.workingDaysInMonthOccured,
            }
        ))

    const monthsTableColumns = [
        {
            field: 'month',
            headerName: 'Год-месяц',
            width: 200,
        },
        {
            field: 'timeSpentFte',
            headerName: 'Трудозатраты (FTE)',
            width: 200,
            align: 'right',
            valueFormatter: ({value}) => value.toLocaleString(undefined, {
                minimumFractionDigits: 2,
                maximumFractionDigits: 2
            }),
        },
        {
            field: 'analysisTimeSpentFte',
            headerName: 'Трудозатраты аналитики (FTE)',
            width: 200,
            align: 'right',
            valueFormatter: ({value}) => value.toLocaleString(undefined, {
                minimumFractionDigits: 2,
                maximumFractionDigits: 2
            }),
        },
        {
            field: 'developmentTimeSpentFte',
            headerName: 'Трудозатраты разработки (FTE)',
            width: 200,
            align: 'right',
            valueFormatter: ({value}) => value.toLocaleString(undefined, {
                minimumFractionDigits: 2,
                maximumFractionDigits: 2
            }),
        },
        {
            field: 'testingTimeSpentFte',
            headerName: 'Трудозатраты тестирования (FTE)',
            width: 200,
            align: 'right',
            valueFormatter: ({value}) => value.toLocaleString(undefined, {
                minimumFractionDigits: 2,
                maximumFractionDigits: 2
            }),
        },
        {
            field: 'managementTimeSpentFte',
            headerName: 'Трудозатраты управление (FTE)',
            width: 200,
            align: 'right',
            valueFormatter: ({value}) => value.toLocaleString(undefined, {
                minimumFractionDigits: 2,
                maximumFractionDigits: 2
            }),
        },
        {
            field: 'incidentFixingTimeSpentFte',
            headerName: 'Трудозатраты инциденты (FTE)',
            width: 200,
            align: 'right',
            valueFormatter: ({value}) => value.toLocaleString(undefined, {
                minimumFractionDigits: 2,
                maximumFractionDigits: 2
            }),
        },
        {
            field: 'nonProjectActivityTimeSpentFte',
            headerName: 'Непроизводственная (текущая) деятельность (FTE)',
            width: 200,
            align: 'right',
            valueFormatter: ({value}) => value.toLocaleString(undefined, {
                minimumFractionDigits: 2,
                maximumFractionDigits: 2
            }),
        },
        {
            field: 'workingDaysInMonthOccured',
            headerName: 'Рабочих дней в месяце',
            width: 200,
            align: 'right',
            valueFormatter: ({value}) => value.toLocaleString(undefined, {
                minimumFractionDigits: 2,
                maximumFractionDigits: 2
            }),
        },
    ];

    const projectTeamsTableContents = projectTeams.slice()
        .sort((a, b) => ((a.timeSpentChrononFte < b.timeSpentChrononFte) ? 1 : ((a.timeSpentChrononFte > b.timeSpentChrononFte) ? -1 : 0)))
        .map(projectTeam => (
            {
                id: projectTeam.id,
                name: projectTeam.name,
                timeSpentChrononFte: projectTeam.timeSpentChrononFte,
            }
        ))

    const projectTeamsTableColumns = [
        {
            field: 'name',
            flex: 1,
            headerName: 'Название',
            renderCell: (params) => (
                <RouterLink to={`/projectTeams/${params.getValue(params.id, 'id')}`}>
                    {params.getValue(params.id, 'name')}
                </RouterLink>
            ),
        },
        {
            field: 'timeSpentChrononFte',
            headerName: 'Трудомощность, FTE',
            width: 200,
            align: 'right',
            valueFormatter: ({value}) => value.toLocaleString(undefined, {
                minimumFractionDigits: 2,
                maximumFractionDigits: 2
            }),
        },
    ];

    return (
        <Box>
            <Typography variant="h6" noWrap>
                Трудозатраты по месяцам
            </Typography>
            <div>
                <DataGridPro
                    rows={monthsTableContents}
                    columns={monthsTableColumns}
                    components={{
                        Toolbar: ToolBarWithExport,
                    }}
                    autoHeight
                />
            </div>
            <br/>
            <br/>

            <Typography variant="h6" noWrap>
                Команды
            </Typography>
            <div>
                <DataGridPro
                    rows={projectTeamsTableContents}
                    columns={projectTeamsTableColumns}
                    components={{
                        Toolbar: ToolBarWithExport,
                    }}
                    autoHeight
                />
            </div>
        </Box>
    );
}

export default ProjectManagerDetail;
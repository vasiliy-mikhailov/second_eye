import React from "react";
import {gql, useQuery} from '@apollo/client';
import Typography from '@material-ui/core/Typography';
import {Box} from "@material-ui/core";
import {Link as RouterLink} from "react-router-dom";
import {DataGridPro, GridToolbarContainer, GridToolbarExport,} from '@mui/x-data-grid-pro';

const fetchProjectTeams = gql`
    query ProjectTeams {
        projectTeams {
            id
            estimate
            timeLeft
            name
            calculatedFinishDate
            timeSpentChrononFte
            queueLength
            positionPersonPlanFactIssueCount
            
            projectManager {
                id
                name
            }
            
            dedicatedTeam {
                id
                name
                
                cio {
                    id
                    name
                }
                cto {
                    id
                    name
                }                   
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

function ProjectTeamList() {
    const {loading, error, data} = useQuery(fetchProjectTeams);

    if (loading) return 'Loading ...'

    if (error) return `Error! ${error.message}`

    const projectTeams = data.projectTeams

    const projectTeamsTableContents = projectTeams.slice()
        .sort((a, b) => ((a.name > b.name) ? 1 : ((a.name < b.name) ? -1 : 0)))
        .map(projectTeam => (
            {
                id: projectTeam.id,
                name: projectTeam.name,
                projectManagerName: projectTeam.projectManager.name,
                cioName: projectTeam.dedicatedTeam.cio.name,
                ctoName: projectTeam.dedicatedTeam.cto.name,
                positionPersonPlanFactIssueCount: projectTeam.positionPersonPlanFactIssueCount,
                timeSpentChrononFte: projectTeam.timeSpentChrononFte,
            }
        ))

    const projectTeamsTableColumns = [
        {
            field: 'name',
            headerName: 'Название',
            flex: 1,
            renderCell: (params) => (
                <RouterLink to={`/projectTeams/${params.getValue(params.id, 'id')}`}>
                    {params.getValue(params.id, 'name')}
                </RouterLink>
            ),
        },
        {
            field: 'projectManagerName',
            headerName: 'Руководитель проекта',
            flex: 1,
        },
        {
            field: 'cioName',
            headerName: 'Бизнес-партнер',
            flex: 1,
        },
        {
            field: 'ctoName',
            headerName: 'Руководитель разработки (CTO)',
            flex: 1,
        },
        {
            field: 'timeSpentChrononFte',
            headerName: 'FTE команды',
            width: 200,
            align: 'right',
            valueFormatter: ({value}) => (value).toLocaleString(undefined, {
                minimumFractionDigits: 2,
                maximumFractionDigits: 2
            }),
        },
        {
            field: 'positionPersonPlanFactIssueCount',
            headerName: 'Количество проблем с планированием команды (количество членов команды разницей между планом и фактом > 0.4 FTE)',
            width: 200,
            align: 'right',
        },
    ];

    return (
        <Box>
            <Typography variant="h6" noWrap>
                Проектные команды
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

export default ProjectTeamList;
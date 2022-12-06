import React from "react";
import {gql, useQuery} from '@apollo/client';
import Typography from '@material-ui/core/Typography';
import {Box, Link} from "@material-ui/core";
import {Link as RouterLink, useParams} from "react-router-dom";
import {DataGridPro,} from '@mui/x-data-grid-pro';

const fetchPlanningPeriodById = gql`
    query PlanningPeriodByIdQuery($id: Int!) {
        planningPeriodById(id: $id) {
            name
            projectTeamPlanningPeriods {
                id
                projectTeam {
                    id
                    name
                    projectManager {
                      id
                      name
                    }
                    dedicatedTeam {
                      id
                      name
                    }
                }
                effortPerFunctionPoint
                functionPoints
            }
        }
    }
`;

function PlanningPeriodProjectTeamsList() {
    const {planningPeriodId} = useParams();
    const {
        loading,
        error,
        data
    } = useQuery(fetchPlanningPeriodById, {
        variables: {id: planningPeriodId}
    });

    if (loading) return 'Loading ...'

    if (error) return `Error! ${error.message}`

    const planningPeriodById = data.planningPeriodById

    const planningPeriodName = planningPeriodById.name

    const projectTeamPlanningPeriods = planningPeriodById.projectTeamPlanningPeriods

    const projectTeamsTableContents = projectTeamPlanningPeriods.slice()
        .sort((a, b) => ((a.projectTeam.name > b.projectTeam.name) ? 1 : ((a.projectTeam.name < b.projectTeam.name) ? -1 : 0)))
        .map(projectTeamPlanningPeriod => (
            {
                id: projectTeamPlanningPeriod.id,
                projectTeamId: projectTeamPlanningPeriod.projectTeam.id,
                projectTeamName: projectTeamPlanningPeriod.projectTeam.name,
                projectManagerName: projectTeamPlanningPeriod.projectTeam.projectManager.name,
                effortPerFunctionPoint: projectTeamPlanningPeriod.effortPerFunctionPoint,
                functionPoints: projectTeamPlanningPeriod.functionPoints,
            }
        ))

    const projectTeamsTableColumns = [
        {
            field: 'projectTeamName',
            headerName: 'Название',
            flex: 1,
            renderCell: (params) => (
                <RouterLink
                    to={`/planningPeriods/${planningPeriodId}/projectTeams/${params.getValue(params.id, 'projectTeamId')}`}>
                    {params.getValue(params.id, 'projectTeamName')}
                </RouterLink>
            ),
        },
        {
            field: 'projectManagerName',
            headerName: 'Руководитель проекта',
            flex: 1,
        },
        {
            field: 'effortPerFunctionPoint',
            headerName: 'Затраты на ф.т.',
            width: 200,
            align: 'right',
            valueFormatter: ({value}) => value.toLocaleString(undefined, {
                minimumFractionDigits: 2,
                maximumFractionDigits: 2
            }),
        },
        {
            field: 'functionPoints',
            headerName: 'Функциональных точек (шт)',
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
                Проектные команды
            </Typography>

            <div>
                <DataGridPro
                    rows={projectTeamsTableContents}
                    columns={projectTeamsTableColumns}
                    autoHeight
                />
            </div>
        </Box>
    );
}

export default PlanningPeriodProjectTeamsList;
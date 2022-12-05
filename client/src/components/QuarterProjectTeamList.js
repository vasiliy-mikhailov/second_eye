import React from "react";
import {gql, useQuery} from '@apollo/client';
import Typography from '@material-ui/core/Typography';
import {Box} from "@material-ui/core";
import {Link as RouterLink, useParams} from "react-router-dom";
import {DataGridPro,} from '@mui/x-data-grid-pro';

const fetchQuarterProjectTeamsByQuarterKey = gql`
    query QuarterProjectTeamsByQuarterKey($quarterKey: String!) {
        quarterProjectTeamsByQuarterKey(quarterKey: $quarterKey) {
            id
            estimate
            timeLeft
            
            calculatedFinishDate
            timeSpentChrononFte
            timeSpentChronon
            timeSpentInCurrentQuarterForQuarterChangeRequestsShare
            changeRequestCalculatedDateAfterQuarterEndIssueCount
            changeRequestCount
            changeRequestCalculatedDateBeforeQuarterEndShare
        
            projectTeam {
                id
                name
                timeSpentChrononFte
                projectManager {
                    id
                    name
                }

                dedicatedTeam {
                    id
                    name
                    
                    cio {
                        id
                        key
                        name
                    }
                    cto {
                        id
                        key
                        name
                    }                   
                }
            }
        }
    }
`;

function QuarterProjectTeamList() {
    const {quarterKey} = useParams();
    const {loading, error, data} = useQuery(fetchQuarterProjectTeamsByQuarterKey, {
        variables: {quarterKey: quarterKey}
    });

    if (loading) return 'Loading ...'

    if (error) return `Error! ${error.message}`

    const quarterProjectTeams = data.quarterProjectTeamsByQuarterKey

    const quarterProjectTeamsTableContents = quarterProjectTeams.slice()
        .sort((a, b) => ((a.projectTeam.name > b.projectTeam.name) ? 1 : ((a.projectTeam.name < b.projectTeam.name) ? -1 : 0)))
        .map(projectTeamQuarter => (
            {
                id: projectTeamQuarter.id,
                projectTeamId: projectTeamQuarter.projectTeam.id,
                name: projectTeamQuarter.projectTeam.name,
                projectManagerName: projectTeamQuarter.projectTeam.projectManager.name,
                cioName: projectTeamQuarter.projectTeam.dedicatedTeam.cio.name,
                ctoName: projectTeamQuarter.projectTeam.dedicatedTeam.cto.name,
                changeRequestCalculatedDateAfterQuarterEndIssueCount: projectTeamQuarter.changeRequestCalculatedDateAfterQuarterEndIssueCount,
                projectTeamQuartertimeSpentChrononFte: projectTeamQuarter.timeSpentChrononFte,
                projectTeamtimeSpentChrononFte: projectTeamQuarter.projectTeam.timeSpentChrononFte,
                changeRequestCalculatedDateBeforeQuarterEndShare: projectTeamQuarter.changeRequestCalculatedDateBeforeQuarterEndShare,
                timeSpentInCurrentQuarterForQuarterChangeRequestsShare: projectTeamQuarter.timeSpentInCurrentQuarterForQuarterChangeRequestsShare
            }
        ))

    const quarterProjectTeamsTableColumns = [
        {
            field: 'name',
            headerName: 'Название',
            flex: 1,
            renderCell: (params) => (
                <RouterLink to={`/quarters/${quarterKey}/projectTeams/${params.getValue(params.id, 'projectTeamId')}`}>
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
            field: 'changeRequestCalculatedDateBeforeQuarterEndShare',
            headerName: 'Прогноз исполнения плана по заявкам на доработку ПО (%)',
            width: 200,
            align: 'right',
            valueFormatter: ({value}) => (value * 100).toLocaleString(undefined, {maximumFractionDigits: 0}),
        },
        {
            field: 'timeSpentInCurrentQuarterForQuarterChangeRequestsShare',
            headerName: 'Процент трудозатрат на задачи квартала (%)',
            width: 200,
            align: 'right',
            valueFormatter: ({value}) => (value * 100).toLocaleString(undefined, {maximumFractionDigits: 0}),
        },
    ];

    return (
        <Box>
            <Typography variant="h6" noWrap>
                Проектные команды
            </Typography>

            <div>
                <DataGridPro
                    rows={quarterProjectTeamsTableContents}
                    columns={quarterProjectTeamsTableColumns}
                    autoHeight
                />
            </div>
        </Box>
    );
}

export default QuarterProjectTeamList;
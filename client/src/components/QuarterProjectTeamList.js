import React, {Component} from "react";
import {gql} from '@apollo/client';
import { graphql } from '@apollo/client/react/hoc';
import Typography from '@material-ui/core/Typography';
import {Box, Link} from "@material-ui/core";
import {Link as RouterLink} from "react-router-dom";
import { DataGridPro,} from '@mui/x-data-grid-pro';

const fetchQuarterProjectTeamsByQuarterKey = gql`
    query QuarterProjectTeamsByQuarterKey($quarterKey: String!) {
        quarterProjectTeamsByQuarterKey(quarterKey: $quarterKey) {
            id
            estimate
            timeLeft
            
            calculatedFinishDate
            newFunctionsFullTimeEquivalentPrevious28Days
            newFunctionsTimeSpentPrevious28Days
            newFunctionsTimeSpentInCurrentQuarterForQuarterChangeRequestsShare
            changeRequestCalculatedDateAfterQuarterEndIssueCount
            changeRequestCount
            changeRequestCalculatedDateBeforeQuarterEndShare
        
            projectTeam {
                id
                name
                newFunctionsFullTimeEquivalentPrevious28Days
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

class QuarterProjectTeamList extends Component {
    render() {
        if (this.props.data.loading) { return <div>Loading ...</div> }

        const quarterKey = this.props.match.params.quarterKey
        const quarterProjectTeams = this.props.data.quarterProjectTeamsByQuarterKey

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
                        projectTeamQuarterNewFunctionsFullTimeEquivalentPrevious28Days: projectTeamQuarter.newFunctionsFullTimeEquivalentPrevious28Days,
                        projectTeamNewFunctionsFullTimeEquivalentPrevious28Days: projectTeamQuarter.projectTeam.newFunctionsFullTimeEquivalentPrevious28Days,
                        changeRequestCalculatedDateBeforeQuarterEndShare: projectTeamQuarter.changeRequestCalculatedDateBeforeQuarterEndShare,
                        newFunctionsTimeSpentInCurrentQuarterForQuarterChangeRequestsShare: projectTeamQuarter.newFunctionsTimeSpentInCurrentQuarterForQuarterChangeRequestsShare
                    }
            ))

        const quarterProjectTeamsTableColumns = [
            {
                field: 'name',
                headerName: 'Название',
                flex: 1,
                renderCell: (params) => (
                    <RouterLink to={ `/quarters/${ quarterKey }/projectTeams/${ params.getValue(params.id, 'projectTeamId') }` }>
                        { params.getValue(params.id, 'name') }
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
                valueFormatter: ({ value }) => (value * 100).toLocaleString(undefined, { maximumFractionDigits: 0}),
            },
            {
                field: 'newFunctionsTimeSpentInCurrentQuarterForQuarterChangeRequestsShare',
                headerName: 'Процент трудозатрат на задачи квартала (%)',
                width: 200,
                align: 'right',
                valueFormatter: ({ value }) => (value * 100).toLocaleString(undefined, { maximumFractionDigits: 0}),
            },
        ];

        return (
            <Box>
                <Typography variant="h6" noWrap>
                    Проектные команды
                </Typography>

                <div>
                    <DataGridPro
                        rows={ quarterProjectTeamsTableContents }
                        columns={ quarterProjectTeamsTableColumns }
                        autoHeight
                    />
                </div>
            </Box>
        );
    }
}

export default graphql(fetchQuarterProjectTeamsByQuarterKey, {
    options: (props) => { return { variables: { quarterKey: props.match.params.quarterKey }}}
})(QuarterProjectTeamList);
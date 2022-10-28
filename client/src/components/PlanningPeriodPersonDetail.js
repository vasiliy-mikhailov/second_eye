import React, {Component} from "react";
import {gql} from '@apollo/client';
import {graphql} from '@apollo/client/react/hoc';
import moment from 'moment';
import Typography from '@material-ui/core/Typography';
import {Link as RouterLink, NavLink} from "react-router-dom"
import {Box, Link} from "@material-ui/core";
import TimeSheetsByDateIssueChart from './TimeSheetsByDateIssueChart'
import {DataGridPro, GridToolbarContainer, GridToolbarExport} from "@mui/x-data-grid-pro";

const fetchPlanningPeriodPersonByPlanningPeriodIdAndPersonKeyQuery = gql`
    query PlanningPeriodPersonByPlanningPeriodIdAndPersonKeyQuery($planningPeriodId: Int!, $personKey: String!) {
        planningPeriodPersonByPlanningPeriodIdAndPersonKey(planningPeriodId: $planningPeriodId, personKey: $personKey) {
          systemChangeRequests {
            systemChangeRequestId
            systemChangeRequestKey
            systemChangeRequestName
            newFunctionsTimeSpent
            effortPerFunctionPoint
            newFunctionsPercentageOfPersonTotalTimeInPlanningPeriod
            effortPerFunctionPointWeightedByPersonTotalTimeInPlanningPeriod
          }
        }
    }
`;

class PlanningPeriodPersonDetail extends Component {
    render() {
        if (this.props.data.loading) { return <div>Loading ...</div> }

        const planningPeriodId = this.props.match.params.planningPeriodId
        const personKey = this.props.match.params.personKey

        const systemChangeRequests = this.props.data.planningPeriodPersonByPlanningPeriodIdAndPersonKey.systemChangeRequests

        const systemChangeRequestsTableContents = systemChangeRequests.slice()
            .sort((a, b) =>  (
                (a.systemChangeRequestId > b.systemChangeRequestId) ? 1 : (
                    (a.systemChangeRequestId == b.systemChangeRequestId) ? 0 : -1
                )
            ))
            .map(systemChangeRequest => (
                    {
                        id: systemChangeRequest.systemChangeRequestId,
                        key: systemChangeRequest.systemChangeRequestKey,
                        name: systemChangeRequest.systemChangeRequestName,
                        effortPerFunctionPoint: systemChangeRequest.effortPerFunctionPoint,
                        newFunctionsPercentageOfPersonTotalTimeInPlanningPeriod: systemChangeRequest.newFunctionsPercentageOfPersonTotalTimeInPlanningPeriod,
                        effortPerFunctionPointWeightedByPersonTotalTimeInPlanningPeriod: systemChangeRequest.effortPerFunctionPointWeightedByPersonTotalTimeInPlanningPeriod,
                        newFunctionsTimeSpent: systemChangeRequest.newFunctionsTimeSpent,
                    }
            ))

            const systemChangeRequestsTableColumns = [
            {
                field: 'name',
                headerName: 'Заявка на доработку системы',
                flex: 1,
                renderCell: (params) => (
                    <RouterLink to={ `/systemChangeRequests/${ params.getValue(params.id, 'key') }` }>
                        { params.getValue(params.id, 'name') }
                    </RouterLink>
                ),
            },
            {
                field: 'effortPerFunctionPoint',
                headerName: 'Затраты на ф.т.',
                width: 200,
                align: 'right',
                valueFormatter: ({ value }) => value.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 }) ,
            },
            {
                field: 'newFunctionsPercentageOfPersonTotalTimeInPlanningPeriod',
                headerName: 'Доля времени, потраченного на доработку системы',
                width: 200,
                align: 'right',
                valueFormatter: ({ value }) => value.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 }) ,
            },
            {
                field: 'effortPerFunctionPointWeightedByPersonTotalTimeInPlanningPeriod',
                headerName: 'Затраты на ф.т. * доля времени, потраченного на доработку системы',
                width: 200,
                align: 'right',
                valueFormatter: ({ value }) => value.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 }) ,
            },
            {
                field: 'newFunctionsTimeSpent',
                headerName: 'Списано на аналитику, разработку и тестирование (ч)',
                width: 200,
                align: 'right',
                valueFormatter: ({ value }) => value.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 }) ,
                renderCell: (params) => (
                    <RouterLink to={ `/systemChangeRequests/${ params.getValue(params.id, 'key') }/persons/${ personKey }` }>
                        { params.getValue(params.id, 'newFunctionsTimeSpent').toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 }) }
                    </RouterLink>
                ),
            },
        ];

        return (
            <Box>
                <Typography variant="h6" noWrap>
                    Заявки на доработку системы
                </Typography>
                <div>
                    <DataGridPro
                        rows={ systemChangeRequestsTableContents }
                        columns={ systemChangeRequestsTableColumns }
                        autoHeight
                    />
                </div>
            </Box>
        );
    }
}

export default graphql(fetchPlanningPeriodPersonByPlanningPeriodIdAndPersonKeyQuery, {
    options: (props) => { return { variables: {
        planningPeriodId: props.match.params.planningPeriodId,
        personKey: props.match.params.personKey,
    }}}
})(PlanningPeriodPersonDetail);
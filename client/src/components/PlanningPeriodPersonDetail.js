import React from "react";
import {gql, useQuery} from '@apollo/client';
import Typography from '@material-ui/core/Typography';
import {Link as RouterLink, NavLink, useParams} from "react-router-dom"
import {Box, Link} from "@material-ui/core";
import {DataGridPro} from "@mui/x-data-grid-pro";

const fetchPlanningPeriodPersonByPlanningPeriodIdAndPersonKeyQuery = gql`
    query PlanningPeriodPersonByPlanningPeriodIdAndPersonKeyQuery($planningPeriodId: Int!, $personKey: String!) {
        planningPeriodPersonByPlanningPeriodIdAndPersonKey(planningPeriodId: $planningPeriodId, personKey: $personKey) {
          systemChangeRequests {
            systemChangeRequest {
                id
                key
                name
                effortPerFunctionPoint
            }
            functionPointsEffort
            percentageOfPersonTotalTimeInPlanningPeriod
            effortPerFunctionPointWeightedByPersonTotalTimeInPlanningPeriod
          }
        }
    }
`;

function PlanningPeriodPersonDetail() {
    const {planningPeriodId, personKey} = useParams();
    const {loading, error, data} = useQuery(fetchPlanningPeriodPersonByPlanningPeriodIdAndPersonKeyQuery, {
        variables: {planningPeriodId: planningPeriodId, personKey: personKey}
    });

    if (loading) return 'Loading ...'

    if (error) return `Error! ${error.message}`

    const systemChangeRequests = data.planningPeriodPersonByPlanningPeriodIdAndPersonKey.systemChangeRequests

    const systemChangeRequestsTableContents = systemChangeRequests.slice()
        .sort((a, b) => ((a.systemChangeRequest.id > b.systemChangeRequest.id) ? 1 : ((a.systemChangeRequest.id == b.systemChangeRequest.id) ? 0 : -1)))
        .map(systemChangeRequest => ({
                id: systemChangeRequest.systemChangeRequest.id,
                key: systemChangeRequest.systemChangeRequest.key,
                name: systemChangeRequest.systemChangeRequest.name,
                effortPerFunctionPoint: systemChangeRequest.systemChangeRequest.effortPerFunctionPoint,
                functionPointsEffort: systemChangeRequest.functionPointsEffort,
                effortPerFunctionPointWeightedByPersonTotalTimeInPlanningPeriod: systemChangeRequest.effortPerFunctionPointWeightedByPersonTotalTimeInPlanningPeriod,
                percentageOfPersonTotalTimeInPlanningPeriod: systemChangeRequest.percentageOfPersonTotalTimeInPlanningPeriod,
            }))

    const systemChangeRequestsTableColumns = [{
        field: 'name',
        headerName: 'Заявка на доработку системы',
        flex: 1,
        renderCell: (params) => (<RouterLink to={`/systemChangeRequests/${params.getValue(params.id, 'key')}`}>
                {params.getValue(params.id, 'name')}
            </RouterLink>),
    }, {
        field: 'effortPerFunctionPoint',
        headerName: 'Затраты (ч/ф.т.)',
        width: 200,
        align: 'right',
        valueFormatter: ({value}) => value.toLocaleString(undefined, {
            minimumFractionDigits: 2, maximumFractionDigits: 2
        }),
    }, {
        field: 'percentageOfPersonTotalTimeInPlanningPeriod',
        headerName: 'Доля времени от года, потраченного на доработку системы',
        width: 200,
        align: 'right',
        valueFormatter: ({value}) => value.toLocaleString(undefined, {
            minimumFractionDigits: 2, maximumFractionDigits: 2
        }),
    }, {
        field: 'effortPerFunctionPointWeightedByPersonTotalTimeInPlanningPeriod',
        headerName: 'Затраты * Доля времени от года, потраченного на доработку системы',
        width: 200,
        align: 'right',
        valueFormatter: ({value}) => value.toLocaleString(undefined, {
            minimumFractionDigits: 2, maximumFractionDigits: 2
        }),
    }, {
        field: 'functionPointsEffort',
        headerName: 'Списано на аналитику, разработку и тестирование (ч)',
        width: 200,
        align: 'right',
        valueFormatter: ({value}) => value.toLocaleString(undefined, {
            minimumFractionDigits: 2, maximumFractionDigits: 2
        }),
        renderCell: (params) => (
            <RouterLink to={`/systemChangeRequests/${params.getValue(params.id, 'key')}/persons/${personKey}`}>
                {params.getValue(params.id, 'functionPointsEffort').toLocaleString(undefined, {
                    minimumFractionDigits: 2, maximumFractionDigits: 2
                })}
            </RouterLink>),
    },];

    return (<Box>
            <Typography variant="h6" noWrap>
                Заявки на доработку системы
            </Typography>
            <div>
                <DataGridPro
                    rows={systemChangeRequestsTableContents}
                    columns={systemChangeRequestsTableColumns}
                    autoHeight
                />
            </div>
        </Box>);
}

export default PlanningPeriodPersonDetail;
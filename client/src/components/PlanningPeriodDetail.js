import React, {Component} from "react";
import {gql} from '@apollo/client';
import { graphql } from '@apollo/client/react/hoc';
import Typography from '@material-ui/core/Typography';
import {Box, Link} from "@material-ui/core";
import {Link as RouterLink} from "react-router-dom";
import TimeSheetsByDatePeriodChart from "./TimeSheetsByDatePeriodChart"
import ValueByDatePeriodChart from "./ValueByDatePeriodChart"
import { DataGridPro,} from '@mui/x-data-grid-pro';

const fetchPlanningPeriodById = gql`
    query PlanningPeriodByIdQuery($id: Int!) {
        planningPeriodById(id: $id) {
            id 
            name
            start
            end
            estimate
            effortPerFunctionPoint
            
            dedicatedTeamPlanningPeriods {
                id
                estimate
                timeLeft
                dedicatedTeam {
                    id
                    name
                }
                effortPerFunctionPoint
            }
            
            systemPlanningPeriods {
                id
                estimate
                timeLeft
                system {
                    id
                    name
                }
                effortPerFunctionPoint
            }
            
            timeSpentPercentWithValueAndWithoutValueByDate {
                date
                timeSpentWithoutValuePercentCumsum
                timeSpentWithValuePercentCumsum
            }
    
            timeSheetsByDate {
                date
                timeSpentCumsum
                timeSpentCumsumPrediction
            }
            
            timeSpentCumsumAtEndPrediction
        }
    }
`;

class PlanningPeriodDetail extends Component {
    render() {
        if (this.props.data.loading) { return <div>Loading ...</div> }

        const planningPeriodId = this.props.match.params.id
        const planningPeriod = this.props.data.planningPeriodById
        const estimate = planningPeriod.estimate
        const effortPerFunctionPoint = planningPeriod.effortPerFunctionPoint
        const planningPeriodStart = planningPeriod.start
        const planningPeriodEnd = planningPeriod.end

        const dedicatedTeamPlanningPeriods = planningPeriod.dedicatedTeamPlanningPeriods
        const systemPlanningPeriods = planningPeriod.systemPlanningPeriods

        const timeSheetsByDate = planningPeriod.timeSheetsByDate
        const timeSpentPercentWithValueAndWithoutValueByDate = planningPeriod.timeSpentPercentWithValueAndWithoutValueByDate
        const timeSpentCumsumAtEndPrediction = planningPeriod.timeSpentCumsumAtEndPrediction

        const xAxisStart = new Date(planningPeriodStart).getTime()
        const xAxisEnd = new Date(planningPeriodEnd).getTime()

        const dedicatedTeamsTableContents = dedicatedTeamPlanningPeriods.slice()
            .sort((a, b) => ((a.dedicatedTeam.name > b.dedicatedTeam.name) ? 1 : ((a.dedicatedTeam.name < b.dedicatedTeam.name) ? -1 : 0)))
            .map(dedicatedTeamPlanningPeriod => (
                    {
                        id: dedicatedTeamPlanningPeriod.id,
                        estimate: dedicatedTeamPlanningPeriod.estimate,
                        timeLeft: dedicatedTeamPlanningPeriod.timeLeft,
                        dedicatedTeamId: dedicatedTeamPlanningPeriod.dedicatedTeam.id,
                        dedicatedTeamName: dedicatedTeamPlanningPeriod.dedicatedTeam.name,
                        effortPerFunctionPoint: dedicatedTeamPlanningPeriod.effortPerFunctionPoint
                    }
            ))

        const dedicatedTeamsTableColumns = [
            {
                field: 'dedicatedTeamName',
                headerName: 'Название',
                flex: 1,
                renderCell: (params) => (
                    <RouterLink to={ `/planningPeriods/${planningPeriodId}/dedicatedTeams/${ params.getValue(params.id, 'dedicatedTeamId') }` }>
                        { params.getValue(params.id, 'dedicatedTeamName') }
                    </RouterLink>
                ),
            },
            {
                field: 'estimate',
                headerName: 'Оценка (ч)',
                width: 200,
                align: 'right',
                valueFormatter: ({ value }) => value.toLocaleString(undefined, { maximumFractionDigits: 0}),
            },
            {
                field: 'timeLeft',
                headerName: 'Осталось (ч)',
                width: 200,
                align: 'right',
                valueFormatter: ({ value }) => value.toLocaleString(undefined, { maximumFractionDigits: 0}),
            },
            {
                field: 'effortPerFunctionPoint',
                headerName: 'Затраты на ф.т.',
                width: 200,
                align: 'right',
                valueFormatter: ({ value }) => value.toLocaleString(undefined, { maximumFractionDigits: 2}),
            },
        ];

        const systemsTableContents = systemPlanningPeriods.slice()
            .sort((a, b) => ((a.system.name > b.system.name) ? 1 : ((a.system.name < b.system.name) ? -1 : 0)))
            .map(systemPlanningPeriod => (
                    {
                        id: systemPlanningPeriod.id,
                        estimate: systemPlanningPeriod.estimate,
                        timeLeft: systemPlanningPeriod.timeLeft,
                        systemId: systemPlanningPeriod.system.id,
                        systemName: systemPlanningPeriod.system.name,
                        effortPerFunctionPoint: systemPlanningPeriod.effortPerFunctionPoint
                    }
            ))

        const systemsTableColumns = [
            {
                field: 'systemName',
                headerName: 'Название',
                flex: 1,
                renderCell: (params) => (
                    <RouterLink to={ `/planningPeriods/${planningPeriodId}/systems/${ params.getValue(params.id, 'systemId') }` }>
                        { params.getValue(params.id, 'systemName') }
                    </RouterLink>
                ),
            },
            {
                field: 'estimate',
                headerName: 'Оценка (ч)',
                width: 200,
                align: 'right',
                valueFormatter: ({ value }) => value.toLocaleString(undefined, { maximumFractionDigits: 0}),
            },
            {
                field: 'timeLeft',
                headerName: 'Осталось (ч)',
                width: 200,
                align: 'right',
                valueFormatter: ({ value }) => value.toLocaleString(undefined, { maximumFractionDigits: 0}),
            },
            {
                field: 'effortPerFunctionPoint',
                headerName: 'Затраты на ф.т.',
                width: 200,
                align: 'right',
                valueFormatter: ({ value }) => value.toLocaleString(undefined, { maximumFractionDigits: 2}),
            },
        ];

        return (
            <Box>
                <Typography variant="body" noWrap>
                    Затраты на функциональную точку (аналитика + разработка + менеджмент) { effortPerFunctionPoint.toFixed(2) } часов / функциональная точка
                </Typography>


                <TimeSheetsByDatePeriodChart
                    planningPeriodEnd={ planningPeriodEnd }
                    title="Аналитика + Разработка + Тестирование"
                    xAxisStart={ xAxisStart }
                    xAxisEnd={ xAxisEnd }
                    color="black"
                    timeSheetsByDate={ timeSheetsByDate }
                    estimate={ estimate }
                    timeSpentCumsumAtEndPrediction={ timeSpentCumsumAtEndPrediction }
                />

                <ValueByDatePeriodChart
                    planningPeriodEnd={ planningPeriodEnd }
                    title="Доля списаний на задачи без бизнес-ценности"
                    xAxisStart={ xAxisStart }
                    xAxisEnd={ xAxisEnd }
                    color="black"
                    timeSpentPercentWithValueAndWithoutValueByDate={ timeSpentPercentWithValueAndWithoutValueByDate }
                />

                <br />

                <Typography variant="h6" noWrap>
                    Выделенные команды
                </Typography>

                <div>
                    <DataGridPro
                        rows={ dedicatedTeamsTableContents }
                        columns={ dedicatedTeamsTableColumns }
                        autoHeight
                    />
                </div>

                <br />

                <Typography variant="h6" noWrap>
                    Системы
                </Typography>
                <div>
                    <DataGridPro
                        rows={ systemsTableContents }
                        columns={ systemsTableColumns }
                        autoHeight
                    />
                </div>
            </Box>
        );
    }
}

export default graphql(fetchPlanningPeriodById, {
    options: (props) => { return { variables: { id: props.match.params.id }}}
})(PlanningPeriodDetail);
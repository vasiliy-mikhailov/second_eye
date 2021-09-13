import React, {Component} from "react";
import {gql} from '@apollo/client';
import { graphql } from '@apollo/client/react/hoc';
import Typography from '@material-ui/core/Typography';
import {Box, Link} from "@material-ui/core";
import {Link as RouterLink} from "react-router-dom";
import moment from "moment";
import TimeSheetsByDatePeriodChart from "./TimeSheetsByDatePeriodChart"
import {DataGrid} from "@material-ui/data-grid";

const fetchSystemPlanningPeriodByPlanningPeriodIdAndSystemId = gql`
    query SystemPlanningPeriodByPlanningPeriodIdAndSystemId($planningPeriodId: Int!, $systemId: Int!) {
          systemPlanningPeriodByPlanningPeriodIdAndSystemId(systemId: $systemId, planningPeriodId: $planningPeriodId) {
                id
                estimate
                effortPerFunctionPoint
                system {
                    name
                }
                planningPeriod {
                    name
                    start
                    end
                }
                
                analysisTimeSheetsByDate {
                    date
                    timeSpentCumsum
                    timeSpentCumsumPrediction
                }
                
                analysisTimeSpentCumsumAtEndPrediction
                
                analysisEstimate
                
                developmentTimeSheetsByDate {
                    date
                    timeSpentCumsum
                    timeSpentCumsumPrediction
                }
                
                developmentTimeSpentCumsumAtEndPrediction
                
                developmentEstimate
                
                testingTimeSheetsByDate {
                    date
                    timeSpentCumsum
                    timeSpentCumsumPrediction
                }
                
                testingTimeSpentCumsumAtEndPrediction
                
                testingEstimate

                timeSheetsByDate {
                    date
                    timeSpentCumsum
                    timeSpentCumsumPrediction
                }
                
                timeSpentCumsumAtEndPrediction
                
                systemChangeRequests {
                    id
                    estimate
                    timeLeft
                    hasValue
                    name
                    stateCategoryId
                    effortPerFunctionPoint
                }
          }
    }
`;

class SystemPlanningPeriodDetail extends Component {
    render() {
        if (this.props.data.loading) { return <div>Loading ...</div> }
        const planningPeriodId = this.props.match.params.planningPeriodId

        const systemPlanningPeriod = this.props.data.systemPlanningPeriodByPlanningPeriodIdAndSystemId

        const systemName = systemPlanningPeriod.system.name
        const estimate = systemPlanningPeriod.estimate
        const effortPerFunctionPoint = systemPlanningPeriod.effortPerFunctionPoint
        const planningPeriodName = systemPlanningPeriod.planningPeriod.name
        const planningPeriodStart = systemPlanningPeriod.planningPeriod.start
        const planningPeriodEnd = systemPlanningPeriod.planningPeriod.end
        const systemChangeRequests = systemPlanningPeriod.systemChangeRequests

        const analysisTimeSheetsByDate = systemPlanningPeriod.analysisTimeSheetsByDate
        const analysisTimeSpentCumsumAtEndPrediction = systemPlanningPeriod.analysisTimeSpentCumsumAtEndPrediction
        const analysisEstimate = systemPlanningPeriod.analysisEstimate

        const developmentTimeSheetsByDate = systemPlanningPeriod.developmentTimeSheetsByDate
        const developmentTimeSpentCumsumAtEndPrediction = systemPlanningPeriod.developmentTimeSpentCumsumAtEndPrediction
        const developmentEstimate = systemPlanningPeriod.developmentEstimate

        const testingTimeSheetsByDate = systemPlanningPeriod.testingTimeSheetsByDate
        const testingTimeSpentCumsumAtEndPrediction = systemPlanningPeriod.testingTimeSpentCumsumAtEndPrediction
        const testingEstimate = systemPlanningPeriod.testingEstimate

        const timeSheetsByDate = systemPlanningPeriod.timeSheetsByDate
        const timeSpentCumsumAtEndPrediction = systemPlanningPeriod.timeSpentCumsumAtEndPrediction

        const xAxisStart = new Date(planningPeriodStart).getTime()
        const xAxisEnd = new Date(planningPeriodEnd).getTime()

        const systemChangeRequestsTableContents = systemChangeRequests.slice()
            .sort((a, b) =>  (
                (a.stateCategoryId === 3 && b.stateCategoryId !== 3) ? 1 : (
                    (a.stateCategoryId === 3 && b.stateCategoryId === 3) ? 0 : (
                        (a.stateCategoryId !== 3 && b.stateCategoryId === 3) ? -1 : (
                            b.timeLeft - a.timeLeft
                        )
                    )
                )
            ))
            .map(systemChangeRequest => (
                    {
                        id: systemChangeRequest.id,
                        name: systemChangeRequest.name,
                        hasValue: systemChangeRequest.hasValue,
                        estimate: systemChangeRequest.estimate,
                        timeLeft: systemChangeRequest.timeLeft,
                        stateCategoryId: systemChangeRequest.stateCategoryId,
                        effortPerFunctionPoint: systemChangeRequest.effortPerFunctionPoint
                    }
            ))

        const systemChangeRequestsTableColumns = [
            {
                field: 'name',
                headerName: 'Название',
                flex: 1,
                renderCell: (params) => (
                    <RouterLink style={{ textDecoration: params.getValue(params.id, 'stateCategoryId') === 3 ? 'line-through' : 'none' }} to={ `/systemChangeRequests/${ params.getValue(params.id, 'id') }` }>
                        { params.getValue(params.id, 'id') } &nbsp;
                        { params.getValue(params.id, 'name') }
                    </RouterLink>
                ),
            },
            {
                field: 'hasValue',
                headerName: 'Есть ценность',
                width: 200,
                valueFormatter: ({ value }) => value ? "Да" : "Нет",
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
                valueFormatter: ({ value }) => value.toLocaleString(undefined, { maximumFractionDigits: 2}) ,
            },
        ];

        return (
            <Box>
                <Typography variant="body" noWrap>
                    Система { systemName }
                    <br />
                    Период планирования { planningPeriodName } ({ planningPeriodStart }-{ planningPeriodEnd })
                    <br />
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

                <TimeSheetsByDatePeriodChart
                    planningPeriodEnd={ planningPeriodEnd }
                    title="Аналитика"
                    xAxisStart={ xAxisStart }
                    xAxisEnd={ xAxisEnd }
                    color="black"
                    timeSheetsByDate={ analysisTimeSheetsByDate }
                    estimate={ analysisEstimate }
                    timeSpentCumsumAtEndPrediction={ analysisTimeSpentCumsumAtEndPrediction }
                />

                <TimeSheetsByDatePeriodChart
                    planningPeriodEnd={ planningPeriodEnd }
                    title="Разработка"
                    xAxisStart={ xAxisStart }
                    xAxisEnd={ xAxisEnd }
                    color="black"
                    timeSheetsByDate={ developmentTimeSheetsByDate }
                    estimate={ developmentEstimate }
                    timeSpentCumsumAtEndPrediction={ developmentTimeSpentCumsumAtEndPrediction }
                />

                <TimeSheetsByDatePeriodChart
                    planningPeriodEnd={ planningPeriodEnd }
                    title="Тестирование"
                    xAxisStart={ xAxisStart }
                    xAxisEnd={ xAxisEnd }
                    color="black"
                    timeSheetsByDate={ testingTimeSheetsByDate }
                    estimate={ testingEstimate }
                    timeSpentCumsumAtEndPrediction={ testingTimeSpentCumsumAtEndPrediction }
                />
               <Typography variant="h6" noWrap>
                    Заявки на доработку системы
                </Typography>
                <div style={{ height: 1200, width: '100%' }}>
                    <DataGrid
                        rows={ systemChangeRequestsTableContents }
                        columns={ systemChangeRequestsTableColumns }
                        pagination
                        autoPageSize
                    />
                </div>
            </Box>
        );
    }
}

export default graphql(fetchSystemPlanningPeriodByPlanningPeriodIdAndSystemId, {
    options: (props) => { return { variables: { planningPeriodId: props.match.params.planningPeriodId, systemId: props.match.params.systemId }}}
})(SystemPlanningPeriodDetail);
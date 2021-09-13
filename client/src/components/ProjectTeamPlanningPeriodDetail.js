import React, {Component} from "react";
import {gql} from '@apollo/client';
import { graphql } from '@apollo/client/react/hoc';
import Typography from '@material-ui/core/Typography';
import {Box, Link} from "@material-ui/core";
import {Link as RouterLink} from "react-router-dom";
import moment from "moment";
import TimeSheetsByDatePeriodChart from "./TimeSheetsByDatePeriodChart"
import ValueByDatePeriodChart from "./ValueByDatePeriodChart"
import {DataGrid} from "@material-ui/data-grid";

const fetchProjectTeamPlanningPeriodByPlanningPeriodIdAndProjectTeamId = gql`
    query ProjectTeamPlanningPeriodByPlanningPeriodIdAndProjectTeamId($planningPeriodId: Int!, $projectTeamId: Int!) {
          projectTeamPlanningPeriodByPlanningPeriodIdAndProjectTeamId(projectTeamId: $projectTeamId, planningPeriodId: $planningPeriodId) {
                id
                estimate
                effortPerFunctionPoint
                
                projectTeam {
                    name
                }
                planningPeriod {
                    name
                    start
                    end
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
                
                changeRequests {
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

class ProjectTeamPlanningPeriodDetail extends Component {
    render() {
        if (this.props.data.loading) { return <div>Loading ...</div> }

        const projectTeamPlanningPeriod = this.props.data.projectTeamPlanningPeriodByPlanningPeriodIdAndProjectTeamId
        const projectTeamName = projectTeamPlanningPeriod.projectTeam.name
        const estimate = projectTeamPlanningPeriod.estimate
        const effortPerFunctionPoint = projectTeamPlanningPeriod.effortPerFunctionPoint
        const planningPeriodName = projectTeamPlanningPeriod.planningPeriod.name
        const planningPeriodStart = projectTeamPlanningPeriod.planningPeriod.start
        const planningPeriodEnd = projectTeamPlanningPeriod.planningPeriod.end
        const changeRequests = projectTeamPlanningPeriod.changeRequests

        const timeSheetsByDate = projectTeamPlanningPeriod.timeSheetsByDate
        const timeSpentPercentWithValueAndWithoutValueByDate = projectTeamPlanningPeriod.timeSpentPercentWithValueAndWithoutValueByDate
        const timeSpentCumsumAtEndPrediction = projectTeamPlanningPeriod.timeSpentCumsumAtEndPrediction

        const xAxisStart = new Date(planningPeriodStart).getTime()
        const xAxisEnd = new Date(planningPeriodEnd).getTime()

        const changeRequestsTableContents = changeRequests.slice()
            .sort((a, b) =>  (
                (a.stateCategoryId === 3 && b.stateCategoryId !== 3) ? 1 : (
                    (a.stateCategoryId === 3 && b.stateCategoryId === 3) ? 0 : (
                        (a.stateCategoryId !== 3 && b.stateCategoryId === 3) ? -1 : (
                            b.timeLeft - a.timeLeft
                        )
                    )
                )
            ))
            .map(changeRequest => (
                    {
                        id: changeRequest.id,
                        name: changeRequest.name,
                        hasValue: changeRequest.hasValue,
                        estimate: changeRequest.estimate,
                        timeLeft: changeRequest.timeLeft,
                        stateCategoryId: changeRequest.stateCategoryId,
                        effortPerFunctionPoint: changeRequest.effortPerFunctionPoint
                    }
            ))

        const changeRequestsTableColumns = [
            {
                field: 'name',
                headerName: 'Название',
                flex: 1,
                renderCell: (params) => (
                    <RouterLink style={{ textDecoration: params.getValue(params.id, 'stateCategoryId') === 3 ? 'line-through' : 'none' }} to={ `/changeRequests/${ params.getValue(params.id, 'id') }` }>
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
                    Проектная команда { projectTeamName }
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

                <ValueByDatePeriodChart
                    planningPeriodEnd={ planningPeriodEnd }
                    title="Доля списаний на задачи без бизнес-ценности"
                    xAxisStart={ xAxisStart }
                    xAxisEnd={ xAxisEnd }
                    color="black"
                    timeSpentPercentWithValueAndWithoutValueByDate={ timeSpentPercentWithValueAndWithoutValueByDate }
                />

               <Typography variant="h6" noWrap>
                    Заявки на доработку ПО
                </Typography>
                <div style={{ height: 1200, width: '100%' }}>
                    <DataGrid
                        rows={ changeRequestsTableContents }
                        columns={ changeRequestsTableColumns }
                        pagination
                        autoPageSize
                    />
                </div>
            </Box>
        );
    }
}

export default graphql(fetchProjectTeamPlanningPeriodByPlanningPeriodIdAndProjectTeamId, {
    options: (props) => { return { variables: { planningPeriodId: props.match.params.planningPeriodId, projectTeamId: props.match.params.projectTeamId }}}
})(ProjectTeamPlanningPeriodDetail);
import React, {Component} from "react";
import {gql} from '@apollo/client';
import { graphql } from '@apollo/client/react/hoc';
import Typography from '@material-ui/core/Typography';
import {Box, Link} from "@material-ui/core";
import {Link as RouterLink} from "react-router-dom";
import TimeSheetsByDatePeriodChart from "./TimeSheetsByDatePeriodChart"
import ValueByDatePeriodChart from "./ValueByDatePeriodChart"
import { DataGridPro } from "@mui/x-data-grid-pro";

const fetchDedicatedTeamPlanningPeriodByPlanningPeriodIdAndDedicatedTeamId = gql`
        query DedicatedTeamPlanningPeriodByPlanningPeriodIdAndDedicatedTeamId($planningPeriodId: Int!, $dedicatedTeamId: Int!) {
              dedicatedTeamPlanningPeriodByPlanningPeriodIdAndDedicatedTeamId(dedicatedTeamId: $dedicatedTeamId, planningPeriodId: $planningPeriodId) {
                    id
                    estimate
                    effortPerFunctionPoint
                    dedicatedTeam {
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
                    
                    projectTeamPlanningPeriods {
                        id
                        estimate
                        timeLeft
                        projectTeam {
                            id
                            name
                        }
                        effortPerFunctionPoint
                        calculatedFinishDate
                    }
                    
                    dedicatedTeamPlanningPeriodSystems {
                        id
                        estimate
                        timeLeft
                        system {
                            id
                            name
                        }
                        effortPerFunctionPoint
                        calculatedFinishDate
                    }
                    
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

class DedicatedTeamPlanningPeriodDetail extends Component {
    render() {
        if (this.props.data.loading) { return <div>Loading ...</div> }
        const planningPeriodId = this.props.match.params.planningPeriodId
        const dedicatedTeamId = this.props.match.params.dedicatedTeamId

        const dedicatedTeamPlanningPeriod = this.props.data.dedicatedTeamPlanningPeriodByPlanningPeriodIdAndDedicatedTeamId

        const dedicatedTeamName = dedicatedTeamPlanningPeriod.dedicatedTeam.name
        const estimate = dedicatedTeamPlanningPeriod.estimate
        const effortPerFunctionPoint = dedicatedTeamPlanningPeriod.effortPerFunctionPoint
        const planningPeriodName = dedicatedTeamPlanningPeriod.planningPeriod.name
        const planningPeriodStart = dedicatedTeamPlanningPeriod.planningPeriod.start
        const planningPeriodEnd = dedicatedTeamPlanningPeriod.planningPeriod.end
        const projectTeamPlanningPeriods = dedicatedTeamPlanningPeriod.projectTeamPlanningPeriods
        const dedicatedTeamPlanningPeriodSystems = dedicatedTeamPlanningPeriod.dedicatedTeamPlanningPeriodSystems
        const changeRequests = dedicatedTeamPlanningPeriod.changeRequests

        const timeSheetsByDate = dedicatedTeamPlanningPeriod.timeSheetsByDate
        const timeSpentPercentWithValueAndWithoutValueByDate = dedicatedTeamPlanningPeriod.timeSpentPercentWithValueAndWithoutValueByDate
        const timeSpentCumsumAtEndPrediction = dedicatedTeamPlanningPeriod.timeSpentCumsumAtEndPrediction

        const xAxisStart = new Date(planningPeriodStart).getTime()
        const xAxisEnd = new Date(planningPeriodEnd).getTime()

        const systemsTableContents = dedicatedTeamPlanningPeriodSystems.slice()
            .sort((a, b) => ((a.system.name > b.system.name) ? 1 : ((a.system.name < b.system.name) ? -1 : 0)))
            .map(dedicatedTeamPlanningPeriodSystem => (
                    {
                        id: dedicatedTeamPlanningPeriodSystem.id,
                        estimate: dedicatedTeamPlanningPeriodSystem.estimate,
                        timeLeft: dedicatedTeamPlanningPeriodSystem.timeLeft,
                        systemId: dedicatedTeamPlanningPeriodSystem.system.id,
                        systemName: dedicatedTeamPlanningPeriodSystem.system.name,
                        effortPerFunctionPoint: dedicatedTeamPlanningPeriodSystem.effortPerFunctionPoint,
                        calculatedFinishDate: dedicatedTeamPlanningPeriodSystem.calculatedFinishDate
                    }
            ))

        const systemsTableColumns = [
            {
                field: 'systemName',
                headerName: 'Название',
                flex: 1,
                renderCell: (params) => (
                    <RouterLink to={ `/planningPeriods/${ planningPeriodId }/dedicatedTeams/${ dedicatedTeamId }/systems/${ params.getValue(params.id, 'systemId') }` }>
                        { params.getValue(params.id, 'systemName') }
                    </RouterLink>
                ),
            },
            {
                field: 'calculatedFinishDate',
                headerName: 'Расчетная дата завершения',
                width: 200,
                align: 'center',
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

        const projectTeamsTableContents = projectTeamPlanningPeriods.slice()
            .sort((a, b) => ((a.name > b.name) ? 1 : ((a.name < b.name) ? -1 : 0)))
            .map(projectTeamPlanningPeriod => (
                    {
                        id: projectTeamPlanningPeriod.id,
                        estimate: projectTeamPlanningPeriod.estimate,
                        timeLeft: projectTeamPlanningPeriod.timeLeft,
                        projectTeamId: projectTeamPlanningPeriod.projectTeam.id,
                        projectTeamName: projectTeamPlanningPeriod.projectTeam.name,
                        effortPerFunctionPoint: projectTeamPlanningPeriod.effortPerFunctionPoint,
                        calculatedFinishDate: projectTeamPlanningPeriod.calculatedFinishDate
                    }
            ))

        const projectTeamsTableColumns = [
            {
                field: 'projectTeamName',
                headerName: 'Название',
                flex: 1,
                renderCell: (params) => (
                    <RouterLink to={ `/planningPeriods/${planningPeriodId}/projectTeams/${ params.getValue(params.id, 'projectTeamId') }` }>
                        { params.getValue(params.id, 'projectTeamName') }
                    </RouterLink>
                ),
            },
            {
                field: 'calculatedFinishDate',
                headerName: 'Расчетная дата завершения',
                width: 200,
                align: 'center',
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
                    Выделенная команда { dedicatedTeamName }
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
                    Проектные команды
                </Typography>

                <div>
                    <DataGridPro
                        rows={ projectTeamsTableContents }
                        columns={ projectTeamsTableColumns }
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

                <br />

                <Typography variant="h6" noWrap>
                    Заявки на доработку ПО
                </Typography>
                <div>
                    <DataGridPro
                        rows={ changeRequestsTableContents }
                        columns={ changeRequestsTableColumns }
                        autoHeight
                    />
                </div>
            </Box>
        );
    }
}

export default graphql(fetchDedicatedTeamPlanningPeriodByPlanningPeriodIdAndDedicatedTeamId, {
    options: (props) => { return { variables: { planningPeriodId: props.match.params.planningPeriodId, dedicatedTeamId: props.match.params.dedicatedTeamId }}}
})(DedicatedTeamPlanningPeriodDetail);
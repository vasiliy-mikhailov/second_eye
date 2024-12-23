import React, {Component} from "react";
import {gql} from '@apollo/client';
import { graphql } from '@apollo/client/react/hoc';
import Typography from '@material-ui/core/Typography';
import {Box, Link} from "@material-ui/core";
import {Link as RouterLink} from "react-router-dom";
import TimeSheetsByDatePeriodChart from "./TimeSheetsByDatePeriodChart"
import { DataGridPro } from "@mui/x-data-grid-pro";

const fetchProjectTeamPlanningPeriodSystemByProjectTeamIdPlanningPeriodIdAndSystemId = gql`
     query ProjectTeamPlanningPeriodSystemByProjectTeamIdPlanningPeriodIdAndSystemId($projectTeamId:Int!, $planningPeriodId: Int!, $systemId: Int!) {
          projectTeamPlanningPeriodSystemByProjectTeamIdPlanningPeriodIdAndSystemId(projectTeamId: $projectTeamId, planningPeriodId: $planningPeriodId, systemId: $systemId) {
                id
                estimate
                calculatedFinishDate
                
                effortPerFunctionPoint
                system {
                    name
                }
                planningPeriod {
                    name
                    start
                    end
                }

                timeSheetsByDate {
                    date
                    timeSpentCumsum
                    timeSpentCumsumPrediction
                }
                
                systemChangeRequests {
                    id
                    key
                    estimate
                    timeLeft
                    hasValue
                    name
                    stateCategoryId
                    effortPerFunctionPoint
                    
                    mainDeveloper {
                        id
                        name
                    }
                }
          }
    }
`;

class ProjectTeamPlanningPeriodSystemDetail extends Component {
    render() {
        if (this.props.data.loading) { return <div>Loading ...</div> }
        const planningPeriodId = this.props.match.params.planningPeriodId

        const projectTeamPlanningPeriodSystem = this.props.data.projectTeamPlanningPeriodSystemByProjectTeamIdPlanningPeriodIdAndSystemId

        const systemName = projectTeamPlanningPeriodSystem.system.name
        const estimate = projectTeamPlanningPeriodSystem.estimate
        const calculatedFinishDate = projectTeamPlanningPeriodSystem.calculatedFinishDate
        const effortPerFunctionPoint = projectTeamPlanningPeriodSystem.effortPerFunctionPoint
        const planningPeriodName = projectTeamPlanningPeriodSystem.planningPeriod.name
        const planningPeriodStart = projectTeamPlanningPeriodSystem.planningPeriod.start
        const planningPeriodEnd = projectTeamPlanningPeriodSystem.planningPeriod.end
        const systemChangeRequests = projectTeamPlanningPeriodSystem.systemChangeRequests

        const timeSheetsByDate = projectTeamPlanningPeriodSystem.timeSheetsByDate

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
                        key: systemChangeRequest.key,
                        name: systemChangeRequest.name,
                        hasValue: systemChangeRequest.hasValue,
                        estimate: systemChangeRequest.estimate,
                        timeLeft: systemChangeRequest.timeLeft,
                        stateCategoryId: systemChangeRequest.stateCategoryId,
                        effortPerFunctionPoint: systemChangeRequest.effortPerFunctionPoint,
                        mainDeveloperName: systemChangeRequest.mainDeveloper.name,
                    }
            ))

        const systemChangeRequestsTableColumns = [
            {
                field: 'name',
                headerName: 'Название',
                flex: 1,
                renderCell: (params) => (
                    <RouterLink style={{ textDecoration: params.getValue(params.id, 'stateCategoryId') === 3 ? 'line-through' : 'none' }} to={ `/systemChangeRequests/${ params.getValue(params.id, 'key') }` }>
                        { params.getValue(params.id, 'key') } &nbsp;
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
                valueFormatter: ({ value }) => value.toLocaleString(undefined, { maximumFractionDigits: 0 }),
            },
            {
                field: 'timeLeft',
                headerName: 'Осталось (ч)',
                width: 200,
                align: 'right',
                valueFormatter: ({ value }) => value.toLocaleString(undefined, { maximumFractionDigits: 0 }),
            },
            {
                field: 'effortPerFunctionPoint',
                headerName: 'Затраты на ф.т.',
                width: 200,
                align: 'right',
                valueFormatter: ({ value }) => value.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 }) ,
            },
            {
                field: 'mainDeveloperName',
                headerName: 'Основной разработчик',
                width: 200,
                align: 'left',
            },
        ];

        return (
            <Box>
                <Typography variant="body" noWrap>
                    Система { systemName }<br />
                    Период планирования { planningPeriodName } ({ planningPeriodStart }-{ planningPeriodEnd })<br />
                    Затраты на функциональную точку (аналитика + разработка + менеджмент) { effortPerFunctionPoint.toFixed(2) } часов / функциональная точка<br/>
                    Расчетная дата завершения { calculatedFinishDate }
                </Typography>

                <TimeSheetsByDatePeriodChart
                    planningPeriodEnd={ planningPeriodEnd }
                    title="Фактический объем работ: Аналитика + Разработка + Тестирование"
                    xAxisStart={ xAxisStart }
                    xAxisEnd={ xAxisEnd }
                    color="black"
                    timeSheetsByDate={ timeSheetsByDate }
                    estimate={ estimate }
                    calculatedFinishDate={ calculatedFinishDate }
                />

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

export default graphql(fetchProjectTeamPlanningPeriodSystemByProjectTeamIdPlanningPeriodIdAndSystemId, {
    options: (props) => { return { variables: { projectTeamId: props.match.params.projectTeamId, planningPeriodId: props.match.params.planningPeriodId, systemId: props.match.params.systemId }}}
})(ProjectTeamPlanningPeriodSystemDetail);
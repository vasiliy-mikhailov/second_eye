import React, {Component} from "react";
import {gql} from '@apollo/client';
import { graphql } from '@apollo/client/react/hoc';
import Typography from '@material-ui/core/Typography';
import {Box, Link} from "@material-ui/core";
import {Link as RouterLink} from "react-router-dom";
import TimeSheetsByDatePeriodChart from "./TimeSheetsByDatePeriodChart"
import ReengineeringByDatePeriodChart from "./ReengineeringByDatePeriodChart"
import ValueByDatePeriodChart from "./ValueByDatePeriodChart"
import { DataGridPro } from "@mui/x-data-grid-pro";

const fetchProjectTeamPlanningPeriodByPlanningPeriodIdAndProjectTeamId = gql`
    query ProjectTeamPlanningPeriodByPlanningPeriodIdAndProjectTeamId($planningPeriodId: Int!, $projectTeamId: Int!) {
          projectTeamPlanningPeriodByPlanningPeriodIdAndProjectTeamId(projectTeamId: $projectTeamId, planningPeriodId: $planningPeriodId) {
                id
                estimate
                effortPerFunctionPoint
                calculatedFinishDate
                
                projectTeam {
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
                    timeSpentWithoutValuePercentCumsum
                    timeSpentWithValuePercentCumsum
                    timeSpentForReengineeringPercentCumsum
                    timeSpentNotForReengineeringPercentCumsum
                }
                
                projectTeamPlanningPeriodSystems {
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
                    key
                    estimate
                    timeLeft
                    hasValue
                    name
                    stateCategoryId
                    effortPerFunctionPoint
                    calculatedFinishDate
                    newFunctionsTimeSpentPrevious28Days
                }
                
                chrononPositions {
                    id
                    position {
                        id
                        url
                        name
                    }
                    person {
                        id
                        key
                        name
                    }
                    newFunctionsTimeSpent
                    newFunctionsFullTimeEquivalentPrevious28Days
                    newFunctionsFullTimeEquivalentCapacity
                }
          }
    }
`;

class ProjectTeamPlanningPeriodDetail extends Component {
    render() {
        if (this.props.data.loading) { return <div>Loading ...</div> }

        const planningPeriodId = this.props.match.params.planningPeriodId
        const projectTeamId = this.props.match.params.projectTeamId
        const projectTeamPlanningPeriod = this.props.data.projectTeamPlanningPeriodByPlanningPeriodIdAndProjectTeamId
        const projectTeamName = projectTeamPlanningPeriod.projectTeam.name
        const estimate = projectTeamPlanningPeriod.estimate
        const effortPerFunctionPoint = projectTeamPlanningPeriod.effortPerFunctionPoint
        const calculatedFinishDate = projectTeamPlanningPeriod.calculatedFinishDate
        const planningPeriodName = projectTeamPlanningPeriod.planningPeriod.name
        const planningPeriodStart = projectTeamPlanningPeriod.planningPeriod.start
        const planningPeriodEnd = projectTeamPlanningPeriod.planningPeriod.end
        const projectTeamPlanningPeriodSystems = projectTeamPlanningPeriod.projectTeamPlanningPeriodSystems
        const changeRequests = projectTeamPlanningPeriod.changeRequests
        const positions = projectTeamPlanningPeriod.positions

        const timeSheetsByDate = projectTeamPlanningPeriod.timeSheetsByDate

        const fourWeeks = 1000 * 60 * 60 * 24 * 7 * 4
        const xAxisStart = new Date(planningPeriodStart).getTime() - fourWeeks
        const xAxisEnd = new Date(planningPeriodEnd).getTime() + fourWeeks

        const systemsTableContents = projectTeamPlanningPeriodSystems.slice()
            .sort((a, b) => ((a.system.name > b.system.name) ? 1 : ((a.system.name < b.system.name) ? -1 : 0)))
            .map(projectTeamPlanningPeriodSystem => (
                    {
                        id: projectTeamPlanningPeriodSystem.id,
                        estimate: projectTeamPlanningPeriodSystem.estimate,
                        timeLeft: projectTeamPlanningPeriodSystem.timeLeft,
                        systemId: projectTeamPlanningPeriodSystem.system.id,
                        systemName: projectTeamPlanningPeriodSystem.system.name,
                        effortPerFunctionPoint: projectTeamPlanningPeriodSystem.effortPerFunctionPoint,
                        calculatedFinishDate: projectTeamPlanningPeriodSystem.calculatedFinishDate
                    }
            ))

        const systemsTableColumns = [
            {
                field: 'systemName',
                headerName: 'Название',
                flex: 1,
                renderCell: (params) => (
                    <RouterLink to={ `/planningPeriods/${ planningPeriodId }/projectTeams/${ projectTeamId }/systems/${ params.getValue(params.id, 'systemId') }` }>
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
                valueFormatter: ({ value }) => value.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 }),
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
                        key: changeRequest.key,
                        name: changeRequest.name,
                        hasValue: changeRequest.hasValue,
                        estimate: changeRequest.estimate,
                        timeLeft: changeRequest.timeLeft,
                        stateCategoryId: changeRequest.stateCategoryId,
                        effortPerFunctionPoint: changeRequest.effortPerFunctionPoint,
                        calculatedFinishDate: changeRequest.calculatedFinishDate,
                        newFunctionsTimeSpentPrevious28Days: changeRequest.newFunctionsTimeSpentPrevious28Days
                    }
            ))

        const changeRequestsTableColumns = [
            {
                field: 'name',
                headerName: 'Название',
                flex: 1,
                renderCell: (params) => (
                    <RouterLink style={{ textDecoration: params.getValue(params.id, 'stateCategoryId') === 3 ? 'line-through' : 'none' }} to={ `/changeRequests/${ params.getValue(params.id, 'key') }` }>
                        { params.getValue(params.id, 'key') } &nbsp;
                        { params.getValue(params.id, 'name') }
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
                field: 'newFunctionsTimeSpentPrevious28Days',
                headerName: 'Фактические трудозатраты за 28 дней (ч)',
                width: 200,
                align: 'right',
                valueFormatter: ({ value }) => value.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 }) ,
            },
        ];

        const positionsTableContents = positions.slice()
            .sort((a, b) =>  (
                (a.newFunctionsFullTimeEquivalentPrevious28Days > b.newFunctionsFullTimeEquivalentPrevious28Days) ? -1 : (
                    (a.newFunctionsFullTimeEquivalentPrevious28Days == b.newFunctionsFullTimeEquivalentPrevious28Days) ? 0 : 1
                )
            ))
            .map(position => (
                    {
                        id: position.id,
                        url: position.position.url,
                        position: position.position.name,
                        personId: position.person.id,
                        personKey: position.person.key,
                        personName: position.person.name,
                        newFunctionsTimeSpent: position.newFunctionsTimeSpent,
                        newFunctionsFullTimeEquivalentPrevious28Days: position.newFunctionsFullTimeEquivalentPrevious28Days,
                        newFunctionsFullTimeEquivalentCapacity: position.newFunctionsFullTimeEquivalentCapacity
                    }
            ))

        const positionsTableColumns = [
            {
                field: 'position',
                headerName: 'Позиция',
                flex: 1,
                renderCell: (params) => {
                    const url = params.getValue(params.id, 'url')

                    return url ?
                        <Link href={ url } target="_blank">
                            { params.getValue(params.id, 'position') }
                        </Link>
                    : params.getValue(params.id, 'position')
                },
            },
            {
                field: 'personName',
                headerName: 'ФИО',
                flex: 1,
                renderCell: (params) => (
                    <RouterLink to={ `/persons/${ params.getValue(params.id, 'personKey') }` }>
                        { params.getValue(params.id, 'personName') }
                    </RouterLink>
                ),
            },
            {
                field: 'newFunctionsTimeSpent',
                headerName: 'Новый функционал: списано всего (ч)',
                width: 200,
                align: 'right',
                valueFormatter: ({ value }) => value.toLocaleString(undefined, { maximumFractionDigits: 0 }),
            },
            {
                field: 'newFunctionsFullTimeEquivalentCapacity',
                headerName: 'Новый функционал: плановый FTE',
                width: 200,
                align: 'right',
                valueFormatter: ({ value }) => (value).toLocaleString(undefined, { minimumFractionDigits: 1, maximumFractionDigits: 1 }),
            },
            {
                field: 'newFunctionsFullTimeEquivalentPrevious28Days',
                headerName: 'Новый функционал: фактический FTE за 28 дней',
                width: 200,
                align: 'right',
                valueFormatter: ({ value }) => (value).toLocaleString(undefined, { minimumFractionDigits: 1, maximumFractionDigits: 1 }),
            },
        ];

        return (
            <Box>
                <Typography variant="body" noWrap>
                    Проектная команда { projectTeamName }
                    <br />
                    Период планирования { planningPeriodName } ({ planningPeriodStart }-{ planningPeriodEnd })
                    <br />
                    Расчетная дата завершения { calculatedFinishDate }
                    <br />
                    Затраты на функциональную точку (аналитика + разработка + менеджмент) { effortPerFunctionPoint.toFixed(2) } часов / функциональная точка
                </Typography>

                <TimeSheetsByDatePeriodChart
                    planningPeriodEnd={ planningPeriodEnd }
                    title="Фактический объем работ: Аналитика + Разработка + Тестирование + Управление + Инциденты"
                    xAxisStart={ xAxisStart }
                    xAxisEnd={ xAxisEnd }
                    color="black"
                    timeSheetsByDate={ timeSheetsByDate }
                    estimate={ estimate }
                    calculatedFinishDate={ calculatedFinishDate }
                />

                <ValueByDatePeriodChart
                    planningPeriodEnd={ planningPeriodEnd }
                    title="Доля списаний на задачи без бизнес-ценности"
                    xAxisStart={ xAxisStart }
                    xAxisEnd={ xAxisEnd }
                    color="black"
                    timeSpentPercentWithValueAndWithoutValueByDate={ timeSheetsByDate }
                />

                <ReengineeringByDatePeriodChart
                    planningPeriodEnd={ planningPeriodEnd }
                    title="Доля списаний на задачи технологического перевооружения и исправления проблем"
                    xAxisStart={ xAxisStart }
                    xAxisEnd={ xAxisEnd }
                    color="black"
                    timeSpentPercentForReengineeringAndNotForReengineeringByDate={ timeSheetsByDate }
                />

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

                <br />
                <Typography variant="h6" noWrap>
                    Команда
                </Typography>
                <div>
                    <DataGridPro
                        rows={ positionsTableContents }
                        columns={ positionsTableColumns }
                        autoHeight
                    />
                </div>
            </Box>
        );
    }
}

export default graphql(fetchProjectTeamPlanningPeriodByPlanningPeriodIdAndProjectTeamId, {
    options: (props) => { return { variables: { planningPeriodId: props.match.params.planningPeriodId, projectTeamId: props.match.params.projectTeamId }}}
})(ProjectTeamPlanningPeriodDetail);
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

const fetchProjectTeamQuarterByQuarterKeyAndProjectTeamId = gql`
   query ProjectTeamQuarterByQuarterKeyAndProjectTeamId($quarterKey: String!, $projectTeamId: Int!) {
          projectTeamQuarterByQuarterKeyAndProjectTeamId(projectTeamId: $projectTeamId, quarterKey: $quarterKey) {
                id
                estimate
                effortPerFunctionPoint
                calculatedFinishDate
                changeRequestCalculatedDateAfterQuarterEndIssueCount
                changeRequestCount
                changeRequestCalculatedDateBeforeQuarterEndShare
                timeSpentInCurrentQuarterForQuarterChangeRequestsShare
                
                projectTeam {
                    name
                    
                    changeRequestsWithTimeSpentInCurrentQuarterWhileItIsNotInCurrentQuarter {
                        id
                        changeRequest {
                            id
                            key
                            estimate
                            timeLeft
                            hasValue
                            name
                            stateCategoryId
                            effortPerFunctionPoint
                            calculatedFinishDate
                            timeSpentInCurrentQuarter
                        }
                    }
                    
                    personsWithTimeSpentForChangeRequestsInCurrentQuarterWhileChangeRequestNotInCurrentQuarter {
                        id
                        person {
                            id
                            key
                            name
                      }
                      timeSpentInCurrentQuarter
                    }
                }
                quarter {
                    key
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
                
                projectTeamQuarterSystems {
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
                    timeSpentInCurrentQuarter
                }
          }
    }
`;

class ProjectTeamQuarterDetail extends Component {
    render() {
        if (this.props.data.loading) { return <div>Loading ...</div> }

        const quarterKey = this.props.match.params.quarterKey
        const projectTeamId = this.props.match.params.projectTeamId
        const projectTeamQuarter = this.props.data.projectTeamQuarterByQuarterKeyAndProjectTeamId
        const projectTeamName = projectTeamQuarter.projectTeam.name
        const changeRequestsWithTimeSpentInCurrentQuarterWhileItIsNotInCurrentQuarter = projectTeamQuarter.projectTeam.changeRequestsWithTimeSpentInCurrentQuarterWhileItIsNotInCurrentQuarter
        const personsWithTimeSpentForChangeRequestsInCurrentQuarterWhileChangeRequestNotInCurrentQuarter = projectTeamQuarter.projectTeam.personsWithTimeSpentForChangeRequestsInCurrentQuarterWhileChangeRequestNotInCurrentQuarter
        const estimate = projectTeamQuarter.estimate
        const effortPerFunctionPoint = projectTeamQuarter.effortPerFunctionPoint
        const calculatedFinishDate = projectTeamQuarter.calculatedFinishDate
        const changeRequestCalculatedDateBeforeQuarterEndShare = projectTeamQuarter.changeRequestCalculatedDateBeforeQuarterEndShare
        const timeSpentInCurrentQuarterForQuarterChangeRequestsShare = projectTeamQuarter.timeSpentInCurrentQuarterForQuarterChangeRequestsShare
        const quarterName = projectTeamQuarter.quarter.name
        const quarterStart = projectTeamQuarter.quarter.start
        const quarterEnd = projectTeamQuarter.quarter.end
        const projectTeamQuarterSystems = projectTeamQuarter.projectTeamQuarterSystems
        const changeRequests = projectTeamQuarter.changeRequests
        const positions = projectTeamQuarter.positions

        const timeSheetsByDate = projectTeamQuarter.timeSheetsByDate

        const fourWeeks = 1000 * 60 * 60 * 24 * 7 * 4
        const xAxisStart = new Date(quarterStart).getTime() - fourWeeks
        const xAxisEnd = new Date(quarterEnd).getTime() + fourWeeks

        const systemsTableContents = projectTeamQuarterSystems.slice()
            .sort((a, b) => ((a.system.name > b.system.name) ? 1 : ((a.system.name < b.system.name) ? -1 : 0)))
            .map(projectTeamQuarterSystem => (
                    {
                        id: projectTeamQuarterSystem.id,
                        estimate: projectTeamQuarterSystem.estimate,
                        timeLeft: projectTeamQuarterSystem.timeLeft,
                        systemId: projectTeamQuarterSystem.system.id,
                        systemName: projectTeamQuarterSystem.system.name,
                        effortPerFunctionPoint: projectTeamQuarterSystem.effortPerFunctionPoint,
                        calculatedFinishDate: projectTeamQuarterSystem.calculatedFinishDate
                    }
            ))

        const systemsTableColumns = [
            {
                field: 'systemName',
                headerName: 'Название',
                flex: 1,
                // renderCell: (params) => (
                //     <RouterLink to={ `/quarters/${ quarterKey }/projectTeams/${ projectTeamId }/systems/${ params.getValue(params.id, 'systemId') }` }>
                //         { params.getValue(params.id, 'systemName') }
                //     </RouterLink>
                // ),
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
                        timeSpentInCurrentQuarter: changeRequest.timeSpentInCurrentQuarter
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
                field: 'timeSpentInCurrentQuarter',
                headerName: 'Фактические трудозатраты с начала квартала (ч)',
                width: 200,
                align: 'right',
                valueFormatter: ({ value }) => value.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 }) ,
            },
        ];

        const changeRequestsWithTimeSpentInCurrentQuarterWhileItIsNotInCurrentQuarterTableContents = changeRequestsWithTimeSpentInCurrentQuarterWhileItIsNotInCurrentQuarter.slice()
            .sort((a, b) =>  (
                (a.changeRequest.stateCategoryId === 3 && b.changeRequest.stateCategoryId !== 3) ? 1 : (
                    (a.changeRequest.stateCategoryId === 3 && b.changeRequest.stateCategoryId === 3) ? 0 : (
                        (a.changeRequest.stateCategoryId !== 3 && b.changeRequest.stateCategoryId === 3) ? -1 : (
                            b.changeRequest.timeLeft - a.changeRequest.timeLeft
                        )
                    )
                )
            ))
            .map(changeRequestWithTimeSpentInCurrentQuarterWhileItIsNotInCurrentQuarter => (
                    {
                        id: changeRequestWithTimeSpentInCurrentQuarterWhileItIsNotInCurrentQuarter.changeRequest.id,
                        key: changeRequestWithTimeSpentInCurrentQuarterWhileItIsNotInCurrentQuarter.changeRequest.key,
                        name: changeRequestWithTimeSpentInCurrentQuarterWhileItIsNotInCurrentQuarter.changeRequest.name,
                        hasValue: changeRequestWithTimeSpentInCurrentQuarterWhileItIsNotInCurrentQuarter.changeRequest.hasValue,
                        estimate: changeRequestWithTimeSpentInCurrentQuarterWhileItIsNotInCurrentQuarter.changeRequest.estimate,
                        timeLeft: changeRequestWithTimeSpentInCurrentQuarterWhileItIsNotInCurrentQuarter.changeRequest.timeLeft,
                        stateCategoryId: changeRequestWithTimeSpentInCurrentQuarterWhileItIsNotInCurrentQuarter.changeRequest.stateCategoryId,
                        effortPerFunctionPoint: changeRequestWithTimeSpentInCurrentQuarterWhileItIsNotInCurrentQuarter.changeRequest.effortPerFunctionPoint,
                        calculatedFinishDate: changeRequestWithTimeSpentInCurrentQuarterWhileItIsNotInCurrentQuarter.changeRequest.calculatedFinishDate,
                        timeSpentInCurrentQuarter: changeRequestWithTimeSpentInCurrentQuarterWhileItIsNotInCurrentQuarter.changeRequest.timeSpentInCurrentQuarter
                    }
            ))

        const changeRequestsWithTimeSpentInCurrentQuarterWhileItIsNotInCurrentQuarterTableColumns = [
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
                field: 'timeSpentInCurrentQuarter',
                headerName: 'Фактические трудозатраты с начала квартала (ч)',
                width: 200,
                align: 'right',
                valueFormatter: ({ value }) => value.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 }) ,
            },
        ];

        const personsWithTimeSpentForChangeRequestsInCurrentQuarterWhileChangeRequestNotInCurrentQuarterTableContents = personsWithTimeSpentForChangeRequestsInCurrentQuarterWhileChangeRequestNotInCurrentQuarter.slice()
            .sort((a, b) =>  (
                (a.timeSpentInCurrentQuarter < b.timeSpentInCurrentQuarter) ? 1 : (
                    (a.timeSpentInCurrentQuarter > b.timeSpentInCurrentQuarter) ? -1 : 0
                )
            ))
            .map(personWithTimeSpentForChangeRequestsInCurrentQuarterWhileChangeRequestNotInCurrentQuarter => (
                    {
                        id: personWithTimeSpentForChangeRequestsInCurrentQuarterWhileChangeRequestNotInCurrentQuarter.id,
                        key: personWithTimeSpentForChangeRequestsInCurrentQuarterWhileChangeRequestNotInCurrentQuarter.key,
                        name: personWithTimeSpentForChangeRequestsInCurrentQuarterWhileChangeRequestNotInCurrentQuarter.person.name,
                        timeSpentInCurrentQuarter: personWithTimeSpentForChangeRequestsInCurrentQuarterWhileChangeRequestNotInCurrentQuarter.timeSpentInCurrentQuarter,
                    }
            ))

        const personsWithTimeSpentForChangeRequestsInCurrentQuarterWhileChangeRequestNotInCurrentQuarterTableColumns = [
            {
                field: 'name',
                headerName: 'ФИО',
                flex: 1,
            },
            {
                field: 'timeSpentInCurrentQuarter',
                headerName: 'Затрачено времени (ч)',
                width: 200,
                align: 'right',
                valueFormatter: ({ value }) => value.toLocaleString(undefined, { maximumFractionDigits: 0 }),
            },
        ];

        return (
            <Box>
                <Typography variant="body" noWrap>
                    Проектная команда { projectTeamName }
                    <br />
                    Период планирования { quarterName } ({ quarterStart }-{ quarterEnd })
                    <br />
                    Расчетная дата завершения { calculatedFinishDate }
                    <br />
                    Затраты на функциональную точку (аналитика + разработка + менеджмент) { effortPerFunctionPoint.toFixed(2) } часов / функциональная точка
                    <br />
                    Прогноз исполнения плана по заявкам на доработку ПО: { (changeRequestCalculatedDateBeforeQuarterEndShare * 100).toLocaleString(undefined, { maximumFractionDigits: 0 }) }%
                    <br />
                    Процент трудозатрат на задачи квартала { (timeSpentInCurrentQuarterForQuarterChangeRequestsShare * 100).toLocaleString(undefined, { maximumFractionDigits: 0 }) }%
                    <br />
                    <br />
                </Typography>

                <TimeSheetsByDatePeriodChart
                    planningPeriodEnd={ quarterEnd }
                    title="Фактический объем работ: Аналитика + Разработка + Тестирование + Управление + Инциденты"
                    xAxisStart={ xAxisStart }
                    xAxisEnd={ xAxisEnd }
                    color="black"
                    timeSheetsByDate={ timeSheetsByDate }
                    estimate={ estimate }
                    calculatedFinishDate={ calculatedFinishDate }
                />

                <ValueByDatePeriodChart
                    planningPeriodEnd={ quarterEnd }
                    title="Доля списаний на задачи без бизнес-ценности"
                    xAxisStart={ xAxisStart }
                    xAxisEnd={ xAxisEnd }
                    color="black"
                    timeSpentPercentWithValueAndWithoutValueByDate={ timeSheetsByDate }
                />

                <ReengineeringByDatePeriodChart
                    planningPeriodEnd={ quarterEnd }
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
                    Заявки на доработку ПО, по которым шла работа, но которые не входят в текущий квартал
                </Typography>
                <div>
                    <DataGridPro
                        rows={ changeRequestsWithTimeSpentInCurrentQuarterWhileItIsNotInCurrentQuarterTableContents }
                        columns={ changeRequestsWithTimeSpentInCurrentQuarterWhileItIsNotInCurrentQuarterTableColumns }
                        autoHeight
                    />
                </div>

                <Typography variant="h6" noWrap>
                    Сотрудники, выполнявшие работы по заявкам на доработку ПО, которые не входят в текущий квартал
                </Typography>
                <div>
                    <DataGridPro
                        rows={ personsWithTimeSpentForChangeRequestsInCurrentQuarterWhileChangeRequestNotInCurrentQuarterTableContents }
                        columns={ personsWithTimeSpentForChangeRequestsInCurrentQuarterWhileChangeRequestNotInCurrentQuarterTableColumns }
                        autoHeight
                    />
                </div>
            </Box>
        );
    }
}

export default graphql(fetchProjectTeamQuarterByQuarterKeyAndProjectTeamId, {
    options: (props) => { return { variables: { quarterKey: props.match.params.quarterKey, projectTeamId: props.match.params.projectTeamId }}}
})(ProjectTeamQuarterDetail);
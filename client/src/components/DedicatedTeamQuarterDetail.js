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

const fetchDedicatedTeamQuarterByQuarterKeyAndDedicatedTeamId = gql`
        query DedicatedTeamQuarterByQuarterKeyAndDedicatedTeamId($quarterKey: String!, $dedicatedTeamId: Int!) {
              dedicatedTeamQuarterByQuarterKeyAndDedicatedTeamId(dedicatedTeamId: $dedicatedTeamId, quarterKey: $quarterKey) {
                    id
                    estimate
                    effortPerFunctionPoint
                    calculatedFinishDate
                    changeRequestCalculatedDateAfterQuarterEndIssueCount
                    changeRequestCount
                    changeRequestCalculatedDateBeforeQuarterEndShare
                    
                    dedicatedTeam {
                        name
                        cio {
                            name
                        }
                        cto {
                            name
                        }
                    }
                    
                    quarter {
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
                    
                    projectTeamQuarters {
                        id
                        estimate
                        timeLeft
                        projectTeam {
                            id
                            name
                        }
                        effortPerFunctionPoint
                        calculatedFinishDate
                        timeSpentInCurrentQuarter
                        changeRequestCalculatedDateBeforeQuarterEndShare
                    }
                    
                    dedicatedTeamQuarterSystems {
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

class DedicatedTeamQuarterDetail extends Component {
    render() {
        if (this.props.data.loading) { return <div>Loading ...</div> }
        const quarterKey = this.props.match.params.quarterKey
        const dedicatedTeamId = this.props.match.params.dedicatedTeamId

        const dedicatedTeamQuarter = this.props.data.dedicatedTeamQuarterByQuarterKeyAndDedicatedTeamId

        const dedicatedTeamName = dedicatedTeamQuarter.dedicatedTeam.name
        const cioName = dedicatedTeamQuarter.dedicatedTeam.cio.name
        const ctoName = dedicatedTeamQuarter.dedicatedTeam.cto.name
        const estimate = dedicatedTeamQuarter.estimate
        const effortPerFunctionPoint = dedicatedTeamQuarter.effortPerFunctionPoint
        const calculatedFinishDate = dedicatedTeamQuarter.calculatedFinishDate
        const changeRequestCalculatedDateBeforeQuarterEndShare = dedicatedTeamQuarter.changeRequestCalculatedDateBeforeQuarterEndShare
        const quarterName = dedicatedTeamQuarter.quarter.name
        const quarterStart = dedicatedTeamQuarter.quarter.start
        const quarterEnd = dedicatedTeamQuarter.quarter.end
        const projectTeamQuarters = dedicatedTeamQuarter.projectTeamQuarters
        const dedicatedTeamQuarterSystems = dedicatedTeamQuarter.dedicatedTeamQuarterSystems
        const changeRequests = dedicatedTeamQuarter.changeRequests
        const positions = dedicatedTeamQuarter.positions

        const timeSheetsByDate = dedicatedTeamQuarter.timeSheetsByDate

        const fourWeeks = 1000 * 60 * 60 * 24 * 7 * 4
        const xAxisStart = new Date(quarterStart).getTime() - fourWeeks
        const xAxisEnd = new Date(quarterEnd).getTime() + fourWeeks

        const systemsTableContents = dedicatedTeamQuarterSystems.slice()
            .sort((a, b) => ((a.system.name > b.system.name) ? 1 : ((a.system.name < b.system.name) ? -1 : 0)))
            .map(dedicatedTeamQuarterSystem => (
                    {
                        id: dedicatedTeamQuarterSystem.id,
                        estimate: dedicatedTeamQuarterSystem.estimate,
                        timeLeft: dedicatedTeamQuarterSystem.timeLeft,
                        systemId: dedicatedTeamQuarterSystem.system.id,
                        systemName: dedicatedTeamQuarterSystem.system.name,
                        effortPerFunctionPoint: dedicatedTeamQuarterSystem.effortPerFunctionPoint,
                        calculatedFinishDate: dedicatedTeamQuarterSystem.calculatedFinishDate,
                    }
            ))

        const systemsTableColumns = [
            {
                field: 'systemName',
                headerName: 'Название',
                flex: 1,
                // renderCell: (params) => (
                //     <RouterLink to={ `/quarters/${ quarterKey }/dedicatedTeams/${ dedicatedTeamId }/systems/${ params.getValue(params.id, 'systemId') }` }>
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

        const projectTeamsTableContents = projectTeamQuarters.slice()
            .sort((a, b) => ((a.name > b.name) ? 1 : ((a.name < b.name) ? -1 : 0)))
            .map(projectTeamQuarter => (
                    {
                        id: projectTeamQuarter.id,
                        estimate: projectTeamQuarter.estimate,
                        timeLeft: projectTeamQuarter.timeLeft,
                        projectTeamId: projectTeamQuarter.projectTeam.id,
                        projectTeamName: projectTeamQuarter.projectTeam.name,
                        effortPerFunctionPoint: projectTeamQuarter.effortPerFunctionPoint,
                        calculatedFinishDate: projectTeamQuarter.calculatedFinishDate,
                        timeSpentInCurrentQuarter: projectTeamQuarter.timeSpentInCurrentQuarter,
                        changeRequestCalculatedDateBeforeQuarterEndShare: projectTeamQuarter.changeRequestCalculatedDateBeforeQuarterEndShare,
                    }
            ))

        const projectTeamsTableColumns = [
            {
                field: 'projectTeamName',
                headerName: 'Название',
                flex: 1,
                renderCell: (params) => (
                    <RouterLink to={ `/quarters/${ quarterKey }/projectTeams/${ params.getValue(params.id, 'projectTeamId') }` }>
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
            {
                field: 'timeSpentInCurrentQuarter',
                headerName: 'Фактические трудозатраты с начала квартала (ч)',
                width: 200,
                align: 'right',
                valueFormatter: ({ value }) => value.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 }) ,
            },
            {
                field: 'changeRequestCalculatedDateBeforeQuarterEndShare',
                headerName: 'Прогноз исполнения плана по заявкам на доработку ПО (%)',
                width: 200,
                align: 'right',
                valueFormatter: ({ value }) => (value * 100).toLocaleString(undefined, { maximumFractionDigits: 0}),
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

        return (
            <Box>
                <Typography variant="body" noWrap>
                    Выделенная команда { dedicatedTeamName }
                    <br />
                    Бизнес-партнер { cioName }
                    <br />
                    Руководитель разработки (CTO) { ctoName }
                    <br />
                    Период планирования { quarterName } ({ quarterStart }-{ quarterEnd })
                    <br />
                    Расчетная дата завершения { calculatedFinishDate }
                    <br />
                    Затраты на функциональную точку (аналитика + разработка + менеджмент) { effortPerFunctionPoint.toFixed(2) } часов / функциональная точка
                    <br />
                    Прогноз исполнения плана по заявкам на доработку ПО: { (changeRequestCalculatedDateBeforeQuarterEndShare * 100).toLocaleString(undefined, { maximumFractionDigits: 0 }) }%
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

                {/*<br />*/}
                {/*<Typography variant="h6" noWrap>*/}
                {/*    Команда*/}
                {/*</Typography>*/}
                {/*<div>*/}
                {/*    <DataGridPro*/}
                {/*        rows={ positionsTableContents }*/}
                {/*        columns={ positionsTableColumns }*/}
                {/*        autoHeight*/}
                {/*    />*/}
                {/*</div>*/}
            </Box>
        );
    }
}

export default graphql(fetchDedicatedTeamQuarterByQuarterKeyAndDedicatedTeamId, {
    options: (props) => { return { variables: { quarterKey: props.match.params.quarterKey, dedicatedTeamId: props.match.params.dedicatedTeamId }}}
})(DedicatedTeamQuarterDetail);
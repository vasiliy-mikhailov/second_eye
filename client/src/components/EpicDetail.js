import React, {Component} from "react";
import {gql} from '@apollo/client';
import { graphql } from '@apollo/client/react/hoc';
import Typography from '@material-ui/core/Typography';
import {Box, Link} from "@material-ui/core";
import {Link as RouterLink, NavLink} from "react-router-dom";
import { DataGridPro,} from '@mui/x-data-grid-pro';
import TimeSheetsByDateIssueChart from './TimeSheetsByDateIssueChart'

const fetchEpicByKey = gql`
    query EpicByKeyQuery($key: String!) {
        epicByKey(key: $key) {
            id 
            key
            name
            
            estimate
            effortPerFunctionPoint
            timeSpent
            timeLeft
            calculatedFinishDate
            timeSheetsByDate {
                date
                timeSpentCumsum
                timeSpentCumsumPrediction
            }
            
            analysisEstimate
            analysisTimeSpent
            analysisTimeLeft
            analysisTimeSheetsByDate {
                date
                timeSpentCumsum
            }
            
            
            developmentEstimate
            developmentTimeSpent
            developmentTimeLeft
            developmentTimeSheetsByDate {
                date
                timeSpentCumsum
            }
            
            testingEstimate
            testingTimeSpent
            testingTimeLeft
            testingTimeSheetsByDate {
                date
                timeSpentCumsum
            }
            
            systems {
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
            
            persons {
                person {
                    id
                    name
                }
                newFunctionsTimeSpent
                newFunctionsFullTimeEquivalentPrevious28Days
            }
        }
    }
`;

class EpicDetail extends Component {
    render() {
        if (this.props.data.loading) { return <div>Loading ...</div> }

        const epicKey = this.props.match.params.key
        const epic = this.props.data.epicByKey

        const timeSheetsByDate = epic.timeSheetsByDate
        const systems = epic.systems
        const changeRequests = epic.changeRequests
        const persons = epic.persons

        const estimate = epic.estimate
        const effortPerFunctionPoint = epic.effortPerFunctionPoint

        const analysisTimeSheetsByDate = epic.analysisTimeSheetsByDate
        const analysisEstimate = epic.analysisEstimate

        const developmentTimeSheetsByDate = epic.developmentTimeSheetsByDate
        const developmentEstimate = epic.developmentEstimate

        const testingTimeSheetsByDate = epic.testingTimeSheetsByDate
        const testingEstimate = epic.testingEstimate

        const calculatedFinishDate = epic.calculatedFinishDate

        const today = (new Date()).getTime()
        const firstTimeSheetDate = timeSheetsByDate.length > 0 ? new Date(timeSheetsByDate[0].date).getTime() : null
        const lastTimeSheetDate = timeSheetsByDate.length > 0 ? new Date(timeSheetsByDate[timeSheetsByDate.length - 1].date).getTime() : null

        const allEdgeDates = [today]

        if (firstTimeSheetDate) {
            allEdgeDates.push(firstTimeSheetDate)
        }

        if (lastTimeSheetDate) {
            allEdgeDates.push(lastTimeSheetDate)
        }

        if (calculatedFinishDate) {
            const calculatedFinishDateAsDate = new Date(calculatedFinishDate)
            allEdgeDates.push(calculatedFinishDateAsDate)
        }

        const xAxisStart = Math.min(...allEdgeDates) - 1000 * 60 * 60 * 24 * 28
        const xAxisEnd = Math.max(...allEdgeDates) + 1000 * 60 * 60 * 24 * 28

        const systemsTableContents = systems.slice()
            .sort((a, b) => ((a.system.name > b.system.name) ? 1 : ((a.system.name < b.system.name) ? -1 : 0)))
            .map(system => (
                    {
                        id: system.id,
                        estimate: system.estimate,
                        timeLeft: system.timeLeft,
                        systemId: system.system.id,
                        systemName: system.system.name,
                        effortPerFunctionPoint: system.effortPerFunctionPoint,
                        calculatedFinishDate: system.calculatedFinishDate,
                    }
            ))

        const systemsTableColumns = [
            {
                field: 'systemName',
                headerName: 'Название',
                flex: 1,
                renderCell: (params) => (
                    <RouterLink to={ `/epics/${ epicKey }/systems/${ params.getValue(params.id, 'systemId') }` }>
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
                        newFunctionsTimeSpentPrevious28Days: changeRequest.newFunctionsTimeSpentPrevious28Days,
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
                headerName: 'Трудомощность, ч',
                width: 200,
                align: 'right',
                valueFormatter: ({ value }) => value.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 }) ,
            },
        ];

        const personsTableContents = persons.slice()
            .sort((a, b) =>  (
                (a.newFunctionsFullTimeEquivalentPrevious28Days > b.newFunctionsFullTimeEquivalentPrevious28Days) ? -1 : (
                    (a.newFunctionsFullTimeEquivalentPrevious28Days == b.newFunctionsFullTimeEquivalentPrevious28Days) ? 0 : 1
                )
            ))
            .map(person => (
                    {
                        id: person.person.id,
                        name: person.person.name,
                        newFunctionsTimeSpent: person.newFunctionsTimeSpent,
                        newFunctionsFullTimeEquivalentPrevious28Days: person.newFunctionsFullTimeEquivalentPrevious28Days
                    }
            ))

            const personsTableColumns = [
            {
                field: 'name',
                headerName: 'Имя',
                flex: 1,
            },
            {
                field: 'newFunctionsTimeSpent',
                headerName: 'Новый функционал: списано всего (ч)',
                width: 200,
                align: 'right',
                valueFormatter: ({ value }) => value.toLocaleString(undefined, { maximumFractionDigits: 0 }),
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
                <Typography variant="body1" noWrap>
                    <NavLink to={ this.props.location.pathname }>
                        { epic.key }
                    </NavLink> &nbsp;
                    { epic.name } &nbsp;
                    <Link href={ epic.url }>
                        [ источник ]
                    </Link>
                    <br />
                    Осталось { epic.timeLeft.toFixed(1) } ч ( { (epic.timeLeft / epic.estimate * 100).toFixed(2) }% ) <br />
                    Сделано { epic.timeSpent.toFixed(1) } ч <br />
                    Оценка { epic.estimate.toFixed(1) } ч <br />
                    Затраты на функциональную точку (аналитика + разработка + менеджмент) { effortPerFunctionPoint.toFixed(2) } часов / функциональная точка <br />
                    Расчетная дата завершения { calculatedFinishDate }
                </Typography>
                <br />

                <TimeSheetsByDateIssueChart
                    title="Фактический объем работ: Аналитика + Разработка + Тестирование + Управление"
                    xAxisStart={ xAxisStart }
                    xAxisEnd={ xAxisEnd }
                    color="black"
                    timeSheetsByDate={ timeSheetsByDate }
                    estimate={ estimate }
                    calculatedFinishDate={ calculatedFinishDate }
                />

                <TimeSheetsByDateIssueChart
                    title="Аналитика"
                    xAxisStart={ xAxisStart }
                    xAxisEnd={ xAxisEnd }
                    color="red"
                    timeSheetsByDate={ analysisTimeSheetsByDate }
                    estimate={ analysisEstimate }
                    calculatedFinishDate={ calculatedFinishDate }
                />

                <TimeSheetsByDateIssueChart
                    title="Разработка"
                    xAxisStart={ xAxisStart }
                    xAxisEnd={ xAxisEnd }
                    color="green"
                    timeSheetsByDate={ developmentTimeSheetsByDate }
                    estimate={ developmentEstimate }
                    calculatedFinishDate={ calculatedFinishDate }
                />

                <TimeSheetsByDateIssueChart
                    title="Тестирование"
                    xAxisStart={ xAxisStart }
                    xAxisEnd={ xAxisEnd }
                    color="blue"
                    timeSheetsByDate={ testingTimeSheetsByDate }
                    estimate={ testingEstimate }
                    calculatedFinishDate={ calculatedFinishDate }
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

                <br />
                <Typography variant="h6" noWrap>
                    Команда
                </Typography>
                <div>
                    <DataGridPro
                        rows={ personsTableContents }
                        columns={ personsTableColumns }
                        autoHeight
                    />
                </div>
            </Box>
        );
    }
}

export default graphql(fetchEpicByKey, {
    options: (props) => { return { variables: { key: props.match.params.key }}}
})(EpicDetail);
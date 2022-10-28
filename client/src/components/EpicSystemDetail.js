import React, {Component} from "react";
import {gql} from '@apollo/client';
import { graphql } from '@apollo/client/react/hoc';
import Typography from '@material-ui/core/Typography';
import {Box, Link} from "@material-ui/core";
import {Link as RouterLink} from "react-router-dom";
import TimeSheetsByDatePeriodChart from "./TimeSheetsByDatePeriodChart"
import { DataGridPro } from "@mui/x-data-grid-pro";

const fetchEpicSystemByEpicKeyAndSystemId = gql`
     query EpicSystemByEpicKeyAndSystemId($epicKey: String!, $systemId: Int!) {
          epicSystemByEpicKeyAndSystemId(epicKey: $epicKey, systemId: $systemId) {
                id
                estimate
                calculatedFinishDate
                effortPerFunctionPoint
                system {
                    name
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
                }
          }
    }
`;

class EpicSystemDetail extends Component {
    render() {
        if (this.props.data.loading) { return <div>Loading ...</div> }
        const epicSystem = this.props.data.epicSystemByEpicKeyAndSystemId

        const systemName = epicSystem.system.name
        const estimate = epicSystem.estimate
        const calculatedFinishDate = epicSystem.calculatedFinishDate
        const effortPerFunctionPoint = epicSystem.effortPerFunctionPoint
        const systemChangeRequests = epicSystem.systemChangeRequests

        const timeSheetsByDate = epicSystem.timeSheetsByDate

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
            allEdgeDates.push(new Date(calculatedFinishDate).getTime())
        }

        const xAxisStart = Math.min(...allEdgeDates) - 1000 * 60 * 60 * 24 * 28
        const xAxisEnd = Math.max(...allEdgeDates) + 1000 * 60 * 60 * 24 * 28

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
                        effortPerFunctionPoint: systemChangeRequest.effortPerFunctionPoint
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
        ];

        return (
            <Box>
                <Typography variant="body" noWrap>
                    Система { systemName }<br />
                    Затраты на функциональную точку (аналитика + разработка + менеджмент) { effortPerFunctionPoint.toFixed(2) } часов / функциональная точка<br />
                    Расчетная дата завершения { calculatedFinishDate }
                </Typography>

                <TimeSheetsByDatePeriodChart
                    title="Фактический объем работ: Аналитика + Разработка + Тестирование + Управление"
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

export default graphql(fetchEpicSystemByEpicKeyAndSystemId, {
    options: (props) => { return { variables: { epicKey: props.match.params.epicKey, systemId: props.match.params.systemId }}}
})(EpicSystemDetail);
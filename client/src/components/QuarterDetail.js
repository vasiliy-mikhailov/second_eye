import React from "react";
import {gql, useQuery} from '@apollo/client';
import Typography from '@material-ui/core/Typography';
import {Box} from "@material-ui/core";
import {Link as RouterLink, useParams} from "react-router-dom";
import TimeSheetsByDatePeriodChart from "./TimeSheetsByDatePeriodChart"
import ReengineeringByDatePeriodChart from "./ReengineeringByDatePeriodChart"
import ValueByDatePeriodChart from "./ValueByDatePeriodChart"
import {DataGridPro,} from '@mui/x-data-grid-pro';

const fetchQuarterByKey = gql`
    query QuarterByKeyQuery($key: String!) {
        quarterByKey(key: $key) {
            id 
            key
            name
            timeSpentChrononFte
            start
            end
            estimate
            effortPerFunctionPoint
            calculatedFinishDate
            changeRequestCalculatedDateAfterQuarterEndIssueCount
            changeRequestCount
            changeRequestCalculatedDateBeforeQuarterEndShare
            
            dedicatedTeamQuarters {
                id
                estimate
                timeLeft
                dedicatedTeam {
                    id
                    name
                }
                effortPerFunctionPoint
                calculatedFinishDate
                timeSpentChronon
                timeSpentChrononFte
                timeSpentForReengineeringPercent
                changeRequestCalculatedDateBeforeQuarterEndShare
            }
            
#            systemQuarters {
#                id
#                estimate
#                timeLeft
#                system {
#                    id
#                    name
#                }
#                effortPerFunctionPoint
#                calculatedFinishDate
#            }
    
            timeSheetsByDate {
                date
                timeSpentCumsum
                timeSpentCumsumPrediction
                timeSpentWithoutValuePercentCumsum
                timeSpentWithValuePercentCumsum
                timeSpentForReengineeringPercentCumsum
                timeSpentNotForReengineeringPercentCumsum
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
                timeSpentChronon
            }
        }
    }
`;

function QuarterDetail() {
    const {key} = useParams();
    const {loading, error, data} = useQuery(fetchQuarterByKey, {
        variables: {key: key}
    });

    if (loading) return 'Loading ...'

    if (error) return `Error! ${error.message}`

    const quarterKey = key
    const quarter = data.quarterByKey
    const timeSpentChrononFte = quarter.timeSpentChrononFte
    const estimate = quarter.estimate
    const effortPerFunctionPoint = quarter.effortPerFunctionPoint
    const calculatedFinishDate = quarter.calculatedFinishDate
    const changeRequestCalculatedDateBeforeQuarterEndShare = quarter.changeRequestCalculatedDateBeforeQuarterEndShare
    const planningPeriodStart = quarter.start
    const planningPeriodEnd = quarter.end

    const dedicatedTeamQuarters = quarter.dedicatedTeamQuarters
    const systemQuarters = quarter.systemQuarters

    const timeSheetsByDate = quarter.timeSheetsByDate
    const today = (new Date()).getTime()
    const firstTimeSheetDate = timeSheetsByDate.length > 0 ? new Date(timeSheetsByDate[0].date).getTime() : null
    const lastTimeSheetDate = timeSheetsByDate.length > 0 ? new Date(timeSheetsByDate[timeSheetsByDate.length - 1].date).getTime() : null

    const changeRequests = quarter.changeRequests

    const fourWeeks = 1000 * 60 * 60 * 24 * 7 * 4

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

    const xAxisStart = Math.min(...allEdgeDates) - fourWeeks
    const xAxisEnd = Math.max(...allEdgeDates) + fourWeeks

    const dedicatedTeamsTableContents = dedicatedTeamQuarters.slice()
        .sort((a, b) => ((a.dedicatedTeam.name > b.dedicatedTeam.name) ? 1 : ((a.dedicatedTeam.name < b.dedicatedTeam.name) ? -1 : 0)))
        .map(dedicatedTeamQuarter => (
            {
                id: dedicatedTeamQuarter.id,
                estimate: dedicatedTeamQuarter.estimate,
                timeLeft: dedicatedTeamQuarter.timeLeft,
                dedicatedTeamId: dedicatedTeamQuarter.dedicatedTeam.id,
                dedicatedTeamName: dedicatedTeamQuarter.dedicatedTeam.name,
                effortPerFunctionPoint: dedicatedTeamQuarter.effortPerFunctionPoint,
                calculatedFinishDate: dedicatedTeamQuarter.calculatedFinishDate,
                timeSpentChronon: dedicatedTeamQuarter.timeSpentChronon,
                timeSpentChrononFte: dedicatedTeamQuarter.timeSpentChrononFte,
                timeSpentForReengineeringPercent: dedicatedTeamQuarter.timeSpentForReengineeringPercent,
                changeRequestCalculatedDateBeforeQuarterEndShare: dedicatedTeamQuarter.changeRequestCalculatedDateBeforeQuarterEndShare,
            }
        ))

    const dedicatedTeamsTableColumns = [
        {
            field: 'dedicatedTeamName',
            headerName: 'Название',
            flex: 1,
            renderCell: (params) => (
                <RouterLink
                    to={`/quarters/${quarterKey}/dedicatedTeams/${params.getValue(params.id, 'dedicatedTeamId')}`}>
                    {params.getValue(params.id, 'dedicatedTeamName')}
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
            valueFormatter: ({value}) => value.toLocaleString(undefined, {maximumFractionDigits: 0}),
        },
        {
            field: 'timeLeft',
            headerName: 'Осталось (ч)',
            width: 200,
            align: 'right',
            valueFormatter: ({value}) => value.toLocaleString(undefined, {maximumFractionDigits: 0}),
        },
        {
            field: 'effortPerFunctionPoint',
            headerName: 'Затраты на ф.т.',
            width: 200,
            align: 'right',
            valueFormatter: ({value}) => value.toLocaleString(undefined, {
                minimumFractionDigits: 2,
                maximumFractionDigits: 2
            }),
        },
        {
            field: 'timeSpentChronon',
            headerName: 'Трудомощность, ч',
            width: 200,
            align: 'right',
            valueFormatter: ({value}) => value.toLocaleString(undefined, {
                minimumFractionDigits: 2,
                maximumFractionDigits: 2
            }),
        },
        {
            field: 'timeSpentChrononFte',
            headerName: 'Трудомощность, FTE',
            width: 200,
            align: 'right',
            valueFormatter: ({value}) => value.toLocaleString(undefined, {
                minimumFractionDigits: 2,
                maximumFractionDigits: 2
            }),
        },
        {
            field: 'timeSpentForReengineeringPercent',
            headerName: 'Затраты на технологическое перевооружение и исправление проблем (%)',
            width: 200,
            align: 'right',
            valueFormatter: ({value}) => (value * 100).toLocaleString(undefined, {
                minimumFractionDigits: 1,
                maximumFractionDigits: 1
            }),
        },
        {
            field: 'changeRequestCalculatedDateBeforeQuarterEndShare',
            headerName: 'Прогноз исполнения плана по заявкам на доработку ПО (%)',
            width: 200,
            align: 'right',
            valueFormatter: ({value}) => (value * 100).toLocaleString(undefined, {maximumFractionDigits: 0}),
        },
    ];

    // const systemsTableContents = systemQuarters.slice()
    //     .sort((a, b) => ((a.system.name > b.system.name) ? 1 : ((a.system.name < b.system.name) ? -1 : 0)))
    //     .map(systemQuarter => (
    //             {
    //                 id: systemQuarter.id,
    //                 estimate: systemQuarter.estimate,
    //                 timeLeft: systemQuarter.timeLeft,
    //                 systemId: systemQuarter.system.id,
    //                 systemName: systemQuarter.system.name,
    //                 effortPerFunctionPoint: systemQuarter.effortPerFunctionPoint,
    //                 calculatedFinishDate: systemQuarter.calculatedFinishDate
    //             }
    //     ))
    //
    // const systemsTableColumns = [
    //     {
    //         field: 'systemName',
    //         headerName: 'Название',
    //         flex: 1,
    //         renderCell: (params) => (
    //             <RouterLink to={ `/quarters/${quarterId}/systems/${ params.getValue(params.id, 'systemId') }` }>
    //                 { params.getValue(params.id, 'systemName') }
    //             </RouterLink>
    //         ),
    //     },
    //     {
    //         field: 'calculatedFinishDate',
    //         headerName: 'Расчетная дата завершения',
    //         width: 200,
    //         align: 'center',
    //     },
    //     {
    //         field: 'estimate',
    //         headerName: 'Оценка (ч)',
    //         width: 200,
    //         align: 'right',
    //         valueFormatter: ({ value }) => value.toLocaleString(undefined, { maximumFractionDigits: 0 }),
    //     },
    //     {
    //         field: 'timeLeft',
    //         headerName: 'Осталось (ч)',
    //         width: 200,
    //         align: 'right',
    //         valueFormatter: ({ value }) => value.toLocaleString(undefined, { maximumFractionDigits: 0 }),
    //     },
    //     {
    //         field: 'effortPerFunctionPoint',
    //         headerName: 'Затраты на ф.т.',
    //         width: 200,
    //         align: 'right',
    //         valueFormatter: ({ value }) => value.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 }),
    //     },
    // ];

    const changeRequestsTableContents = changeRequests.slice()
        .sort((a, b) => (
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
                timeSpentChronon: changeRequest.timeSpentChronon
            }
        ))

    const changeRequestsTableColumns = [
        {
            field: 'name',
            headerName: 'Название',
            flex: 1,
            renderCell: (params) => (
                <RouterLink
                    style={{textDecoration: params.getValue(params.id, 'stateCategoryId') === 3 ? 'line-through' : 'none'}}
                    to={`/changeRequests/${params.getValue(params.id, 'key')}`}>
                    {params.getValue(params.id, 'key')} &nbsp;
                    {params.getValue(params.id, 'name')}
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
            valueFormatter: ({value}) => value ? "Да" : "Нет",
        },
        {
            field: 'estimate',
            headerName: 'Оценка (ч)',
            width: 200,
            align: 'right',
            valueFormatter: ({value}) => value.toLocaleString(undefined, {maximumFractionDigits: 0}),
        },
        {
            field: 'timeLeft',
            headerName: 'Осталось (ч)',
            width: 200,
            align: 'right',
            valueFormatter: ({value}) => value.toLocaleString(undefined, {maximumFractionDigits: 0}),
        },
        {
            field: 'effortPerFunctionPoint',
            headerName: 'Затраты на ф.т.',
            width: 200,
            align: 'right',
            valueFormatter: ({value}) => value.toLocaleString(undefined, {
                minimumFractionDigits: 2,
                maximumFractionDigits: 2
            }),
        },
        {
            field: 'timeSpentChronon',
            headerName: 'Трудомощность, ч',
            width: 200,
            align: 'right',
            valueFormatter: ({value}) => value.toLocaleString(undefined, {
                minimumFractionDigits: 2,
                maximumFractionDigits: 2
            }),
        },
    ];

    return (
        <Box>
            <Typography variant="body" noWrap>
                Расчетная дата завершения {calculatedFinishDate}
                <br/>
                Затраты на функциональную точку (аналитика + разработка +
                менеджмент) {effortPerFunctionPoint.toFixed(2)} часов / функциональная точка
                <br/>
                Трудомощность, FTE: {timeSpentChrononFte.toLocaleString(undefined, {maximumFractionDigits: 0})}
                <br/>
                Прогноз исполнения плана по заявкам на доработку
                ПО: {(changeRequestCalculatedDateBeforeQuarterEndShare * 100).toLocaleString(undefined, {maximumFractionDigits: 0})}%
                <br/>
                <br/>
            </Typography>


            <TimeSheetsByDatePeriodChart
                planningPeriodEnd={planningPeriodEnd}
                title="Фактический объем работ: Аналитика + Разработка + Тестирование + Управление + Инциденты"
                xAxisStart={xAxisStart}
                xAxisEnd={xAxisEnd}
                color="black"
                timeSheetsByDate={timeSheetsByDate}
                estimate={estimate}
                calculatedFinishDate={calculatedFinishDate}
            />

            <ValueByDatePeriodChart
                planningPeriodEnd={planningPeriodEnd}
                title="Доля списаний на задачи без бизнес-ценности"
                xAxisStart={xAxisStart}
                xAxisEnd={xAxisEnd}
                color="black"
                timeSpentPercentWithValueAndWithoutValueByDate={timeSheetsByDate}
            />

            <ReengineeringByDatePeriodChart
                planningPeriodEnd={planningPeriodEnd}
                title="Доля списаний на задачи технологического перевооружения и исправления проблем"
                xAxisStart={xAxisStart}
                xAxisEnd={xAxisEnd}
                color="black"
                timeSpentPercentForReengineeringAndNotForReengineeringByDate={timeSheetsByDate}
            />

            <br/>

            <Typography variant="h6" noWrap>
                Выделенные команды
            </Typography>

            <div>
                <DataGridPro
                    rows={dedicatedTeamsTableContents}
                    columns={dedicatedTeamsTableColumns}
                    autoHeight
                />
            </div>

            <br/>

            <Typography variant="body1">
                <RouterLink to={`/quarters/${quarterKey}/projectTeams`}>
                    Проектные команды одним списком
                </RouterLink>
            </Typography>
            <br/>

            {/*<Typography variant="h6" noWrap>*/}
            {/*    Системы*/}
            {/*</Typography>*/}
            {/*<div>*/}
            {/*    <DataGridPro*/}
            {/*        rows={ systemsTableContents }*/}
            {/*        columns={ systemsTableColumns }*/}
            {/*        autoHeight*/}
            {/*    />*/}
            {/*</div>*/}

            <Typography variant="h6" noWrap>
                Заявки на доработку ПО
            </Typography>
            <div>
                <DataGridPro
                    rows={changeRequestsTableContents}
                    columns={changeRequestsTableColumns}
                    autoHeight
                />
            </div>
        </Box>
    );
}

export default QuarterDetail;
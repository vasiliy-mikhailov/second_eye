import React from "react";
import {gql, useQuery} from '@apollo/client';
import Typography from '@material-ui/core/Typography';
import {Box} from "@material-ui/core";
import {Link as RouterLink, useParams} from "react-router-dom";
import {DataGridPro} from "@mui/x-data-grid-pro";
import TimeSheetsByDateIssueChart from "./TimeSheetsByDateIssueChart";
import ReengineeringByDatePeriodChart from "./ReengineeringByDatePeriodChart";

const fetchDedicatedTeamByDedicatedTeamId = gql`
         query DedicatedTeamById($id: Int!) {
              dedicatedTeamById(id: $id) {
                    id
                    estimate
                    name
                    cio {
                        name
                    }
                    cto {
                        name
                    }
                    calculatedFinishDate
               
                    timeSheetsByDate {
                        date
                        timeSpentCumsum
                        timeSpentCumsumPrediction
                        timeSpentWithoutValuePercentCumsum
                        timeSpentWithValuePercentCumsum
                        timeSpentForReengineeringPercentCumsum
                        timeSpentNotForReengineeringPercentCumsum
                    }
               
                    projectTeams {
                        id
                        estimate
                        timeLeft
                        name
                        calculatedFinishDate
                        timeSpentChrononFte
                        queueLength
                        positionPersonPlanFactIssueCount
                        timeSpentForReengineeringPercent
                    }
                    
                    dedicatedTeamPlanningPeriods {
                        planningPeriod {
                            id 
                            name
                            start
                            end
                        }
                        calculatedFinishDate
                        estimate
                        timeLeft
                        effortPerFunctionPoint
                        timeSpentChrononFte
                    }
              }
        }
`;

function DedicatedTeamDetail() {
    const {dedicatedTeamId} = useParams();
    const {loading, error, data} = useQuery(fetchDedicatedTeamByDedicatedTeamId, {
        variables: {id: dedicatedTeamId}
    });

    if (loading) return 'Loading ...'

    if (error) return `Error! ${error.message}`

    const dedicatedTeam = data.dedicatedTeamById

    const dedicatedTeamName = dedicatedTeam.name
    const cioName = dedicatedTeam.cio.name
    const ctoName = dedicatedTeam.cto.name
    const estimate = dedicatedTeam.estimate

    const timeSheetsByDate = dedicatedTeam.timeSheetsByDate
    const calculatedFinishDate = dedicatedTeam.calculatedFinishDate

    const dedicatedTeamPlanningPeriods = dedicatedTeam.dedicatedTeamPlanningPeriods

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

    const projectTeams = dedicatedTeam.projectTeams

    const projectTeamsTableContents = projectTeams.slice()
        .sort((a, b) => ((a.name > b.name) ? 1 : ((a.name < b.name) ? -1 : 0)))
        .map(projectTeam => (
            {
                id: projectTeam.id,
                estimate: projectTeam.estimate,
                timeLeft: projectTeam.timeLeft,
                name: projectTeam.name,
                calculatedFinishDate: projectTeam.calculatedFinishDate,
                timeSpentChrononFte: projectTeam.timeSpentChrononFte,
                queueLength: projectTeam.queueLength,
                positionPersonPlanFactIssueCount: projectTeam.positionPersonPlanFactIssueCount,
                timeSpentForReengineeringPercent: projectTeam.timeSpentForReengineeringPercent,
            }
        ))

    const projectTeamsTableColumns = [
        {
            field: 'projectTeamName',
            headerName: 'Название',
            flex: 1,
            renderCell: (params) => (
                <RouterLink to={`/projectTeams/${params.getValue(params.id, 'id')}`}>
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
            field: 'queueLength',
            headerName: 'Длина очереди (мес)',
            width: 200,
            align: 'right',
            valueFormatter: ({value}) => value.toLocaleString(undefined, {maximumFractionDigits: 0}),
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
            field: 'positionPersonPlanFactIssueCount',
            headerName: 'Количество проблем с планированием команды (количество членов команды разницей между планом и фактом > 0.4 FTE)',
            width: 200,
            align: 'right',
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
    ];

    const planningPeriodsTableContents = dedicatedTeamPlanningPeriods.slice()
        .sort((a, b) => ((a.planningPeriod.start < b.planningPeriod.start) ? 1 : ((a.planningPeriod.start > b.planningPeriod.start) ? -1 : 0)))
        .filter(a => a.estimate > 0)
        .map(dedicatedTeamPlanningPeriod => (
            {
                id: dedicatedTeamPlanningPeriod.planningPeriod.id,
                name: dedicatedTeamPlanningPeriod.planningPeriod.name,
                estimate: dedicatedTeamPlanningPeriod.estimate,
                timeLeft: dedicatedTeamPlanningPeriod.timeLeft,
                effortPerFunctionPoint: dedicatedTeamPlanningPeriod.effortPerFunctionPoint,
                calculatedFinishDate: dedicatedTeamPlanningPeriod.calculatedFinishDate,
                timeSpentChrononFte: dedicatedTeamPlanningPeriod.timeSpentChrononFte,
            }
        ))

    const planningPeriodsTableColumns = [
        {
            field: 'name',
            headerName: 'Название',
            flex: 1,
            renderCell: (params) => (
                <RouterLink
                    to={`/planningPeriods/${params.getValue(params.id, 'id')}/dedicatedTeams/${dedicatedTeamId}`}>
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
            field: 'timeSpentChrononFte',
            headerName: 'Трудомощность, FTE',
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
                Выделенная команда {dedicatedTeamName}
                <br/>
                Бизнес-партнер {cioName}
                <br/>
                Руководитель разработки (CTO) {ctoName}
                <br/>
                Расчетная дата завершения {calculatedFinishDate}
                <br/>
                <br/>
            </Typography>

            <TimeSheetsByDateIssueChart
                title="Фактический объем работ: Аналитика + Разработка + Тестирование + Управление + Инциденты"
                xAxisStart={xAxisStart}
                xAxisEnd={xAxisEnd}
                color="black"
                timeSheetsByDate={timeSheetsByDate}
                estimate={estimate}
                calculatedFinishDate={calculatedFinishDate}
            />

            <ReengineeringByDatePeriodChart
                planningPeriodEnd={xAxisEnd}
                title="Доля списаний на задачи технологического перевооружения и исправления проблем"
                xAxisStart={xAxisStart}
                xAxisEnd={xAxisEnd}
                color="black"
                timeSpentPercentForReengineeringAndNotForReengineeringByDate={timeSheetsByDate}
            />

            <Typography variant="h6" noWrap>
                Проектные команды
            </Typography>

            <div>
                <DataGridPro
                    rows={projectTeamsTableContents}
                    columns={projectTeamsTableColumns}
                    autoHeight
                />
            </div>
            <br/>

            {/*<Typography variant="h6" noWrap>*/}
            {/*    Периоды*/}
            {/*</Typography>*/}

            {/*<div>*/}
            {/*    <DataGridPro*/}
            {/*        rows={ planningPeriodsTableContents }*/}
            {/*        columns={ planningPeriodsTableColumns }*/}
            {/*        autoHeight*/}
            {/*    />*/}
            {/*</div>*/}

            {/*<br />*/}
        </Box>
    );
}

export default DedicatedTeamDetail;
import React from "react";
import {gql, useQuery} from '@apollo/client';
import Typography from '@material-ui/core/Typography';
import {Box, Link} from "@material-ui/core";
import TimeSheetsByDateIssueChart from "./TimeSheetsByDateIssueChart";
import {Link as RouterLink, useParams} from "react-router-dom";
import {DataGridPro, GridToolbarContainer, GridToolbarExport} from "@mui/x-data-grid-pro";
import ReengineeringByDatePeriodChart from "./ReengineeringByDatePeriodChart";

const fetchProjectTeamByDedicatedTeamId = gql`
    query ProjectTeamById($id: Int!) {
        projectTeamById(id: $id) {
            id
            estimate
            name
            url
            
            calculatedFinishDate
            
            dedicatedTeam {
                id
                name
            }
            
            projectManager {
                id
                name
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
            
            timeSheetsByMonth {
                id
                month
                timeSpentFte
                analysisTimeSpentFte
                developmentTimeSpentFte
                testingTimeSpentFte
                managementTimeSpentFte
                incidentFixingTimeSpentFte
                workingDaysInMonthOccured
            }
            
            projectTeamPlanningPeriods {
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
                timeSpentChronon
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
                timeSpent
                timeSpentChrononFte
                totalCapacityFte
                
                planFactFteDifference
                
                state {
                    name
                }
            }
            
            positionPersonPlanFactIssueCount
        }
    }
`;

function ToolBarWithExport() {
    return (
        <GridToolbarContainer>
            <GridToolbarExport
                csvOptions={{
                    delimiter: ";",
                    utf8WithBom: true,
                }}
            />


        </GridToolbarContainer>
    );
}

function ProjectTeamDetail() {
    const {projectTeamId} = useParams();
    const {loading, error, data} = useQuery(fetchProjectTeamByDedicatedTeamId, {
        variables: {id: projectTeamId}
    });

    if (loading) return 'Loading ...'

    if (error) return `Error! ${error.message}`

    const projectTeam = data.projectTeamById

    const projectTeamName = projectTeam.name
    const projectTeamUrl = projectTeam.url
    const estimate = projectTeam.estimate

    const dedicatedTeam = projectTeam.dedicatedTeam
    const dedicatedTeamId = dedicatedTeam.id
    const dedicatedTeamName = dedicatedTeam.name

    const projectManager = projectTeam.projectManager
    const projectManagerName = projectManager.name

    const timeSheetsByDate = projectTeam.timeSheetsByDate
    const timeSheetsByMonth = projectTeam.timeSheetsByMonth
    const calculatedFinishDate = projectTeam.calculatedFinishDate

    const projectTeamPlanningPeriods = projectTeam.projectTeamPlanningPeriods
    const positions = projectTeam.chrononPositions

    const positionPersonPlanFactIssueCount = projectTeam.positionPersonPlanFactIssueCount

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

    const planningPeriodsTableContents = projectTeamPlanningPeriods.slice()
        .sort((a, b) => ((a.planningPeriod.start < b.planningPeriod.start) ? 1 : ((a.planningPeriod.start > b.planningPeriod.start) ? -1 : 0)))
        .filter(a => a.estimate > 0)
        .map(projectTeamPlanningPeriod => (
            {
                id: projectTeamPlanningPeriod.planningPeriod.id,
                name: projectTeamPlanningPeriod.planningPeriod.name,
                estimate: projectTeamPlanningPeriod.estimate,
                timeLeft: projectTeamPlanningPeriod.timeLeft,
                effortPerFunctionPoint: projectTeamPlanningPeriod.effortPerFunctionPoint,
                calculatedFinishDate: projectTeamPlanningPeriod.calculatedFinishDate,
                timeSpentChronon: projectTeamPlanningPeriod.timeSpentChronon,
            }
        ))

    const planningPeriodsTableColumns = [
        {
            field: 'name',
            headerName: 'Название',
            flex: 1,
            renderCell: (params) => (
                <RouterLink to={`/planningPeriods/${params.getValue(params.id, 'id')}/projectTeams/${projectTeamId}`}>
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

    const positionsTableContents = positions.slice()
        .filter(position => position.timeSpentChrononFte > 0 || position.position.id != "-1"
        )
        .sort((a, b) => (
            (a.timeSpentChrononFte > b.timeSpentChrononFte) ? -1 : (
                (a.timeSpentChrononFte == b.timeSpentChrononFte) ? 0 : 1
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
                timeSpent: position.timeSpent,
                timeSpentChrononFte: position.timeSpentChrononFte,
                totalCapacityFte: position.totalCapacityFte,
                planFactFteDifference: position.planFactFteDifference,
                stateName: position.state.name
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
                    <Link href={url} target="_blank">
                        {params.getValue(params.id, 'position')}
                    </Link>
                    : params.getValue(params.id, 'position')
            },
        },
        {
            field: 'stateName',
            headerName: 'Статус',
            flex: 1,
        },
        {
            field: 'personName',
            headerName: 'ФИО',
            flex: 1,
            renderCell: (params) => (
                <RouterLink to={`/persons/${params.getValue(params.id, 'personKey')}`}>
                    {params.getValue(params.id, 'personName')}
                </RouterLink>
            ),
        },
        {
            field: 'timeSpent',
            headerName: 'Списано всего, ч',
            width: 200,
            align: 'right',
            valueFormatter: ({value}) => value.toLocaleString(undefined, {maximumFractionDigits: 0}),
        },
        {
            field: 'totalCapacityFte',
            headerName: 'Плановая трудомощность, FTE',
            width: 200,
            align: 'right',
            valueFormatter: ({value}) => (value).toLocaleString(undefined, {
                minimumFractionDigits: 2,
                maximumFractionDigits: 2
            }),
        },
        {
            field: 'timeSpentChrononFte',
            headerName: 'Фактическая трудомощность, FTE',
            width: 200,
            align: 'right',
            valueFormatter: ({value}) => (value).toLocaleString(undefined, {
                minimumFractionDigits: 2,
                maximumFractionDigits: 2
            }),
        },
        {
            field: 'planFactFteDifference',
            headerName: 'Разница между планом и фактом, FTE',
            width: 200,
            align: 'right',
            valueFormatter: ({value}) => (value).toLocaleString(undefined, {
                minimumFractionDigits: 2,
                maximumFractionDigits: 2
            }),
        },

    ];

    const timeSheetsByMonthTableContents = timeSheetsByMonth.slice()
        .sort((a, b) => ((a.month < b.month) ? 1 : ((a.month > b.month) ? -1 : 0)))
        .map(timeSheetByMonth => (
            {
                id: timeSheetByMonth.id,
                month: timeSheetByMonth.month,
                timeSpentFte: timeSheetByMonth.timeSpentFte,
                analysisTimeSpentFte: timeSheetByMonth.analysisTimeSpentFte,
                developmentTimeSpentFte: timeSheetByMonth.developmentTimeSpentFte,
                testingTimeSpentFte: timeSheetByMonth.testingTimeSpentFte,
                managementTimeSpentFte: timeSheetByMonth.managementTimeSpentFte,
                incidentFixingTimeSpentFte: timeSheetByMonth.incidentFixingTimeSpentFte,
                workingDaysInMonthOccured: timeSheetByMonth.workingDaysInMonthOccured,
            }
        ))

    const timeSheetsByMonthTableColumns = [
        {
            field: 'month',
            headerName: 'Год-месяц',
            width: 200,
            renderCell: (params) => (
                <RouterLink to={`/projectTeams/${projectTeamId}/month/${params.getValue(params.id, 'month')}/persons/`}>
                    {params.getValue(params.id, 'month')}
                </RouterLink>
            ),
        },
        {
            field: 'timeSpentFte',
            headerName: 'Трудозатраты (FTE)',
            width: 200,
            align: 'right',
            valueFormatter: ({value}) => value.toLocaleString(undefined, {
                minimumFractionDigits: 2,
                maximumFractionDigits: 2
            }),
        },
        {
            field: 'analysisTimeSpentFte',
            headerName: 'Трудозатраты аналитики (FTE)',
            width: 200,
            align: 'right',
            valueFormatter: ({value}) => value.toLocaleString(undefined, {
                minimumFractionDigits: 2,
                maximumFractionDigits: 2
            }),
        },
        {
            field: 'developmentTimeSpentFte',
            headerName: 'Трудозатраты разработки (FTE)',
            width: 200,
            align: 'right',
            valueFormatter: ({value}) => value.toLocaleString(undefined, {
                minimumFractionDigits: 2,
                maximumFractionDigits: 2
            }),
        },
        {
            field: 'testingTimeSpentFte',
            headerName: 'Трудозатраты тестирования (FTE)',
            width: 200,
            align: 'right',
            valueFormatter: ({value}) => value.toLocaleString(undefined, {
                minimumFractionDigits: 2,
                maximumFractionDigits: 2
            }),
        },
        {
            field: 'managementTimeSpentFte',
            headerName: 'Трудозатраты управление (FTE)',
            width: 200,
            align: 'right',
            valueFormatter: ({value}) => value.toLocaleString(undefined, {
                minimumFractionDigits: 2,
                maximumFractionDigits: 2
            }),
        },
        {
            field: 'incidentFixingTimeSpentFte',
            headerName: 'Трудозатраты инциденты (FTE)',
            width: 200,
            align: 'right',
            valueFormatter: ({value}) => value.toLocaleString(undefined, {
                minimumFractionDigits: 2,
                maximumFractionDigits: 2
            }),
        },
        {
            field: 'workingDaysInMonthOccured',
            headerName: 'Рабочих дней в месяце',
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
                Проектная команда {projectTeamName} &nbsp;
                <Link href={projectTeamUrl} target="_blank">
                    [ источник ]
                </Link>
                <br/>
                Менеджер проекта {projectManagerName}
                <br/>
                Расчетная дата завершения {calculatedFinishDate}
                <br/>
                Количество проблем с планированием команды (количество членов команды разницей между планом и фактом >
                0.4 FTE) {positionPersonPlanFactIssueCount}
                <br/>
                Выделенная команда &nbsp;
                <RouterLink to={`/dedicatedTeams/${dedicatedTeamId}`}>
                    {dedicatedTeamName}
                </RouterLink>
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

            <Typography variant="h6" noWrap>
                Команда
            </Typography>
            <div>
                <DataGridPro
                    rows={positionsTableContents}
                    columns={positionsTableColumns}
                    autoHeight
                />
            </div>

            <br/>

            <Typography variant="h6" noWrap>
                Трудозатраты по месяцам
            </Typography>
            <div>
                <DataGridPro
                    rows={timeSheetsByMonthTableContents}
                    columns={timeSheetsByMonthTableColumns}
                    components={{
                        Toolbar: ToolBarWithExport,
                    }}
                    autoHeight
                />
            </div>
        </Box>
    );
}

export default ProjectTeamDetail;
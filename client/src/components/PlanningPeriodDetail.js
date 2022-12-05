import React from "react";
import {gql, useQuery} from '@apollo/client';
import Typography from '@material-ui/core/Typography';
import {Box} from "@material-ui/core";
import {Link as RouterLink, useParams} from "react-router-dom";
import TimeSheetsByDatePeriodChart from "./TimeSheetsByDatePeriodChart"
import ReengineeringByDatePeriodChart from "./ReengineeringByDatePeriodChart"
import ValueByDatePeriodChart from "./ValueByDatePeriodChart"
import {DataGridPro,} from '@mui/x-data-grid-pro';

const fetchPlanningPeriodById = gql`
    query PlanningPeriodByIdQuery($id: Int!) {
        planningPeriodById(id: $id) {
            id 
            name
            start
            end
            estimate
            effortPerFunctionPoint
            calculatedFinishDate
            
            dedicatedTeamPlanningPeriods {
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
                timeSpentForReengineeringPercent
            }
            
            systemPlanningPeriods {
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
    
            timeSheetsByDate {
                date
                timeSpentCumsum
                timeSpentCumsumPrediction
                timeSpentWithoutValuePercentCumsum
                timeSpentWithValuePercentCumsum
                timeSpentForReengineeringPercentCumsum
                timeSpentNotForReengineeringPercentCumsum
            }
        }
    }
`;

function PlanningPeriodDetail() {
    const {id} = useParams();
    const {loading, error, data} = useQuery(fetchPlanningPeriodById, {
        variables: {id: id}
    });

    if (loading) return 'Loading ...'

    if (error) return `Error! ${error.message}`

    const planningPeriodId = id
    const planningPeriod = data.planningPeriodById
    const estimate = planningPeriod.estimate
    const effortPerFunctionPoint = planningPeriod.effortPerFunctionPoint
    const calculatedFinishDate = planningPeriod.calculatedFinishDate
    const planningPeriodStart = planningPeriod.start
    const planningPeriodEnd = planningPeriod.end

    const dedicatedTeamPlanningPeriods = planningPeriod.dedicatedTeamPlanningPeriods
    const systemPlanningPeriods = planningPeriod.systemPlanningPeriods

    const timeSheetsByDate = planningPeriod.timeSheetsByDate

    const fourWeeks = 1000 * 60 * 60 * 24 * 7 * 4
    const xAxisStart = new Date(planningPeriodStart).getTime() - fourWeeks
    const xAxisEnd = new Date(planningPeriodEnd).getTime() + fourWeeks

    const dedicatedTeamsTableContents = dedicatedTeamPlanningPeriods.slice()
        .sort((a, b) => ((a.dedicatedTeam.name > b.dedicatedTeam.name) ? 1 : ((a.dedicatedTeam.name < b.dedicatedTeam.name) ? -1 : 0)))
        .map(dedicatedTeamPlanningPeriod => (
            {
                id: dedicatedTeamPlanningPeriod.id,
                estimate: dedicatedTeamPlanningPeriod.estimate,
                timeLeft: dedicatedTeamPlanningPeriod.timeLeft,
                dedicatedTeamId: dedicatedTeamPlanningPeriod.dedicatedTeam.id,
                dedicatedTeamName: dedicatedTeamPlanningPeriod.dedicatedTeam.name,
                effortPerFunctionPoint: dedicatedTeamPlanningPeriod.effortPerFunctionPoint,
                calculatedFinishDate: dedicatedTeamPlanningPeriod.calculatedFinishDate,
                timeSpentChronon: dedicatedTeamPlanningPeriod.timeSpentChronon,
                timeSpentForReengineeringPercent: dedicatedTeamPlanningPeriod.timeSpentForReengineeringPercent,
            }
        ))

    const dedicatedTeamsTableColumns = [
        {
            field: 'dedicatedTeamName',
            headerName: 'Название',
            flex: 1,
            renderCell: (params) => (
                <RouterLink
                    to={`/planningPeriods/${planningPeriodId}/dedicatedTeams/${params.getValue(params.id, 'dedicatedTeamId')}`}>
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
            headerName: 'Трудомощность (ч)',
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

    ];

    const systemsTableContents = systemPlanningPeriods.slice()
        .sort((a, b) => ((a.system.name > b.system.name) ? 1 : ((a.system.name < b.system.name) ? -1 : 0)))
        .map(systemPlanningPeriod => (
            {
                id: systemPlanningPeriod.id,
                estimate: systemPlanningPeriod.estimate,
                timeLeft: systemPlanningPeriod.timeLeft,
                systemId: systemPlanningPeriod.system.id,
                systemName: systemPlanningPeriod.system.name,
                effortPerFunctionPoint: systemPlanningPeriod.effortPerFunctionPoint,
                calculatedFinishDate: systemPlanningPeriod.calculatedFinishDate
            }
        ))

    const systemsTableColumns = [
        {
            field: 'systemName',
            headerName: 'Название',
            flex: 1,
            renderCell: (params) => (
                <RouterLink
                    to={`/planningPeriods/${planningPeriodId}/systems/${params.getValue(params.id, 'systemId')}`}>
                    {params.getValue(params.id, 'systemName')}
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
    ];

    return (
        <Box>
            <Typography variant="body" noWrap>
                Расчетная дата завершения {calculatedFinishDate}
                <br/>
                Затраты на функциональную точку (аналитика + разработка +
                менеджмент) {effortPerFunctionPoint.toFixed(2)} часов / функциональная точка
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

            <Typography variant="body1">
                <RouterLink to={`/planningPeriods/${planningPeriodId}/projectTeams`}>
                    Затраты на функциональные точки по проектным командам
                </RouterLink>
            </Typography>
            <br/>

            <Typography variant="body1">
                <RouterLink to={`/planningPeriods/${planningPeriodId}/persons`}>
                    Затраты на функциональную точку по сотрудникам
                </RouterLink>
            </Typography>
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

            <Typography variant="h6" noWrap>
                Системы
            </Typography>
            <div>
                <DataGridPro
                    rows={systemsTableContents}
                    columns={systemsTableColumns}
                    autoHeight
                />
            </div>
        </Box>
    );
}

export default PlanningPeriodDetail;
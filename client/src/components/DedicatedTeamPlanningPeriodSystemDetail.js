import React from "react";
import {gql, useQuery} from '@apollo/client';
import Typography from '@material-ui/core/Typography';
import {Box} from "@material-ui/core";
import {Link as RouterLink, useParams} from "react-router-dom";
import TimeSheetsByDatePeriodChart from "./TimeSheetsByDatePeriodChart"
import {DataGridPro} from "@mui/x-data-grid-pro";

const fetchDedicatedTeamPlanningPeriodSystemByDedicatedTeamIdPlanningPeriodIdAndSystemId = gql`
     query DedicatedTeamPlanningPeriodSystemByDedicatedTeamIdPlanningPeriodIdAndSystemId($dedicatedTeamId:Int!, $planningPeriodId: Int!, $systemId: Int!) {
          dedicatedTeamPlanningPeriodSystemByDedicatedTeamIdPlanningPeriodIdAndSystemId(dedicatedTeamId: $dedicatedTeamId, planningPeriodId: $planningPeriodId, systemId: $systemId) {
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
                }
          }
    }
`;

function DedicatedTeamPlanningPeriodSystemDetail() {
    const {planningPeriodId, dedicatedTeamId, systemId} = useParams();

    const {
        loading,
        error,
        data
    } = useQuery(fetchDedicatedTeamPlanningPeriodSystemByDedicatedTeamIdPlanningPeriodIdAndSystemId, {
        variables: {planningPeriodId: planningPeriodId, dedicatedTeamId: dedicatedTeamId, systemId: systemId}
    });

    if (loading) return 'Loading ...'

    if (error) return `Error! ${error.message}`

    const dedicatedTeamPlanningPeriodSystem = data.dedicatedTeamPlanningPeriodSystemByDedicatedTeamIdPlanningPeriodIdAndSystemId

    const systemName = dedicatedTeamPlanningPeriodSystem.system.name
    const estimate = dedicatedTeamPlanningPeriodSystem.estimate
    const calculatedFinishDate = dedicatedTeamPlanningPeriodSystem.calculatedFinishDate
    const effortPerFunctionPoint = dedicatedTeamPlanningPeriodSystem.effortPerFunctionPoint
    const planningPeriodName = dedicatedTeamPlanningPeriodSystem.planningPeriod.name
    const planningPeriodStart = dedicatedTeamPlanningPeriodSystem.planningPeriod.start
    const planningPeriodEnd = dedicatedTeamPlanningPeriodSystem.planningPeriod.end
    const systemChangeRequests = dedicatedTeamPlanningPeriodSystem.systemChangeRequests

    const timeSheetsByDate = dedicatedTeamPlanningPeriodSystem.timeSheetsByDate

    const xAxisStart = new Date(planningPeriodStart).getTime()
    const xAxisEnd = new Date(planningPeriodEnd).getTime()

    const systemChangeRequestsTableContents = systemChangeRequests.slice()
        .sort((a, b) => (
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
                <RouterLink
                    style={{textDecoration: params.getValue(params.id, 'stateCategoryId') === 3 ? 'line-through' : 'none'}}
                    to={`/systemChangeRequests/${params.getValue(params.id, 'key')}`}>
                    {params.getValue(params.id, 'key')} &nbsp;
                    {params.getValue(params.id, 'name')}
                </RouterLink>
            ),
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
    ];

    return (
        <Box>
            <Typography variant="body" noWrap>
                Система {systemName}<br/>
                Период планирования {planningPeriodName} ({planningPeriodStart}-{planningPeriodEnd})<br/>
                Затраты на функциональную точку (аналитика + разработка +
                менеджмент) {effortPerFunctionPoint.toFixed(2)} часов / функциональная точка<br/>
                Расчетная дата завершения {calculatedFinishDate}
            </Typography>

            <TimeSheetsByDatePeriodChart
                planningPeriodEnd={planningPeriodEnd}
                title="Фактический объем работ: Аналитика + Разработка + Тестирование+ Управление"
                xAxisStart={xAxisStart}
                xAxisEnd={xAxisEnd}
                color="black"
                timeSheetsByDate={timeSheetsByDate}
                estimate={estimate}
                calculatedFinishDate={calculatedFinishDate}
            />

            <Typography variant="h6" noWrap>
                Заявки на доработку системы
            </Typography>
            <div>
                <DataGridPro
                    rows={systemChangeRequestsTableContents}
                    columns={systemChangeRequestsTableColumns}
                    autoHeight
                />
            </div>
        </Box>
    );
}

export default DedicatedTeamPlanningPeriodSystemDetail;
import React, {Component} from "react";
import {gql, useQuery} from '@apollo/client';
import Typography from '@material-ui/core/Typography';
import {Box, Link} from "@material-ui/core";
import {Link as RouterLink, useParams} from "react-router-dom";
import TimeSheetsByDatePeriodChart from "./TimeSheetsByDatePeriodChart"
import {DataGridPro} from "@mui/x-data-grid-pro";

const fetchSystemPlanningPeriodByPlanningPeriodIdAndSystemId = gql`
    query SystemPlanningPeriodByPlanningPeriodIdAndSystemId($planningPeriodId: Int!, $systemId: Int!) {
          systemPlanningPeriodByPlanningPeriodIdAndSystemId(systemId: $systemId, planningPeriodId: $planningPeriodId) {
                id
                estimate
                effortPerFunctionPoint
                calculatedFinishDate
                
                
                system {
                    name
                }
                planningPeriod {
                    name
                    start
                    end
                }
                
                analysisTimeSheetsByDate {
                    date
                    timeSpentCumsum
                    timeSpentCumsumPrediction
                }
                
                analysisCalculatedFinishDate
                
                analysisEstimate
                
                developmentTimeSheetsByDate {
                    date
                    timeSpentCumsum
                    timeSpentCumsumPrediction
                }
                
                developmentCalculatedFinishDate
                
                developmentEstimate
                
                testingTimeSheetsByDate {
                    date
                    timeSpentCumsum
                    timeSpentCumsumPrediction
                }
                
                testingCalculatedFinishDate
                
                testingEstimate

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
                    mainDeveloper {
                        id
                        name
                    }
                }
          }
    }
`;

function SystemPlanningPeriodDetail() {

    const {planningPeriodId, systemId} = useParams();

    const {loading, error, data} = useQuery(fetchSystemPlanningPeriodByPlanningPeriodIdAndSystemId, {
        variables: {planningPeriodId: planningPeriodId, systemId: systemId}
    });

    if (loading) return 'Loading ...'

    if (error) return `Error! ${error.message}`

    const systemPlanningPeriod = data.systemPlanningPeriodByPlanningPeriodIdAndSystemId

    const systemName = systemPlanningPeriod.system.name
    const estimate = systemPlanningPeriod.estimate
    const calculatedFinishDate = systemPlanningPeriod.calculatedFinishDate
    const effortPerFunctionPoint = systemPlanningPeriod.effortPerFunctionPoint
    const planningPeriodName = systemPlanningPeriod.planningPeriod.name
    const planningPeriodStart = systemPlanningPeriod.planningPeriod.start
    const planningPeriodEnd = systemPlanningPeriod.planningPeriod.end
    const systemChangeRequests = systemPlanningPeriod.systemChangeRequests

    const analysisTimeSheetsByDate = systemPlanningPeriod.analysisTimeSheetsByDate
    const analysisEstimate = systemPlanningPeriod.analysisEstimate
    const analysisCalculatedFinishDate = systemPlanningPeriod.analysisCalculatedFinishDate

    const developmentTimeSheetsByDate = systemPlanningPeriod.developmentTimeSheetsByDate
    const developmentEstimate = systemPlanningPeriod.developmentEstimate
    const developmentCalculatedFinishDate = systemPlanningPeriod.developmentCalculatedFinishDate

    const testingTimeSheetsByDate = systemPlanningPeriod.testingTimeSheetsByDate
    const testingEstimate = systemPlanningPeriod.testingEstimate
    const testingCalculatedFinishDate = systemPlanningPeriod.testingCalculatedFinishDate

    const timeSheetsByDate = systemPlanningPeriod.timeSheetsByDate

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
                effortPerFunctionPoint: systemChangeRequest.effortPerFunctionPoint,
                mainDeveloperName: systemChangeRequest.mainDeveloper.name,
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
        {
            field: 'mainDeveloperName',
            headerName: 'Основной разработчик',
            width: 200,
            align: 'left',
        },
    ];

    return (
        <Box>
            <Typography variant="body1" noWrap>
                Система {systemName}<br/>
                Период планирования {planningPeriodName} ({planningPeriodStart}-{planningPeriodEnd})<br/>
                Затраты на функциональную точку (аналитика + разработка +
                менеджмент) {effortPerFunctionPoint.toFixed(2)} часов / функциональная точка<br/>
                Расчетная дата завершения {calculatedFinishDate}
            </Typography>

            <TimeSheetsByDatePeriodChart
                planningPeriodEnd={planningPeriodEnd}
                title="Фактический объем работ: Аналитика + Разработка + Тестирование + Управление"
                xAxisStart={xAxisStart}
                xAxisEnd={xAxisEnd}
                color="black"
                timeSheetsByDate={timeSheetsByDate}
                estimate={estimate}
                calculatedFinishDate={calculatedFinishDate}
            />

            <TimeSheetsByDatePeriodChart
                planningPeriodEnd={planningPeriodEnd}
                title="Аналитика"
                xAxisStart={xAxisStart}
                xAxisEnd={xAxisEnd}
                color="black"
                timeSheetsByDate={analysisTimeSheetsByDate}
                estimate={analysisEstimate}
                calculatedFinishDate={analysisCalculatedFinishDate}
            />

            <TimeSheetsByDatePeriodChart
                planningPeriodEnd={planningPeriodEnd}
                title="Разработка"
                xAxisStart={xAxisStart}
                xAxisEnd={xAxisEnd}
                color="black"
                timeSheetsByDate={developmentTimeSheetsByDate}
                estimate={developmentEstimate}
                calculatedFinishDate={developmentCalculatedFinishDate}
            />

            <TimeSheetsByDatePeriodChart
                planningPeriodEnd={planningPeriodEnd}
                title="Тестирование"
                xAxisStart={xAxisStart}
                xAxisEnd={xAxisEnd}
                color="black"
                timeSheetsByDate={testingTimeSheetsByDate}
                estimate={testingEstimate}
                calculatedFinishDate={testingCalculatedFinishDate}
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

export default SystemPlanningPeriodDetail;
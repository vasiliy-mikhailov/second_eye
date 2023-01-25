import React from "react";
import {gql, useQuery} from '@apollo/client';
import Typography from '@material-ui/core/Typography';
import {Box} from "@material-ui/core";
import {Link as RouterLink, useParams} from "react-router-dom";
import TimeSheetsByDatePeriodChart from "./TimeSheetsByDatePeriodChart"
import ReengineeringByDatePeriodChart from "./ReengineeringByDatePeriodChart"
import ValueByDatePeriodChart from "./ValueByDatePeriodChart"
import {DataGridPro} from "@mui/x-data-grid-pro";

const fetchDedicatedTeamPlanningPeriodByPlanningPeriodIdAndDedicatedTeamId = gql`
        query DedicatedTeamPlanningPeriodByPlanningPeriodIdAndDedicatedTeamId($planningPeriodId: Int!, $dedicatedTeamId: Int!) {
              dedicatedTeamPlanningPeriodByPlanningPeriodIdAndDedicatedTeamId(dedicatedTeamId: $dedicatedTeamId, planningPeriodId: $planningPeriodId) {
                    id
                    estimate
                    effortPerFunctionPoint
                    calculatedFinishDate
                    dedicatedTeam {
                        name
                        cio {
                            name
                        }
                        cto {
                            name
                        }
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
                        timeSpentWithoutValuePercentCumsum
                        timeSpentWithValuePercentCumsum
                        timeSpentForReengineeringPercentCumsum
                        timeSpentNotForReengineeringPercentCumsum
                    }
                    
                    projectTeamPlanningPeriods {
                        id
                        estimate
                        timeLeft
                        projectTeam {
                            id
                            name
                        }
                        effortPerFunctionPoint
                        calculatedFinishDate
                        timeSpentChronon
                    }
                    
                    dedicatedTeamPlanningPeriodSystems {
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
                        isReengineering
                        name
                        stateCategoryId
                        effortPerFunctionPoint
                        calculatedFinishDate
                        timeSpentChronon
                    }
                    
                    positionPersons {
                        position {
                            id
                            name
                            url
                        }
                        
                        person {
                            id
                            key
                            name
                        }
                        timeSpent
                        timeSpentChrononFte
                        totalCapacityFte
                    }
              }
        }
`;

function DedicatedTeamPlanningPeriodDetail() {
    const {planningPeriodId, dedicatedTeamId} = useParams();

    const {loading, error, data} = useQuery(fetchDedicatedTeamPlanningPeriodByPlanningPeriodIdAndDedicatedTeamId, {
        variables: {planningPeriodId: planningPeriodId, dedicatedTeamId: dedicatedTeamId}
    });

    if (loading) return 'Loading ...'

    if (error) return `Error! ${error.message}`

    const dedicatedTeamPlanningPeriod = data.dedicatedTeamPlanningPeriodByPlanningPeriodIdAndDedicatedTeamId

    const dedicatedTeamName = dedicatedTeamPlanningPeriod.dedicatedTeam.name
    const cioName = dedicatedTeamPlanningPeriod.dedicatedTeam.cio.name
    const ctoName = dedicatedTeamPlanningPeriod.dedicatedTeam.cto.name
    const estimate = dedicatedTeamPlanningPeriod.estimate
    const effortPerFunctionPoint = dedicatedTeamPlanningPeriod.effortPerFunctionPoint
    const calculatedFinishDate = dedicatedTeamPlanningPeriod.calculatedFinishDate
    const planningPeriodName = dedicatedTeamPlanningPeriod.planningPeriod.name
    const planningPeriodStart = dedicatedTeamPlanningPeriod.planningPeriod.start
    const planningPeriodEnd = dedicatedTeamPlanningPeriod.planningPeriod.end
    const projectTeamPlanningPeriods = dedicatedTeamPlanningPeriod.projectTeamPlanningPeriods
    const dedicatedTeamPlanningPeriodSystems = dedicatedTeamPlanningPeriod.dedicatedTeamPlanningPeriodSystems
    const changeRequests = dedicatedTeamPlanningPeriod.changeRequests
    const positionPersons = dedicatedTeamPlanningPeriod.positionPersons

    const timeSheetsByDate = dedicatedTeamPlanningPeriod.timeSheetsByDate

    const fourWeeks = 1000 * 60 * 60 * 24 * 7 * 4
    const xAxisStart = new Date(planningPeriodStart).getTime() - fourWeeks
    const xAxisEnd = new Date(planningPeriodEnd).getTime() + fourWeeks

    const systemsTableContents = dedicatedTeamPlanningPeriodSystems.slice()
        .sort((a, b) => ((a.system.name > b.system.name) ? 1 : ((a.system.name < b.system.name) ? -1 : 0)))
        .map(dedicatedTeamPlanningPeriodSystem => (
            {
                id: dedicatedTeamPlanningPeriodSystem.id,
                estimate: dedicatedTeamPlanningPeriodSystem.estimate,
                timeLeft: dedicatedTeamPlanningPeriodSystem.timeLeft,
                systemId: dedicatedTeamPlanningPeriodSystem.system.id,
                systemName: dedicatedTeamPlanningPeriodSystem.system.name,
                effortPerFunctionPoint: dedicatedTeamPlanningPeriodSystem.effortPerFunctionPoint,
                calculatedFinishDate: dedicatedTeamPlanningPeriodSystem.calculatedFinishDate,
            }
        ))

    const systemsTableColumns = [
        {
            field: 'systemName',
            headerName: 'Название',
            flex: 1,
            renderCell: (params) => (
                <RouterLink
                    to={`/planningPeriods/${planningPeriodId}/dedicatedTeams/${dedicatedTeamId}/systems/${params.getValue(params.id, 'systemId')}`}>
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

    const projectTeamsTableContents = projectTeamPlanningPeriods.slice()
        .sort((a, b) => ((a.name > b.name) ? 1 : ((a.name < b.name) ? -1 : 0)))
        .map(projectTeamPlanningPeriod => (
            {
                id: projectTeamPlanningPeriod.id,
                estimate: projectTeamPlanningPeriod.estimate,
                timeLeft: projectTeamPlanningPeriod.timeLeft,
                projectTeamId: projectTeamPlanningPeriod.projectTeam.id,
                projectTeamName: projectTeamPlanningPeriod.projectTeam.name,
                effortPerFunctionPoint: projectTeamPlanningPeriod.effortPerFunctionPoint,
                calculatedFinishDate: projectTeamPlanningPeriod.calculatedFinishDate,
                timeSpentChronon: projectTeamPlanningPeriod.timeSpentChronon
            }
        ))

    const projectTeamsTableColumns = [
        {
            field: 'projectTeamName',
            headerName: 'Название',
            flex: 1,
            renderCell: (params) => (
                <RouterLink
                    to={`/planningPeriods/${planningPeriodId}/projectTeams/${params.getValue(params.id, 'projectTeamId')}`}>
                    {params.getValue(params.id, 'projectTeamName')}
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
                isReengineering: changeRequest.isReengineering,
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
            field: 'isReengineering',
            headerName: 'Технологическое перевооружение',
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

    const positionPersonsTableContents = positionPersons.slice()
        .sort((a, b) => (
            (a.timeSpentChrononFte > b.timeSpentChrononFte) ? -1 : (
                (a.timeSpentChrononFte == b.timeSpentChrononFte) ? 0 : 1
            )
        ))
        .map(positionPerson => (
            {
                id: positionPerson.person.id,
                key: positionPerson.person.key,
                name: positionPerson.person.name,
                position: positionPerson.position.name,
                timeSpent: positionPerson.timeSpent,
                timeSpentChrononFte: positionPerson.timeSpentChrononFte,
                totalCapacityFte: positionPerson.totalCapacityFte
            }
        ))

    const positionPersonsTableColumns = [
        {
            field: 'position',
            headerName: 'Позиция',
            flex: 1,
        },
        {
            field: 'name',
            headerName: 'Имя',
            flex: 1,
        },
        {
            field: 'timeSpent',
            headerName: 'Списано всего (ч)',
            width: 200,
            align: 'right',
            valueFormatter: ({value}) => value.toLocaleString(undefined, {maximumFractionDigits: 0}),
        },
        {
            field: 'totalCapacityFte',
            headerName: 'Плановый FTE',
            width: 200,
            align: 'right',
            valueFormatter: ({value}) => (value).toLocaleString(undefined, {
                minimumFractionDigits: 1,
                maximumFractionDigits: 1
            }),
        },
        {
            field: 'timeSpentChrononFte',
            headerName: 'Фактический FTE',
            width: 200,
            align: 'right',
            valueFormatter: ({value}) => (value).toLocaleString(undefined, {
                minimumFractionDigits: 1,
                maximumFractionDigits: 1
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
                Период планирования {planningPeriodName} ({planningPeriodStart}-{planningPeriodEnd})
                <br/>
                Расчетная дата завершения {calculatedFinishDate}
                <br/>
                Затраты на функциональную точку (аналитика + разработка +
                менеджмент) {effortPerFunctionPoint.toFixed(2)} часов / функциональная точка
            </Typography>

            <TimeSheetsByDatePeriodChart
                planningPeriodEnd={planningPeriodEnd}
                title="Фактический объем работ:Аналитика + Разработка + Тестирование + Управление + Инциденты"
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

            <br/>

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

            <br/>
            <Typography variant="h6" noWrap>
                Команда
            </Typography>
            <div>
                <DataGridPro
                    rows={positionPersonsTableContents}
                    columns={positionPersonsTableColumns}
                    autoHeight
                />
            </div>
        </Box>
    );
}

export default DedicatedTeamPlanningPeriodDetail;
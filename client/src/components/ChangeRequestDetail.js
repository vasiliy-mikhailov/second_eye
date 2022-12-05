import React from "react";
import {gql, useQuery} from '@apollo/client';
import moment from 'moment';
import Typography from '@material-ui/core/Typography';
import {Link as RouterLink, NavLink, useParams, useLocation} from "react-router-dom"
import {Box, Link} from "@material-ui/core";
import TimeSheetsByDateIssueChart from './TimeSheetsByDateIssueChart'
import {DataGridPro} from "@mui/x-data-grid-pro";

const fetchChangeRequest = gql`
    query ChangeRequestByKeyQuery($key: String!) {
        changeRequestByKey(key: $key) {
            id 
            key
            url
            name
            state {
                name
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
            
            estimate
            effortPerFunctionPoint
            timeSpent
            timeLeft
            timeSheetsByDate {
                date
                timeSpentCumsum
                timeSpentCumsumPrediction
            }
            
            plannedInstallDate
            
            calculatedFinishDate
            
            systemChangeRequests {
                id
                key
                name
                
                estimate
                effortPerFunctionPoint
                
                timeLeft
                state {
                    name
                }
                stateCategory {
                    id
                }
                
                calculatedFinishDate
                
                mainDeveloper {
                    id
                    name
                }
            }
            
            persons {
                person {
                    id
                    name
                }
                timeSpent
                timeSpentChrononFte
            }
        }
    }
`;

function ChangeRequestDetail() {
    const {key} = useParams();
    const location = useLocation();
    const {loading, error, data} = useQuery(fetchChangeRequest, {
        variables: {key: key}
    });

    if (loading) return 'Loading ...'

    if (error) return `Error! ${error.message}`

    const changeRequest = data.changeRequestByKey

    const plannedInstallDate = changeRequest.plannedInstallDate ? new Date(changeRequest.plannedInstallDate).getTime() : null
    const timeSheetsByDate = changeRequest.timeSheetsByDate

    const estimate = changeRequest.estimate
    const effortPerFunctionPoint = changeRequest.effortPerFunctionPoint

    const analysisTimeSheetsByDate = changeRequest.analysisTimeSheetsByDate
    const analysisEstimate = changeRequest.analysisEstimate

    const developmentTimeSheetsByDate = changeRequest.developmentTimeSheetsByDate
    const developmentEstimate = changeRequest.developmentEstimate

    const testingTimeSheetsByDate = changeRequest.testingTimeSheetsByDate
    const testingEstimate = changeRequest.testingEstimate

    const calculatedFinishDate = changeRequest.calculatedFinishDate

    const systemChangeRequests = changeRequest.systemChangeRequests
    const persons = changeRequest.persons

    const today = (new Date()).getTime()
    const firstTimeSheetDate = timeSheetsByDate.length > 0 ? new Date(timeSheetsByDate[0].date).getTime() : null
    const lastTimeSheetDate = timeSheetsByDate.length > 0 ? new Date(timeSheetsByDate[timeSheetsByDate.length - 1].date).getTime() : null

    const allEdgeDates = [today]
    if (plannedInstallDate) {
        allEdgeDates.push(plannedInstallDate)
    }

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
                calculatedFinishDate: systemChangeRequest.calculatedFinishDate,
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
            field: 'mainDeveloperName',
            headerName: 'Основной разработчик',
            width: 200,
            align: 'left',
        },
    ];

    const personsTableContents = persons.slice()
        .sort((a, b) => (
            (a.timeSpentChrononFte > b.timeSpentChrononFte) ? -1 : (
                (a.timeSpentChrononFte == b.timeSpentChrononFte) ? 0 : 1
            )
        ))
        .map(person => (
            {
                id: person.person.id,
                name: person.person.name,
                timeSpent: person.timeSpent,
                timeSpentChrononFte: person.timeSpentChrononFte
            }
        ))

    const personsTableColumns = [
        {
            field: 'name',
            headerName: 'Имя',
            flex: 1,
        },
        {
            field: 'timeSpent',
            headerName: 'Трудозатраты (ч)',
            width: 200,
            align: 'right',
            valueFormatter: ({value}) => value.toLocaleString(undefined, {maximumFractionDigits: 0}),
        },
        {
            field: 'timeSpentChrononFte',
            headerName: 'Трудомощность, FTE',
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
            <Typography variant="body1" noWrap>
                <NavLink to={location.pathname}>
                    {changeRequest.key}
                </NavLink> &nbsp;
                {changeRequest.name} &nbsp;
                {changeRequest.state.name} &nbsp;
                <Link href={changeRequest.url} target="_blank">
                    [ источник ]
                </Link>
                <br/>
                Осталось {changeRequest.timeLeft.toFixed(1)} ч
                ( {(changeRequest.timeLeft / changeRequest.estimate * 100).toFixed(2)}% ) <br/>
                Сделано {changeRequest.timeSpent.toFixed(1)} ч <br/>
                Оценка {changeRequest.estimate.toFixed(1)} ч <br/>
                Плановая дата
                установки {plannedInstallDate ? moment(plannedInstallDate).format("YYYY-MM-DD") : "не указана"} <br/>
                Затраты на функциональную точку (аналитика + разработка +
                менеджмент) {effortPerFunctionPoint.toFixed(2)} часов / функциональная точка <br/>
                Расчетная дата завершения {calculatedFinishDate}
                <br/>
            </Typography>
            <br/>

            <TimeSheetsByDateIssueChart
                plannedInstallDate={plannedInstallDate}
                title="Фактический объем работ: Аналитика + Разработка + Тестирование + Управление"
                xAxisStart={xAxisStart}
                xAxisEnd={xAxisEnd}
                color="black"
                timeSheetsByDate={timeSheetsByDate}
                estimate={estimate}
                calculatedFinishDate={calculatedFinishDate}
            />

            <TimeSheetsByDateIssueChart
                plannedInstallDate={plannedInstallDate}
                title="Аналитика"
                xAxisStart={xAxisStart}
                xAxisEnd={xAxisEnd}
                color="red"
                timeSheetsByDate={analysisTimeSheetsByDate}
                estimate={analysisEstimate}
            />

            <TimeSheetsByDateIssueChart
                plannedInstallDate={plannedInstallDate}
                title="Разработка"
                xAxisStart={xAxisStart}
                xAxisEnd={xAxisEnd}
                color="green"
                timeSheetsByDate={developmentTimeSheetsByDate}
                estimate={developmentEstimate}
            />

            <TimeSheetsByDateIssueChart
                plannedInstallDate={plannedInstallDate}
                title="Тестирование"
                xAxisStart={xAxisStart}
                xAxisEnd={xAxisEnd}
                color="blue"
                timeSheetsByDate={testingTimeSheetsByDate}
                estimate={testingEstimate}
            />

            <Typography variant="h6" noWrap>
                Доработки систем
            </Typography>
            <div>
                <DataGridPro
                    rows={systemChangeRequestsTableContents}
                    columns={systemChangeRequestsTableColumns}
                    autoHeight
                />
            </div>

            <br/>
            <Typography variant="h6" noWrap>
                Команда
            </Typography>
            <div>
                <DataGridPro
                    rows={personsTableContents}
                    columns={personsTableColumns}
                    autoHeight
                />
            </div>
        </Box>
    );
}

export default ChangeRequestDetail;